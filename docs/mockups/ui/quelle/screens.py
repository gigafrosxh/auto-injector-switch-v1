import os
I={ # schlichte Linien-Icons (eigene)
'wifi':'<path d="M2 8.5a15 15 0 0 1 20 0M5 12a10 10 0 0 1 14 0M8.5 15.5a5 5 0 0 1 7 0"/><circle cx="12" cy="19" r="1"/>',
'bt':'<path d="M7 7l10 10-5 5V2l5 5L7 17"/>',
'bat':'<rect x="2" y="7" width="18" height="10" rx="2"/><path d="M22 11v2"/><rect x="4" y="9" width="11" height="6" rx="1" fill="currentColor"/>',
'home':'<path d="M3 11l9-8 9 8v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
'grid':'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
'bag':'<path d="M5 8h14l-1 13H6z"/><path d="M9 8a3 3 0 0 1 6 0"/>',
'gear':'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
'term':'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M12 15h5"/>',
'folder':'<path d="M3 6a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/>',
'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
'play':'<path d="M7 4l13 8-13 8z" fill="currentColor"/>',
'desk':'<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
'code':'<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
'music':'<path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/>',
'moon':'<path d="M20 14A8 8 0 1 1 10 4a6.5 6.5 0 0 0 10 10z"/>',
'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
'vol':'<path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/>',
'power':'<path d="M12 2v10"/><path d="M6.3 6.3a8 8 0 1 0 11.4 0"/>',
'pad':'<path d="M6 8h12a4 4 0 0 1 4 4l-1 5a2 2 0 0 1-3.5 1L15 16H9l-2.5 2A2 2 0 0 1 3 17l-1-5a4 4 0 0 1 4-4z"/><path d="M7 11v3M5.5 12.5h3"/><circle cx="16" cy="11.5" r=".8" fill="currentColor"/><circle cx="18" cy="13.5" r=".8" fill="currentColor"/>',
'shield':'<path d="M12 2l8 3v7c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
'bolt':'<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
'disk':'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 14h18"/><circle cx="17" cy="17" r="1" fill="currentColor"/>',
'refresh':'<path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/>',
'info':'<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/>',
'user':'<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
'plus':'<path d="M12 5v14M5 12h14"/>',
'search':'<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>',
'tv':'<rect x="2" y="5" width="20" height="13" rx="2"/><path d="M8 2l4 3 4-3"/>',
'star':'<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z" fill="currentColor"/>',
'down':'<path d="M12 4v12M6 11l6 6 6-6M5 20h14"/>',
'dots':'<circle cx="5" cy="12" r="1.6" fill="currentColor"/><circle cx="12" cy="12" r="1.6" fill="currentColor"/><circle cx="19" cy="12" r="1.6" fill="currentColor"/>',
'reboot':'<path d="M4 12a8 8 0 1 0 2.3-5.7M4 4v5h5"/>',
'bell':'<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>',
}
def ic(n,s=20,cls=''): return f'<svg class="ic {cls}" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{I[n]}</svg>'

