// Captures Play Store screenshots of the app in many states via headless Chrome.
// Serves must be running on :8790 (shot.html). Output → store-screenshots/.
import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const OUT = path.resolve('store-screenshots');
fs.mkdirSync(OUT, { recursive: true });

// shared library of dhikrs (varied progress) + seeded activity logs for stats
const zikirs = [
  { id: 100, name: 'Sübhânallah', target: 99, count: 47, cat: 'daily', sound: 'soft', vib: { on: true, style: 'kisa', str: 'orta' }, pinned: true },
  { id: 1, name: 'Elhamdülillah', target: 33, count: 22, cat: 'daily', sound: 'drop', vib: { on: true, style: 'cift', str: 'orta' } },
  { id: 2, name: 'Allâhu Ekber', target: 0, count: 128, cat: 'daily', sound: 'beads', vib: { on: true, style: 'kisa', str: 'orta' } },
  { id: 3, name: 'Estağfirullah', target: 100, count: 64, cat: 'prayer', sound: 'soft', vib: { on: true, style: 'kisa', str: 'hafif' } },
  { id: 4, name: 'Lâ ilâhe illallah', target: 1000, count: 342, cat: 'custom', sound: 'soft', vib: { on: true, style: 'uzun', str: 'guclu' } },
  { id: 5, name: 'Lâ havle', target: 66, count: 44, cat: 'prayer', sound: 'beads', vib: { on: true, style: 'kisa', str: 'orta' } },
];
// Logs MUST be anchored to the real current time — the app computes "today" with
// Date.now() at render, so fixed timestamps fall outside the heatmap window.
const now = Date.now();
const base0 = now - (now % 86400000);
// light logs (a couple of active days) for the non-heavy states
const logs = [];
for (let d = 0; d < 120; d++) {
  const n = 6 + ((d * 7) % 34);
  for (let i = 0; i < n; i++) logs.push([now - d * 86400000 - (i * 137000 % 80000000), (i % 5) + 1]);
}
// HEAVY dataset — a power user with tens of thousands of dhikrs: dense heatmap
// (every day of the last 27 weeks, varied intensity), long streak, tall bars.
// today gets a full spread across hours; recent week is boosted.
const heavyLogs = [];
for (let d = 0; d < 189; d++) {
  const seed = (((d + 1) * 2654435761) >>> 0);
  const n = (12 + (seed % 44)) + (d < 7 ? 55 : 0) + (d === 0 ? 130 : 0);
  const ids = [100, 1, 2, 3, 4]; // real dhikr ids so the distribution donut is realistic
  for (let i = 0; i < n; i++) {
    const off = (((seed * (i + 7)) >>> 0) % 86399000);
    heavyLogs.push([base0 - d * 86400000 + off, ids[i % 5]]);
  }
}
const heavyZikirs = [
  { id: 100, name: 'Sübhânallah', target: 99, count: 12874, cat: 'daily', sound: 'soft', vib: { on: true }, pinned: true },
  { id: 1, name: 'Elhamdülillah', target: 33, count: 9241, cat: 'daily', sound: 'drop', vib: { on: true } },
  { id: 2, name: 'Allâhu Ekber', target: 0, count: 8560, cat: 'daily', sound: 'beads', vib: { on: true } },
  { id: 3, name: 'Estağfirullah', target: 100, count: 11020, cat: 'prayer', sound: 'soft', vib: { on: true } },
  { id: 4, name: 'Lâ ilâhe illallah', target: 1000, count: 6813, cat: 'custom', sound: 'soft', vib: { on: true } },
];
const base = { zikirs, activeId: 100, lang: 'tr', showRemaining: true, haptic: true, sound: true, reminders: [
  { id: 1, time: '05:45', label: 'Sabah', on: true }, { id: 2, time: '13:30', label: 'Öğle', on: true }, { id: 3, time: '21:00', label: 'Yatsı', on: false } ] };

const S = (o) => Object.assign({}, base, o);
const HEAVY = (o) => Object.assign({}, base, { zikirs: heavyZikirs, logs: heavyLogs }, o);
const configs = [
  ['01-sayac-klasik-gece',       S({ theme: 'nocturne', tab: 'sayac', design: 'klasik' })],
  ['02-tespih-zumrut',           S({ theme: 'zumrut', tab: 'sayac', design: 'tespih', activeId: 5 })],
  ['03-birlesik-gul',            S({ theme: 'gul', tab: 'sayac', design: 'birlesik' })],
  ['04-kilit-kehribar',          S({ theme: 'kehribar', tab: 'sayac', design: 'klasik', layout: 'center', locked: true })],
  ['05-sayac-kare-buz',          S({ theme: 'buz', tab: 'sayac', design: 'klasik', counterShape: 'square' })],
  ['06-zikirler-gece',           S({ theme: 'nocturne', tab: 'kutup' })],
  ['07-istatistik-okyanus',      HEAVY({ theme: 'okyanus', tab: 'stat', statRange: 'weekly' })],
  ['08-ayarlar-lavanta',         S({ theme: 'lavanta', tab: 'ayar' })],
  ['09-tespih-yakut-33',         S({ theme: 'yakut', tab: 'sayac', design: 'tespih', activeId: 1 })],
  ['10-arapca-rtl-gece',         S({ theme: 'nocturne', tab: 'sayac', design: 'klasik', lang: 'ar' })],
  ['11-modern-klasik',           S({ theme: 'modernist', tab: 'sayac', design: 'klasik' })],
  ['12-istatistik-gece-gunluk',  HEAVY({ theme: 'nocturne', tab: 'stat', statRange: 'daily' })],
  ['13-zikirler-zumrut',         S({ theme: 'zumrut', tab: 'kutup' })],
  ['14-dalga-okyanus',           S({ theme: 'okyanus', tab: 'sayac', design: 'klasik', effect: 'wave' })],
  ['15-ayarlar-gece',            S({ theme: 'nocturne', tab: 'ayar' })],
];

const STATE_DIR = path.resolve('android/app/src/main/assets/app/_shots');
fs.mkdirSync(STATE_DIR, { recursive: true });
const only = process.argv[2]; // optional substring filter, e.g. `node tools/shots.mjs istatistik`
for (const [name, state] of configs) {
  if (only && !name.includes(only)) continue;
  // write state to a served JSON file (URLs would 414 on the large heavy datasets)
  fs.writeFileSync(path.join(STATE_DIR, `${name}.json`), JSON.stringify(state), 'utf8');
  const url = `http://localhost:8790/shot.html?st=${name}`;
  const out = path.join(OUT, `${name}.png`);
  // headless Chrome enforces a ~500px min window width, so narrow phone widths get
  // clipped; 540px CSS renders the phone layout uncut. scale 2.5 → ~1350px wide PNG.
  execFileSync(CHROME, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
    '--force-device-scale-factor=2.5', '--window-size=540,1170',
    '--virtual-time-budget=6000', `--screenshot=${out}`, url,
  ], { stdio: 'ignore' });
  const kb = Math.round(fs.statSync(out).size / 1024);
  console.log(`  ${name}.png  ${kb}K`);
}
console.log('done →', OUT);
