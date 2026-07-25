(() => {
  "use strict";

  const TOOLTIP_ATTRIBUTE = "data-footnote-tooltip";

  function footnoteText(definition) {
    const copy = definition.cloneNode(true);
    copy.querySelectorAll("a").forEach((link) => link.remove());
    return copy.textContent
      .replace(/\s+/g, " ")
      .replace(/\s*[·|]\s*$/, "")
      .trim();
  }

  function installFootnoteTooltips(root = document) {
    for (const reference of root.querySelectorAll("a.footnote-ref[href^='#fn']")) {
      if (reference.hasAttribute(TOOLTIP_ATTRIBUTE)) continue;

      const targetId = reference.hash.slice(1);
      const definition = document.getElementById(targetId);
      if (!definition) continue;

      const text = footnoteText(definition);
      if (!text) continue;

      reference.setAttribute(TOOLTIP_ATTRIBUTE, text);
      reference.setAttribute("aria-label", `각주: ${text}`);
    }
  }

  let pending = false;
  function scheduleSetup() {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => {
      pending = false;
      installFootnoteTooltips();
    });
  }

  new MutationObserver(scheduleSetup).observe(document.documentElement, {
    childList: true,
    subtree: true,
  });
  document.addEventListener("DOMContentLoaded", scheduleSetup);
  window.addEventListener("load", scheduleSetup);
})();
