# Seder Palms Restaurant — Digital Menu

## What this is

A branded, mobile-first digital menu (QR-code style) for **Seder Palms Restaurant**, a Swiss-run restaurant inside the Seder Village compound in Riyadh. Built as the first pilot for a broader product idea: a digital menu tool that, unlike most QR-menu platforms on the market, is designed to actually look like the restaurant's own brand rather than a generic template.

**Goal of this pilot:** ship something in 1–2 days, get it in front of the restaurant, get real feedback, then decide whether to productize it for other restaurants.

No POS integration, no online ordering — this is a **view-only branded menu** guests reach by scanning a QR code at the table. Prices, photos, and structure are pulled straight from the restaurant's physical menu (4 photographed pages).

---

## Why this design direction

Researched the existing QR-menu market first (Toast, Square, Popmenu, MustHaveMenus, TableQR, Digitalemenu, MenuHoster, and others). The consistent gap across nearly all of them: they either bundle a full POS system (expensive, overkill) or are template-driven tools that all end up looking the same — "looks like the software, not the restaurant."

This build leans into brand-specific design instead of a template, MENA-first details (SAR pricing with USD equivalent, halal tagging, Arabic/Russian language support), and stays lightweight — a static, fast-loading page with no ordering backend to maintain.

---

## Files in this project

| File | Purpose |
|---|---|
| `seder-palms-menu.html` | The complete menu — single-file HTML/CSS/JS, no build step needed. This is the deployable artifact. |
| `generate_menu.py` | Python script that generates all 133 menu items (English + translations) and writes them directly into `seder-palms-menu.html`. Re-run this if items or translations need to be added/edited/removed — much safer than hand-editing the HTML. |
| `photo-naming-guide.txt` | Full list of all 133 dishes mapped to their required photo filename. Hand this to whoever is sourcing/shooting photos. |

---

## Design system

- **Colors:** deep palm green (`#2B4A3A`) + brass gold accent (`#B98A3D`) + warm sand background (`#EDE7DA`) — chosen to tie to the "Palms" name and avoid the generic AI-template look (cream + terracotta).
- **Type:** Space Grotesk (headings/display) + Inter (body) — modern, geometric, per the client's request for a "modern" direction (not ornate/calligraphic).
- **Signature detail:** a thin frond-line SVG divider under the header, a subtle nod to "Palms" without being literal.
- **Layout:** mobile-first, single column. Sticky header (logo, welcome line, language toggle) → sticky filter chip bar → sticky category tabs → scrollable item cards.

---

## Structure

**3 top-level tabs**, each containing multiple subcategories (15 total, matching the physical menu):

- **Food** — Breakfast, Salad, Main Course, Appetizer, Sandwiches, Pizza, Create Your Own Pasta, Soup, Sides
- **Dessert** — Dessert Menu
- **Beverages** — Frappe & Coffee, Fresh Juice, Smoothies, Mojitos, Soft Drinks

**133 items total**, each with:
- Name, short description
- Price in SAR + USD equivalent (converted at the official peg, 1 USD = 3.75 SAR)
- Dietary/attribute tags: Halal, Vegetarian, Seafood, Spicy (visible as small labels on the card)
- A photo slot (see below)

---

## Filter system

Four filter chips sit under the header: **Halal, Vegetarian, Seafood, Spicy**. Each chip cycles through three states on tap:

1. **Any** (default, gray) — no effect
2. **Only show this** (green, checkmark) — filters menu to items with that tag
3. **Hide this** (red, ✕) — filters out items with that tag

This covers both "show me X" and "hide X from me" (useful for allergies/preferences) with a single control per attribute, rather than needing two separate toggles. Filters combine (AND logic) — e.g. Halal + Spicy shows only dishes tagged both. If a category has zero matches, it shows a "no dishes match" message instead of going blank.

---

## Photo system — action needed from the restaurant

Every item currently shows a **gray placeholder box** reading "PHOTO PENDING." This is intentional — no photos exist yet from the restaurant.

**How to add real photos:**
1. Create a folder named exactly `photos` in the same directory as `seder-palms-menu.html`.
2. Save each photo as a `.jpg`, named exactly per `photo-naming-guide.txt` (e.g. `photos/grilled-rosemary-salmon.jpg`).
3. That's it — no code changes needed. The page tries to load each photo automatically; if the file exists, it displays; if not, it silently falls back to the placeholder. You can roll out photos gradually, one dish at a time.

