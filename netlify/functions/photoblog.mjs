import { randomUUID } from "node:crypto";

const OWNER = "zzamboni";
const REPO = "zzamboni.org";
// Netlify exposes BRANCH during builds, but not to deployed Functions.
// Require an explicit runtime target so staging can never silently write to main.
const BRANCH = process.env.PHOTOBLOG_BRANCH;
const API = `https://api.github.com/repos/${OWNER}/${REPO}`;
const MAX_PHOTOS = 20;
const MAX_IMAGE_BYTES = 2_500_000;
const MAX_TOTAL_BYTES = 3_000_000;

function tomlString(value) {
  return JSON.stringify(String(value));
}

function slugify(value) {
  return value.normalize("NFKD").replace(/\p{Diacritic}/gu, "")
    .toLowerCase().replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "").slice(0, 70) || "photos";
}

function zurichDate(value) {
  const date = value ? new Date(value) : new Date();
  if (Number.isNaN(date.getTime())) throw new Error("Invalid date");
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Europe/Zurich", year: "numeric", month: "2-digit",
    day: "2-digit", hour: "2-digit", minute: "2-digit",
    second: "2-digit", fractionalSecondDigits: 3, hourCycle: "h23",
  }).formatToParts(date);
  const p = Object.fromEntries(parts.map(({ type, value }) => [type, value]));
  return `${p.year}-${p.month}-${p.day}T${p.hour}:${p.minute}:${p.second}.${p.fractionalSecond}`;
}

function photoBytes(value) {
  if (typeof value !== "string") throw new Error("Each photo must be a base64 string");
  const base64 = value.replace(/\s/g, "");
  if (!base64 || !/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(base64)) {
    throw new Error("Invalid base64 photo");
  }
  const bytes = Buffer.from(base64, "base64");
  //if (bytes.length > MAX_IMAGE_BYTES) throw new Error("Photo exceeds 2.5 MB; resize it in Shortcuts");
  if (bytes.subarray(0, 3).equals(Buffer.from([0xff, 0xd8, 0xff]))) return { bytes, extension: "jpg" };
  if (bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) return { bytes, extension: "png" };
  if (bytes.toString("ascii", 0, 4) === "RIFF" && bytes.toString("ascii", 8, 12) === "WEBP") return { bytes, extension: "webp" };
  throw new Error("Convert photos to JPEG, PNG or WebP before uploading");
}

async function github(path, { method = "GET", body } = {}) {
  const response = await fetch(`${API}${path}`, {
    method,
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${process.env.PHOTOBLOG_GITHUB_TOKEN || process.env.LINKBLOG_GITHUB_TOKEN}`,
      "X-GitHub-Api-Version": "2026-03-10",
      "Content-Type": "application/json",
    },
    ...(body && { body: JSON.stringify(body) }),
  });
  if (!response.ok) throw new Error(`GitHub ${method} ${path} failed (${response.status})`);
  return response.json();
}

async function createPost(files, title) {
  const blobs = await Promise.all(files.map(async ({ path, bytes }) => {
    const blob = await github("/git/blobs", {
      method: "POST", body: { content: bytes.toString("base64"), encoding: "base64" },
    });
    return { path, mode: "100644", type: "blob", sha: blob.sha };
  }));

  // Retry a concurrent branch update without producing a partially written post.
  for (let attempt = 0; attempt < 3; attempt++) {
    const ref = await github(`/git/ref/heads/${BRANCH}`);
    const parent = await github(`/git/commits/${ref.object.sha}`);
    const tree = await github("/git/trees", {
      method: "POST", body: { base_tree: parent.tree.sha, tree: blobs },
    });
    const commit = await github("/git/commits", {
      method: "POST", body: {
        message: `auto: photoblog: ${title}`,
        tree: tree.sha, parents: [ref.object.sha],
      },
    });
    const update = await fetch(`${API}/git/refs/heads/${BRANCH}`, {
      method: "PATCH",
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${process.env.PHOTOBLOG_GITHUB_TOKEN || process.env.LINKBLOG_GITHUB_TOKEN}`,
        "X-GitHub-Api-Version": "2026-03-10",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sha: commit.sha, force: false }),
    });
    if (update.ok) return;
    if (![409, 422].includes(update.status)) throw new Error(`GitHub branch update failed (${update.status})`);
  }
  throw new Error("Branch changed during upload; please try again");
}

