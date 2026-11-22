// Teria-Shell: Konsolen-Oberflaeche. Bedienung mit Joy-Cons/Pro Controller (ueber den Dienst),
// Tastatur (Pfeile, Enter = A, Escape/Backspace = B, Home/F1 = Schnellmenue, Q/E = L/R) und Touch.
"use strict";
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const I = {
  wifi: '<path d="M2 8.5a15 15 0 0 1 20 0M5 12a10 10 0 0 1 14 0M8.5 15.5a5 5 0 0 1 7 0"/><circle cx="12" cy="19" r="1"/>',
  bt: '<path d="M7 7l10 10-5 5V2l5 5L7 17"/>',
  bat: '<rect x="2" y="7" width="18" height="10" rx="2"/><path d="M22 11v2"/><rect x="4" y="9" width="11" height="6" rx="1" fill="currentColor"/>',
  home: '<path d="M3 11l9-8 9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
  grid: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  bag: '<path d="M5 8h14l-1 13H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
  gear: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
  term: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M12 15h5"/>',
  folder: '<path d="M3 6a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/>',
  globe: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
  play: '<path d="M7 4l13 8-13 8z" fill="currentColor"/>',
  desk: '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
  code: '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
  music: '<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
  moon: '<path d="M20 14A8 8 0 1 1 10 4a6.5 6.5 0 0 0 10 10z"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  vol: '<path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/>',
  power: '<path d="M12 2v10"/><path d="M6.3 6.3a8 8 0 1 0 11.4 0"/>',
  pad: '<path d="M6 8h12a4 4 0 0 1 4 4l-1 5a2 2 0 0 1-3.5 1L15 16H9l-2.5 2A2 2 0 0 1 3 17l-1-5a4 4 0 0 1 4-4z"/><path d="M7 11v3M5.5 12.5h3"/>',
  shield: '<path d="M12 2l8 3v7c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
  bolt: '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
  disk: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 14h18"/><circle cx="17" cy="17" r="1" fill="currentColor"/>',
  refresh: '<path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  tv: '<rect x="2" y="5" width="20" height="13" rx="2"/><path d="M8 2l4 3 4-3"/>',
  star: '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z" fill="currentColor"/>',
  down: '<path d="M12 4v12M6 11l6 6 6-6M5 20h14"/>',
  check: '<path d="M5 12l5 5 9-10"/>',
  reboot: '<path d="M4 12a8 8 0 1 0 2.3-5.7M4 4v5h5"/>',
  bell: '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>',
  lock: '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
  kbd: '<rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
};
const ic = (n, s = 20) => `<svg class="ic" width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${I[n] || I.grid}</svg>`;
const GRAD = { system: "linear-gradient(135deg,#2b2f45,#151829)", apps: "linear-gradient(135deg,#4d7cfe,#2f4cc0)", medien: "linear-gradient(135deg,#8a5cf6,#5b33c9)", entwicklung: "linear-gradient(135deg,#1d2343,#3b4fb0)", spiele: "linear-gradient(135deg,#ff8a3d,#e5484d)" };
const ARTS = ["t-orbit", "t-sterne", "t-pixel", "t-berg", "t-code", "t-wellen", "t-raster", "t-film"];
const CAT = { spiele: "Spiel", apps: "App", medien: "Medien", entwicklung: "Entwicklung", system: "System" };

// ---------------------------------------------------------------- Daten
let S = null, APPS = [], STORE = [], INFO = {}, WIFI = [];
const api = (p, body) => fetch(p, body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then(r => r.json());
async function load() {
  [S, APPS, STORE] = await Promise.all([api("/api/state"), api("/api/apps"), api("/api/store")]);
}
function hash(s) { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) | 0; return Math.abs(h); }
function artOf(a) { return a.art || (a.category === "spiele" ? ARTS[hash(a.id) % ARTS.length] : null); }
function iconHtml(a, size) {
  if (a.icon) return `<img src="/api/icon/${encodeURIComponent(a.icon)}" alt="" onerror="this.replaceWith(document.createRange().createContextualFragment('${ic(a.glyph || "grid", size).replace(/'/g, "\\'").replace(/"/g, "&quot;")}'))">`;
  return ic(a.glyph || { system: "term", medien: "music", entwicklung: "code" }[a.category] || "grid", size);
}
function tileStyle(a) { const art = artOf(a); return art ? `background-image:url(art/${art}.jpg)` : `background:${GRAD[a.category] || GRAD.apps}`; }

// ---------------------------------------------------------------- Bausteine
function statusBar(extra = "") {
  const b = S.battery || {};
  return `<div class="status"><div class="me"><div class="av">${esc((S.user || "T")[0].toUpperCase())}</div>${esc(S.user)}</div>${extra}<div class="sp"></div>
  <div class="r">${ic("bell", 18)}<span class="${S.bluetooth?.on ? "" : "off"}">${ic("bt", 18)}</span><span class="${S.wifi?.on && S.wifi?.ssid ? "" : "off"}">${ic("wifi", 18)}</span>
  <span class="pill ${b.charging ? "chg" : ""}">${ic(b.charging ? "bolt" : "bat", 18)} ${b.capacity ?? "–"} %</span><span class="time" id="clock">${clock()}</span></div></div>`;
}
function hints(...h) { return `<div class="hints">${h.map(([k, t]) => `<span><i class="k">${k}</i>${t}</span>`).join("")}</div>`; }
function clock() { return new Date().toLocaleTimeString("de-AT", { hour: "2-digit", minute: "2-digit" }); }
function dateStr() { return new Date().toLocaleDateString("de-AT", { weekday: "long", day: "numeric", month: "long" }); }
// Glasflaechen: vorberechneten Weichzeichner genau unter die Flaeche legen (keine GPU noetig)
const GLASS = ".glass,.card,.qt,.hints,.status .r,.tabs,.chip,.ghost,.seg,.side .navrow.cur,#toast,.appicon.sys";
function glassify(root = $("#stage")) {
  const sr = $("#stage").getBoundingClientRect(), s = sr.width / 1280 || 1;
  for (const el of $$(GLASS, root)) {
    const r = el.getBoundingClientRect();
    el.style.backgroundPosition = `0 0, ${-(r.left - sr.left) / s}px ${-(r.top - sr.top) / s}px`;
  }
}
function toast(t) { const el = $("#toast"); el.textContent = t; el.classList.add("on"); glassify(el.parentNode); clearTimeout(toast.t); toast.t = setTimeout(() => el.classList.remove("on"), 2600); }