**Note:** filenames currently assume `.jpg`. If photos come in as `.png` or `.webp`, the `<img>` `src` paths in the HTML (or the `slugify`/`render_item` function in `generate_menu.py`) need a one-line update to match.

---

## Language toggle & translation storage

EN / AR / RU buttons in the header. **Russian is fully translated** (all 133 item names/descriptions, all 15 subcategory titles, the 3 tabs, the 4 dietary tags, and the fixed UI strings). Arabic is wired up the same way but not yet populated with copy. Layout stays left-to-right in all three languages (client's explicit call — text translates, layout doesn't flip to RTL).

**Where translations live:** `generate_menu.py` is the single source of truth for every language, not just English.

- **Per-dish text** — each item tuple in `DATA` optionally ends with a 5th element, a dict keyed by language code sitting right next to the English it translates:
  ```python
  ("Hummus", 14, "A smooth, creamy blend of chick peas...", ["halal", "vegetarian"],
   {"ru": {"name": "Хумус", "desc": "Нежная паста из нута..."}}),
  ```
  A missing language (or a missing `name`/`desc` inside it) silently falls back to English — nothing breaks if a translation is only half-filled-in.
- **Fixed UI text** (tab names, the 15 subcategory headers, the 4 dietary tag labels, filter hint, footer, "no results" message) — small lookup dicts near the top of the file: `TAB_I18N`, `SUBCAT_I18N`, `TAG_I18N`, `UI_I18N`.
- **To correct a Russian translation:** find the item/string in `generate_menu.py` (English and Russian are on the same line/block) and edit it, then re-run `python generate_menu.py`.
- **To add Arabic:** add an `"ar": {...}` entry next to each existing `"ru": {...}` entry (same shape), fill in `TAB_I18N`/`SUBCAT_I18N`/`TAG_I18N`/`UI_I18N`'s `"ar"` keys, then add `"ar"` to the `langs` list in `build_i18n_js()` inside `generate_menu.py`. No HTML/JS changes needed — the toggle button already exists and the rendering logic is language-agnostic.

**How the swap works in the browser:** the script embeds the translation data as JS objects in `seder-palms-menu.html` (between `// === I18N DATA START/END ===` markers) plus `data-i18n*` attributes on the relevant elements. Clicking a language button calls `applyTranslation(lang)`, which looks up each element's key in the matching dict and swaps its text, falling back to the original English if no translation exists for that language.

---

## What's NOT done yet (next steps)

- [ ] Real photos from the restaurant (blocked on them — see naming guide)
- [ ] Full Arabic translation of all 133 item names/descriptions (Russian is done — see "Language toggle & translation storage" above; Arabic slots into the identical structure)
- [ ] Deployment to the DigitalOcean droplet (menu currently only exists as a local HTML file)
- [ ] QR code generation pointing at the deployed URL
- [ ] Sanity check with the restaurant on the halal/vegetarian/spicy tags — these were assigned by reasonable judgment from the descriptions, not confirmed with the kitchen
- [ ] Decide on scope for the productized version (for other restaurants) once feedback comes back from this pilot

---

## How to resume work in VS Code

1. Open this folder in VS Code.
2. `seder-palms-menu.html` can be opened directly in a browser (right-click → "Open with Live Server" if you have that extension, or just double-click the file) to preview.
3. To add/edit/remove menu items (or translations): edit the `DATA` dictionary (and/or the `*_I18N` dicts) at the top of `generate_menu.py`, then re-run it:
   ```
   python generate_menu.py
   ```
   This regenerates `seder-palms-menu.html` **in place** — it rewrites the `<main>` section and the embedded translation objects directly, no manual copy-paste needed — and refreshes `photo-naming-guide.txt`.
4. To deploy: copy `seder-palms-menu.html` (and the `photos/` folder once populated) to the DigitalOcean droplet, serve as a static file (nginx or any basic web server), generate a QR code pointing at its public URL.
5. Git: `git init`, add a `.gitignore` if needed, commit, then `git remote add origin <your-repo-url>` and `git push -u origin main`.