CSS='''
:root{--ink:#eef1f8;--ink2:#a9b0c8;--ink3:#6f7694;--teal:#3ee0c5;--teal2:#20b39c;--amber:#ff8a3d;--glass:rgba(22,26,48,.62);--glass2:rgba(255,255,255,.07);--line:rgba(255,255,255,.10);
--f:"Ubuntu",system-ui,sans-serif;--m:"Ubuntu Mono",ui-monospace,monospace}
*{box-sizing:border-box}html,body{margin:0;background:#05060f}
.s{zoom:.625;width:1280px;height:720px;position:relative;overflow:hidden;font-family:var(--f);color:var(--ink);background:#0b0d1d}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.shade{position:absolute;inset:0}
.status{position:absolute;top:22px;left:40px;right:40px;display:flex;align-items:center;gap:18px;font-size:15px;z-index:5}
.status .me{display:flex;align-items:center;gap:10px;font-weight:500}
.av{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#3ee0c5,#3b6fd8);display:grid;place-items:center;font-weight:700;color:#071018;font-size:14px;box-shadow:0 0 0 2px rgba(255,255,255,.25)}
.status .sp{flex:1}.status .r{display:flex;gap:16px;align-items:center;color:var(--ink2)}
.pill{display:flex;align-items:center;gap:6px;padding:5px 10px;border-radius:999px;background:var(--glass2);border:1px solid var(--line);color:var(--ink)}
.time{font-weight:500;color:var(--ink);font-size:16px}
.hints{position:absolute;bottom:20px;right:40px;display:flex;gap:22px;font-size:14px;color:var(--ink2);z-index:5}
.hints span{display:flex;align-items:center;gap:8px}
.btn{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;background:rgba(255,255,255,.14);color:var(--ink);font-size:12px;font-weight:700;border:1px solid rgba(255,255,255,.25)}
.btn.sq{border-radius:7px;width:auto;padding:0 6px}
.tabs{display:flex;gap:28px;font-size:18px;color:var(--ink3);font-weight:500}
.tabs b{color:var(--ink);position:relative}.tabs b::after{content:"";position:absolute;left:0;right:0;bottom:-8px;height:3px;border-radius:3px;background:var(--teal)}
.appicon{border-radius:24px;display:grid;place-items:center;color:#fff;position:relative;box-shadow:0 10px 30px rgba(0,0,0,.35);overflow:hidden;background-size:cover;background-position:center}
.focus{outline:3px solid #fff;outline-offset:5px;box-shadow:0 0 0 10px rgba(62,224,197,.22),0 18px 50px rgba(0,0,0,.5)}
.cta{display:inline-flex;align-items:center;gap:10px;height:48px;padding:0 26px;border-radius:999px;background:var(--ink);color:#0a0d1c;font-weight:700;font-size:17px}
.ghost{display:inline-grid;place-items:center;width:48px;height:48px;border-radius:50%;background:rgba(255,255,255,.12);border:1px solid var(--line)}
.card{border-radius:18px;background:var(--glass);border:1px solid var(--line);backdrop-filter:blur(18px)}
.lbl{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);font-weight:500}
.chip{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 14px;border-radius:999px;border:1px solid var(--line);color:var(--ink2);font-size:14px;background:rgba(255,255,255,.04)}
.chip.on{background:var(--ink);color:#0a0d1c;border-color:transparent;font-weight:500}
.tog{width:44px;height:26px;border-radius:999px;background:rgba(255,255,255,.18);position:relative;flex:none}
.tog::after{content:"";position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff}
.tog.on{background:var(--teal)}.tog.on::after{left:21px;background:#05201b}
'''
def page(body,extra=''):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&family=Ubuntu+Mono&display=swap"><style>{CSS}{extra}</style></head><body><div class="s">{body}</div></body></html>'''
def status(name='daniel',extra=''):
    return f'''<div class="status"><div class="me"><div class="av">D</div>{name}</div>{extra}<div class="sp"></div><div class="r">{ic("bell",18)}{ic("bt",18)}{ic("wifi",18)}<span class="pill">{ic("bat",18)} 78 %</span><span class="time">14:32</span></div></div>'''
def hints(*h): return '<div class="hints">'+''.join(f'<span><i class="btn{" sq" if len(k)>1 else ""}">{k}</i>{t}</span>' for k,t in h)+'</div>'

TILES=[('Orbitfall','t-orbit.jpg',None),('Sternenläufer','t-sterne.jpg',None),('Pixelgarten','t-pixel.jpg',None),('Abendrot','t-berg.jpg',None),
       ('Code-Studio','t-code.jpg',None),('Wellen','t-wellen.jpg',None)]
SYS=[('Browser','globe','linear-gradient(135deg,#ff8a3d,#e5484d)'),('Terminal','term','linear-gradient(135deg,#2b2f45,#151829)'),('Dateien','folder','linear-gradient(135deg,#4d7cfe,#2f4cc0)'),('Store','bag','linear-gradient(135deg,#3ee0c5,#1f8f9c)'),('Desktop','desk','linear-gradient(135deg,#8a5cf6,#5b33c9)'),('Einstellungen','gear','linear-gradient(135deg,#5b6280,#353a52)')]

# 1 Home
row=''
for i,(n,img,_) in enumerate(TILES[:4]):
    sz=132 if i==0 else 104
    row+=f'<div class="appicon{" focus" if i==0 else ""}" style="width:{sz}px;height:{sz}px;background-image:url(art/{img})"></div>'
row+='<div style="width:1px;height:70px;background:var(--line);margin:0 6px"></div>'
for n,icn,g in SYS:
    row+=f'<div class="appicon" style="width:104px;height:104px;background:{g}">{ic(icn,40)}</div>'
