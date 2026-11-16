# sinha-disha.github.io

Personal website of Disha Sinha, served by GitHub Pages at <https://sinha-disha.github.io/>.

It is a single static page with no build step: `index.html` holds the markup, styles and a small script (theme toggle, mobile menu, reveal on scroll, active section in the nav).

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | The whole site |
| `assets/img/logo.svg`, `logo-dark.svg` | Site logo for dark and light backgrounds |
| `assets/img/photo.jpg` | Profile photo (hero and link previews) |
| `assets/img/favicon.svg`, `apple-touch-icon.png` | Favicon and home-screen icon |
| `assets/logos/` | Institution logos used in Experience and Education |
| `scripts/make_logo.py` | Regenerates the logo and favicon SVGs |

## Editing

- **Content:** edit `index.html` directly. Each section (`#about`, `#experience`, `#education`, `#publications`, `#skills`, `#honors`) is a plain block of HTML.
- **Colours:** the teal palette is the set of CSS variables at the top of `index.html`, one block for dark and one for light.
- **Photo:** replace `assets/img/photo.jpg` (square, at least 360 × 360).
- **Logo:** change `PALETTES` or the geometry in `scripts/make_logo.py`, then run `python3 scripts/make_logo.py` from the repository root.

## Logo credits

Institution logos belong to their owners and are used only to identify affiliations: Indiana State University (Wikimedia Commons, public domain), Jadavpur University and Dr. B. R. Ambedkar University Delhi (Wikipedia, non-free logos), the Field Museum (historic logo, Wikimedia Commons, public domain) and SPAARC (from spaarc.org).
