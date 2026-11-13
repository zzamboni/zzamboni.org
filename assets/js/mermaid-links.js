/* Keep author-supplied Mermaid links native and keyboard accessible.
   A box with one destination becomes one SVG link; multi-link labels stay separate. */
(() => {
  const svgNS = "http://www.w3.org/2000/svg";

  function enhance(diagram) {
    // Mermaid measures a temporary SVG inside a div before publishing the final SVG.
    // Never touch that working tree: changing it can corrupt label sizes and layout.
    diagram.querySelectorAll(":scope > svg g.node").forEach((node) => {
      const links = node.querySelectorAll("a[href]");
      if (links.length !== 1 || node.parentElement.classList.contains("mermaid-node-link")) return;

      const original = links[0];
      const boxLink = document.createElementNS(svgNS, "a");
      boxLink.classList.add("mermaid-node-link");
      boxLink.setAttribute("href", original.getAttribute("href"));
      boxLink.setAttribute("aria-label", original.textContent.trim());
      boxLink.setAttribute("tabindex", "0");
      for (const name of ["target", "rel", "title"]) {
        if (original.hasAttribute(name)) boxLink.setAttribute(name, original.getAttribute(name));
      }

      // Avoid nesting HTML and SVG links. Keep just the linked words underlined.
      const label = document.createElement("span");
      label.className = "mermaid-link-label";
      label.append(...original.childNodes);
      original.replaceWith(label);
      node.before(boxLink);
      boxLink.append(node);
    });
  }

  function init() {
    document.querySelectorAll("pre.mermaid").forEach((diagram) => {
      enhance(diagram);
      // Blowfish regenerates the SVG when switching light/dark appearance.
      const observer = new MutationObserver(() => enhance(diagram));
      observer.observe(diagram, { childList: true, subtree: true });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