home=f'''<div class="bg" style="background-image:url(art/home.jpg)"></div>
<div class="shade" style="background:linear-gradient(90deg,rgba(6,7,18,.92) 0%,rgba(6,7,18,.55) 45%,rgba(6,7,18,0) 75%),linear-gradient(0deg,rgba(6,7,18,.95) 0%,rgba(6,7,18,0) 45%)"></div>
{status(extra='<div class="tabs" style="margin-left:34px"><b>Spiele</b><span>Apps</span><span>Medien</span></div>')}
<div style="position:absolute;top:92px;left:40px;font-size:15px;color:var(--ink2);font-weight:500">Orbitfall</div>
<div style="position:absolute;top:122px;left:40px;display:flex;gap:18px;align-items:center">{row}</div>
<div style="position:absolute;top:278px;left:40px;width:560px">
  <div class="lbl">Weiterspielen</div>
  <div style="font-size:48px;font-weight:700;letter-spacing:-.01em;margin:6px 0 4px">Orbitfall</div>
  <div style="color:var(--ink2);font-size:17px;line-height:1.5">Kapitel 3 · Der Ring um Teria. Zuletzt gespielt vor 2 Stunden.</div>
  <div style="display:flex;align-items:center;gap:12px;margin-top:10px"><div style="width:220px;height:6px;border-radius:6px;background:rgba(255,255,255,.15)"><div style="width:42%;height:100%;border-radius:6px;background:var(--teal)"></div></div><span style="color:var(--ink2);font-size:14px">42 %</span></div>
  <div style="display:flex;gap:12px;margin-top:18px"><span class="cta">{ic("play",18)} Spielen</span><span class="ghost">{ic("dots",20)}</span></div>
</div>
<div style="position:absolute;left:40px;right:40px;bottom:62px;display:flex;gap:16px;align-items:flex-end">
 <div style="flex:none"><div class="lbl" style="margin-bottom:10px">Zuletzt verwendet</div><div style="display:flex;gap:14px">
  {''.join(f'<div style="width:170px"><div style="height:92px;border-radius:14px;background:url(art/{i}) center/cover;box-shadow:0 8px 24px rgba(0,0,0,.4)"></div><div style="font-size:14px;margin-top:8px;color:var(--ink2)">{n}</div></div>' for n,i in [('Code-Studio','t-code.jpg'),('Pixelgarten','t-pixel.jpg'),('Wellen · Musik','t-wellen.jpg')])}
 </div></div>
 <div class="sp" style="flex:1"></div>
 <div class="card" style="width:330px;padding:18px 20px;display:flex;gap:14px;align-items:center"><div class="appicon" style="width:52px;height:52px;border-radius:14px;background:linear-gradient(135deg,#3ee0c5,#1f8f9c)">{ic("refresh",24)}</div><div><div style="font-weight:500">Teria 0.3.0 ist bereit</div><div style="color:var(--ink2);font-size:13px;margin-top:2px">Neues Design, Einrichtungsassistent</div></div></div>
</div>
{hints(("A","Starten"),("B","Zurück"),("+","Optionen"),("⌂","Schnellmenü"))}'''

# 2 Schnellmenü
def qt(icn,t,sub,on):
    return f'<div class="card" style="padding:16px;display:flex;flex-direction:column;gap:14px;{"background:rgba(62,224,197,.16);border-color:rgba(62,224,197,.45)" if on else ""}"><div style="display:flex;justify-content:space-between;align-items:center"><span style="color:{"var(--teal)" if on else "var(--ink2)"}">{ic(icn,24)}</span><span class="tog{" on" if on else ""}"></span></div><div><div style="font-weight:500">{t}</div><div style="color:var(--ink2);font-size:13px;margin-top:2px">{sub}</div></div></div>'
def slider(icn,t,v):
    return f'<div style="display:flex;align-items:center;gap:14px"><span style="color:var(--ink2)">{ic(icn,22)}</span><div style="flex:1"><div style="display:flex;justify-content:space-between;font-size:14px;margin-bottom:8px"><span>{t}</span><span style="color:var(--ink2)">{v} %</span></div><div style="height:8px;border-radius:8px;background:rgba(255,255,255,.12)"><div style="width:{v}%;height:100%;border-radius:8px;background:linear-gradient(90deg,var(--teal2),var(--teal))"></div></div></div></div>'
