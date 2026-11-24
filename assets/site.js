(() => {
  const root = document.documentElement;
  const workspace = document.querySelector(".workspace");
  const explorer = document.querySelector("#explorer");
  const currentFile = document.body.dataset.currentFile;
  const files = new Map(Array.from(explorer.querySelectorAll("[data-file-id]"),
    (link) => [link.dataset.fileId, link]));

  function readSession(key) {
    try {
      return sessionStorage.getItem(key);
    } catch {
      return null;
    }
  }

  function writeSession(key, value) {
    try {
      sessionStorage.setItem(key, value);
    } catch {
      // The current page works without session storage.
    }
  }

  for (const option of document.querySelectorAll(".theme-option input")) {
    option.disabled = false;
    option.checked = option.value === root.dataset.theme;
    option.addEventListener("change", () => {
      root.dataset.theme = option.value;
      try {
        localStorage.setItem("mystic-theme", option.value);
      } catch {
        // The current page still uses the selected theme.
      }
    });
  }

  const mobile = matchMedia("(max-width: 46rem)");
  const sidebarButton = document.querySelector(".activitybar [data-explorer]");
  const mobileButton = document.querySelector(".mobile-explorer");
  const resizer = document.querySelector(".explorer-resizer");
  const explorerPreference = "mystic-explorer";
  const explorerWidth = "mystic-explorer-width";

  function setWidth(width) {
    const min = Number(resizer.getAttribute("aria-valuemin"));
    const max = Number(resizer.getAttribute("aria-valuemax"));
    const clamped = Math.round(Math.min(max, Math.max(min, width)));
    workspace.style.setProperty("--side", `${clamped}px`);
    resizer.setAttribute("aria-valuenow", String(clamped));
  }

  function updateWidthValue() {
    if (explorer.offsetWidth) resizer.setAttribute("aria-valuenow", String(explorer.offsetWidth));
  }

  function setSidebar(open) {
    workspace.dataset.explorer = open ? "open" : "closed";
    sidebarButton.setAttribute("aria-expanded", String(open));
    if (!mobile.matches) updateWidthValue();
  }
  function setMobileExplorer(open) {
    workspace.dataset.mobileExplorer = open ? "open" : "closed";
    mobileButton.setAttribute("aria-expanded", String(open));
  }
  const savedWidth = Number(readSession(explorerWidth));
  if (savedWidth > 0) setWidth(savedWidth);
  setSidebar(readSession(explorerPreference) !== "closed");
  sidebarButton.hidden = false;
  mobileButton.hidden = false;
  resizer.hidden = false;
  sidebarButton.addEventListener("click", () => {
    const open = workspace.dataset.explorer === "closed";
    setSidebar(open);
    writeSession(explorerPreference, workspace.dataset.explorer);
  });
  mobileButton.addEventListener("click", () => {
    const open = workspace.dataset.mobileExplorer !== "open";
    setMobileExplorer(open);
    if (open) explorer.querySelector(".workspace-folder > summary").focus();
  });
  explorer.addEventListener("keydown", (event) => {
    if (mobile.matches && event.key === "Escape") {
      setMobileExplorer(false);
      mobileButton.focus();
    }
  });
  mobile.addEventListener("change", () => setMobileExplorer(false));
  window.addEventListener("resize", () => {
    if (!mobile.matches) updateWidthValue();
  });

  let dragStart;
  resizer.addEventListener("pointerdown", (event) => {
    if (event.button !== 0) return;
    dragStart = {x: event.clientX, width: explorer.offsetWidth};
    resizer.setPointerCapture(event.pointerId);
    resizer.dataset.dragging = "";
  });
  resizer.addEventListener("pointermove", (event) => {
    if (dragStart && resizer.hasPointerCapture(event.pointerId)) {
      setWidth(dragStart.width + event.clientX - dragStart.x);
    }
  });
  resizer.addEventListener("lostpointercapture", () => {
    delete resizer.dataset.dragging;
    dragStart = undefined;
    writeSession(explorerWidth, resizer.getAttribute("aria-valuenow"));
  });
  resizer.addEventListener("keydown", (event) => {
    const widths = {
      ArrowLeft: explorer.offsetWidth - 12,
      ArrowRight: explorer.offsetWidth + 12,
      Home: Number(resizer.getAttribute("aria-valuemin")),
      End: Number(resizer.getAttribute("aria-valuemax")),
    };
    if (!Object.hasOwn(widths, event.key)) return;
    event.preventDefault();
    setWidth(widths[event.key]);
    writeSession(explorerWidth, resizer.getAttribute("aria-valuenow"));
  });

  const tabStore = "mystic-tabs";
  const tabs = document.querySelector("#open-tabs");
  const previousTabs = (readSession(tabStore) ?? "readme").split(",");
  let openFiles = [...new Set(["welcome", ...previousTabs, currentFile])]
    .filter((id) => files.has(id));

  function closeTab(id) {
    const prevIndex = openFiles.indexOf(id) - 1;
    openFiles = openFiles.filter((file) => file !== id);
    writeSession(tabStore, openFiles.join(","));
    const nextId = openFiles[Math.max(0, prevIndex)];
    if (id === currentFile) {
      window.location.assign(files.get(nextId).href);
      return;
    }
    renderTabs();
    tabs.querySelector(`[data-file-id="${nextId}"]`)?.focus();
  }

  function renderTabs() {
    tabs.replaceChildren(...openFiles.map((id) => {
      const tab = document.createElement("div");
      tab.className = "editor-tab";
      const link = files.get(id).cloneNode(true);
      link.removeAttribute("class");
      tab.append(link);
      if (id !== "welcome") {
        const close = document.createElement("button");
        close.className = "tab-close";
        close.type = "button";
        close.setAttribute("aria-label", `Close ${link.dataset.fileName} tab`);
        close.append(document.querySelector("[data-terminal-close] .icon").cloneNode(true));
        close.addEventListener("click", () => closeTab(id));
        tab.append(close);
      }
      return tab;
    }));
    tabs.querySelector("[aria-current]")?.scrollIntoView({block: "nearest", inline: "nearest"});
  }

  if (files.has(currentFile)) {
    renderTabs();
    writeSession(tabStore, openFiles.join(","));
  }

  const terminal = document.querySelector("#terminal");
  const terminalForm = terminal.querySelector("form");
  const terminalInput = terminalForm.querySelector("input");
  const terminalLog = terminal.querySelector(".terminal-log");
  const terminalButtons = document.querySelectorAll("[data-terminal]");
  let terminalOpener;
  const history = [];
  let historyIndex = 0;

  function setTerminal(open) {
    terminal.hidden = !open;
    for (const button of terminalButtons) {
      button.setAttribute("aria-expanded", String(open));
      const label = button.querySelector("[data-terminal-label]");
      if (label) label.textContent = open ? "Hide terminal" : "Open terminal";
    }
    if (open) terminalInput.focus();
    else terminalOpener?.focus();
  }

  for (const button of terminalButtons) {
    button.hidden = false;
    button.addEventListener("click", () => {
      terminalOpener = button;
      setTerminal(terminal.hidden);
    });
  }
  terminal.querySelector("[data-terminal-close]").addEventListener("click", () => setTerminal(false));

  function print(message, className = "") {
    const row = document.createElement("p");
    row.className = className;
    row.textContent = message;
    terminalLog.append(row);
    if (terminalLog.childElementCount > 100) terminalLog.firstElementChild.remove();
    terminalLog.scrollTop = terminalLog.scrollHeight;
  }

  terminalForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const input = terminalInput.value.trim();
    terminalInput.value = "";
    if (!input) return;
    history.push(input);
    if (history.length > 35) history.shift();
    historyIndex = history.length;
    const [command, ...args] = input.toLowerCase().split(/\s+/);
    const requested = args.join(" ").split("/").at(-1);
    const file = files.get(requested) ?? [...files.values()].find((link) => link.dataset.fileName.toLowerCase() === requested);

    if (command === "clear") {
      terminalLog.replaceChildren();
      return;
    }
    print(`mystic:~$ ${input}`, "terminal-command");
    switch (command) {
      case "help":
        print("help · ls · cat <file> · open <file> · whoami · themes · clear · exit");
        break;
      case "ls":
        print([...files.values()].map((link) => link.dataset.fileName).join("  "));
        break;
      case "cat":
        print(file ? file.dataset.fileIntro : "File not found. Try ls.");
        break;
      case "open":
        if (file) window.location.assign(file.href);
        else print("File not found. Try ls.");
        break;
      case "whoami":
        print(files.get("readme").dataset.fileIntro);
        break;
      case "themes":
        print("Open settings.json to change the color theme.");
        break;
      case "exit":
        setTerminal(false);
        break;
      default:
        print(`Unknown command: ${command}. Try help.`);
    }
  });
  terminal.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setTerminal(false);
  });
  terminalInput.addEventListener("keydown", (event) => {
    if (!["ArrowUp", "ArrowDown"].includes(event.key) || !history.length) return;
    event.preventDefault();
    historyIndex = Math.max(0, Math.min(history.length, historyIndex + (event.key === "ArrowUp" ? -1 : 1)));
    terminalInput.value = history[historyIndex] ?? "";
  });

  const dialog = document.querySelector("#jump-dialog");
  if (typeof dialog.showModal !== "function") return;
  const search = dialog.querySelector("input");
  const rows = Array.from(dialog.querySelectorAll(".jump-results li"), (row) => ({
    row,
    link: row.querySelector("a"),
    text: `${row.textContent} ${row.dataset.search}`.toLowerCase(),
  }));
  const empty = dialog.querySelector(".jump-empty");
  const status = dialog.querySelector("#jump-status");
  const apple = /Mac|iPhone|iPad|iPod/.test(navigator.platform);
  document.querySelector(".quick-open kbd").textContent = apple ? "⌘ K" : "Ctrl K";
  const visibleRows = () => rows.filter(({ row }) => !row.hidden);

  function filter() {
    const words = search.value.toLowerCase().trim().split(/\s+/);
    for (const { row, text } of rows) {
      row.hidden = !words.every((word) => text.includes(word));
    }
    const count = visibleRows().length;
    empty.hidden = count > 0;
    status.textContent = count === 1 ? "1 matching file" : `${count} matching files`;
  }

  function openSearch() {
    if (dialog.open) return;
    search.value = "";
    filter();
    dialog.showModal();
  }

  for (const trigger of document.querySelectorAll("[data-jump]")) {
    trigger.setAttribute("aria-keyshortcuts", apple ? "Meta+K" : "Control+K");
    trigger.hidden = false;
    trigger.addEventListener("click", openSearch);
  }
  search.addEventListener("input", filter);
  search.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && search.value.trim()) visibleRows()[0]?.link.click();
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
      openSearch();
    }
  });
})();
