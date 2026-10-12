// Netlify ignore convention: 0 skips, 1 builds. No npm dependencies required.
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

export function nonSitePath(path) {
  return ['AGENTS.md', 'README.md', '.pages.yml'].includes(path)
    || path.startsWith('docs/')
    || path.startsWith('scripts/tests/')
    || /^content-org\/.*\.org$/.test(path);
}

export function decide(env = process.env, cwd = process.cwd()) {
  if (env.NETLIFY_FORCE_BUILD === 'true') return [1, 'Forced build requested'];
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
    const relevant = paths.filter(path => !nonSitePath(path));
    if (relevant.length) return [1, `Site or unclassified changes: ${relevant.map(p => JSON.stringify(p)).join(', ')}`];
    return [0, `Only documentation, CMS configuration, Org source, or tests changed (${paths.length} files)`];
  } catch {
    return [1, 'Git comparison unavailable; building conservatively'];
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [code, reason] = decide();
  console.log(`[netlify-ignore] ${code === 0 ? 'SKIP' : 'BUILD'}: ${reason}`);
  process.exitCode = code;
}
