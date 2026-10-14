import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { decide, nonSitePath } from '../netlify-ignore.mjs';

test('on-demand skips without Git history, with force-build taking precedence', () => {
  assert.equal(decide({ NETLIFY_ON_DEMAND: 'true' })[0], 0);
  assert.equal(decide({ NETLIFY_ON_DEMAND: 'true', NETLIFY_FORCE_BUILD: 'true' })[0], 1);
  assert.equal(decide({ NETLIFY_ON_DEMAND: 'false' })[0], 1);
  assert.equal(decide({ NETLIFY_ON_DEMAND: '' })[0], 1);
});

test('only a narrow set of paths is ignored', () => {
  for (const p of ['README.md', 'AGENTS.md', '.pages.yml', 'docs/guide.md', 'scripts/tests/test.py', 'scripts/netlify-ignore.mjs', 'scripts/generate-feature-image.py', 'scripts/theme-overrides.toml', '.github/workflows/a.yml', 'content-org/zzamboni.org']) {
    assert.equal(nonSitePath(p), true, p);
  }
  for (const p of ['content/post/a.md', 'content-legacy/a.html', 'content-pagescms/a.md', 'content-photos/a/index.md', 'content-org/images/a.jpg', 'assets/a.css', 'static/a.png', 'layouts/a.html', 'config/a.toml', 'themes/blowfish', 'netlify.toml', 'netlify/functions/a.mjs', 'package-lock.json', '.github/workflows-other/a.yml', '.github/actions/a.yml', 'unknown']) {
    assert.equal(nonSitePath(p), false, p);
  }
});

test('real Git comparisons preserve changes across commits, deletions and renames', () => {
  const cwd = mkdtempSync(join(tmpdir(), 'netlify-ignore-test-'));
  const git = (...args) => execFileSync('git', args, { cwd, encoding: 'utf8' }).trim();
  const put = (path, data) => { mkdirSync(dirname(join(cwd, path)), { recursive: true }); writeFileSync(join(cwd, path), data); };
  const commit = () => { git('add', '.'); git('-c', 'user.name=Test', '-c', 'user.email=test@example.org', 'commit', '-qm', 'test'); return git('rev-parse', 'HEAD'); };
  try {
    git('init', '-q'); put('README.md', 'one'); const a = commit();
    put('README.md', 'two'); const b = commit();
    const check = (before, after) => decide({ CACHED_COMMIT_REF: before, COMMIT_REF: after }, cwd)[0];
    assert.equal(check(a, b), 0);
    put('scripts/netlify-ignore.mjs', '// maintenance change'); const scriptsOnly = commit();
    assert.equal(check(b, scriptsOnly), 0);
    put('.github/workflows/build.yml', 'name: Test'); const workflowOnly = commit();
    assert.equal(check(scriptsOnly, workflowOnly), 0);
    put('content/post/a.md', 'post'); const c = commit();
    assert.equal(check(scriptsOnly, c), 1); // Workflow plus content changes still build.
    assert.equal(check(b, c), 1); // Scripts plus generated content still build.
    put('README.md', 'three'); const d = commit();
    assert.equal(check(b, d), 1); // Do not inspect only the last commit.
    assert.equal(decide({ NETLIFY_ON_DEMAND: 'true', CACHED_COMMIT_REF: b, COMMIT_REF: d }, cwd)[0], 0);
    mkdirSync(join(cwd, 'docs')); git('mv', 'content/post/a.md', 'docs/a.md'); const e = commit();
    assert.equal(check(d, e), 1); // Removed deployed file still requires a build.
    assert.equal(check(e, e), 1);
    assert.equal(check('f'.repeat(40), e), 1);
    assert.equal(decide({}, cwd)[0], 1);
    assert.equal(decide({ NETLIFY_FORCE_BUILD: 'true', CACHED_COMMIT_REF: a, COMMIT_REF: b }, cwd)[0], 1);
  } finally { rmSync(cwd, { recursive: true, force: true }); }
});

