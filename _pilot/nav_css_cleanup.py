#!/usr/bin/env python3
"""Migration helper: clean orphan nav-targeting CSS from inline <style> blocks.

Also exports a verification check that flags rules that would hide the new
.nav-menu on mobile.
"""
import re

NAV_SELECTOR_PATTERNS = [
    re.compile(r'^header\.site-header(\b|[\s>+~\.:,#])'),
    re.compile(r'^footer\.site-footer(\b|[\s>+~\.:,#])'),
    re.compile(r'^nav(\b|[\s>+~\.:,#])'),
    re.compile(r'^\.main-nav(\b|[\s>+~\.:,#])'),
    re.compile(r'^\.menu-toggle(\b|[\s>+~\.:,#])'),
    re.compile(r'^\.has-dropdown(\b|[\s>+~\.:,#])'),
    re.compile(r'^\.dropdown(\b|[\s>+~\.:,#])'),
    re.compile(r'^\.site-banner(\b|[\s>+~\.:,#])'),
]


def _is_nav_selector(selector_text):
    """selector_text may be a comma list. Return True if ANY part is nav-targeting."""
    for part in selector_text.split(','):
        part = part.strip()
        if not part:
            continue
        if any(pat.match(part) for pat in NAV_SELECTOR_PATTERNS):
            return True
    return False


def _strip_leading_comments_and_ws(text):
    """Return (skipped_text, remainder) — skipping leading whitespace and /* ... */ comments."""
    i = 0
    n = len(text)
    while i < n:
        if text[i].isspace():
            i += 1
        elif text[i:i+2] == '/*':
            end = text.find('*/', i + 2)
            i = end + 2 if end >= 0 else n
        else:
            break
    return text[:i], text[i:]


def _iter_top_level_rules(css):
    """Yield (leading_ws_and_comments, prelude, body) for each top-level rule.

    leading_ws_and_comments captures comments + whitespace before the rule (for re-assembly).
    prelude is the actual selector or at-rule preamble (no leading comments).
    body is the {...}-enclosed text WITHOUT the braces.
    """
    pos = 0
    n = len(css)
    while pos < n:
        # Skip leading whitespace + comments, capture them as `leading`
        leading_start = pos
        while pos < n:
            if css[pos].isspace():
                pos += 1
            elif css[pos:pos+2] == '/*':
                end = css.find('*/', pos + 2)
                pos = end + 2 if end >= 0 else n
            else:
                break
        leading = css[leading_start:pos]
        if pos >= n:
            if leading:
                yield (leading, '', '')
            return

        # Parse prelude until first { at depth 0 (skipping comments inside the prelude)
        prelude_start = pos
        while pos < n and css[pos] != '{':
            if css[pos:pos+2] == '/*':
                end = css.find('*/', pos + 2)
                pos = end + 2 if end >= 0 else n
                continue
            pos += 1
        if pos >= n:
            # Unterminated rule
            yield (leading, css[prelude_start:pos], '')
            return
        prelude = css[prelude_start:pos]

        # Parse body until matching close brace
        pos += 1  # consume opening {
        body_start = pos
        depth = 1
        while pos < n and depth > 0:
            c = css[pos]
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    break
            elif css[pos:pos+2] == '/*':
                end = css.find('*/', pos + 2)
                pos = end + 2 if end >= 0 else n
                continue
            pos += 1
        if depth != 0:
            yield (leading, prelude, css[body_start:pos])
            return
        body = css[body_start:pos]
        pos += 1  # consume closing }

        yield (leading, prelude, body)


def _clean_at_block_body(body):
    """Recursively filter rules inside a non-print @media body."""
    pieces = []
    for leading, prelude, b in _iter_top_level_rules(body):
        prelude_stripped = prelude.strip()
        if not prelude_stripped:
            pieces.append(leading)  # only whitespace/comments
            continue
        if prelude_stripped.startswith('@media print'):
            pieces.append(leading + prelude + '{' + b + '}')
            continue
        if prelude_stripped.startswith('@media') or prelude_stripped.startswith('@supports'):
            inner = _clean_at_block_body(b)
            if inner.strip():
                pieces.append(leading + prelude + '{' + inner + '}')
            continue
        if _is_nav_selector(prelude_stripped):
            # Drop this rule. Also drop its leading comment block.
            continue
        pieces.append(leading + prelude + '{' + b + '}')
    return ''.join(pieces)


def clean_nav_css_from_inline_style(html):
    """Strip nav-targeting rules from every inline <style>...</style> block."""
    def clean_one(match):
        opening = match.group(1)
        css = match.group(2)
        closing = match.group(3)
        pieces = []
        for leading, prelude, body in _iter_top_level_rules(css):
            prelude_stripped = prelude.strip()
            if not prelude_stripped:
                pieces.append(leading)  # trailing whitespace/comments
                continue
            if prelude_stripped.startswith('@media print'):
                pieces.append(leading + prelude + '{' + body + '}')
                continue
            if prelude_stripped.startswith('@media') or prelude_stripped.startswith('@supports'):
                inner = _clean_at_block_body(body)
                if inner.strip():
                    pieces.append(leading + prelude + '{' + inner + '}')
                continue
            if _is_nav_selector(prelude_stripped):
                continue
            pieces.append(leading + prelude + '{' + body + '}')
        return opening + ''.join(pieces) + closing

    return re.sub(
        r'(<style[^>]*>)(.*?)(</style>)',
        clean_one,
        html,
        flags=re.DOTALL
    )


HIDE_NAV_SELECTOR_PATTERNS = [
    re.compile(r'(^|\s|,)nav\s+ul\b'),
    re.compile(r'(^|\s|,)\.nav-menu\b'),
    re.compile(r'(^|\s|,)header\.site-header\b'),
    re.compile(r'(^|\s|,)header\s*>\s*nav\b'),
]


def check_mobile_nav_not_hidden(html):
    """Return list of offending rule descriptions; empty list = pass."""
    findings = []
    for sm in re.finditer(r'<style[^>]*>(.*?)</style>', html, re.DOTALL):
        css = sm.group(1)
        def walk(css_text, in_mobile_media):
            for leading, prelude, body in _iter_top_level_rules(css_text):
                ps = prelude.strip()
                if not ps:
                    continue
                if ps.startswith('@media print'):
                    continue
                if ps.startswith('@media') or ps.startswith('@supports'):
                    mw = re.search(r'max-width\s*:\s*(\d+)px', ps)
                    is_mobile = bool(mw and int(mw.group(1)) <= 768)
                    walk(body, in_mobile_media or is_mobile)
                    continue
                if not in_mobile_media:
                    continue
                if any(p.search(ps) for p in HIDE_NAV_SELECTOR_PATTERNS):
                    if re.search(r'display\s*:\s*none\b', body):
                        findings.append(ps + ' { ... display: none; ... }')
        walk(css, in_mobile_media=False)
    return findings