quick=f'''<div class="bg" style="background-image:url(art/home.jpg);filter:blur(6px) brightness(.45);transform:scale(1.04)"></div>
{status()}
<div style="position:absolute;left:40px;right:40px;bottom:66px;display:grid;grid-template-columns:1.25fr 1fr;gap:18px">
 <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
  {qt("wifi","WLAN","Heimnetz · 5 GHz",True)}{qt("bt","Bluetooth","2 Joy-Cons verbunden",True)}{qt("moon","Nicht stören","Aus",False)}
  {qt("tv","Dock-Modus","Automatisch 1080p",True)}{qt("shield","eMMC-Schutz","Geschützt",True)}{qt("bolt","Ladegrenze","85 %",True)}
 </div>
 <div class="card" style="padding:22px;display:flex;flex-direction:column;gap:20px">
  <div class="lbl">Leistung</div>
  <div style="display:flex;gap:8px"><span class="chip">Eco</span><span class="chip on">Ausgewogen</span><span class="chip">Max</span><span style="flex:1"></span><span style="color:var(--ink2);font-size:13px;align-self:center">CPU 47 °C</span></div>
  {slider("sun","Helligkeit",64)}{slider("vol","Lautstärke",40)}
  <div style="display:flex;gap:10px;margin-top:2px"><span class="chip">{ic("reboot",16)} Neustart in Hekate</span><span class="chip">{ic("moon",16)} Ruhezustand</span><span class="chip">{ic("power",16)} Aus</span></div>
 </div>
</div>
<div style="position:absolute;left:40px;top:96px;display:flex;align-items:flex-end;gap:26px">
 <div><div class="lbl">Schnellmenü</div><div style="font-size:44px;font-weight:700;margin-top:6px">Samstag, 21. November</div></div>
</div>
<div class="card" style="position:absolute;right:40px;top:96px;width:330px;padding:18px 20px;display:flex;flex-direction:column;gap:12px">
 <div style="display:flex;justify-content:space-between"><span class="lbl">Akku</span><span style="color:var(--teal);font-size:13px">lädt · 5,2 W</span></div>
 <div style="display:flex;align-items:baseline;gap:8px"><span style="font-size:40px;font-weight:700">78 %</span><span style="color:var(--ink2);font-size:14px">voll in 52 min</span></div>
 <div style="display:flex;gap:10px">{''.join(f'<div style="flex:1;padding:10px;border-radius:12px;background:rgba(255,255,255,.06);font-size:13px"><div style="color:var(--ink2)">{a}</div><div style="margin-top:4px;font-weight:500">{b}</div></div>' for a,b in [('Joy-Con L','Hoch'),('Joy-Con R','Niedrig'),('Zyklen','140')])}</div>
</div>
{hints(("B","Schließen"),("⌂","Startbildschirm"))}'''

# 3 Bibliothek
lib_items=[('Orbitfall','t-orbit.jpg','Spiel','2,1 GB'),('Sternenläufer','t-sterne.jpg','Spiel','860 MB'),('Pixelgarten','t-pixel.jpg','Spiel','420 MB'),('Abendrot','t-berg.jpg','Spiel','1,4 GB'),('Code-Studio','t-code.jpg','Entwicklung','812 MB'),
           ('Wellen','t-wellen.jpg','Musik','96 MB'),('Raster','t-raster.jpg','Werkzeug','38 MB'),('Kino','t-film.jpg','Medien','140 MB'),('Terminal','', 'System','integriert'),('Browser','','Internet','260 MB')]
cells=''
for i,(n,img,cat,sz) in enumerate(lib_items):
    bgc=f'background:url(art/{img}) center/cover' if img else ('background:linear-gradient(135deg,#2b2f45,#151829)' if n=='Terminal' else 'background:linear-gradient(135deg,#ff8a3d,#e5484d)')
    inner='' if img else f'<div style="position:absolute;inset:0;display:grid;place-items:center">{ic("term" if n=="Terminal" else "globe",44)}</div>'
    cells+=f'<div><div class="{"focus" if i==4 else ""}" style="position:relative;height:118px;border-radius:14px;{bgc};box-shadow:0 8px 24px rgba(0,0,0,.35)">{inner}</div><div style="display:flex;justify-content:space-between;margin-top:9px;font-size:14px"><span style="font-weight:500">{n}</span><span style="color:var(--ink3)">{sz}</span></div><div style="color:var(--ink2);font-size:12px;margin-top:2px">{cat}</div></div>'
