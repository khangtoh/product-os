#!/usr/bin/env node
// Package only the reviewed onboarding HTML; keep repository source links on GitHub.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, posix, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const names = ['index.html', 'new-project.html', 'existing-project.html'];
const sourceDir = 'docs/onboarding';
const destination = process.argv[2];
if (!destination) throw new Error('Usage: node scripts/build_onboarding_site.mjs NEW_OUTPUT_DIRECTORY');
const output = resolve(destination);
if (existsSync(output)) throw new Error('Output already exists; choose a new directory: ' + output);
const revision = encodeURIComponent(process.env.GITHUB_SHA || 'main');
const sourceURL = 'https://github.com/khangtoh/product-os/blob/' + revision + '/';
const pages = new Map(names.map(name => [
  name, readFileSync(join(root, sourceDir, name), 'utf8'),
]));
const ids = new Map([...pages].map(([name, html]) => [
  name, new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1])),
]));

const built = [...pages].map(([name, html]) => {
  if (/<(?:script|iframe|link|img)\b/i.test(html)) {
    throw new Error(name + ': unexpected script or external resource');
  }
  const result = html.replace(/href="([^"]+)"/g, (attribute, href) => {
    if (/^https:\/\//.test(href)) return attribute;
    if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith('/')) {
      throw new Error(name + ': unsupported URL ' + href);
    }
    const [target, anchor] = href.split('#');
    if (!target || names.includes(target)) {
      const targetName = target || name;
      if (anchor && !ids.get(targetName).has(anchor)) {
        throw new Error(name + ': missing anchor ' + href);
      }
      return attribute;
    }
    const repoPath = posix.normalize(posix.join(sourceDir, target));
    if (repoPath.startsWith('../') || !repoPath.endsWith('.md') ||
        !existsSync(join(root, repoPath))) {
      throw new Error(name + ': unresolvable source link ' + href);
    }
    return 'href="' + sourceURL + repoPath +
      (anchor ? '#' + anchor : '') + '"';
  });
  return [name, result];
});

// Create only after all input pages and links have passed validation.
mkdirSync(output);
for (const [name, html] of built) writeFileSync(join(output, name), html);
writeFileSync(join(output, '.nojekyll'), '');
console.log('Built 3 onboarding pages in ' + output);
console.log('Repository Markdown stays on GitHub; no other repository files are copied.');
