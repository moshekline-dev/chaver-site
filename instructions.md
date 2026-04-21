# Torah Weave Project — Instructions for Claude (Cowork)

## Project Overview
Torah commentary project at chaver.com. 86 total Torah units (76 regular + 10 irregular). Site runs on Cloudflare Pages via GitHub (repo: chaver-site), deployed through GitHub Desktop. Site built in Microsoft Expression Web using Dynamic Web Templates (DWT). Main CSS at `[repo]/torah-weave/Admin/Assets/CSS/main.css`.

Author: Moshe Kline. 40 years of peer-reviewed structural Torah scholarship. Author of *Before Chapter and Verse* (2022). Publications in JBL (2025), JHS (2008), SBL book chapter.

## COWORK ENVIRONMENT

Claude has direct access to local files. This changes the workflow:

- **READ main.css BEFORE creating any HTML.** No guessing at classes — open the file and verify.
- **READ existing exemplars** (commentaries, articles) before creating similar content. Match exact structure.
- **GREP the repo** to verify structural claims, find patterns, check links.
- **WRITE files directly** to the working folder. Do not create files in arbitrary locations.
- **NEVER modify deployed files in the repo** without explicit permission. Work in the project folder; Moshe deploys via Expression Web and GitHub Desktop.

## FILE DELIVERY PROTOCOL (CRITICAL)

Every HTML file for the site is delivered as TWO files:

**File 1 — Clean HTML for DWT attachment:**
- Head contains ONLY `<title>` and page-specific `<style>` (if truly needed)
- NO meta description, NO keywords, NO schema JSON-LD, NO OG/Twitter tags
- NO Google Analytics
- NO DWT markers (BeginEditable, EndEditable, BeginTemplate)
- NO header, nav, footer, `<main>` wrapper
- Expression Web adds all DWT elements on attachment; pre-existing markers PREVENT proper attachment

**File 2 — Meta tags (separate file, named [filename]-meta.html):**
- Description, keywords, canonical, OG, Twitter, schema JSON-LD
- Pasted into the "meta" editable region AFTER DWT attachment in Expression Web

**Before delivering any file, run this checklist:**
1. Does the head contain ONLY title + page CSS? (no meta, no schema, no OG)
2. Are ALL CSS classes from main.css? (open main.css and verify — do not guess)
3. Are there any DWT markers? (there must be none)
4. Is there a separate meta file?

## CSS RULES (CRITICAL)

- **FIRST STEP for any file creation:** Open main.css and read the relevant sections
- NEVER invent colors, classes, or styles
- Use ONLY existing classes from main.css
- NO inline styles, NO hardcoded colors
- If a needed class doesn't exist, ASK Moshe first — then add to main.css as a separate deliverable
- Page-specific CSS only for elements that exist nowhere else on the site

## LANGUAGE AND VOICE
- **Commentary voice:** Kugel style — conversational scholarship, "we/us," progressive revelation, "suggests" not "proves"
- **Never use "God" generically** — use Elohim or YHWH specifically. "Deity" for generic divine references
- **Never use "theological"** — not descriptive enough. Use specific terms
- **Never use "salvation"** — use "deliverance," "rescue," or "preservation"
- **Never use:** profound, remarkable, striking, extraordinary, crucial, critical, essential, transforms, revolutionary
- **Pure literary analysis only** — no interpretive judgments. Describe what the text does structurally

## STRUCTURAL RULES
- **Unit notation:** Numbers = rows, UPPERCASE = columns (A, B), lowercase = subdivisions. Example: 2Bc = Row 2, Column B, subdivision c
- **Unit dimensions:** 76 regular (e.g., 3×2), 10 irregular (e.g., 12221). All units are symmetrical
- **NEVER state structural claims from memory** — verify from Torah Database, source files, or ask Moshe
- **Patterns must come from actual highlighted markers** in woven Torah HTML (horizontal1, vertical1, closure, ciasm1, ciasm2 classes). Never fabricate
- **Seven independent units** (not in triadic patterns): Gen 4, Exo 5/10/15, Lev 13, Num 7, Deut 13

## FILE NAMING
- Unit commentaries: `[book]-unit-[#]-commentary.html`
- Unit texts: `[book]-unit-[#].html`
- No leading zeros. Lowercase only. All URLs and file paths lowercase

## URL FORMAT
- Units: `/torah-weave/[Book]/[book]-unit-X/[book]-unit-X.html`
- Book analysis: `/torah-weave/[Book]/genesis-analysis/`
- Unit references in commentaries MUST include links

## PREPARATION BEFORE WRITING COMMENTARIES
1. Open and read 2–3 existing commentaries from the repo
2. Open and read ALL parts A/B/C/D for the relevant book
3. Open main.css and identify relevant classes
4. Grep the unit HTML for actual pattern markers before describing patterns
5. Verify unit format against the Torah Database spreadsheet
6. Ask Moshe for permission before modifying his content
7. Never describe a unit's content from assumption — read it first

## KEY FILES IN THIS PROJECT
- **Torah_Database_Updated.xlsx:** All 86 unit formats and verse references. Authoritative source.
- **main.css:** All site styles. Open and read before creating any HTML.
- **instructions.md:** This file. Read at session start.
- **The-Sixth-Book-of-theTorah.html:** Current working version of the major essay (~38K words)
- **The-Sixth-Book-of-theTorah-meta.html:** Meta tags for the essay (step 2 of deployment)
- **The-Sixth-Book-of-theTorah-editorial-outline.md:** Status of every section
- **envelope-vs-core-table.md:** Working reference for envelope/core analysis

## BC&V REFERENCES
*Before Chapter and Verse* is secondary. Site content (Genesis series, unit commentaries, articles) is now primary. When both exist for a topic, cite the site content first, BC&V second.

## DEPLOYMENT WORKFLOW
1. Claude creates clean HTML + meta file in project folder
2. Moshe opens HTML in Expression Web, attaches DWT
3. Moshe pastes meta tags into "meta" editable region
4. Moshe saves, commits via GitHub Desktop, pushes
5. Moshe purges Cloudflare cache
6. Git case-sensitivity workaround on Windows: rename → temp → commit → correct case → commit → push

## CURRENT STATUS
**Major essay:** "The Voice Is the Voice of YHWH, and the Hands Are the Hands of Elohim: The Sixth Book of the Torah." Three stubs remain: First Look at the Warp (~171w → 400w), Warp Thread M (~136w → 500w), Conclusion (~232w → 400-500w). See editorial outline for full details.

**Leviticus commentary series:** Mid-book; outer ring (Units 1–3, 20–22) completed.

**Insights articles:** Short popular SEO articles under site menu category "Insights."