// ---------------------------------------------------------------- Navigation
const NAV = { view: "home", stack: [], homeTab: "spiele", libFilter: "alle", storeTab: "spiele", app: null, setPage: "energie" };
let sel = null;
function focusables(root) { return $$(".nav", root).filter(e => e.offsetParent !== null); }
function scope() { if ($("#dialog").classList.contains("on")) return $("#dialog"); if ($("#quick").classList.contains("on")) return $("#quick"); return $(".view.on"); }
function select(el, scroll = true) {
  if (!el) return;
  if (sel) sel.classList.remove("sel");
  sel = el; el.classList.add("sel");
  if (el.dataset.onsel) HANDLERS[el.dataset.onsel]?.(el);
  if (scroll) el.scrollIntoView?.({ block: "nearest", inline: "nearest" });
}
function move(dir) {
  const items = focusables(scope());
  if (!items.length) return;
  if (!sel || !items.includes(sel)) return select(items[0]);
  const r = sel.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
  let best = null, bestScore = Infinity;
  for (const el of items) {
    if (el === sel) continue;
    const q = el.getBoundingClientRect(), x = q.left + q.width / 2, y = q.top + q.height / 2, dx = x - cx, dy = y - cy;
    const ok = { left: dx < -4 && Math.abs(dx) >= Math.abs(dy) * 0.3, right: dx > 4 && Math.abs(dx) >= Math.abs(dy) * 0.3, up: dy < -4, down: dy > 4 }[dir];
    if (!ok) continue;
    const main = dir === "left" || dir === "right" ? Math.abs(dx) : Math.abs(dy);
    const cross = dir === "left" || dir === "right" ? Math.abs(dy) : Math.abs(dx);
    const score = main + cross * 2.2;
    if (score < bestScore) { bestScore = score; best = el; }
  }
  if (best) select(best);
}
function activate() { if (sel) sel.click(); }
function back() {
  if ($("#dialog").classList.contains("on")) return closeDialog();
  if ($("#quick").classList.contains("on")) return toggleQuick(false);
  if (NAV.stack.length) { const v = NAV.stack.pop(); show(v, false); }
}
function show(view, push = true) {
  if (push && NAV.view !== view) NAV.stack.push(NAV.view);
  NAV.view = view;
  $("#stage").classList.toggle("deep", view !== "home");
  $$(".view").forEach(v => v.classList.toggle("on", v.id === "v-" + view));
  render();
}
function render(keepSel = true) {
  const prevKey = keepSel && sel ? sel.dataset.key : null;
  RENDER[NAV.view]();
  const items = focusables(scope());
  const again = prevKey && items.find(e => e.dataset.key === prevKey);
  sel = null; select(again || items.find(e => e.dataset.first) || items[0], false);
  glassify();
}
const HANDLERS = {};
function nav(attrs, key, extra = "") { return `class="nav ${attrs}" data-key="${esc(key)}" ${extra}`; }