test('draft front matter requires valid TOML and an explicit boolean', async () => {
  const { isDraftPost } = await import('../netlify-ignore.mjs');
  for (const source of ['+++\ndraft = true\n+++\nbody', '\uFEFF+++\r\ndraft = true\r\n+++\r\nbody']) {
    assert.equal(isDraftPost(source), true);
  }
  for (const front of [
    'title = "post"', 'draft = false', 'draft = "true"', 'draft = true\ndraft = false',
    'draft = true\nDraft = false', 'draft = true\nbroken = [', '[params]\ndraft = true',
    'summary = """\ndraft = true\n"""',
  ]) assert.equal(isDraftPost(`+++\n${front}\n+++\nbody`), false, front);
  assert.equal(isDraftPost('---\ndraft: true\n---'), false);
  assert.equal(isDraftPost('body\n+++\ndraft = true\n+++'), false);
});

test('draft transitions, mixed commits, overrides and config changes', () => {
  const cwd = mkdtempSync(join(tmpdir(), 'netlify-drafts-test-'));
  const git = (...args) => execFileSync('git', args, { cwd, encoding: 'utf8' }).trim();
  const put = (path, data) => { mkdirSync(dirname(join(cwd, path)), { recursive: true }); writeFileSync(join(cwd, path), data); };
  const commit = () => { git('add', '.'); git('-c', 'user.name=Test', '-c', 'user.email=test@example.org', 'commit', '-qm', 'test'); return git('rev-parse', 'HEAD'); };
  const check = (before, after, env = {}) => decide({ CACHED_COMMIT_REF: before, COMMIT_REF: after, ...env }, cwd)[0];
  const post = (draft, body = '') => `+++\ntitle = 'Test'\ndraft = ${draft}\n+++\n${body}`;
  try {
    git('init', '-q');
    put('config/_default/hugo.toml', 'buildDrafts = false'); const base = commit();
    put('content-pagescms/a.md', post(true)); const added = commit();
    assert.equal(check(base, added), 0);
    assert.equal(check(base, added, { BUILD_DRAFTS: 'true' }), 1);
    assert.equal(check(base, added, { HUGO_BUILDDRAFTS: 'true' }), 1);
    assert.equal(check(base, added, { HUGO_CONFIG: 'other.toml' }), 1);
    assert.equal(check(base, added, { NETLIFY_FORCE_BUILD: 'true' }), 1);
    assert.equal(check(base, added, { NETLIFY_ON_DEMAND: 'true' }), 0);
    put('content-pagescms/a.md', post(true, 'updated')); const edited = commit();
    assert.equal(check(added, edited), 0);
    put('content-pagescms/a.md', post(false)); const published = commit();
    assert.equal(check(edited, published), 1);
    put('content-pagescms/a.md', post(true)); const unpublished = commit();
    assert.equal(check(published, unpublished), 1);
    git('mv', 'content-pagescms/a.md', 'content-pagescms/b.md'); const renamed = commit();
    assert.equal(check(unpublished, renamed), 0);
    assert.equal(check(published, renamed), 1);
    git('rm', '-q', 'content-pagescms/b.md'); const deleted = commit();
    assert.equal(check(renamed, deleted), 0);
    assert.equal(check(published, deleted), 1);
    put('content-pagescms/b.md', post(true)); put('static/image.png', 'image'); const mixed = commit();
    assert.equal(check(deleted, mixed), 1);
    put('config/staging/hugo.toml', 'buildDrafts = true'); const config = commit();
    put('content-pagescms/b.md', post(true, 'another edit')); const withDrafts = commit();
    assert.equal(check(config, withDrafts), 1);
    git('rm', '-q', 'config/staging/hugo.toml'); const reset = commit();
    put('content-pagescms/b.md', '+++\ndraft = true\nbroken = [\n+++'); const malformed = commit();
    assert.equal(check(reset, malformed), 1);
    assert.equal(check(malformed, reset), 1);
    put('content-pagescms/_index.md', post(true)); const section = commit();
    assert.equal(check(malformed, section), 1);
  } finally { rmSync(cwd, { recursive: true, force: true }); }
});
