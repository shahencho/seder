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
| `generate_menu.py` | Python script that generated all 133 menu items programmatically from structured data (see below). Re-run this if items need to be added/edited/removed — much safer than hand-editing the HTML. |
| `photo-naming-guide.txt` | Full list of all 133 dishes mapped to their required photo filename. Hand this to whoever is sourcing/shooting photos. |
| `menu_sections.html` | Intermediate output from the generator script (the `<main>` content only) — not needed directly, kept for reference. |

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

## Language toggle

EN / AR / RU buttons in the header. Currently only the header text (brand name + welcome line) is wired to translate — full item-level translation (all 133 names/descriptions in Arabic and Russian) is **not yet built**. Layout stays left-to-right in all three languages (client's explicit call — text translates, layout doesn't flip to RTL).

---

## What's NOT done yet (next steps)

- [ ] Real photos from the restaurant (blocked on them — see naming guide)
- [ ] Full Arabic and Russian translation of all 133 item names/descriptions
- [ ] Deployment to the DigitalOcean droplet (menu currently only exists as a local HTML file)
- [ ] QR code generation pointing at the deployed URL
- [ ] Sanity check with the restaurant on the halal/vegetarian/spicy tags — these were assigned by reasonable judgment from the descriptions, not confirmed with the kitchen
- [ ] Decide on scope for the productized version (for other restaurants) once feedback comes back from this pilot

---

## How to resume work in VS Code

1. Open this folder in VS Code.
2. `seder-palms-menu.html` can be opened directly in a browser (right-click → "Open with Live Server" if you have that extension, or just double-click the file) to preview.
3. To add/edit/remove menu items: edit the `DATA` dictionary at the top of `generate_menu.py`, then re-run it:
   ```
   python3 generate_menu.py
   ```
   This regenerates `menu_sections.html`. You'd then need to splice that back into `seder-palms-menu.html` between the `<main>` and `</main>` tags (or ask Claude to do this step again).
4. To deploy: copy `seder-palms-menu.html` (and the `photos/` folder once populated) to the DigitalOcean droplet, serve as a static file (nginx or any basic web server), generate a QR code pointing at its public URL.
5. Git: `git init`, add a `.gitignore` if needed, commit, then `git remote add origin <your-repo-url>` and `git push -u origin main`.