// ---------------------------------------------------------------- Startbildschirm
let heroApp = null;
const RENDER = {
  home() {
    const tab = NAV.homeTab;
    const list = APPS.filter(a => tab === "spiele" ? a.category === "spiele" : tab === "medien" ? a.category === "medien" : a.category !== "spiele" && a.category !== "medien");
    const sys = [["Bibliothek", "grid", GRAD.apps, "go:library"], ["Store", "bag", "linear-gradient(135deg,#3ee0c5,#1f8f9c)", "go:store"], ["Desktop", "desk", "linear-gradient(135deg,#8a5cf6,#5b33c9)", "desktop"], ["Einstellungen", "gear", "linear-gradient(135deg,#5b6280,#353a52)", "go:settings"]];
    heroApp = heroApp && list.includes(heroApp) ? heroApp : list[0] || null;
    const tiles = list.slice(0, 6).map((a, i) => `<div ${nav("appicon", "app:" + a.id, `data-onsel="hero" data-app="${esc(a.id)}" onclick="launch('${esc(a.id)}')" ${a === heroApp ? "data-first=1" : ""} style="width:104px;height:104px;${tileStyle(a)}"`)}>${artOf(a) ? "" : iconHtml(a, 40)}</div>`).join("");
    const sysT = sys.map(([n, g, bg, act]) => `<div ${nav("appicon sys", "sys:" + n, `data-onsel="hero" data-sys="${n}" onclick="doAct('${act}')" style="width:104px;height:104px"`)}>${ic(g, 40)}</div>`).join("");
    const recent = APPS.filter(a => a !== heroApp && a.recent != null).slice(0, 3);
    $("#v-home").innerHTML = `<div class="bg" id="homebg" style="background-image:url(art/home.jpg)"></div>
    <div class="shade" style="background:linear-gradient(90deg,rgba(6,7,18,.92) 0%,rgba(6,7,18,.55) 45%,rgba(6,7,18,0) 75%),linear-gradient(0deg,rgba(6,7,18,.95) 0%,rgba(6,7,18,0) 45%)"></div>
    ${statusBar(`<div class="tabs">${[["spiele", "Spiele"], ["apps", "Apps"], ["medien", "Medien"]].map(([k, t]) => `<span class="tab ${tab === k ? "on" : ""}" onclick="homeTab('${k}')">${t}</span>`).join("")}</div>`)}
    <div id="selname" style="position:absolute;top:92px;left:40px;font-size:15px;color:var(--ink2);font-weight:500"></div>
    <div id="tiles">${tiles}${list.length ? '<div class="sep"></div>' : ""}${sysT}</div>
    <div id="hero"></div>
    <div class="homefoot" style="position:absolute;left:40px;right:40px;bottom:62px;display:flex;gap:16px;align-items:flex-end">
      <div>${recent.length ? `<div class="lbl" style="margin-bottom:10px">Zuletzt verwendet</div><div id="recent">${recent.map(a => `<div ${nav("mini", "rec:" + a.id, `onclick="launch('${esc(a.id)}')"`)}><div class="art" style="${tileStyle(a)}">${artOf(a) ? "" : iconHtml(a, 36)}</div><div>${esc(a.name)}</div></div>`).join("")}</div>` : ""}</div>
      <div style="flex:1"></div>
      <div class="card" style="width:330px;padding:18px 20px;display:flex;gap:14px;align-items:center"><div class="appicon sys" style="width:52px;height:52px;border-radius:16px">${ic("shield", 24)}</div><div><div style="font-weight:500">Teria ${esc(S.version)}</div><div style="color:var(--ink2);font-size:13px;margin-top:2px">eMMC ${esc(S.emmc)} · ${S.storage?.free_gb ?? "?"} GB frei</div></div></div>
    </div>
    ${hints(["A", "Starten"], ["L R", "Bereich"], ["+", "Schnellmenü"])}`;
    drawHero();
  },
  library() {
    const f = NAV.libFilter;
    const list = APPS.filter(a => f === "alle" || a.category === f);
    $("#v-library").innerHTML = `<div class="bg" style="background:radial-gradient(900px 500px at 85% -10%,rgba(62,224,197,.18),transparent 60%),radial-gradient(700px 500px at 10% 110%,rgba(255,138,61,.12),transparent 60%),#0b0d1d"></div>
    ${statusBar()}${sidebar("library")}
    <div style="position:absolute;top:86px;left:270px;right:40px;bottom:60px">
      <div style="display:flex;align-items:center;gap:14px"><div style="font-size:34px;font-weight:700">Bibliothek</div><span style="color:var(--ink3);font-size:16px;margin-top:6px">${APPS.length} Einträge</span></div>
      <div style="display:flex;gap:10px;margin:18px 0 22px">${[["alle", "Alle"], ["spiele", "Spiele"], ["apps", "Apps"], ["entwicklung", "Entwicklung"], ["medien", "Medien"], ["system", "System"]].map(([k, t]) => `<span ${nav("chip " + (f === k ? "on" : ""), "f:" + k, `onclick="libFilter('${k}')"`)}>${t}</span>`).join("")}</div>
      <div class="scroll" id="libgrid" style="height:470px;overflow-y:auto;padding:6px 8px 20px;margin:-6px -8px">${list.length ? `<div class="grid5">${list.map((a, i) => `<div ${nav("cell", "lib:" + a.id, `onclick="launch('${esc(a.id)}')" ${i === 0 ? "data-first=1" : ""}`)} style="border-radius:14px"><div class="art" style="${tileStyle(a)}">${artOf(a) ? "" : iconHtml(a, 44)}</div><div class="t"><b>${esc(a.name)}</b></div><div class="c">${CAT[a.category] || ""}</div></div>`).join("")}</div>` : `<div class="empty">Hier ist noch nichts. Im <b>Store</b> findest du Spiele und Apps.</div>`}</div>
    </div>${hints(["A", "Öffnen"], ["B", "Zurück"])}`;
  },
  store() {
    const t = NAV.storeTab;
    const list = STORE.filter(i => t === "alle" || i.kind === t || (t === "apps" && i.kind === "entwicklung"));
    $("#v-store").innerHTML = `<div class="bg" style="background:radial-gradient(900px 500px at 85% -10%,rgba(62,224,197,.16),transparent 60%),#0b0d1d"></div>
    ${statusBar(`<div class="tabs">${[["spiele", "Spiele"], ["apps", "Apps"], ["medien", "Medien"], ["alle", "Alle"]].map(([k, x]) => `<span class="tab ${t === k ? "on" : ""}" onclick="storeTab('${k}')">${x}</span>`).join("")}</div>`)}
    ${sidebar("store")}
    <div style="position:absolute;top:86px;left:270px;right:40px;bottom:60px">
      <div style="font-size:34px;font-weight:700">Store</div>
      <div style="color:var(--ink2);margin:6px 0 20px">Geprüfte Pakete aus Debian, passend für die Switch.</div>
      <div class="scroll" style="height:480px;overflow-y:auto;padding:6px 8px 20px;margin:-6px -8px"><div class="grid5">${list.map((i, n) => `<div ${nav("cell", "st:" + i.pkg, `onclick="openApp('${esc(i.pkg)}')" ${n === 0 ? "data-first=1" : ""}`)} style="border-radius:14px"><div class="art" style="background-image:url(art/${esc(i.art)}.jpg)">${i.installed ? `<span class="badge">installiert</span>` : ""}</div><div class="t"><b>${esc(i.name)}</b><span style="color:var(--ink3)">${esc(i.size)}</span></div><div class="c">${CAT[i.kind] || ""}</div></div>`).join("")}</div></div>
    </div>${hints(["A", "Details"], ["L R", "Bereich"], ["B", "Zurück"])}`;
  },
  app() {
    const i = STORE.find(x => x.pkg === NAV.app); if (!i) return;
    const job = Object.values(JOBS).find(j => j.pkg === i.pkg && j.status === "laeuft");
    $("#v-app").innerHTML = `<div class="bg" style="background-image:url(art/${esc(i.art)}.jpg);opacity:.35"></div>
    <div class="shade" style="background:linear-gradient(0deg,#0b0d1d 40%,rgba(11,13,29,.55) 75%,rgba(11,13,29,.25))"></div>
    ${statusBar()}
    <div style="position:absolute;left:40px;top:150px;display:flex;gap:26px;align-items:flex-end">
      <div class="appicon" style="width:132px;height:132px;border-radius:30px;background-image:url(art/${esc(i.art)}.jpg)"></div>
      <div><div class="lbl">${CAT[i.kind]} · Debian</div><div style="font-size:52px;font-weight:700;margin:6px 0 4px">${esc(i.name)}</div><div style="color:var(--ink2);font-size:15px">Paket <span style="font-family:var(--m)">${esc(i.pkg)}</span> · ${esc(i.size)}</div></div>
    </div>
    <div style="position:absolute;left:40px;top:330px;width:700px">
      <div style="display:flex;gap:12px;align-items:center">${i.installed
        ? `<button ${nav("cta", "inst", `data-first=1 onclick="toast('Starte über die Bibliothek')"`)}>${ic("check", 18)} Installiert</button>`
        : job ? `<button class="cta teal" style="opacity:.8">${ic("down", 18)} Wird installiert · ${job.progress} %</button>`
        : `<button ${nav("cta teal", "inst", `data-first=1 onclick="install('${esc(i.pkg)}')"`)}>${ic("down", 18)} Installieren · ${esc(i.size)}</button>`}
      <span style="color:var(--ink2);font-size:14px;margin-left:8px">Läuft auf arm64 · ${esc(i.controls)}</span></div>
      <p style="color:var(--ink2);font-size:17px;line-height:1.55;margin:24px 0;max-width:620px">${esc(i.desc)}</p>
    </div>
    <div class="card" style="position:absolute;right:40px;top:330px;width:380px;padding:20px 22px">
      ${[["Quelle", "Debian 13 (trixie)"], ["Größe", i.size], ["Steuerung", i.controls], ["Paket", i.pkg]].map(([a, b]) => `<div class="kv"><span>${a}</span><span>${esc(b)}</span></div>`).join("")}
      <div style="display:flex;gap:10px;align-items:center;margin-top:14px;color:var(--teal)">${ic("shield", 18)}<span>Geprüft, kein Zugriff auf den eMMC</span></div>
    </div>${hints(["A", i.installed ? "OK" : "Installieren"], ["B", "Zurück"])}`;
  },
  settings() {
    const pages = [["netzwerk", "wifi", "Netzwerk"], ["bluetooth", "bt", "Bluetooth"], ["anzeige", "sun", "Anzeige & Ton"], ["energie", "bolt", "Energie & Leistung"], ["sicherheit", "shield", "Sicherheit"], ["system", "info", "Über Teria"]];
    $("#v-settings").innerHTML = `<div class="bg" style="background:radial-gradient(900px 600px at 100% 0%,rgba(62,224,197,.10),transparent 60%),#0b0d1d"></div>
    ${statusBar()}
    <div class="side" style="gap:2px;font-size:15px"><div style="font-size:30px;font-weight:700;padding:0 14px 14px">Einstellungen</div>
    ${pages.map(([k, g, t]) => `<div ${nav("navrow " + (NAV.setPage === k ? "cur" : ""), "sp:" + k, `onclick="setPage('${k}')" ${NAV.setPage === k ? "data-first=1" : ""}`)}>${ic(g, 19)}${t}</div>`).join("")}</div>
    <div class="list" style="position:absolute;top:92px;left:300px;right:40px;bottom:60px">${SETTINGS[NAV.setPage]()}</div>
    ${hints(["A", "Auswählen"], ["B", "Zurück"])}`;
  },
};
HANDLERS.hero = el => {
  const a = APPS.find(x => x.id === el.dataset.app);
  if (a) heroApp = a;
  drawHero(a ? null : el.dataset.sys);
};
function drawHero(sysName) {
  const h = $("#hero"); if (!h) return;
  $("#selname").textContent = sysName || heroApp?.name || "";
  $$("#tiles .appicon").forEach(t => { const big = t === sel; t.style.width = t.style.height = big ? "132px" : "104px"; });
  glassify($("#tiles"));
  if (sysName) {
    const d = { Bibliothek: "Alles Installierte an einem Ort.", Store: "Spiele und Apps für die Switch.", Desktop: "Klassischer Desktop mit Dock, für die Arbeit im Dock.", Einstellungen: "WLAN, Bluetooth, Energie, Sicherheit." }[sysName];
    h.innerHTML = `<div class="lbl">System</div><h1>${esc(sysName)}</h1><p>${d}</p>`;
    $("#homebg").style.backgroundImage = "url(art/home.jpg)";
    return;
  }
  if (!heroApp) { h.innerHTML = `<div class="lbl">Willkommen</div><h1>Teria ist bereit</h1><p>Hier tauchen deine Spiele auf. Im Store findest du welche.</p><div style="display:flex;gap:12px;margin-top:18px"><span class="cta" onclick="show('store')">${ic("bag", 18)} Zum Store</span></div>`; return; }
  const art = artOf(heroApp);
  $("#homebg").style.backgroundImage = `url(art/${art && heroApp.category === "spiele" ? "home" : "home"}.jpg)`;
  h.innerHTML = `<div class="lbl">${heroApp.category === "spiele" ? "Weiterspielen" : CAT[heroApp.category] || "App"}</div><h1>${esc(heroApp.name)}</h1><p>${esc(heroApp.comment || "")}</p>
  <div style="display:flex;gap:12px;margin-top:18px"><span class="cta" onclick="launch('${esc(heroApp.id)}')">${ic("play", 18)} ${heroApp.category === "spiele" ? "Spielen" : "Öffnen"}</span></div>`;
}
function sidebar(cur) {
  return `<div class="side">${[["home", "home", "Start"], ["library", "grid", "Bibliothek"], ["store", "bag", "Store"], ["settings", "gear", "Einstellungen"]].map(([k, g, t]) => `<div ${nav("navrow " + (cur === k ? "cur" : ""), "side:" + k, `onclick="show('${k}')"`)}>${ic(g, 20)}${t}</div>`).join("")}
  <div class="card" style="margin-top:18px;padding:14px;font-size:13px;color:var(--ink2)"><div style="display:flex;justify-content:space-between;color:var(--ink)"><span>Speicher</span><span>${S.storage?.free_gb ?? "?"} GB frei</span></div><div class="bar" style="height:6px;margin-top:10px"><i style="width:${S.storage ? Math.round(100 - S.storage.free_gb * 100 / S.storage.total_gb) : 0}%"></i></div><div style="margin-top:8px">SD-Karte · ${S.storage?.total_gb ?? "?"} GB</div></div></div>`;
}

