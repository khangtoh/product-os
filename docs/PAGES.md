# Publish the onboarding guides with GitHub Pages

The [onboarding hub](onboarding/index.html) links to the guides for [new projects](onboarding/new-project.html) and [existing projects](onboarding/existing-project.html). All three pages work directly from a downloaded checkout.

## What gets published

The [Onboarding pages workflow](../.github/workflows/onboarding-pages.yml) builds a fixed allowlist: `index.html`, `new-project.html`, and `existing-project.html` from `docs/onboarding/`, plus an empty `.nojekyll` marker. It never uploads the repository or the full docs directory.

The [build helper](../scripts/build_onboarding_site.mjs) keeps links between the three HTML pages relative, so they work under a GitHub Pages project path. It converts relative Markdown source links to the same commit's GitHub file view. Those source documents remain in GitHub and still require repository access. The build verifies linked page anchors and the existence of linked source files.

Pull requests and relevant pushes to `main` build and upload a reviewable Pages artifact. They do not publish it. A workflow dispatch also defaults to build-only.

## Enable publication after review

The repository is private. GitHub documents that Pages sites may be public even when their source repository is private. Review and approve the three HTML pages for that audience before enabling publication. Do not change repository visibility just to enable this feature.

GitHub Pages for a private repository requires an eligible GitHub plan. Repository Pages administration is not available through the current connected GitHub tools, so an administrator must perform the settings step.

1. Review and merge the onboarding changes into `main`.
2. Open repository **Settings → Pages**.
3. Under **Build and deployment → Source**, select **GitHub Actions**. If this is unavailable, check the account plan or policy; keep the repository private.
4. Open **Actions → Onboarding pages → Run workflow**.
5. Choose `main`, explicitly enable `publish`, and run it.
6. Read the published URL from the **github-pages** environment or deployment step. Without a custom domain, the expected project URL is `https://khangtoh.github.io/product-os/`.

The deployment job requires the explicit publish input and the `main` ref. A later merge updates the build artifact; publishing an update requires another explicit dispatch.

## Build locally

Use Node.js 22 and a new output directory outside the repository:

```sh
node scripts/build_onboarding_site.mjs /tmp/product-os-onboarding-site
```

The helper refuses an existing output directory. Choose a fresh path for another build. Open its `index.html` in a browser, or serve the output with a local static-file server.

The source HTML files keep repository-relative Markdown links for offline checkout use. The generated output rewrites those links for Pages without editing the source files.

## Validation

The existing Demo checks workflow checks repository and isolated-template Markdown links. The Onboarding pages workflow additionally builds the exact deployment artifact and checks HTML navigation and source-file references. Browser visual verification is a separate check.

Reference: [GitHub's publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
