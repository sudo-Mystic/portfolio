(() => {
  const supportedThemes = ["dark-modern", "dark-plus", "oled", "dreamscape"];
  const root = document.documentElement;
  root.classList.add("editor-js");
  function restorePreferences() {
    try {
      const savedTheme = localStorage.getItem("mystic-theme");
      const theme = supportedThemes.includes(savedTheme) ? savedTheme : "dark-modern";
      const motion = localStorage.getItem("mystic-motion") === "reduce" ? "reduce" : "system";
      if (root.dataset.theme === theme && root.dataset.motion === motion) return;
      root.dataset.theme = theme;
      root.dataset.motion = motion;
      window.dispatchEvent(new Event("mystic:preferences"));
    } catch {
      // The defaults also work with storage disabled.
    }
  }
  restorePreferences();
  window.addEventListener("pageshow", event => {
    if (event.persisted) restorePreferences();
  });
  window.addEventListener("storage", event => {
    if (!event.key || ["mystic-theme", "mystic-motion"].includes(event.key)) restorePreferences();
  });
})();