// ---------------------------------------------------------------- Einstellungen
function srow(key, title, sub, right, onclick) { return `<div ${nav("srow", key, `onclick="${onclick}"`)}><div class="t"><div>${title}</div><div>${sub}</div></div>${right}</div>`; }
const tog = on => `<span class="tog ${on ? "on" : ""}"></span>`;
const SETTINGS = {
  netzwerk() {
    return `<div style="font-size:24px;font-weight:500;margin-bottom:12px">Netzwerk</div>
    ${srow("wifi", "WLAN", S.wifi.on ? (S.wifi.ssid ? `Verbunden mit ${esc(S.wifi.ssid)} · ${esc(S.wifi.band || "")}` : "Nicht verbunden") : "Aus", tog(S.wifi.on), "toggle('wifi')")}
    <div class="lbl" style="margin:18px 0 6px">Netze in der Nähe</div>
    ${WIFI.length ? WIFI.map(n => srow("net:" + n.ssid, esc(n.ssid), `${n.active ? "Verbunden · " : ""}Signal ${n.signal} %${n.secure ? " · geschützt" : ""}`, n.active ? `<span style="color:var(--teal)">${ic("check", 20)}</span>` : (n.secure ? `<span style="color:var(--ink3)">${ic("lock", 18)}</span>` : ""), `connectWifi(this.dataset.key.slice(4),${n.secure})`)).join("") : `<div class="empty">Suche läuft …</div>`}`;
  },
  bluetooth() {
    return `<div style="font-size:24px;font-weight:500;margin-bottom:12px">Bluetooth</div>
    ${srow("bt", "Bluetooth", S.bluetooth.on ? "An" : "Aus", tog(S.bluetooth.on), "toggle('bluetooth')")}
    <div class="lbl" style="margin:18px 0 6px">Verbunden</div>
    ${(S.bluetooth.connected || []).map(d => `<div class="srow"><div class="t"><div>${esc(d)}</div><div>Verbunden</div></div></div>`).join("") || `<div class="empty">Keine Geräte verbunden. Joy-Cons an der Schiene sind direkt verbunden.</div>`}`;
  },
  anzeige() {
    const sl = (k, icn, t, v) => `<div ${nav("srow", k, `onclick="step('${k}',10)"`)}><span style="color:var(--ink2)">${ic(icn, 22)}</span><div class="t"><div style="display:flex;justify-content:space-between"><span>${t}</span><span style="color:var(--ink2)">${v ?? "–"} %</span></div><div class="bar" style="margin-top:10px"><i style="width:${v || 0}%"></i></div></div></div>`;
    return `<div style="font-size:24px;font-weight:500;margin-bottom:12px">Anzeige &amp; Ton</div>${sl("brightness", "sun", "Helligkeit", S.brightness)}${sl("volume", "vol", "Lautstärke", S.volume?.value)}
    <div class="empty" style="margin-top:14px">Mit links und rechts auf dem Steuerkreuz anpassen.</div>
    ${srow("kbd", "Bildschirmtastatur", "Für Texteingaben ohne Tastatur", ic("kbd", 22), "doAct('keyboard')")}`;
  },
  energie() {
    const p = S.perf;
    const seg = [["eco", "Eco", "lange Laufzeit"], ["ausgewogen", "Ausgewogen", "Standard"], ["max", "Max", "für das Dock"]].map(([k, t, s]) => `<div ${nav(p === k ? "on" : "", "perf:" + k, `onclick="setPerf('${k}')"`)}>${t}<small>${s}</small></div>`).join("");
    const b = S.battery || {};
    return `<div style="display:grid;grid-template-columns:1fr 330px;gap:26px"><div>
    <div style="font-size:24px;font-weight:500;margin-bottom:16px">Energie &amp; Leistung</div><div class="seg">${seg}</div>
    ${srow("lim", "Ladegrenze", b.limit ? `Lädt bis ${esc(b.limit)} %, schont den Akku` : "Vom System verwaltet", `<span style="color:var(--ink2)">${b.limit ? esc(b.limit) + " %" : "–"}</span>`, "")}
    ${srow("hek", "Neu starten in Hekate", "Ohne RCM und Jig, über Reboot 2 Payload", ic("reboot", 20), "power('hekate')")}
    ${srow("rb", "Neu starten", "Startet Teria neu", ic("refresh", 20), "power('reboot')")}
    ${srow("off", "Ausschalten", "", ic("power", 20), "power('poweroff')")}
    </div><div style="display:flex;flex-direction:column;gap:16px">
    <div class="card" style="padding:20px"><div class="lbl">Jetzt</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px">
    ${[["Akku", (b.capacity ?? "–") + " %"], ["Leistung", (b.power_w ?? "–") + " W"], ["CPU", (S.temps?.cpu ?? "–") + " °C"], ["GPU", (S.temps?.gpu ?? "–") + " °C"]].map(([a, v]) => `<div><div style="color:var(--ink2);font-size:12px">${a}</div><div style="font-size:24px;font-weight:700;margin-top:2px">${v}</div></div>`).join("")}</div>
    <div style="color:var(--ink3);font-size:12px;margin-top:14px">${b.cycles ? `${esc(b.cycles)} Ladezyklen · ${b.health ?? "?"} % Kapazität` : ""}</div></div>
    ${(b.joycons || []).length ? `<div class="card" style="padding:16px 20px">${b.joycons.map(j => `<div class="kv"><span>${esc(j.name)}</span><span>${esc(j.level)}</span></div>`).join("")}</div>` : ""}
    </div></div>`;
  },
  sicherheit() {
    const ok = /gesch/.test(S.emmc) || /nicht sichtbar/.test(S.emmc);
    return `<div style="font-size:24px;font-weight:500;margin-bottom:12px">Sicherheit</div>
    <div class="card" style="padding:20px;display:flex;gap:16px;align-items:center;margin-bottom:12px"><span style="color:${ok ? "var(--teal)" : "var(--amber)"}">${ic("shield", 34)}</span><div><div style="font-size:18px;font-weight:500">eMMC: ${esc(S.emmc)}</div><div style="color:var(--ink2);font-size:14px;margin-top:3px">Teria schreibt nie auf den internen Speicher der Switch. Er wird beim Start schreibgeschützt und im Dateimanager ausgeblendet.</div></div></div>
    ${srow("ssh", "SSH-Zugang", "Anmeldung nur mit Passwort des Benutzers, kein Root-Login", `<span style="color:var(--ink2)">aktiv</span>`, "")}`;
  },
  system() {
    return `<div style="font-size:24px;font-weight:500;margin-bottom:12px">Über Teria</div><div class="card" style="padding:16px 22px">${Object.entries(INFO).map(([k, v]) => `<div class="kv"><span>${esc(k)}</span><span style="font-family:var(--m);text-align:right">${esc(v)}</span></div>`).join("") || `<div class="empty">Lade …</div>`}</div>`;
  },
};
async function setPage(k) { NAV.setPage = k; if (k === "system") INFO = await api("/api/info"); if (k === "netzwerk") api("/api/wifi").then(w => { WIFI = w; if (NAV.view === "settings" && NAV.setPage === "netzwerk") render(); }); render(false); select($(`[data-key="sp:${k}"]`)); }
async function toggle(what) { const cur = what === "wifi" ? S.wifi.on : S.bluetooth.on; const r = await api("/api/action/" + what, { value: !cur }); if (r.ok) { (what === "wifi" ? S.wifi : S.bluetooth).on = !cur; render(); toast((what === "wifi" ? "WLAN " : "Bluetooth ") + (!cur ? "an" : "aus")); } else toast("Ging nicht"); }
async function step(k, d) { const v = k === "volume" ? S.volume.value : S.brightness; const nv = Math.max(k === "volume" ? 0 : 5, Math.min(100, (v ?? 50) + d)); const r = await api("/api/action/" + k, { value: nv }); if (r.ok) { if (k === "volume") S.volume.value = nv; else S.brightness = nv; render(); } }
async function setPerf(p) { const r = await api("/api/action/perf", { value: p }); if (r.ok) { S.perf = p; render(); toast("Leistungsprofil: " + { eco: "Eco", ausgewogen: "Ausgewogen", max: "Max" }[p]); } else toast("Profil nicht geändert"); }
async function power(v) {
  const t = { hekate: "Jetzt in Hekate neu starten?", reboot: "Teria neu starten?", poweroff: "Switch ausschalten?", suspend: "Ruhezustand?" }[v];
  dialog(`<div style="font-size:22px;font-weight:500">${t}</div><div style="display:flex;gap:12px;justify-content:flex-end"><span ${nav("chip", "no", `onclick="closeDialog()"`)}>Abbrechen</span><span ${nav("chip on", "yes", `data-first=1 onclick="closeDialog();api('/api/action/power',{value:'${v}'})"`)}>Ja</span></div>`);
}
function connectWifi(ssid, secure) {
  if (!secure) return doConnect(ssid, "");
  dialog(`<div style="font-size:22px;font-weight:500">Mit „${esc(ssid)}“ verbinden</div><input id="pw" type="password" placeholder="Passwort" autocomplete="off">
  <div style="display:flex;gap:12px;justify-content:flex-end"><span ${nav("chip", "kb", `onclick="doAct('keyboard');$('#pw').focus()"`)}>${ic("kbd", 16)} Tastatur</span><span ${nav("chip", "no", `onclick="closeDialog()"`)}>Abbrechen</span><span ${nav("chip on", "go", `data-first=1`)}>Verbinden</span></div>`);
  $("#dialog [data-key=go]").onclick = () => doConnect(ssid, $("#pw").value);
}
async function doConnect(ssid, pw) { closeDialog(); toast("Verbinde mit " + ssid + " …"); const r = await api("/api/action/wifi-connect", { ssid, password: pw }); toast(r.ok ? "Verbunden" : "Verbindung fehlgeschlagen"); refresh(); }

