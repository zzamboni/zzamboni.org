const OWNER = "zzamboni";
const REPO = "zzamboni.org";
const BRANCH = "main";
const CONTENT_DIR = "content-pagescms";

function tomlString(value) {
  // JSON strings are valid TOML basic strings.
  return JSON.stringify(String(value));
}

function slugify(value) {
  return value
    .normalize("NFKD")
    .replace(/\p{Diacritic}/gu, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "link";
}

function decodeHtml(value) {
  return value
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/&apos;/gi, "'")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) =>
      String.fromCodePoint(parseInt(n, 16))
    );
}

function attr(tag, name) {
  const match = tag.match(
    new RegExp(`${name}\\s*=\\s*["']([^"']*)["']`, "i")
  );
  return match?.[1];
}

function validateUrl(value) {
  const url = new URL(value);

  if (!["http:", "https:"].includes(url.protocol)) {
    throw new Error("Only HTTP and HTTPS URLs are allowed");
  }

  // Avoid some obvious server-side fetch nastiness.
  const host = url.hostname.toLowerCase();

  if (
    host === "localhost" ||
    host.endsWith(".local") ||
    host === "127.0.0.1" ||
    host === "::1"
  ) {
    throw new Error("Local URLs are not allowed");
  }

  return url;
}

async function fetchPageTitle(url) {
  try {
    const response = await fetch(url, {
      headers: {
        "User-Agent": "zzamboni-linkblog/1.0",
        Accept: "text/html",
      },
      signal: AbortSignal.timeout(5000),
      redirect: "follow",
    });

    if (!response.ok) {
      return null;
    }

    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("text/html")) {
      return null;
    }

    // Plenty for <head>, without enthusiastically ingesting the internet.
    const html = (await response.text()).slice(0, 300_000);

    const metaTags = html.match(/<meta\b[^>]*>/gi) || [];

    for (const tag of metaTags) {
      const property = (
        attr(tag, "property") ||
        attr(tag, "name") ||
        ""
      ).toLowerCase();

      if (property === "og:title" || property === "twitter:title") {
        const content = attr(tag, "content");
        if (content) {
          return decodeHtml(content).trim();
        }
      }
    }

    const title = html.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i);
    if (title) {
      return decodeHtml(title[1].replace(/\s+/g, " ")).trim();
    }
  } catch (error) {
    console.log("Could not fetch page title:", error.message);
  }

  return null;
}

async function createGitHubFile(path, content, title) {
  const token = process.env.LINKBLOG_GITHUB_TOKEN;

  const response = await fetch(
    `https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}`,
    {
      method: "PUT",
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${token}`,
        "X-GitHub-Api-Version": "2026-03-10",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: `Linkblog: ${title}`,
        content: Buffer.from(content, "utf8").toString("base64"),
        branch: BRANCH,
      }),
    }
  );

  return response;
}

export default async function handler(request) {

  if (request.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const expected = `Bearer ${process.env.LINKBLOG_SECRET}`;

  if (request.headers.get("authorization") !== expected) {
    return new Response("Unauthorized", { status: 401 });
  }

  try {
    const input = await request.json();

    if (!input.url) {
      throw new Error("Missing URL");
    }

    const url = validateUrl(input.url);
    const commentary = String(input.commentary || "").trim();

    /*
     * Preserve the date supplied by the phone, including its timezone.
     * Fall back to UTC if none was supplied.
     */
    const date =
      typeof input.date === "string" && !Number.isNaN(Date.parse(input.date))
        ? input.date
        : new Date().toISOString();

    const title =
      String(input.title || "").trim() ||
      (await fetchPageTitle(url.href)) ||
      url.hostname;

    const tags = [
      "zznippets",
      ...(Array.isArray(input.tags) ? input.tags : []),
    ]
      .map(String)
      .map((tag) => tag.trim())
      .filter(Boolean)
      .filter((tag, index, all) => all.indexOf(tag) === index);

    /*
     * These are link posts, so make the semantic distinction explicit
     * instead of relying only on CSS to hide the metadata.
     */
    const frontmatter = [
      "+++",
      `title = ${tomlString(title)}`,
      `externalUrl = ${tomlString(url.href)}`,
      `summary = ""`,
      `date = ${tomlString(date)}`,
      `tags = ${JSON.stringify(tags)}`,
      `draft = true`,
      `toc = false`,
      `showReadingTime = false`,
      `showWordCount = false`,
      "+++",
      "",
    ].join("\n");

    const content =
      frontmatter +
      `\n[${url.href}](${url.href})\n\n` +
      (commentary ? `${commentary}\n` : "");

    const day = date.slice(0, 10);
    const slug = slugify(title);
    let filename = `${day}-${slug}.md`;
    let path = `${CONTENT_DIR}/${filename}`;

    let githubResponse = await createGitHubFile(path, content, title);

    /*
     * Same title twice on the same day? Rare, but computers enjoy
     * discovering precisely the edge case you didn't handle.
     */
    if (githubResponse.status === 422) {
      const suffix = new Date()
        .toISOString()
        .slice(11, 19)
        .replaceAll(":", "");

      filename = `${day}-${slug}-${suffix}.md`;
      path = `${CONTENT_DIR}/${filename}`;

      githubResponse = await createGitHubFile(path, content, title);
    }

    if (!githubResponse.ok) {
      const text = await githubResponse.text();
      console.error(text);
      throw new Error(`GitHub returned ${githubResponse.status}`);
    }

    const editUrl =
          `https://app.pagescms.org/` +
          `${OWNER}/${REPO}/${BRANCH}/collection/posts/edit/` +
          encodeURIComponent(path);
      
    return Response.json({
      ok: true,
      title,
      path,
      editUrl,
    });
  } catch (error) {
    console.error(error);

    return Response.json(
      {
        ok: false,
        error: error.message,
      },
      { status: 400 }
    );
  }
}

export const config = {
  path: "/api/linkblog",
};
