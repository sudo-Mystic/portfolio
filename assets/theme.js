(() => {
  const supportedThemes = ["dark-modern", "dark-plus", "oled", "dreamscape"];
  try {
    const savedTheme = localStorage.getItem("mystic-theme");
    if (supportedThemes.includes(savedTheme)) {
      document.documentElement.dataset.theme = savedTheme;
    }
  } catch {
    // The default theme works when the browser blocks local storage.
  }
})();
