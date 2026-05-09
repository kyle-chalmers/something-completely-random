/**
 * REVERIE · inter-dream navigation
 *
 * Injects a small "previous · hall · next · random" nav strip at the bottom
 * of each dream so visitors can walk the gallery sequentially without going
 * back to the hall. Reads the dream order from a hardcoded list (must match
 * the manifest order).
 */
(function () {
  "use strict";

  const ORDER = [
    { id: "01-cartographer", title: "the cartographer of lost maps" },
    { id: "02-surgeon",      title: "the surgeon of wasted hours" },
    { id: "03-botanist",     title: "the botanist of glass gardens" },
    { id: "04-architect",    title: "the architect of forgotten buildings" },
    { id: "05-witch",        title: "the witch of mirrors and recursion" },
    { id: "06-astronomer",   title: "the astronomer of silent stars" },
    { id: "07-engineer",     title: "the engineer of impossible machines" },
    { id: "08-weaver",       title: "the weaver of half-remembered songs" },
  ];

  // Find the current dream from the URL path
  const m = location.pathname.match(/dreams\/([^/]+)/);
  if (!m) return;
  const here = ORDER.findIndex(d => d.id === m[1]);
  if (here < 0) return;

  const prev = ORDER[(here - 1 + ORDER.length) % ORDER.length];
  const next = ORDER[(here + 1) % ORDER.length];

  // Build nav element
  const nav = document.createElement("nav");
  nav.className = "dream-nav";
  nav.setAttribute("aria-label", "between dreams");
  nav.innerHTML = `
    <a class="dream-nav-link dream-nav-prev" href="../${prev.id}/" title="${prev.title}">
      <span class="dream-nav-arrow">‹</span>
      <span class="dream-nav-label">${String(here).padStart(2, "0")} · ${prev.title}</span>
    </a>
    <a class="dream-nav-hall" href="../../" title="back to the hall">·</a>
    <a class="dream-nav-link dream-nav-next" href="../${next.id}/" title="${next.title}">
      <span class="dream-nav-label">${String(here + 2).padStart(2, "0")} · ${next.title}</span>
      <span class="dream-nav-arrow">›</span>
    </a>
  `;
  document.body.appendChild(nav);

  // Keyboard nav: arrow keys move between dreams
  document.addEventListener("keydown", (e) => {
    // Don't hijack typing in inputs
    const t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    if (e.metaKey || e.ctrlKey || e.altKey) return;

    if (e.key === "ArrowLeft" || e.key === "[") {
      location.href = `../${prev.id}/`;
    } else if (e.key === "ArrowRight" || e.key === "]") {
      location.href = `../${next.id}/`;
    } else if (e.key === "Escape" || e.key === "h") {
      location.href = "../../";
    }
  });

  // Inject CSS for the nav (so we don't need to edit each dream's <style>).
  // Uses shared CSS variables when available.
  const css = `
    .dream-nav {
      position: fixed;
      bottom: 0; left: 0; right: 0;
      z-index: 9998;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.6rem 1rem;
      font-family: var(--type-mono, "JetBrains Mono", monospace);
      font-size: 0.72rem;
      letter-spacing: 0.18em;
      background: linear-gradient(180deg, transparent, rgba(0,0,0,0.55) 70%);
      pointer-events: none;
      opacity: 0.5;
      transition: opacity 400ms cubic-bezier(0.22,1,0.36,1);
    }
    .dream-nav:hover { opacity: 1; }
    .dream-nav-link, .dream-nav-hall {
      pointer-events: auto;
      color: rgba(232,226,212,0.55);
      text-decoration: none;
      border: none;
      padding: 0.4rem 0.6rem;
      transition: color 200ms;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
    }
    .dream-nav-link:hover, .dream-nav-hall:hover { color: rgba(232,226,212,1); }
    .dream-nav-arrow { font-size: 1.2rem; line-height: 1; opacity: 0.7; }
    .dream-nav-label { text-transform: lowercase; }
    .dream-nav-hall { font-size: 1.2rem; opacity: 0.4; }
    .dream-nav-hall:hover { opacity: 1; transform: scale(1.4); }
    @media (max-width: 720px) {
      .dream-nav-label { display: none; }
      .dream-nav { font-size: 1rem; }
      .dream-nav-link { padding: 0.6rem 0.8rem; }
    }
    @media (prefers-reduced-motion: reduce) {
      .dream-nav { transition: none; opacity: 0.85; }
    }
  `;
  const style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);
})();
