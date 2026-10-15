# zzamboni.org: Recommended Next Improvements

**Date:** October 15, 2026  
**Purpose:** Roadmap and working guidance for future improvements to zzamboni.org, based on the October 14 Codex context update and subsequent ChatGPT recommendations.

**Status:** Planning document. Nothing here authorizes implementation, commits, pushes, merges, deployments, or paid API usage without an explicit request.

## 1. Current State

The blog's infrastructure is now relatively mature. Recent improvements include:

- Multiple authoring workflows: Org-mode/ox-hugo, Pages CMS, and iPhone Shortcuts backed by Netlify functions.
- Production, draft, and staging environments.
- Custom homepage with recent article summaries and a photo sidebar.
- Automated summaries, featured images, and favicon support.
- Customized Blowfish theme with tracked overrides.
- Conservative Netlify build filtering, including draft-only change detection.
- On-demand draft builds.
- Hugo resource caching, reducing typical Netlify build times from approximately 45 to 30 seconds.
- Maintained developer documentation and automated tests.

At the October 14 inspected commits, `main` and `staging` contained matching application code, configuration, workflows, and tooling. Their remaining differences were primarily content and images. Verify current branch state before making changes.

**Overall direction:** Shift investment away from infrastructure expansion and toward publishing reliability, content discovery, reader experience, and maintainability.

## 2. Development Principles

### Local-first workflow

Minimize Netlify build usage:

1. Inspect the current repository state, relevant files, and existing conventions.
2. Use `staging` for experimental site changes unless instructed otherwise.
3. Develop and test locally using the pinned Hugo and existing tooling.
4. Run relevant automated tests and local Hugo builds.
5. Validate desktop and mobile layouts locally when possible.
6. Batch related changes into coherent commits.
7. Push only when explicitly requested, ideally after local validation is complete.
8. Reserve Netlify deployments for integration and environment-specific checks that cannot be performed locally.

Use `mise run serve` or `mise run serve-drafts` for local development.

Preserve the existing branch and authoring conventions:

- GitHub is the source of truth; GitLab is a mirror.
- Long-form posts are authored in `content-org/zzamboni.org` and exported through ox-hugo.
- Pages CMS content belongs in `content-pagescms/`.
- Photo posts belong in `content-photos/`.
- Automated commit subjects begin with `auto:`.
- Keep content changes separate from tooling/theme changes where practical.
- Keep requested drafts unpublished.
- Use Elvish syntax when providing shell commands.
- Inspect `AGENTS.md`, existing documentation, and the current checkout before modifying anything.

## 3. Priority 1: Improve Publishing Reliability

**Goal:** Make it as easy as possible to create, preview, and publish short posts from a phone or laptop.

### Potential improvements

- Review the linkblog and photoblog Netlify functions for duplicated validation, error handling, and response structures.
- Improve error messages returned to iOS Shortcuts, especially for malformed payloads.
- Consider request identifiers to correlate client errors with function logs.
- Review the process of saving a draft, triggering the on-demand draft build, and opening its preview.
- Ensure both `summary` and `commentary` fields behave consistently with the existing fallback rules.
- Add local integration tests covering representative linkblog and photoblog requests without publishing actual content.

### Important constraints

- Do not replace the existing functions or combine them merely for architectural neatness.
- Preserve their current API contracts and compatibility with existing Shortcuts.
- Prefer small, well-tested changes over major refactoring.
- Avoid triggering live Netlify functions during routine tests.

**Suggested first step:** Audit the current implementations and tests, identify concrete reliability gaps, and propose targeted improvements.

## 4. Priority 2: Improve Content Discovery

**Goal:** Make older technical articles easier to find and encourage readers to explore related material.

### A. Related posts

Investigate adding a small related-posts section to individual articles.

Possible approach:

- Prefer Hugo's built-in related-content functionality.
- Use existing tags or other available metadata.
- Display two or three relevant posts below the article.
- Reuse Blowfish's existing layouts and styling where practical.
- Avoid showing the current article or duplicate recommendations.
- Handle posts with no meaningful related content gracefully.

Check whether Blowfish already supports this functionality before introducing a custom implementation.

### B. Curated topic pages

Explore lightweight topic landing pages for recurring subjects such as:

- Emacs and Org-mode
- Hammerspoon
- Cybersecurity and cloud security
- Automation and scripting
- Blogging infrastructure

Each topic page could contain a brief introduction, recommended starting points, and automatically populated recent articles.

Prefer existing Hugo taxonomies and content organization rather than introducing another content management system.

### C. Blog archive

Consider a compact chronological archive with articles grouped by year.

The goal is easier browsing without requiring visitors to paginate through large article cards.

Before implementing, inspect existing Blowfish archive, taxonomy, and listing capabilities.

**Suggested first step:** Audit current discovery features and prepare a small proposal comparing built-in Blowfish/Hugo capabilities with minimal customizations.

## 5. Priority 3: Polish the Photo Experience

**Goal:** Improve the reliability and usability of the existing photo features rather than adding more functionality.

Areas to investigate:

- Gallery and lightbox behavior on desktop and mobile.
- Touch navigation, swiping, and closing behavior.
- Keyboard accessibility.
- Image loading and layout stability.
- Alt text and descriptive image metadata.
- Thumbnail consistency across the homepage sidebar, Photos listing, and individual photo posts.
- Responsive image sizing and optimization.

