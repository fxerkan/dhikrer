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
];
// deterministic-ish logs across ~120 days for real charts (no Math.random dependence on time)
const now = 1765000000000; // fixed ts so runs are reproducible
const logs = [];
for (let d = 0; d < 120; d++) {
  const n = 6 + ((d * 7) % 34);
  for (let i = 0; i < n; i++) logs.push([now - d * 86400000 - (i * 137000 % 80000000), (i % 5) + 1]);
}
const base = { zikirs, activeId: 100, lang: 'tr', showRemaining: true, haptic: true, sound: true, reminders: [
  { id: 1, time: '05:45', label: 'Sabah', on: true }, { id: 2, time: '13:30', label: 'Öğle', on: true }, { id: 3, time: '21:00', label: 'Yatsı', on: false } ] };

const S = (o) => Object.assign({}, base, o);
const configs = [
  ['01-sayac-klasik-gece',       S({ theme: 'nocturne', tab: 'sayac', design: 'klasik' })],
  ['02-tespih-zumrut',           S({ theme: 'zumrut', tab: 'sayac', design: 'tespih' })],
  ['03-birlesik-gul',            S({ theme: 'gul', tab: 'sayac', design: 'birlesik' })],
  ['04-merkez-kehribar',         S({ theme: 'kehribar', tab: 'sayac', design: 'klasik', layout: 'center' })],
  ['05-sayac-kare-buz',          S({ theme: 'buz', tab: 'sayac', design: 'klasik', counterShape: 'square' })],
  ['06-zikirler-gece',           S({ theme: 'nocturne', tab: 'kutup' })],
  ['07-istatistik-okyanus',      S({ theme: 'okyanus', tab: 'stat', statRange: 'weekly', logs })],
  ['08-ayarlar-lavanta',         S({ theme: 'lavanta', tab: 'ayar' })],
  ['09-tespih-yakut-33',         S({ theme: 'yakut', tab: 'sayac', design: 'tespih', activeId: 1 })],
  ['10-arapca-rtl-gece',         S({ theme: 'nocturne', tab: 'sayac', design: 'klasik', lang: 'ar' })],
  ['11-modern-klasik',           S({ theme: 'modernist', tab: 'sayac', design: 'klasik' })],
  ['12-istatistik-gece-gunluk',  S({ theme: 'nocturne', tab: 'stat', statRange: 'daily', logs })],
  ['13-zikirler-zumrut',         S({ theme: 'zumrut', tab: 'kutup' })],
  ['14-dalga-okyanus',           S({ theme: 'okyanus', tab: 'sayac', design: 'klasik', effect: 'wave' })],
];

for (const [name, state] of configs) {
  const b64 = Buffer.from(JSON.stringify(state), 'utf8').toString('base64');
  const url = `http://localhost:8790/shot.html?zk=${b64}`;
  const out = path.join(OUT, `${name}.png`);
  execFileSync(CHROME, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-sandbox',
    '--force-device-scale-factor=2.5', '--window-size=440,900',
    '--virtual-time-budget=6000', `--screenshot=${out}`, url,
  ], { stdio: 'ignore' });
  const kb = Math.round(fs.statSync(out).size / 1024);
  console.log(`  ${name}.png  ${kb}K`);
}
console.log('done →', OUT);
