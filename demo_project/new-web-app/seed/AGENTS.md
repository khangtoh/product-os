# Working in this repository

- Keep `src/` dependency-free. No build step, no bundler, no framework.
- Use plain ES modules and vanilla DOM APIs.
- Two-space indentation in JavaScript and HTML.
- Prefer small pure functions in `src/store.js` and `src/search.js`; keep DOM work in `index.html`.
- Do not add analytics, telemetry, or third-party scripts.
- Run nothing on save. There are no tests yet; verify by opening `src/index.html`.