nav=''.join(f'<div style="display:flex;align-items:center;gap:12px;padding:11px 14px;border-radius:12px;{"background:rgba(255,255,255,.10);color:var(--ink)" if a else "color:var(--ink2)"}">{ic(i,20)}{t}</div>' for i,t,a in [('home','Start',False),('grid','Bibliothek',True),('bag','Store',False),('down','Downloads',False),('gear','Einstellungen',False)])
library=f'''<div class="bg" style="background:radial-gradient(900px 500px at 85% -10%,rgba(62,224,197,.18),transparent 60%),radial-gradient(700px 500px at 10% 110%,rgba(255,138,61,.12),transparent 60%),#0b0d1d"></div>
{status()}
<div style="position:absolute;top:86px;left:24px;width:210px;display:flex;flex-direction:column;gap:4px;font-size:16px">{nav}
 <div class="card" style="margin-top:18px;padding:14px;font-size:13px;color:var(--ink2)"><div style="display:flex;justify-content:space-between;color:var(--ink)"><span>Speicher</span><span>54 GB frei</span></div><div style="height:6px;border-radius:6px;background:rgba(255,255,255,.12);margin-top:10px"><div style="width:22%;height:100%;border-radius:6px;background:var(--teal)"></div></div><div style="margin-top:8px">SD-Karte · 64 GB</div></div>
</div>
<div style="position:absolute;top:86px;left:262px;right:40px">
 <div style="display:flex;align-items:center;gap:14px"><div style="font-size:34px;font-weight:700">Bibliothek</div><span style="color:var(--ink3);font-size:16px;margin-top:6px">24 Einträge</span><span style="flex:1"></span><span class="chip">{ic("search",16)} Suchen</span></div>
 <div style="display:flex;gap:10px;margin:18px 0 22px"><span class="chip on">Alle</span><span class="chip">Spiele</span><span class="chip">Entwicklung</span><span class="chip">Medien</span><span class="chip">System</span><span style="flex:1"></span><span class="chip">Zuletzt gespielt ▾</span></div>
 <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:22px 18px">{cells}</div>
</div>
{hints(("A","Öffnen"),("X","Sortieren"),("Y","Suchen"),("B","Zurück"))}'''

# 4 Store
shots=''.join(f'<div style="width:220px;height:124px;border-radius:12px;background:url(art/{i}) center/cover;box-shadow:0 6px 20px rgba(0,0,0,.35)"></div>' for i in ['t-code.jpg','t-raster.jpg','t-wellen.jpg'])
store=f'''<div class="bg" style="background-image:url(art/b-code.jpg);filter:blur(18px) saturate(1.3);transform:scale(1.1)"></div>
<div class="shade" style="background:linear-gradient(0deg,#0b0d1d 40%,rgba(11,13,29,.55) 75%,rgba(11,13,29,.25))"></div>
{status(extra='<div class="tabs" style="margin-left:34px"><span>Entdecken</span><b>Apps</b><span>Spiele</span><span>Updates</span></div>')}
<div style="position:absolute;left:40px;top:190px;display:flex;gap:26px;align-items:flex-end">
 <div class="appicon" style="width:132px;height:132px;border-radius:30px;background:linear-gradient(135deg,#1d2343,#3b4fb0)">{ic("code",62)}</div>
 <div><div class="lbl">Entwicklung · Flatpak</div><div style="font-size:52px;font-weight:700;margin:6px 0 4px">Code-Studio</div>
  <div style="display:flex;gap:16px;color:var(--ink2);font-size:15px;align-items:center"><span style="color:var(--amber);display:flex;gap:2px">{ic("star",16)*4}{ic("star",16,"dim")}</span><span>4,6 · 2 318 Bewertungen</span><span>·</span><span>Version 2025.3</span></div></div>
</div>
<div style="position:absolute;left:40px;top:372px;width:700px">
 <div style="display:flex;gap:12px;align-items:center"><span class="cta" style="background:var(--teal);color:#04201b">{ic("down",18)} Installieren · 812 MB</span><span class="ghost">{ic("dots",20)}</span><span style="color:var(--ink2);font-size:14px;margin-left:8px">Läuft auf arm64 · Touch &amp; Controller</span></div>
 <p style="color:var(--ink2);font-size:16px;line-height:1.55;margin:22px 0 18px;max-width:620px">Eine vollwertige Entwicklungsumgebung für Java, Kotlin und Web. Optimiert für den Dock-Modus mit Tastatur, im Handheld mit Bildschirmtastatur bedienbar.</p>
 <div class="lbl" style="margin-bottom:10px">Bildschirmfotos</div><div style="display:flex;gap:14px">{shots}</div>
</div>
<div class="card" style="position:absolute;right:40px;top:372px;width:380px;padding:20px 22px;font-size:14px">
 {''.join(f'<div style="display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--line)"><span style="color:var(--ink2)">{a}</span><span>{b}</span></div>' for a,b in [('Quelle','Flathub'),('Größe','812 MB'),('Benötigt','2 GB RAM empfohlen'),('Steuerung','Tastatur, Touch, Joy-Con'),('Berechtigungen','Dateien, Netzwerk')])}
 <div style="display:flex;gap:10px;align-items:center;margin-top:14px;color:var(--teal)">{ic("shield",18)}<span>Geprüft, kein Zugriff auf den eMMC</span></div>
</div>
{hints(("A","Installieren"),("R","Nächster Tab"),("B","Zurück"))}'''

