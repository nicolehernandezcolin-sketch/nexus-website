# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

NEXUS is a single-file static website (`nexus-final7.html`) — no build step, no dependencies, no package manager. Open the file directly in a browser to run it.

## Architecture

The entire site lives in one HTML file (~3800 lines) structured as:

- **Inline `<style>` blocks** — CSS is split across multiple `<style>` tags, each scoped to a page section
- **Page divs** — each "page" is a `<div class="page" id="pg-*">` fixed to the viewport; only one is visible at a time via the `.on` class
- **One `<script>` block** at the bottom handles all interactivity

### Pages

| ID | Line | Description |
|----|------|-------------|
| `home` | ~430 | Solar system hub — animated globe, orbiting planet nav nodes |
| `pg-music` | 641 | Artist archive + Nexus Stage |
| `pg-dance` | 1212 | Dance page |
| `pg-fashion` | 1739 | Fashion/runway page with canvas animation |
| `pg-film` | 2148 | Film page with curtain theater sub-pages |
| `pg-golf` | 2839 | Golf tournament with canvas green + rolling ball |

### Navigation system

`go(id)` (line 3140) — all page transitions run through this function. It triggers a circular wipe via `#wipe` (`clip-path` circle expand/collapse), swaps `.on` classes, and resets scroll. Elements use `data-go="pg-*"` attributes to trigger navigation.

### Animation systems

Each interactive page has its own canvas-based init function, lazy-loaded on first visit:

- `initGolf()` — draws canvas golf green, places clickable ball nodes
- `initFashion()` — runway canvas with runway lights + flash entrance
- Home star field — `<canvas id="stars">` with cursor parallax (cursor slows nearby stars)
- Music page — `<canvas id="music-star-canvas">` with green-tinted stars
- Globe intro — SVG stroke-dashoffset animation sequence with precise delays, then CSS spin

### Design tokens (CSS variables on `:root`)

`--space` (bg dark), `--green` / `--glow` (`#3ECF5A`), `--orange` (`#E07828`), `--cream`, `--white`, `--black`. Green is the primary accent throughout; orange is fashion-only.

### Fonts

Loaded from Google Fonts: `Cormorant Garamond` (serif body/display), `Space Mono` (UI/labels), `Unbounded` (logo/headings).

### Cursor

Custom cursor (`#cur`) replaces the system cursor site-wide. Grows on hover via `.h` class. The `cursor:none` is set on `body` and repeated on interactive elements.

## Scripts

- `extract_images.py` — extracts all base64-encoded images from `nexus-final7.html` into `images/`, rewrites `src` attributes to use file paths. Run with `python3 extract_images.py`.

## Verification after edits

Because the file is 3800+ lines of hand-written HTML, structural bugs are easy to introduce and hard to spot visually. After any edit that touches repeated HTML structures (artist cards, dancer profiles, film rows, golf holes, etc.), run this JS in the browser console to verify grid children match expectations:

```js
// Example: artist grid should have exactly 14 direct children
document.querySelector('.artist-grid').children.length
```

For any CSS grid or flex container, the rule is: **only direct children are layout items**. A missing `</div>` anywhere inside a card causes all subsequent cards to nest inside it and disappear from the grid — the browser won't warn you.

Quick sanity checks to run after editing card-based HTML:
- Count direct children of the grid/container with JS and compare to expected
- Grep for the opening tag count vs closing tag count: `grep -c "<div class=\"artist-card\">" nexus-final7.html` should match the number of cards

## Editing guidelines

- When adding a new page: add a `<div class="page" id="pg-*">` div, a planet node on the home page with `data-go="pg-*"`, and a click listener in the script block.
- Page-specific CSS goes in its own `<style>` block near the HTML for that page, not in the shared block at the top.
- The `.on` class controls visibility — never use `display:none` or `visibility` to show/hide pages.
- All interactive elements need `cursor:none` to match the custom cursor.
- Sub-page navs use a 3-column grid (`1fr auto 1fr`) to centre the globe orb: back button left, `.nav-globe-orb` centre, logo/label right.
