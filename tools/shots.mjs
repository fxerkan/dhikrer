// Captures Play Store screenshots of the app, PER LANGUAGE, via headless Chrome.
// Self-contained: regenerates the shot.html capture page from the built app.html
// (app.html + a synchronous state-injector), starts a static server on :8790,
// then renders each config in every language.
//
//   node tools/shots.mjs            # capture the 6 hero screens × [tr,en,ar]
//   node tools/shots.mjs all        # capture all 15 gallery screens × langs
//   node tools/shots.mjs <substr>   # only configs whose name includes <substr>
//
// Output → store/<lang>/_raw/<name>.png  (unframed; frame.py wraps them next).
import { execFile } from 'child_process';
import http from 'http';
import fs from 'fs';
import os from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const ASSETS = path.join(ROOT, 'android/app/src/main/assets/app');
const STATE_DIR = path.join(ASSETS, '_shots');
const LANGS = ['tr', 'en', 'ar'];

// Default dhikr NAMES are user content, not UI strings — so the app never
// translates them. Localize them here so each language's screenshots read native.
const NAMES = {
  100: { tr: 'Sübhânallah', en: 'Subhanallah', ar: 'سبحان الله' },
  1: { tr: 'Elhamdülillah', en: 'Alhamdulillah', ar: 'الحمد لله' },
  2: { tr: 'Allâhu Ekber', en: 'Allahu Akbar', ar: 'الله أكبر' },
  3: { tr: 'Estağfirullah', en: 'Astaghfirullah', ar: 'أستغفر الله' },
  4: { tr: 'Lâ ilâhe illallah', en: 'La ilaha illallah', ar: 'لا إله إلا الله' },
  5: { tr: 'Lâ havle', en: 'La hawla', ar: 'لا حول ولا قوة إلا بالله' },
};
const nm = (id, lang) => (NAMES[id] ? NAMES[id][lang] : undefined);

const mkZikirs = (lang) => [
  { id: 100, name: nm(100, lang), target: 99, count: 47, cat: 'daily', sound: 'soft', vib: { on: true, style: 'kisa', str: 'orta' }, pinned: true },
  { id: 1, name: nm(1, lang), target: 33, count: 22, cat: 'daily', sound: 'drop', vib: { on: true, style: 'cift', str: 'orta' } },
  { id: 2, name: nm(2, lang), target: 0, count: 128, cat: 'daily', sound: 'beads', vib: { on: true, style: 'kisa', str: 'orta' } },
  { id: 3, name: nm(3, lang), target: 100, count: 64, cat: 'prayer', sound: 'soft', vib: { on: true, style: 'kisa', str: 'hafif' } },
  { id: 4, name: nm(4, lang), target: 1000, count: 342, cat: 'custom', sound: 'soft', vib: { on: true, style: 'uzun', str: 'guclu' } },
  { id: 5, name: nm(5, lang), target: 66, count: 44, cat: 'prayer', sound: 'beads', vib: { on: true, style: 'kisa', str: 'orta' } },
];
// Logs MUST be anchored to the real current time — the app computes "today" with
// Date.now() at render, so fixed timestamps fall outside the heatmap window.
const now = Date.now();
const base0 = now - (now % 86400000);
// HEAVY dataset — a power user: dense heatmap, long streak, tall bars.
const heavyLogs = [];
for (let d = 0; d < 189; d++) {
  const seed = (((d + 1) * 2654435761) >>> 0);
  const n = (12 + (seed % 44)) + (d < 7 ? 55 : 0) + (d === 0 ? 130 : 0);
  const ids = [100, 1, 2, 3, 4];
  for (let i = 0; i < n; i++) {
    const off = (((seed * (i + 7)) >>> 0) % 86399000);
    heavyLogs.push([base0 - d * 86400000 + off, ids[i % 5]]);
  }
}
const mkHeavyZikirs = (lang) => [
  { id: 100, name: nm(100, lang), target: 99, count: 12874, cat: 'daily', sound: 'soft', vib: { on: true }, pinned: true },
  { id: 1, name: nm(1, lang), target: 33, count: 9241, cat: 'daily', sound: 'drop', vib: { on: true } },
  { id: 2, name: nm(2, lang), target: 0, count: 8560, cat: 'daily', sound: 'beads', vib: { on: true } },
  { id: 3, name: nm(3, lang), target: 100, count: 11020, cat: 'prayer', sound: 'soft', vib: { on: true } },
  { id: 4, name: nm(4, lang), target: 1000, count: 6813, cat: 'custom', sound: 'soft', vib: { on: true } },
];
const reminders = [
  { id: 1, time: '05:45', label: 'Sabah', on: true }, { id: 2, time: '13:30', label: 'Öğle', on: true }, { id: 3, time: '21:00', label: 'Yatsı', on: false }];

