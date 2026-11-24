(() => {
  const themeOptions = document.querySelectorAll(".theme-option input");
  for (const option of themeOptions) {
    option.disabled = false;
    option.checked = option.value === document.documentElement.dataset.theme;
    option.addEventListener("change", () => {
      document.documentElement.dataset.theme = option.value;
      try {
        localStorage.setItem("mystic-theme", option.value);
      } catch {
        // The selected theme still applies on the current page.
      }
    });
  }

  const dialog = document.querySelector("#jump-dialog");
  const trigger = document.querySelector(".jump-trigger");
  if (!dialog || typeof dialog.showModal !== "function") return;

  const search = dialog.querySelector("input");
  const rows = Array.from(dialog.querySelectorAll(".jump-results li"), (row) => ({
    row,
    link: row.querySelector("a"),
    text: `${row.textContent} ${row.dataset.search}`.toLowerCase(),
  }));
  const empty = dialog.querySelector(".jump-empty");
  const status = dialog.querySelector("#jump-status");
  const keys = trigger.querySelector("kbd");
  const isApple = /Mac|iPhone|iPad|iPod/.test(navigator.platform);
  keys.textContent = isApple ? "⌘ K" : "Ctrl K";
  trigger.setAttribute("aria-keyshortcuts", isApple ? "Meta+K" : "Control+K");
  trigger.setAttribute("aria-label", "Jump to a page");
  trigger.hidden = false;

  const visibleRows = () => rows.filter(({ row }) => !row.hidden);

  function filter() {
    const words = search.value.toLowerCase().trim().split(/\s+/);
    for (const { row, text } of rows) {
      row.hidden = !words.every((word) => text.includes(word));
    }
    const count = visibleRows().length;
    empty.hidden = count > 0;
    status.textContent = count === 1 ? "1 matching page" : `${count} matching pages`;
  }

  function open() {
    if (dialog.open) return;
    search.value = "";
    filter();
    dialog.showModal();
  }

  trigger.addEventListener("click", open);
  search.addEventListener("input", filter);
  search.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && search.value.trim()) {
      visibleRows()[0]?.link.click();
    }
  });
  dialog.addEventListener("keydown", (event) => {
    if (!["ArrowDown", "ArrowUp"].includes(event.key)) return;
    const links = visibleRows().map(({ link }) => link);
    if (!links.length) return;
    event.preventDefault();
    const current = links.indexOf(document.activeElement);
    const next = event.key === "ArrowDown" ? current + 1 : (current < 1 ? links.length - 1 : current - 1);
    links[next % links.length].focus();
  });
  dialog.addEventListener("click", (event) => {
    if (event.target.closest("a")) dialog.close();
  });
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && !event.altKey && !event.shiftKey && event.key.toLowerCase() === "k") {
      event.preventDefault();
      open();
    }
  });
})();
