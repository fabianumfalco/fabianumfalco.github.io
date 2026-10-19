# Fabiano Falcão — personal website

English-language professional portfolio and resume, hosted on GitHub Pages.

## Local preview

Run from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/. Use an HTTP server to preview the SVG icon sprite and browser preferences correctly.

## Maintained files

- `index.html`: professional overview, expertise, research and contact.
- `resume.html`: academic background and complete professional history.
- `assets/css/site.css`: maintained styles, responsive rules, themes, focus and print layout.
- `assets/js/dark-mode.js`: early theme application, system preference and local persistence.
- `assets/js/site.js`: progressively enhanced mobile navigation.
- `assets/images/icons.svg`: only the Font Awesome icons used by the pages, collected from the existing licensed assets; preserves icon attribution.
- `sitemap.xml` and `robots.txt`: canonical public URLs. Update if the domain changes.
- `CONTENT_REVIEW.md`: factual sources and information requiring the owner's confirmation.

The site has no build step or runtime package dependencies. It uses system fonts and local assets. Navigation remains available without JavaScript; appearance follows browser defaults if scripts are unavailable.

`theme-1.css` is a frozen legacy vendor stylesheet containing Bootstrap and template styling. Keep `site.css` after it and make future visual changes in `site.css`. The legacy SCSS files do not fully reproduce the deployed vendor CSS; do not regenerate it over the current stylesheet. Unused vendor assets remain in the repository but are not loaded by the pages.

Headers and footers are static HTML so each page works independently. Keep them synchronized when changing navigation, profile details, theme options or attribution. The local checker compares these shared regions while allowing the active navigation link to differ.

## Validation

```sh
python3 scripts/check_site.py
node --check assets/js/dark-mode.js
node --check assets/js/site.js
```

Before publication, preview both pages at 320, 375, 768, 1024 and 1440 pixels. Check keyboard focus, skip link, menu expansion and Escape, light/dark/system appearance, persistence between pages, no-JavaScript navigation and resume printing. Automated checks complement manual screen-reader and visual review.

## Content and licensing

Use `CONTENT_REVIEW.md` before changing dates, degree names or publication claims. The owner's degree completion in the first half of 2026 and the official dissertation defense on 26 May 2026 are distinct facts.

Preserve the template credit in both footers under the free license in `license.txt`. Icons come from Font Awesome Free and retain CC BY 4.0 attribution in the SVG sprite. Other vendor files retain their existing license notices.

Publishing and Git operations are separate from editing: do not commit or push without the owner's explicit approval.
