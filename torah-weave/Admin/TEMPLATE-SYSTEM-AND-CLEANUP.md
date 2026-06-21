# chaver.com — How the Template System Works + Open Cleanup Items

_Reference note for future maintenance sessions. Last updated June 21, 2026._

## How the site is built and updated

There is **no build step and no live templating engine**. Expression Web (now
discontinued) was the original "build tool," and the site has since moved off it.

- **The individual HTML pages are the source of truth.** What's on disk is what
  ships. Nothing regenerates or overwrites the pages, so edits to a page are safe
  and permanent.
- **Cross-page consistency is maintained manually, by propagation.** There are two
  **reference templates** — one English, one Hebrew. When a site-wide change is
  needed (e.g. a new footer link, a nav change), the workflow is:
  1. Update the relevant reference template (English and/or Hebrew).
  2. Have a Cowork agent rewrite every affected page in the repo to match the
     template.
  The template is a **reference**, not a live template — it does nothing on its own.
  Cowork is the propagation mechanism.

### Important consequence
"Edit the template and re-apply" does **not** cascade automatically. A human has to
trigger a Cowork propagation pass. The old Expression Web `.dwt` files are **dead**
and must not be treated as authoritative (see cleanup items).

## Known divergence (state as of June 2026)

The pages have drifted since the last full propagation pass:

- **Footers:** at least 3 distinct footer variants exist across the site. The
  **richer variant is the newest and the intended one** — it includes "Torah Units
  Dataset," "As It Was Written," and similar links. The reference template is
  **behind** this footer, not ahead of it.
  - ⚠️ **Before any full footer propagation:** update the reference template to match
    the richer/current footer first. Otherwise a propagation pass will overwrite the
    good footer with the template's older, poorer one.
- **Navs:** sampled pages share a newer nav (`<div class="nav-row">` with dropdown
  submenus). The old `.dwt` template has a simpler `<nav class="main-nav">` with 5
  flat links — also stale.

## Canonical URL convention

- Canonical form is **extensionless**: `https://chaver.com/{path-without-.html}`.
- Cloudflare 308-redirects the `.html` form to extensionless (pretty-URLs is on), so
  extensionless is the display/canonical form and the `.html` file is the source.
- Canonical tags live **per-page** in each file's `<head>`, placed right after
  `<meta name="description">`. They are NOT in any template. Generate each canonical
  by deriving it from the file path in code (domain + repo-relative path − `.html`),
  never by retyping slugs.
- Redirect-stub pages (e.g. a meta-refresh page that 301s server-side) should have
  **no canonical tag** at all.

## Open cleanup items (deferred — not yet done)

1. **Delete the 4 orphaned `.dwt` files.** They are dead Expression Web templates,
   stale and misleading. The June 2026 audit misread them as authoritative. Safe to
   remove once confirmed nothing references them as actual content.
2. **Strip vestigial DWT markers.** ~290 HTML pages still contain Expression Web
   `InstanceBegin` / `InstanceEnd` / `InstanceBeginEditable` comments. Harmless but
   noise; can be removed in a propagation pass.
3. **Footer/nav reconciliation pass.** Decide the single intended current footer and
   nav (the richer footer variant), update both reference templates to match, then
   run a full Cowork propagation so all pages converge. This is the proper fix for
   the divergence above — distinct from any narrow link fix.
4. **Old WordPress-export remnants.** Some paths still carry `/index.html` suffixes
   and other WP-export artifacts (e.g. in commentary pages). These contributed
   defunct-URL noise in Search Console. Clean up as encountered.
5. **Leaked staging subdomain (verify).** Earlier Search Console data showed a
   `tjq.qeb.temporary.site.chaver.com` host indexed. The repo scan found no
   references, so this is likely a Cloudflare/DNS-level subdomain, not a repo file —
   confirm it's blocked from indexing (noindex/robots) at the edge.

## Completed (June 21, 2026 session)

- Added per-page extensionless canonical tags to the 10 Insights pages and ~113
  other previously-untagged public pages.
- Fixed 10 broken Genesis links in The-Sixth-Book (missing `genesis-analysis/`
  subdir; converted to extensionless).
- Added in-body internal links from the homepage and the Torah-pdf landing page into
  the 10 Insights pages (previously reachable only via the nav dropdown).
- Converted `.html` internal hrefs to extensionless in the affected pages.
- Converted footer `http://www.facebook.com` / `http://www.youtube.com` links to
  `https://` across the public HTML pages (matched on full host strings only, to
  avoid touching namespace/DOCTYPE/citation http:// references).

## One-line summary for whoever's next

The pages are the source of truth; consistency is maintained by manually updating the
English/Hebrew reference templates and having Cowork propagate them across the repo.
The `.dwt` files are dead. The current footer is the richer variant; fix the template
to match it before any full propagation.
