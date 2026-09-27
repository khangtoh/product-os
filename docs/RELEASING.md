# Releasing ProductOS

[VERSION](../VERSION) is the framework release and the trigger. A push to `main`
that changes it runs the [release workflow](../.github/workflows/release.yml), which
releases that version once as a Git tag `vX.Y.Z` and a GitHub Release. Nothing is
published to a package registry.

The workflow and `scripts/release-kit/` are a shared release kit, byte-identical
with [specloop](https://github.com/khangtoh/specloop), which holds the source copy.
[release.config.json](../release.config.json) describes this repository's steps.
The kit needs Node.js 18 or later for maintainers who bump versions; adopting the
documentation model still needs no runtime.

## Release a version

Record the changes under `## Unreleased` in [CHANGELOG](../CHANGELOG.md), commit
them on `main`, then bump:

```sh
node scripts/release-kit/release.mjs bump minor   # or patch, major, or an explicit X.Y.Z
```

`bump` needs a clean tree and a version newer than the current one with no
existing tag. It writes VERSION, syncs "Current release" in the README and
"Template version" in `template/product/README.md`, turns `## Unreleased` into
`## X.Y.Z — date` with a fresh empty Unreleased section, commits `Release vX.Y.Z`
and pushes `main`. On another branch, or with `--no-push`, it only commits: merge
or push the commit to release. `node scripts/release-kit/release.mjs check`
confirms VERSION and the synced lines agree.

## What the workflow does

1. **plan**: skips a version whose tag exists, fails a version older than an
   existing tag, and releases only from `main`.
2. **verify**: installer and packaging tests, relative links and anchors in
   the repository and in an isolated template copy, and the release-kit tests.
3. **package**: `scripts/package_release.py` builds three reproducible archives,
   then checks them:
   - `product-os-X.Y.Z-codex-skill.tar.gz`: extract into `.agents/skills/`.
   - `product-os-X.Y.Z-claude-skill.tar.gz`: extract into `.claude/skills/`.
   - `product-os-X.Y.Z-template.tar.gz`: the blank `product/` instance.

   The skill archives equal what `install_skill.py` writes. `SHA256SUMS` and
   the verification evidence are added.
4. **publish**: nothing to do; no registry is configured.
5. **github-release**: tags the released commit and creates the release from
   this version's CHANGELOG section, the evidence, the archives and
   `SHA256SUMS`. An existing release is left unchanged.

A pull request that changes VERSION, the config or the kit runs the same steps as
a dry run. The `kit-drift` job fails when this copy of the kit differs from
specloop's `main`. Copy the three kit files from specloop to fix it; make kit
changes in specloop first.

To resume a failed release, fix the cause and re-run the workflow run. An
existing tag or release is kept, never replaced. Do not bump again.

0.2.0 predates the kit and has no tag. Do not dispatch the workflow for it:
`main` now contains unreleased changes, so a 0.2.0 tag would point at the wrong
content. Release the next version with `bump`.
