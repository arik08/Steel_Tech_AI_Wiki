(() => {
  "use strict";

  if (!window.mermaid) return;

  window.mermaid.initialize({
    startOnLoad: true,
    theme: "base",
    themeVariables: {
      background: "transparent",
      primaryColor: "#edf2fb",
      primaryTextColor: "#20242c",
      primaryBorderColor: "#3f66c9",
      secondaryColor: "#f5f6f7",
      secondaryTextColor: "#20242c",
      tertiaryColor: "#ffffff",
      tertiaryTextColor: "#20242c",
      lineColor: "#6c737e",
      textColor: "#20242c",
      noteBkgColor: "#edf2fb",
      noteTextColor: "#20242c",
      actorBkg: "#ffffff",
      actorBorder: "#d4d8de",
      actorTextColor: "#20242c",
      clusterBkg: "#f5f6f7",
      clusterBorder: "#d4d8de",
    },
  });
})();
