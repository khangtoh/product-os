# Working in this repository

- Keep `src/` dependency-free. No build step, no bundler, no framework.
- Use plain ES modules and vanilla DOM APIs.
- Two-space indentation in JavaScript and HTML.
- Prefer small pure functions in `src/store.js` and `src/search.js`; keep DOM work in `index.html`.
- Do not add analytics, telemetry, or third-party scripts.
- Run nothing on save. There are no tests yet; verify by opening `src/index.html`.

## Product context

For product work, read PRODUCT.md, product/AGENTS.md, and product/STATE.md
before making changes. Follow linked vision, requirements, roadmap, and
work records as needed. Update the affected context after material
product decisions or results.
