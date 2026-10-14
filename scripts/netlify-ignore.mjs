// Netlify ignore convention: 0 skips, 1 builds. No npm dependencies required.
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import toml from './vendor/smol-toml/index.cjs';

export function isDraftPost(source) {
  const match = /^\uFEFF?\+\+\+\r?\n([\s\S]*?)^\+\+\+[ \t]*\r?$/m.exec(source);
  if (!match || match.index !== 0) return false;
  try {
    const front = toml.parse(match[1]);
    // Conflicting case variants are ambiguous to Hugo's case-insensitive params.
    const keys = Object.keys(front).filter(key => key.toLowerCase() === 'draft');
    return keys.length === 1 && front[keys[0]] === true;
  } catch { return false; }
}

function excludesDrafts(env, git, ref) {
  if (env.BUILD_DRAFTS === 'true') return false;
  if (env.HUGO_CONFIG || env.HUGO_CONFIGDIR) return false;
  // Unknown environment overrides are not safe to interpret as false.
  if (env.HUGO_BUILDDRAFTS && env.HUGO_BUILDDRAFTS !== 'false') return false;
  // Inspect all tracked config variants, not just the default environment.
  const files = git('ls-tree', '-r', '--name-only', ref, '--', 'config',
    'hugo.toml', 'hugo.yaml', 'hugo.yml', 'hugo.json',
    'config.toml', 'config.yaml', 'config.yml', 'config.json').trim().split('\n').filter(Boolean);
  const hasDrafts = value => value && typeof value === 'object' && Object.entries(value).some(
    ([key, item]) => key.toLowerCase() === 'builddrafts' ? item !== false : hasDrafts(item));
  for (const file of files) {
    if (!file.endsWith('.toml')) return false;
    if (hasDrafts(toml.parse(git('show', `${ref}:${file}`)))) return false;
  }
  return files.includes('config/_default/hugo.toml');
}

export function nonSitePath(path) {
  return ['AGENTS.md', 'README.md', '.pages.yml'].includes(path)
    || path.startsWith('docs/')
    || path.startsWith('scripts/')
    || path.startsWith('.github/workflows/')
    || /^content-org\/.*\.org$/.test(path);
}

export function decide(env = process.env, cwd = process.cwd()) {
  if (env.NETLIFY_FORCE_BUILD === 'true') return [1, 'Forced build requested'];
  if (env.NETLIFY_ON_DEMAND === 'true') return [0, 'On-demand builds enabled; use a Netlify build hook to refresh'];
  const refs = [env.CACHED_COMMIT_REF, env.COMMIT_REF];
  if (refs.some(ref => !/^[a-f0-9]{40,64}$/i.test(ref || ''))) {
    return [1, 'Missing or invalid comparison commits'];
  }
  try {
    const git = (...args) => execFileSync('git', args, {
      cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'],
    });
    for (const ref of refs) git('cat-file', '-e', `${ref}^{commit}`);
    // Disable rename detection so BOTH the old and new paths are classified.
    const paths = git('diff', '--name-only', '-z', '--no-renames', ...refs, '--')
      .split('\0').filter(Boolean);
    // Empty comparisons may be explicit rebuilds for changed environment settings.
    if (!paths.length) return [1, 'No file changes; preserve explicit rebuilds'];
    const candidates = paths.filter(path => !nonSitePath(path));
    const eligible = path => (
      /^(?:content-pagescms|content\/post)\/[^/]+\.md$/.test(path)
      && !/\/(?:_?index)\.md$/.test(path)
    ) || /^content\/post\/[^/]+\/index\.md$/.test(path);
    const skipDrafts = candidates.some(eligible) && excludesDrafts(env, git, refs[1]);
    const draftOnly = path => {
      if (!skipDrafts || !eligible(path)) return false;
      return refs.every(ref => {
        // An absent tree entry is different from failure to read an existing blob.
        const entry = git('ls-tree', ref, '--', path).trim();
        if (!entry) return true;
        if (!entry.startsWith('100644 blob ') && !entry.startsWith('100755 blob ')) return false;
        return isDraftPost(git('show', `${ref}:${path}`));
      });
    };
    const relevant = candidates.filter(path => !draftOnly(path));
    if (relevant.length) return [1, `Site or unclassified changes: ${relevant.map(p => JSON.stringify(p)).join(', ')}`];
    return [0, `Only non-site files or excluded draft posts changed (${paths.length} files)`];
  } catch {
    return [1, 'Git comparison unavailable; building conservatively'];
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [code, reason] = decide();
  console.log(`[netlify-ignore] ${code === 0 ? 'SKIP' : 'BUILD'}: ${reason}`);
  process.exitCode = code;
}