// ---------------------------------------------------------------- Schnellmenü
function toggleQuick(on = !$("#quick").classList.contains("on")) {
  const q = $("#quick");
  if (!on) { q.classList.remove("on"); $("#stage").classList.remove("dim"); render(); return; }
  const b = S.battery || {};
  const qt = (key, icn, t, sub, isOn, act) => `<div ${nav("card qt " + (isOn ? "on" : ""), key, `onclick="${act}"`)}><div style="display:flex;justify-content:space-between;align-items:center"><span style="color:${isOn ? "var(--teal)" : "var(--ink2)"}">${ic(icn, 24)}</span>${tog(isOn)}</div><div><div style="font-weight:500">${t}</div><div style="color:var(--ink2);font-size:13px;margin-top:2px">${sub}</div></div></div>`;
  const sl = (k, icn, t, v) => `<div ${nav("", "q" + k, `onclick="step('${k}',10).then(()=>toggleQuick(true))"`)} style="display:flex;align-items:center;gap:14px;border-radius:10px;padding:4px"><span style="color:var(--ink2)">${ic(icn, 22)}</span><div style="flex:1"><div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:8px"><span>${t}</span><span style="color:var(--ink2)">${v ?? "–"} %</span></div><div class="bar"><i style="width:${v || 0}%"></i></div></div></div>`;
  q.innerHTML = `<div class="veil"></div>${statusBar()}
  <div style="position:absolute;left:40px;top:96px"><div class="lbl">Schnellmenü</div><div style="font-size:44px;font-weight:700;margin-top:6px">${dateStr()}</div></div>
  <div class="card" style="position:absolute;right:40px;top:96px;width:330px;padding:18px 20px;display:flex;flex-direction:column;gap:12px">
   <div style="display:flex;justify-content:space-between"><span class="lbl">Akku</span><span style="color:var(--teal);font-size:13px">${b.charging ? "lädt" : "Akku"}${b.power_w ? " · " + b.power_w + " W" : ""}</span></div>
   <div style="display:flex;align-items:baseline;gap:8px"><span style="font-size:40px;font-weight:700">${b.capacity ?? "–"} %</span><span style="color:var(--ink2);font-size:14px">${b.cycles ? b.cycles + " Zyklen" : ""}</span></div>
   <div style="display:flex;gap:10px">${(b.joycons || []).slice(0, 2).map(j => `<div style="flex:1;padding:10px;border-radius:12px;background:rgba(255,255,255,.06);font-size:13px"><div style="color:var(--ink2)">${esc(j.name)}</div><div style="margin-top:4px;font-weight:500">${esc(j.level)}</div></div>`).join("")}<div style="flex:1;padding:10px;border-radius:12px;background:rgba(255,255,255,.06);font-size:13px"><div style="color:var(--ink2)">Gesundheit</div><div style="margin-top:4px;font-weight:500">${b.health ?? "–"} %</div></div></div>
  </div>
  <div style="position:absolute;left:40px;right:40px;bottom:66px;display:grid;grid-template-columns:1.25fr 1fr;gap:18px">
   <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
    ${qt("qwifi", "wifi", "WLAN", S.wifi.on ? (S.wifi.ssid ? esc(S.wifi.ssid) + (S.wifi.band ? " · " + S.wifi.band : "") : "nicht verbunden") : "Aus", S.wifi.on, "toggle('wifi').then(()=>toggleQuick(true))")}
    ${qt("qbt", "bt", "Bluetooth", S.bluetooth.on ? (S.bluetooth.connected.length ? S.bluetooth.connected.length + " verbunden" : "An") : "Aus", S.bluetooth.on, "toggle('bluetooth').then(()=>toggleQuick(true))")}
    ${qt("qdesk", "desk", "Desktop-Modus", "Mit Dock und Fenstern", false, "doAct('desktop')")}
    ${qt("qdock", "tv", "Dock", S.docked ? "Angedockt" : "Handheld", S.docked, "")}
    ${qt("qemmc", "shield", "eMMC-Schutz", esc(S.emmc), true, "toggleQuick(false);show('settings');setPage('sicherheit')")}
    ${qt("qset", "gear", "Einstellungen", "Alles weitere", false, "toggleQuick(false);show('settings')")}
   </div>
   <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:18px">
    <div class="lbl">Leistung</div>
    <div style="display:flex;gap:8px">${[["eco", "Eco"], ["ausgewogen", "Ausgewogen"], ["max", "Max"]].map(([k, t]) => `<span ${nav("chip " + (S.perf === k ? "on" : ""), "qp:" + k, `onclick="setPerf('${k}').then(()=>toggleQuick(true))"`)}>${t}</span>`).join("")}<span style="flex:1"></span><span style="color:var(--ink2);font-size:13px;align-self:center">CPU ${S.temps?.cpu ?? "–"} °C</span></div>
    ${sl("brightness", "sun", "Helligkeit", S.brightness)}${sl("volume", "vol", "Lautstärke", S.volume?.value)}
    <div style="display:flex;gap:10px">${[["hekate", "reboot", "Neustart in Hekate"], ["suspend", "moon", "Ruhezustand"], ["poweroff", "power", "Aus"]].map(([v, g, t]) => `<span ${nav("chip", "qpw:" + v, `onclick="power('${v}')"`)}>${ic(g, 16)} ${t}</span>`).join("")}</div>
   </div>
  </div>${hints(["B", "Schließen"], ["+", "Schnellmenü"])}`;
  q.classList.add("on"); $("#stage").classList.add("dim"); glassify(q);
  const keep = sel?.dataset.key, items = focusables(q);
  sel = null; select(items.find(e => e.dataset.key === keep) || items[0], false);
}