# 5 Einstellungen
setnav=''.join(f'<div style="display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:12px;{"background:rgba(62,224,197,.14);color:var(--ink);box-shadow:inset 3px 0 0 var(--teal)" if a else "color:var(--ink2)"}">{ic(i,19)}{t}</div>' for i,t,a in [('desk','Anzeige',False),('wifi','Netzwerk',False),('bt','Bluetooth',False),('pad','Controller',False),('bolt','Energie & Leistung',True),('disk','Speicher',False),('shield','Sicherheit',False),('refresh','Updates',False),('user','Benutzer',False),('info','Über Teria',False)])
def row(t,sub,right): return f'<div style="display:flex;align-items:center;gap:16px;padding:16px 0;border-bottom:1px solid var(--line)"><div style="flex:1"><div style="font-size:16px">{t}</div><div style="color:var(--ink2);font-size:13px;margin-top:3px">{sub}</div></div>{right}</div>'
seg='<div style="display:flex;padding:4px;border-radius:14px;background:rgba(255,255,255,.07);gap:4px">'+''.join(f'<div style="flex:1;padding:12px 10px;border-radius:10px;text-align:center;{"background:var(--ink);color:#0a0d1c" if a else "color:var(--ink2)"}"><div style="font-weight:500">{t}</div><div style="font-size:12px;opacity:.75;margin-top:2px">{s}</div></div>' for t,s,a in [('Eco','bis 9 h · 1,0 GHz',False),('Ausgewogen','bis 6 h · 1,4 GHz',True),('Max','Dock · 1,9 GHz',False)])+'</div>'
settings=f'''<div class="bg" style="background:radial-gradient(900px 600px at 100% 0%,rgba(62,224,197,.10),transparent 60%),#0b0d1d"></div>
{status()}
<div style="position:absolute;top:86px;left:24px;width:250px;display:flex;flex-direction:column;gap:2px;font-size:15px"><div style="font-size:30px;font-weight:700;padding:0 14px 14px">Einstellungen</div>{setnav}</div>
<div style="position:absolute;top:92px;left:310px;right:40px;bottom:60px;display:grid;grid-template-columns:1fr 330px;gap:26px">
 <div>
  <div style="font-size:24px;font-weight:500;margin-bottom:16px">Energie &amp; Leistung</div>
  {seg}
  {row("Im Dock automatisch Max","Wechselt beim Andocken auf volle Leistung",'<span class="tog on"></span>')}
  {row("Ladegrenze 85 %","Schont den Akku, wenn die Switch oft am Strom hängt",'<span class="tog on"></span>')}
  {row("Bildschirm aus nach","Im Akkubetrieb",'<span class="chip">2 Minuten ▾</span>')}
  {row("Ruhezustand nach","Downloads laufen weiter",'<span class="chip">10 Minuten ▾</span>')}
  {row("Lüfter","Leise bis 60 °C, dann schneller",'<span class="chip">Automatisch ▾</span>')}
  {row("Neustart-Ziel","Wohin „Neu starten“ führt",'<span class="chip">Teria ▾</span>')}
 </div>
 <div style="display:flex;flex-direction:column;gap:16px">
  <div class="card" style="padding:20px"><div class="lbl">Jetzt</div>
   <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px">{''.join(f'<div><div style="color:var(--ink2);font-size:12px">{a}</div><div style="font-size:24px;font-weight:700;margin-top:2px">{b}</div></div>' for a,b in [('Akku','78 %'),('Leistung','5,2 W'),('CPU','47 °C'),('GPU','48 °C')])}</div>
   <svg viewBox="0 0 290 60" width="100%" height="60" style="margin-top:14px"><path d="M0 44 L20 40 L40 42 L60 30 L80 34 L100 22 L120 26 L140 18 L160 24 L180 20 L200 28 L220 16 L240 22 L260 14 L290 18 L290 60 L0 60Z" fill="rgba(62,224,197,.15)"/><path d="M0 44 L20 40 L40 42 L60 30 L80 34 L100 22 L120 26 L140 18 L160 24 L180 20 L200 28 L220 16 L240 22 L260 14 L290 18" fill="none" stroke="#3ee0c5" stroke-width="2"/><circle cx="290" cy="18" r="3.5" fill="#3ee0c5"/></svg>
   <div style="color:var(--ink3);font-size:12px">Leistungsaufnahme, letzte 30 Minuten</div></div>
  <div class="card" style="padding:18px 20px;display:flex;gap:14px;align-items:center"><span style="color:var(--teal)">{ic("shield",28)}</span><div><div style="font-weight:500">eMMC geschützt</div><div style="color:var(--ink2);font-size:13px;margin-top:2px">Teria schreibt nie auf den internen Speicher.</div></div></div>
 </div>
</div>
{hints(("A","Auswählen"),("B","Zurück"))}'''