export default async function handler(request) {
  if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
  const secret = process.env.PHOTOBLOG_SECRET || process.env.LINKBLOG_SECRET;
  console.info("Photoblog request headers:", {
    contentType: request.headers.get("content-type"),
    contentLength: request.headers.get("content-length"),
    authorizationPresent: request.headers.has("authorization"),
    authorizationMatches: Boolean(secret) && request.headers.get("authorization") === `Bearer ${secret}`,
  });
  if (!secret || request.headers.get("authorization") !== `Bearer ${secret}`) {
    return new Response("Unauthorized", { status: 401 });
  }
  if (!process.env.PHOTOBLOG_GITHUB_TOKEN && !process.env.LINKBLOG_GITHUB_TOKEN) {
    return Response.json({ ok: false, error: "Missing GitHub token" }, { status: 500 });
  }
  if (!BRANCH || !["main", "staging"].includes(BRANCH)) {
    return Response.json({
      ok: false,
      error: "Set PHOTOBLOG_BRANCH to main or staging in the Netlify site's Function environment",
    }, { status: 500 });
  }

  try {
    const input = await request.json();
    console.info("Photoblog request body:", {
      type: Array.isArray(input) ? "array" : typeof input,
      keys: input && typeof input === "object" ? Object.keys(input) : [],
      title: typeof input?.title === "string" ? input.title.slice(0, 150) : typeof input?.title,
      commentary: typeof input?.commentary === "string" ? input.commentary.slice(0, 150) : typeof input?.commentary,
      date: typeof input?.date === "string" ? input.date.slice(0, 80) : typeof input?.date,
      draft: input?.draft === true || input?.draft === false ? input.draft : typeof input?.draft,
      tags: Array.isArray(input?.tags) ? input.tags.slice(0, 10).map(tag => String(tag).slice(0, 80)) : typeof input?.tags,
      photos: Array.isArray(input?.photos)
        ? input.photos.map(photo => typeof photo === "string"
          ? { type: "string", base64Length: photo.length }
          : { type: typeof photo, keys: photo && typeof photo === "object" ? Object.keys(photo) : [] })
        : { type: typeof input?.photos },
    });
    if (!Array.isArray(input.photos) || !input.photos.length || input.photos.length > MAX_PHOTOS) {
      throw new Error(`Provide 1–${MAX_PHOTOS} photos`);
    }
    const photos = input.photos.map(photoBytes);
    // if (photos.reduce((sum, photo) => sum + photo.bytes.length, 0) > MAX_TOTAL_BYTES) {
    //   throw new Error("Photos exceed 3 MB total; resize or send fewer photos");
    // }

    const date = zurichDate(input.date);
    const title = String(input.title || "").trim().replace(/\s+/g, " ").slice(0, 150) || `Photos from ${date.slice(0, 10)}`;
    const commentary = String(input.commentary || "").trim();
    const tags = ["photos", ...(Array.isArray(input.tags) ? input.tags : [])]
      .map(String).map(tag => tag.trim()).filter(Boolean)
      .filter((tag, index, all) => all.indexOf(tag) === index);
    const bundle = `content-photos/${date.slice(0, 10)}-${slugify(title)}-${randomUUID().slice(0, 8)}`;
    const mediaFolder = `static/img/photos/${bundle.split("/").pop()}`;
    const images = photos.map((photo, i) => ({
      path: `${mediaFolder}/${i === 0 ? "feature" : String(i + 1).padStart(2, "0")}.${photo.extension}`,
      bytes: photo.bytes,
    }));
    const photoPaths = images.map(image => `/${image.path.slice("static/".length)}`);
    const frontmatter = [
      "+++", `title = ${tomlString(title)}`, `date = ${tomlString(date)}`,
      `slug = ${tomlString(bundle.split("/").pop())}`,
      `summary = ${tomlString(commentary.replace(/\s+/g, " ").slice(0, 280) || title)}`,
      `tags = ${JSON.stringify(tags)}`, `draft = ${input.draft === false ? "false" : "true"}`, "toc = false",
      `photos = ${JSON.stringify(photoPaths)}`,
      "showHero = false", "showReadingTime = false", "showWordCount = false", "+++", "",
    ].join("\n");
    const markdown = frontmatter + (commentary ? `${commentary}\n` : "");
    const files = [
      { path: `${bundle}/index.md`, bytes: Buffer.from(markdown, "utf8") },
      ...images.map((image, i) => ({ path: image.path, bytes: photos[i].bytes })),
    ];
    await createPost(files, title);

    return Response.json({
        ok: true,
        title: title,
        path: `${bundle}/index.md`,
        branch: BRANCH,
        editUrl: `https://app.pagescms.org/${OWNER}/${REPO}/${BRANCH}/collection/photos/edit/${encodeURIComponent(`${bundle}/index.md`)}`,
        githubUrl: `https://github.com/${OWNER}/${REPO}/edit/${BRANCH}/${bundle}/index.md`,
    });
  } catch (error) {
    console.error("Photoblog upload failed:", error);
    return Response.json({ ok: false, error: error.message }, { status: 400 });
  }
}

export const config = { path: "/api/photoblog" };