// ---------------------------------------------------------------- Aktionen
const JOBS = {};
async function launch(id) { const r = await api("/api/launch", { id }); const a = APPS.find(x => x.id === id); toast(r.ok ? `${a ? a.name : "App"} wird gestartet …` : "Konnte nicht gestartet werden"); if (r.ok && a) { a.recent = 0; APPS = [a, ...APPS.filter(x => x !== a)]; } }
function doAct(a) {
  if (a.startsWith("go:")) return show(a.slice(3));
  if (a === "desktop") { toggleQuick(false); api("/api/action/mode", { value: "desktop" }); return toast("Desktop-Modus …"); }
  if (a === "keyboard") return api("/api/action/keyboard", {});
}
function homeTab(k) { NAV.homeTab = k; heroApp = null; render(false); }
function libFilter(k) { NAV.libFilter = k; render(); }
function storeTab(k) { NAV.storeTab = k; render(false); }
function openApp(pkg) { NAV.app = pkg; show("app"); }
async function install(pkg) { const r = await api("/api/install", { pkg }); if (r.ok) { JOBS[r.job] = { pkg, status: "laeuft", progress: 0 }; render(); toast("Installation gestartet"); } else toast("Nicht erlaubt"); }
function dialog(html) { const d = $("#dialog"); d.innerHTML = `<div class="card">${html}</div>`; d.classList.add("on"); glassify(d); sel = null; const items = focusables(d); select(items.find(e => e.dataset.first) || items[0], false); }
function closeDialog() { $("#dialog").classList.remove("on"); $("#dialog").innerHTML = ""; if ($("#quick").classList.contains("on")) toggleQuick(true); else render(); }
async function refresh() { S = await api("/api/state"); if (!$("#dialog").classList.contains("on")) { if ($("#quick").classList.contains("on")) toggleQuick(true); else render(); } }

