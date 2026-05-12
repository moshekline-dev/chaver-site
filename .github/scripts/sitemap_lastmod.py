#!/usr/bin/env python3
"""
sitemap_lastmod.py — Add <lastmod> dates to sitemap.xml from git commit history.

Usage:
    cd /path/to/chaver-site        (your local repo root)
    python sitemap_lastmod.py       (reads sitemap.xml, writes sitemap-updated.xml)
    python sitemap_lastmod.py --inplace   (overwrites sitemap.xml directly)

How it works:
    For each <url> in the sitemap, converts the URL path to a likely local
    file path, then runs `git log` to get the last commit date for that file.
    If the file isn't found or has no git history, uses today's date.

    Does NOT touch URLs that already have <lastmod> tags.
"""

import xml.etree.ElementTree as ET
import subprocess
import os
import sys
from datetime import date
from urllib.parse import unquote

SITE_ROOT = "https://chaver.com"
NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"

# Register namespace to avoid ns0: prefix in output
ET.register_namespace("", NAMESPACE)


def url_to_filepath(url: str) -> list[str]:
    """Convert a sitemap URL to candidate local file paths."""
    path = url.replace(SITE_ROOT, "").lstrip("/")
    path = unquote(path)  # decode %20 etc.

    candidates = []

    if path == "" or path == "/":
        candidates.append("index.html")
    elif path.endswith("/"):
        candidates.append(f"{path}index.html")
    elif path.endswith(".pdf") or path.endswith(".htm"):
        candidates.append(path)
    elif "." in path.split("/")[-1]:
        # Already has an extension
        candidates.append(path)
    else:
        # Clean URL — try with .html extension
        candidates.append(f"{path}.html")
        candidates.append(path)  # might be a directory with index.html
        candidates.append(f"{path}/index.html")

    return candidates


def get_git_date(filepath: str) -> str | None:
    """Get last commit date for a file from git log. Returns YYYY-MM-DD or None."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", filepath],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            # git outputs ISO format like 2026-04-16T10:30:00+03:00
            # We just need the date part
            return result.stdout.strip()[:10]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def process_sitemap(input_file: str, output_file: str):
    tree = ET.parse(input_file)
    root = tree.getroot()

    ns = {"sm": NAMESPACE}
    today = date.today().isoformat()

    stats = {"updated": 0, "already_had": 0, "fallback": 0, "total": 0}

    for url_elem in root.findall("sm:url", ns):
        stats["total"] += 1
        loc_elem = url_elem.find("sm:loc", ns)
        lastmod_elem = url_elem.find("sm:lastmod", ns)

        if loc_elem is None:
            continue

        # Skip if lastmod already exists
        if lastmod_elem is not None:
            stats["already_had"] += 1
            continue

        url = loc_elem.text
        candidates = url_to_filepath(url)

        git_date = None
        found_file = None
        for candidate in candidates:
            if os.path.exists(candidate):
                git_date = get_git_date(candidate)
                found_file = candidate
                if git_date:
                    break

        if git_date:
            stats["updated"] += 1
        else:
            git_date = today
            stats["fallback"] += 1

        # Insert <lastmod> after <loc>
        new_lastmod = ET.SubElement(url_elem, f"{{{NAMESPACE}}}lastmod")
        new_lastmod.text = git_date

        # Move lastmod to be right after loc (for readability)
        loc_index = list(url_elem).index(loc_elem)
        url_elem.remove(new_lastmod)
        url_elem.insert(loc_index + 1, new_lastmod)

    # Write output with XML declaration
    tree.write(output_file, xml_declaration=True, encoding="UTF-8")

    # Pretty-print: add newlines (ElementTree doesn't indent well)
    # Re-read and format
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Add newlines between url entries for readability
    content = content.replace("</url><url>", "</url>\n<url>")
    content = content.replace("</url></urlset>", "</url>\n</urlset>")
    content = content.replace("<urlset", "\n<urlset")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nSitemap lastmod update complete:")
    print(f"  Total URLs:         {stats['total']}")
    print(f"  Already had date:   {stats['already_had']}")
    print(f"  Updated from git:   {stats['updated']}")
    print(f"  Fallback (today):   {stats['fallback']}")
    print(f"\nOutput: {output_file}")


if __name__ == "__main__":
    input_file = "sitemap.xml"
    inplace = "--inplace" in sys.argv

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run this from your repo root.")
        sys.exit(1)

    # Check we're in a git repo
    if not os.path.exists(".git"):
        print("Warning: Not in a git repo root. Git dates will use fallback.")

    output_file = input_file if inplace else "sitemap-updated.xml"
    process_sitemap(input_file, output_file)

    if not inplace:
        print(f"\nReview the output, then: copy sitemap-updated.xml sitemap.xml")