// name, extra-state. `lang` is set by the capture loop, not here.
const configs = [
  ['01-sayac-klasik-gece', { theme: 'nocturne', tab: 'sayac', design: 'klasik' }],
  ['02-tespih-zumrut', { theme: 'zumrut', tab: 'sayac', design: 'tespih', activeId: 5 }],
  ['03-birlesik-gul', { theme: 'gul', tab: 'sayac', design: 'birlesik' }],
  ['04-kilit-kehribar', { theme: 'kehribar', tab: 'sayac', design: 'klasik', layout: 'center', locked: true }],
  ['05-sayac-kare-buz', { theme: 'buz', tab: 'sayac', design: 'klasik', counterShape: 'square' }],
  ['06-zikirler-gece', { theme: 'nocturne', tab: 'kutup' }],
  ['07-istatistik-okyanus', { theme: 'okyanus', tab: 'stat', statRange: 'weekly', heavy: true }],
  ['08-ayarlar-lavanta', { theme: 'lavanta', tab: 'ayar' }],
  ['09-tespih-yakut-33', { theme: 'yakut', tab: 'sayac', design: 'tespih', activeId: 1 }],
  ['10-modern-klasik', { theme: 'modernist', tab: 'sayac', design: 'klasik' }],
  ['11-sayac-dalga-okyanus', { theme: 'okyanus', tab: 'sayac', design: 'klasik', effect: 'wave' }],
  ['12-istatistik-gece-gunluk', { theme: 'nocturne', tab: 'stat', statRange: 'daily', heavy: true }],
  ['13-zikirler-zumrut', { theme: 'zumrut', tab: 'kutup' }],
  ['14-ayarlar-gece', { theme: 'nocturne', tab: 'ayar' }],
  ['15-tespih-gul-33', { theme: 'gul', tab: 'sayac', design: 'tespih', activeId: 1 }],
];
// The 6 screens the hero set composites — the default capture set.
const HERO_SCREENS = ['01-sayac-klasik-gece', '02-tespih-zumrut', '03-birlesik-gul',
  '06-zikirler-gece', '07-istatistik-okyanus', '08-ayarlar-lavanta'];

function buildState(extra, lang) {
  const heavy = extra.heavy;
  const s = {
    zikirs: heavy ? mkHeavyZikirs(lang) : mkZikirs(lang),
    activeId: 100, lang, showRemaining: true, haptic: true, sound: true, reminders,
  };
  if (heavy) s.logs = heavyLogs;
  Object.assign(s, extra);
  delete s.heavy;
  return s;
}

// --- regenerate shot.html = built app.html + synchronous state injector ---
function writeShotHtml() {
  const html = fs.readFileSync(path.join(ASSETS, 'app.html'), 'utf8');
  const inj = '<script>try{var st=new URLSearchParams(location.search).get("st");'
    + 'if(st){var x=new XMLHttpRequest();x.open("GET","_shots/"+st+".json",false);'
    + 'x.send();if(x.status<400)localStorage.setItem("zikirci-v1",x.responseText);}}catch(e){}</script>\n';
  fs.writeFileSync(path.join(ASSETS, 'shot.html'), html.replace('<head>', '<head>\n' + inj, 1));
}

// --- tiny static file server rooted at ASSETS (state JSONs would 414 as URLs) ---
function serve(port) {
  const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.png': 'image/png', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.svg': 'image/svg+xml' };
  const srv = http.createServer((req, res) => {
    const p = path.join(ASSETS, decodeURIComponent(req.url.split('?')[0]));
    fs.readFile(p, (err, data) => {
      if (err) { res.writeHead(404); res.end(); return; }
      res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' });
      res.end(data);
    });
  });
  return new Promise((r) => srv.listen(port, () => r(srv)));
}

// Chrome runs ASYNC (execFile, not the *Sync variant): the in-process HTTP
// server above must stay responsive to serve the page while Chrome loads it —
// a synchronous spawn would block Node's event loop and deadlock the capture.
function capture(args) {
  return new Promise((resolve, reject) => {
    execFile(CHROME, args, { timeout: 30000 }, (err) => (err ? reject(err) : resolve()));
  });
}

async function main() {
  const arg = process.argv[2];
  const all = arg === 'all';
  const filter = all ? null : arg;
  const wanted = configs.filter(([name]) =>
    filter ? name.includes(filter) : (all || HERO_SCREENS.includes(name)));

  fs.mkdirSync(STATE_DIR, { recursive: true });
  writeShotHtml();
  const srv = await serve(8790);

  for (const lang of LANGS) {
    const out = path.join(ROOT, 'store', lang, '_raw');
    fs.mkdirSync(out, { recursive: true });
    for (const [name, extra] of wanted) {
      const key = `${lang}-${name}`;
      fs.writeFileSync(path.join(STATE_DIR, `${key}.json`), JSON.stringify(buildState(extra, lang)), 'utf8');
      const file = path.join(out, `${name}.png`);
      // Each invocation needs its own --user-data-dir, else headless Chrome
      // singleton-locks on the shared default profile and hangs.
      const udd = fs.mkdtempSync(path.join(os.tmpdir(), 'zk-shot-'));
      // headless Chrome enforces a ~500px min width; 540px CSS renders uncut. scale 2.5.
      await capture([
        '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
        '--no-first-run', '--no-default-browser-check', `--user-data-dir=${udd}`,
        '--force-device-scale-factor=2.5', '--window-size=540,1170',
        '--virtual-time-budget=6000', `--screenshot=${file}`,
        `http://localhost:8790/shot.html?st=${key}`,
      ]);
      fs.rmSync(udd, { recursive: true, force: true });
      console.log(`  ${lang}/${name}.png  ${Math.round(fs.statSync(file).size / 1024)}K`);
    }
  }
  srv.close();
  // shot.html + _shots are capture-only scaffolding living inside the packaged
  // assets dir — remove them so they never bloat or ship in the APK.
  fs.rmSync(path.join(ASSETS, 'shot.html'), { force: true });
  fs.rmSync(STATE_DIR, { recursive: true, force: true });
  console.log('done →', path.join(ROOT, 'store', '<lang>', '_raw'));
}

main();