// ---------------------------------------------------------------- Eingabe
function tabCycle(d) {
  if (NAV.view === "home") { const t = ["spiele", "apps", "medien"]; homeTab(t[(t.indexOf(NAV.homeTab) + d + 3) % 3]); }
  else if (NAV.view === "store") { const t = ["spiele", "apps", "medien", "alle"]; storeTab(t[(t.indexOf(NAV.storeTab) + d + 4) % 4]); }
}
function key(k) {
  if (document.activeElement?.tagName === "INPUT" && !["a", "b", "up", "down"].includes(k)) return;
  if (NAV.view === "settings" && NAV.setPage === "anzeige" && sel && ["brightness", "volume"].includes(sel.dataset.key) && (k === "left" || k === "right")) return step(sel.dataset.key, k === "left" ? -10 : 10);
  ({ up: () => move("up"), down: () => move("down"), left: () => move("left"), right: () => move("right"), a: activate, b: back,
     plus: () => toggleQuick(), home: () => toggleQuick(true), l: () => tabCycle(-1), r: () => tabCycle(1),
     y: () => { if (NAV.view !== "library") show("library"); }, x: () => { if (NAV.view !== "store") show("store"); } }[k] || (() => {}))();
}
document.addEventListener("keydown", e => {
  if (e.target.tagName === "INPUT" && !["Enter", "Escape", "ArrowUp", "ArrowDown"].includes(e.key)) return;
  const m = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right", Enter: "a", " ": "a", Escape: "b", Backspace: "b", Home: "home", F1: "home", "+": "plus", q: "l", e: "r", Q: "l", E: "r" }[e.key];
  if (m) { e.preventDefault(); key(m); }
});
document.addEventListener("pointerdown", e => { const n = e.target.closest(".nav"); if (n) select(n, false); });
function fit() { const s = Math.min(innerWidth / 1280, innerHeight / 720); const st = $("#stage"); st.style.transform = `scale(${s})`; st.style.left = (innerWidth - 1280 * s) / 2 + "px"; st.style.top = (innerHeight - 720 * s) / 2 + "px"; }
addEventListener("resize", fit);
setInterval(() => { const c = $("#clock"); if (c) $$("#clock").forEach(x => x.textContent = clock()); }, 15000);