The earlier project history mentions possible gallery and mobile issues, but these have not been independently confirmed as outstanding bugs.

**Suggested first step:** Reproduce and document actual issues before changing gallery code.

Avoid replacing the current lightbox implementation without clear evidence of a problem.

## 6. Priority 4: Accessibility and Reader-Facing Performance

**Goal:** Improve the experience for readers rather than focusing exclusively on Netlify build duration.

### Areas to audit

- Mobile layout and responsiveness.
- Keyboard navigation and visible focus indicators.
- Image alt text.
- Color contrast.
- Heading hierarchy.
- Responsive image sizes.
- Lazy loading.
- Cumulative layout shift.
- Overall page weight.
- Core Web Vitals.
- Custom CSS/JavaScript regressions.

### Testing approach

Use local tools and browser developer tools wherever possible.

Avoid re-enabling Lighthouse on every Netlify build; it was deliberately disabled to conserve build minutes.

Prioritize demonstrable problems over cosmetic benchmark improvements.

**Suggested first step:** Establish a local baseline for the homepage, an article, and a photo post. Identify the highest-impact issues before implementing fixes.

## 7. Priority 5: Infrastructure Cleanup

**Goal:** Improve maintainability without introducing additional complexity.

### A. Dependency reproducibility

Investigate adding a tracked `package-lock.json` and standardizing on `npm ci`.

The October 14 update notes that `AGENTS.md` recommends `npm ci`, but no lockfile was tracked at that time.

Check the current dependency setup first.

### B. Netlify plugin configuration

Verify whether the obsolete UI-installed instance of `netlify-plugin-hugo-cache-resources` has been removed.

The tracked plugin configuration is already present in `netlify.toml`.

Avoid duplicated configuration.

### C. Build-ignore validation

Continue checking draft-only build suppression under normal development activity, including:

- Creating drafts.
- Modifying drafts.
- Deleting drafts.
- Publishing previously drafted content.
- Unpublishing existing content.

The local test suite already covers these cases. Additional live deployments should not be triggered solely for validation unless necessary.

### D. Link checking

Consider lightweight automated checking for:

- Broken internal links.
- Missing local images.
- Invalid internal references.

Prefer checks that can run locally or in GitHub Actions without unnecessary Netlify deployments.

### E. Theme maintenance

Review the current Blowfish version and available upgrade tooling.

Preserve the documented customizations in `scripts/theme-overrides.toml`.

Upgrade only when there is a clear benefit, and run relevant compatibility checks locally.

### F. Additional build-ignore optimizations

Possible future work includes more precise treatment of photo bundles and draft-specific assets.

**Low priority:** The existing conservative behavior favors correctness over avoiding every possible build. Do not expand classification logic without evidence that additional savings justify the complexity.

## 8. Longer-Term Idea: Technical Knowledge Base

Explore presenting the existing blog as a lightweight technical knowledge base in addition to a chronological publication.

The intention is not to migrate posts or introduce a new platform.

Potential capabilities:

- Curated technical topic pages.
- Recommended starting points for newcomers.
- Related-post navigation.
- Automatically populated topic-specific article lists.
- Clearer navigation among historical tutorials and ongoing projects.

Favor Hugo's existing taxonomy, content, and template capabilities.

This is an exploratory concept, not an approved implementation.

## 9. Suggested Implementation Order

| Order | Work item | Initial scope |
|---|---|---|
| 1 | Publishing workflow audit | Review functions, error handling, draft previews, and test coverage |
| 2 | Related-post navigation | Assess built-in support; implement minimal changes if worthwhile |
| 3 | Photo/mobile/accessibility audit | Identify reproducible defects and prioritize fixes |
| 4 | Dependency and Netlify configuration cleanup | Lockfile, plugin configuration, documentation consistency |
| 5 | Curated topic pages | Prototype one topic locally |
| 6 | Archive improvements | Evaluate compact chronological browsing |
| 7 | Additional build optimization | Only if evidence supports it |

These are approximate priorities, not a requirement to complete every item or follow the order rigidly.

## 10. Things to Avoid

Do not introduce complexity without a concrete benefit.

In particular, avoid:

- Migrating away from Hugo.
- Replacing Pages CMS without a demonstrated need.
- Adding a database or server-side application framework.
- Introducing a new JavaScript framework.
- Rebuilding features already available in Blowfish.
- Replacing the current gallery/lightbox merely for novelty.
- Adding an elaborate AI publishing assistant.
- Triggering frequent staging builds for changes that can be verified locally.
- Optimizing build-ignore logic beyond what can be safely validated.

The existing static-file architecture and multiple authoring paths are strengths worth preserving.

## 11. Instructions for Codex

Treat this document as a roadmap and prioritization guide, not a request to implement all improvements.

For each selected task:

1. Inspect the relevant repository files, current branch, tests, and documentation.
2. Determine whether the functionality already exists in Hugo, Blowfish, or the current custom code.
3. Distinguish confirmed problems from hypothetical improvements.
4. Recommend the smallest practical change.
5. Implement only the specifically requested scope.
6. Run appropriate local checks.
7. Explain what changed and what was verified.
8. Identify any remaining verification that genuinely requires a live deployment.
9. Report the branch and commit when changes are committed.

**Guiding principle:** The next phase of zzamboni.org development should make publishing easier, content easier to discover, and the site more pleasant to use, while keeping the underlying system simple, reliable, and inexpensive to operate.