# 6 Login
users=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:14px;opacity:{o}"><div class="{"focus" if f else ""}" style="width:{s}px;height:{s}px;border-radius:50%;display:grid;place-items:center;background:{bg};font-size:{s//3}px;font-weight:700;color:#071018">{t}</div><div style="font-size:{18 if f else 15}px;font-weight:{500 if f else 400}">{n}</div></div>' for n,t,bg,s,f,o in [('Gast',ic("user",34),'rgba(255,255,255,.14)',96,False,.7),('daniel','D','linear-gradient(135deg,#3ee0c5,#3b6fd8)',140,True,1),('Neu',ic("plus",34),'rgba(255,255,255,.14)',96,False,.7)])
login=f'''<div class="bg" style="background-image:url(art/login.jpg)"></div>
<div style="position:absolute;top:22px;right:40px;display:flex;gap:16px;align-items:center;color:var(--ink2);z-index:5">{ic("wifi",18)}<span class="pill">{ic("bat",18)} 78 %</span></div>
<div style="position:absolute;top:90px;left:0;right:0;text-align:center"><div style="font-size:120px;font-weight:300;letter-spacing:-.02em;line-height:1">14:32</div><div style="font-size:22px;color:var(--ink2);margin-top:8px">Samstag, 21. November</div></div>
<div style="position:absolute;top:380px;left:0;right:0;display:flex;justify-content:center;align-items:flex-end;gap:56px">{users}</div>
<div style="position:absolute;bottom:56px;left:0;right:0;text-align:center;color:var(--ink2);font-size:16px;display:flex;justify-content:center;gap:10px;align-items:center"><i class="btn">A</i> Anmelden</div>
<div style="position:absolute;bottom:24px;left:40px;display:flex;align-items:center;gap:10px;color:var(--ink3);font-size:13px"><svg width="22" height="22" viewBox="0 0 24 24"><circle cx="12" cy="12" r="6" fill="#3ee0c5"/><ellipse cx="12" cy="12" rx="11" ry="3.2" fill="none" stroke="#eef1f8" stroke-width="1.4"/></svg>Teria 0.3</div>'''

# 7 Desktop-Modus
WIN=''.join(f'<i style="width:12px;height:12px;border-radius:50%;background:{c};display:block"></i>' for c in ['#444a66','#444a66','#ff8a3d'])
DOT='<i style="position:absolute;left:-9px;top:21px;width:4px;height:10px;border-radius:3px;background:var(--teal)"></i>'
dock=''.join(f'<div style="position:relative;width:52px;height:52px;border-radius:14px;display:grid;place-items:center;background:{g};color:#fff">{ic(i,26)}{DOT if a else ""}</div>' for i,g,a in [('globe','linear-gradient(135deg,#ff8a3d,#e5484d)',False),('folder','linear-gradient(135deg,#4d7cfe,#2f4cc0)',True),('term','linear-gradient(135deg,#2b2f45,#151829)',True),('code','linear-gradient(135deg,#1d2343,#3b4fb0)',False),('bag','linear-gradient(135deg,#3ee0c5,#1f8f9c)',False),('gear','linear-gradient(135deg,#5b6280,#353a52)',False)])
files=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;width:88px;font-size:12px;color:var(--ink2)"><span style="color:{c}">{ic("folder",46)}</span>{n}</div>' for n,c in [('Dokumente','#4d7cfe'),('Downloads','#3ee0c5'),('Bilder','#ff8a3d'),('Musik','#8a5cf6'),('Projekte','#4d7cfe'),('teria','#3ee0c5')])
desktop=f'''<div class="bg" style="background-image:url(art/home.jpg);filter:saturate(1.1)"></div>
<div style="position:absolute;inset:0 0 auto;height:30px;background:rgba(6,7,16,.85);display:flex;align-items:center;padding:0 16px;font-size:13px;gap:16px;z-index:5"><b style="font-weight:500">Aktivitäten</b><span style="flex:1;text-align:center;font-weight:500">Sa 21. Nov 14:32</span><span style="display:flex;gap:12px;color:var(--ink2);align-items:center">{ic("wifi",15)}{ic("vol",15)}{ic("bat",15)} 78 %{ic("power",15)}</span></div>
<div style="position:absolute;top:30px;left:0;bottom:0;width:76px;background:rgba(8,9,20,.78);display:flex;flex-direction:column;align-items:center;gap:12px;padding-top:14px">{dock}<div style="flex:1"></div><div style="width:52px;height:52px;display:grid;place-items:center;color:var(--ink2);margin-bottom:12px">{ic("grid",26)}</div></div>
<div style="position:absolute;left:120px;top:70px;width:620px;height:400px;border-radius:12px;background:#15172a;box-shadow:0 20px 60px rgba(0,0,0,.55);overflow:hidden;border:1px solid var(--line)">
 <div style="height:46px;display:flex;align-items:center;gap:12px;padding:0 14px;background:#1c1f36;border-bottom:1px solid var(--line);font-size:14px"><span style="color:var(--ink2)">‹ ›</span><span class="chip" style="height:28px">/home/teria</span><span style="flex:1"></span><span style="display:flex;gap:8px">{WIN}</span></div>
 <div style="display:flex;height:100%"><div style="width:150px;padding:14px;font-size:13px;color:var(--ink2);display:flex;flex-direction:column;gap:10px;border-right:1px solid var(--line)"><span style="color:var(--ink)">Persönlicher Ordner</span><span>Zuletzt</span><span>Favoriten</span><span>SD-Karte</span><span>USB-Stick</span></div>
 <div style="flex:1;padding:22px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px;align-content:start">{files}</div></div>
</div>
<div style="position:absolute;left:560px;top:250px;width:660px;height:410px;border-radius:12px;background:rgba(14,15,28,.97);box-shadow:0 24px 70px rgba(0,0,0,.6);overflow:hidden;border:1px solid var(--line)">
 <div style="height:40px;display:flex;align-items:center;justify-content:center;background:#1c1f36;font-size:13px;color:var(--ink2);position:relative">teria@teria: ~<span style="position:absolute;right:14px;top:14px;display:flex;gap:8px">{WIN}</span></div>
<pre style="margin:0;padding:14px 18px;font:15px/1.42 var(--m);color:#cfd5e6"><span style="color:#3ee0c5">teria@teria</span>:<span style="color:#7aa2ff">~</span>$ teria info
<span style="color:#6f7694">System:</span>    Teria 0.3.0 (Debian GNU/Linux 13, Switchroot L4T)
<span style="color:#6f7694">Gerät:</span>     Nintendo Switch (2017) · Kernel 4.9.140-l4t
<span style="color:#6f7694">L4T:</span>       R32.3.1 · Leistung: Ausgewogen
<span style="color:#6f7694">eMMC:</span>      <span style="color:#3ee0c5">geschützt</span>
<span style="color:#6f7694">Akku:</span>      78 % (lädt) · 140 Zyklen · 99 %
<span style="color:#6f7694">CPU/GPU:</span>   47 °C / 48 °C
<span style="color:#6f7694">Speicher:</span>  54 GB von 63 GB frei

<span style="color:#3ee0c5">teria@teria</span>:<span style="color:#7aa2ff">~</span>$ teria perf max
Leistungsprofil: <b style="color:#ff8a3d">Max</b> (Dock erkannt)
<span style="color:#3ee0c5">teria@teria</span>:<span style="color:#7aa2ff">~</span>$ ▌</pre>
</div>'''

SCREENS=[('1-start',home),('2-schnellmenue',quick),('3-bibliothek',library),('4-store',store),('5-einstellungen',settings),('6-anmeldung',login),('7-desktop-modus',desktop)]
for n,b in SCREENS:
    open(f'{n}.html','w').write(page(b,'.dim{opacity:.35}'))
print('ok')
