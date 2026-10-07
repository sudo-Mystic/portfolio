
(function(){
  var root = document.documentElement;
  try {
    var t = localStorage.getItem('mystic-theme');
    if (t) root.setAttribute('data-theme', t);
  } catch(e){}
  window.mysticSetTheme = function(id){
    root.setAttribute('data-theme', id);
    try { localStorage.setItem('mystic-theme', id); } catch(e){}
    renderThemeCards();
  };
  window.mysticTheme = function(){ return root.getAttribute('data-theme'); };

  function renderThemeCards(){
    var wrap = document.getElementById('theme-cards');
    if (!wrap || !window.__THEMES) return;
    var cur = window.mysticTheme();
    wrap.innerHTML = '';
    window.__THEMES.forEach(function(th){
      var card = document.createElement('button');
      card.type = 'button';
      card.className = 'rounded-[8px] border p-4 text-left transition-colors ' +
        (th.id === cur ? 'border-[var(--vscode-focusBorder,#4ec9b0)]' : 'border-border hover:border-muted');
      card.style.borderColor = th.id === cur ? '#4ec9b0' : '';
      card.innerHTML =
        '<div class="flex gap-1.5 mb-3">' +
        '<span class="h-8 flex-1 rounded" style="background:' + th.base + ';border:1px solid rgba(255,255,255,.12)"></span>' +
        '<span class="h-8 w-8 rounded" style="background:#4ec9b0"></span>' +
        '<span class="h-8 w-8 rounded" style="background:#4fc1ff"></span>' +
        '<span class="h-8 w-8 rounded" style="background:#c586c0"></span></div>' +
        '<div class="text-[13px] text-tab-active-fg font-medium">' + th.name + '</div>' +
        '<div class="text-[12px] text-muted mt-0.5">' + th.desc + '</div>' +
        (th.id === cur ? '<div class="text-[12px] mt-2" style="color:#4ec9b0">● active</div>' : '');
      card.addEventListener('click', function(){ window.mysticSetTheme(th.id); });
      wrap.appendChild(card);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', renderThemeCards);
  else renderThemeCards();

  // mobile drawer (Open Editors sheet)
  var drawer = document.querySelector('section.absolute.inset-x-0.bottom-0.z-30');
  var backdrop = document.querySelector('div.absolute.inset-0.z-20.bg-backdrop');
  function setDrawer(open){
    if (!drawer) return;
    drawer.classList.toggle('invisible', !open);
    drawer.classList.toggle('translate-y-full', !open);
    if (backdrop) {
      backdrop.classList.toggle('invisible', !open);
      backdrop.classList.toggle('opacity-0', !open);
    }
  }
  if (backdrop) backdrop.addEventListener('click', function(){ setDrawer(false); });
  var drawerClose = drawer ? drawer.querySelector('button[aria-label^="Close"]') : null;
  if (drawerClose) drawerClose.addEventListener('click', function(){ setDrawer(false); });
  // bottom nav (mobile): first button = files, last = terminal
  var bottomNav = document.querySelector('nav.relative.z-40');
  if (bottomNav) {
    var btns = bottomNav.querySelectorAll('button');
    if (btns[0]) btns[0].addEventListener('click', function(){
      var isOpen = drawer && !drawer.classList.contains('invisible');
      setDrawer(!isOpen);
    });
    if (btns[btns.length-1]) btns[btns.length-1].addEventListener('click', openTerm);
  }
  // activity bar (desktop): last icon opens terminal too
  var actBar = document.querySelector('nav.flex.w-12');
  if (actBar) {
    var ab = actBar.querySelectorAll('button');
    if (ab[ab.length-1]) ab[ab.length-1].addEventListener('click', openTerm);
  }

  // ---------- terminal ----------
  var term = document.getElementById('mterm'),
      out = document.getElementById('mterm-out'),
      inp = document.getElementById('mterm-in');
  function print(html){ if(out){ out.insertAdjacentHTML('beforeend', html); out.scrollTop = out.scrollHeight; } }
  function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;'); }
  var FILES = {
    'README.md': 'Rishabh Bohra — B.Tech undergrad at IET DAVV.\nEmbedded / Mobile / Security.\n\n"If it runs code, it can be understood."',
    'scoot.dart': 'Flutter companion app for TVS smart scooters.\nBLE telemetry, trips, cluster nav. Shipped to real users.',
    'detroit_jev.py': 'AI plays Detroit: Become Human. All 226 decisions, live.',
    'esp_reddit.cpp': 'Reddit API wrapper for ESP32. OAuth2, rate limiting, 39 tests.',
    'exam_eval.md': 'AI examination evaluation platform. Next.js + Gemini pipeline.',
    'settings.json': '{ "theme": "' + (window.mysticTheme && window.mysticTheme() || 'dark-modern') + '" }'
  };
  function openTerm(){
    if (!term) return;
    term.classList.remove('hidden');
    if (!term.dataset.booted){
      term.dataset.booted = '1';
      print('<div class="text-muted">mystic.code shell — type <span class="text-editor-fg">help</span></div>');
    }
    setTimeout(function(){ inp && inp.focus(); }, 50);
  }
  window.mysticOpenTerm = openTerm;
  document.querySelectorAll('[data-open-terminal]').forEach(function(b){
    b.addEventListener('click', openTerm);
  });
  var closeBtn = document.getElementById('mterm-close');
  if (closeBtn) closeBtn.addEventListener('click', function(){ term.classList.add('hidden'); });
  if (inp) inp.addEventListener('keydown', function(e){
    if (e.key !== 'Enter') return;
    var raw = inp.value; inp.value = '';
    print('<div><span class="text-ansi-green">rishabh@mystic:~$</span> <span>' + esc(raw) + '</span></div>');
    var parts = raw.trim().split(/\s+/), cmd = parts[0] || '', arg = parts.slice(1).join(' ');
    switch(cmd){
      case '': break;
      case 'help':
        print('<div class="text-muted">help · ls · cat &lt;file&gt; · whoami · neofetch · themes · open &lt;file&gt; · clear · exit</div>'); break;
      case 'ls':
        print('<div class="text-editor-fg">README.md&nbsp;&nbsp;projects/&nbsp;&nbsp;.vscode/</div><div class="text-muted">projects/: scoot.dart detroit_jev.py esp_reddit.cpp exam_eval.md</div>'); break;
      case 'cat':
        if (FILES[arg]) print('<div class="whitespace-pre-wrap text-editor-fg">' + esc(FILES[arg]) + '</div>');
        else print('<div class="text-muted">cat: ' + esc(arg || '') + ': no such file. Try ls.</div>');
        break;
      case 'whoami': print('<div class="text-editor-fg">rishabh — builder, breaker, shipper</div>'); break;
      case 'neofetch':
        print('<div class="text-editor-fg">mystic.code</div><div class="text-muted">user: rishabh bohra<br>stack: embedded / flutter / security<br>editor: this website<br>uptime: always building</div>'); break;
      case 'themes': print('<div class="text-muted">dark-modern · dark-plus · oled · dreamscape — change them on the <span class="text-editor-fg">settings</span> page</div>'); break;
      case 'open':
        if (FILES[arg]) print('<div class="text-muted">opening ' + esc(arg) + '… (it is already open in the editor above)</div>');
        else print('<div class="text-muted">open: unknown file. Try ls.</div>');
        break;
      case 'clear': out.innerHTML = ''; break;
      case 'exit': term.classList.add('hidden'); break;
      default: print('<div class="text-muted">command not found: ' + esc(cmd) + ' — try help</div>');
    }
  });
})();