(async function start() {
  fit();
  await load();
  show("home", false);
  const ev = new EventSource("/api/events");
  ev.addEventListener("pad", m => key(JSON.parse(m.data).key));
  ev.addEventListener("state", m => { S = JSON.parse(m.data); if (!$("#dialog").classList.contains("on") && !$("#quick").classList.contains("on") && NAV.view !== "home") return; $$("#clock").forEach(x => x.textContent = clock()); });
  ev.addEventListener("job", m => { const j = JSON.parse(m.data); JOBS[j.id] = j; if (j.status !== "laeuft") { toast(j.status === "fertig" ? "Installation fertig" : "Installation fehlgeschlagen"); Promise.all([api("/api/store"), api("/api/apps")]).then(([s, a]) => { STORE = s; APPS = a; render(); }); } else if (NAV.view === "app") render(); });
  ev.addEventListener("show", () => { render(); });
  // Erste Seite: Hash erlaubt direkte Ansicht (z. B. #settings), nützlich fürs Prüfen
  const h = location.hash.slice(1);
  if (h === "quick") toggleQuick(true); else if (h.startsWith("settings")) { show("settings"); setPage(h.split("-")[1] || "energie"); } else if (h.startsWith("app-")) openApp(h.slice(4)); else if (["library", "store"].includes(h)) show(h);
})();
