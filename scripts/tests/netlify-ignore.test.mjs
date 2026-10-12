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
