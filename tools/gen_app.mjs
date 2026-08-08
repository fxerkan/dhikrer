// Generates the offline app.html (WebView UI) from the web source in webapp/.
// - slices the .zk-app template + logic script out of webapp/Zikirci.dc.html
// - strips the device-frame preview chrome
// - rewrites all CDN URLs to vendored offline assets
// - injects the native<->web bridge + tap marker
import fs from 'fs';
import path from 'path';
import LANGS from './langs.js';

const root = path.resolve(process.argv[2] || '.');
const webapp = path.join(root, 'webapp');
const assets = path.join(root, 'android/app/src/main/assets/app');
const src = fs.readFileSync(path.join(webapp, 'Zikirci.dc.html'), 'utf8');
const lines = src.split('\n');

// helmet block (inclusive) — from <helmet> to </helmet>
const helmetStart = lines.findIndex(l => l.includes('<helmet>'));
const helmetEnd = lines.findIndex(l => l.includes('</helmet>'));
let helmet = lines.slice(helmetStart, helmetEnd + 1).join('\n');

// app template: the .zk-app div through its matching close, i.e. line with
// class="zk-app up to the </div> right before </x-import>
const appStart = lines.findIndex(l => l.includes('class="zk-app'));
const xImportClose = lines.findIndex(l => l.includes('</x-import>'));
// the </div> closing zk-app is the line immediately before </x-import>
const appEnd = xImportClose - 1;
let appTpl = lines.slice(appStart, appEnd + 1).join('\n');

// logic script: the <script ... data-dc-script ...> ... </script>
const scriptStart = lines.findIndex(l => l.includes('data-dc-script'));
const scriptEnd = lines.findIndex((l, i) => i > scriptStart && l.trim() === '</script>');
let scriptBlock = lines.slice(scriptStart, scriptEnd + 1).join('\n');

// --- inject extra languages (ar/id/hi/zh) into the L{} table ---
const langInjection = Object.entries(LANGS)
  .map(([k, v]) => `  ${k}: ${JSON.stringify(v)}`)
  .join(',\n');
// L ends with "...}\n};" right before `function mulberry32`
const marker = '\n};\nfunction mulberry32';
if (!scriptBlock.includes(marker)) throw new Error('could not locate end of L table for lang injection');
scriptBlock = scriptBlock.replace(marker, `,\n${langInjection}\n};\nfunction mulberry32`);

// --- stamp the real app version into the footer (t.dev), single source = build.gradle.kts ---
const gradle = fs.readFileSync(path.join(root, 'android/app/build.gradle.kts'), 'utf8');
const ver = (gradle.match(/versionName\s*=\s*"([^"]+)"/) || [])[1] || '1.0';
const before = scriptBlock;
scriptBlock = scriptBlock.replace(/(Zikirci · v)[\d.]+( · )/g, `$1${ver}$2`);
if (scriptBlock === before) throw new Error('could not locate footer version (t.dev) to stamp');

// --- rewrite URLs in helmet to vendored offline assets ---
helmet = helmet
  .replace(/https:\/\/fonts\.googleapis\.com\/css2\?family=Archivo[^"']*/g, 'vendor/archivo/archivo.css')
  .replace(/https:\/\/unpkg\.com\/@phosphor-icons\/web@[^/]+\/src\/regular\/style\.css/g, 'vendor/phosphor/regular.css')
  .replace(/https:\/\/unpkg\.com\/@phosphor-icons\/web@[^/]+\/src\/fill\/style\.css/g, 'vendor/phosphor/fill.css');

// --- INLINE the design-system stylesheet (dark-theme base tokens + .card/.btn/.input).
// The external <link> to it does not reliably apply in the WebView, which left dark
// themes with unresolved --color-text (dark text on dark bg). Inlining guarantees it. ---
let dsCss = fs.readFileSync(path.join(assets, '_ds/nocturne-95389983-81ff-45dc-bcbc-e1628f5ec4dd/styles.css'), 'utf8')
  .replace(/@import[^;]+;/g, ''); // drop the network @import (Inter font) — Archivo/system suffices
// Dark themes inherited Inter-500 headings (thin). Unify to bold Archivo like light themes.
dsCss = dsCss
  .replace(/--font-heading:\s*"Inter"[^;]*;/, '--font-heading: "Archivo", system-ui, sans-serif;')
  .replace(/--font-heading-weight:\s*500;/, '--font-heading-weight: 800;')
  .replace(/--font-body:\s*"Inter"[^;]*;/, '--font-body: "Archivo", system-ui, sans-serif;')
  // roomier spacing so cards/modals/buttons breathe (DS defaults are very tight)
  .replace(/--space-2:\s*[\d.]+px;/, '--space-2: 8px;')
  .replace(/--space-3:\s*[\d.]+px;/, '--space-3: 14px;')
  .replace(/--space-4:\s*[\d.]+px;/, '--space-4: 18px;');
// The DC runtime scopes injected helmet CSS, so a bare `:root {}` token block
// does NOT reach <html>. Retarget the token block to `.zk-app` (the same
// class-scoped pattern the light-theme overrides use, which DOES apply).
dsCss = dsCss.replace(/:root\s*\{/, ':root, .zk-app {');
helmet = helmet.replace(
  /<link rel="stylesheet" href="_ds\/nocturne[^"]*styles\.css">/,
  `<style>\n${dsCss}\n</style>`
);

// drop the Design-Studio dev runtime <script> — it isn't packaged into the APK,
// so it 404s on every launch; the app runs on its own inline React + support.js.
helmet = helmet.replace(/\s*<script[^>]*src="_ds\/[^"]*_ds_bundle\.js"[^>]*><\/script>/g, '');

// make the app fill the viewport (device frame previously constrained it).
// #zk-root is padded by the system-bar insets (targetSdk 35 edge-to-edge) that
// MainActivity pushes in as --zk-sat/sab/sal/sar; the theme bg fills behind bars.
const fillCss = `<style>
*{box-sizing:border-box}
html,body{height:100%;margin:0;background:var(--color-bg);overflow-x:hidden}
html,body,#zk-root{max-width:100%}
#zk-root{position:fixed;inset:0;overflow-x:hidden;background:var(--color-bg);
 padding-top:var(--zk-sat,0px);padding-bottom:var(--zk-sab,0px);
 padding-left:var(--zk-sal,0px);padding-right:var(--zk-sar,0px)}
.zk-app{height:100%!important;max-width:100%}
</style>`;

// tap-button marker so native (volume keys / widget) can trigger a real tap
appTpl = appTpl.replace('onClick="{{ tap }}"', 'id="zk-tapbtn" onClick="{{ tap }}"');

// enable the previously "coming soon" languages now that translations exist
appTpl = appTpl
  .replace(/<option value="ar" disabled>العربية · \{\{ t\.yakinda \}\}<\/option>/, '<option value="ar">العربية</option>')
  .replace(/<option value="id" disabled>Bahasa Indonesia · \{\{ t\.yakinda \}\}<\/option>/, '<option value="id">Bahasa Indonesia</option>')
  .replace(/<option value="hi" disabled>हिन्दी · \{\{ t\.yakinda \}\}<\/option>/, '<option value="hi">हिन्दी</option>')
  .replace(/<option value="zh" disabled>中文 · \{\{ t\.yakinda \}\}<\/option>/, '<option value="zh">中文</option>');

// native bridge: mirror counter state to native, and let native drive taps
const bridge = `<script>
(function(){
  var KEY='zikirci-v1';
  // Route haptics through native — navigator.vibrate is unreliable in WebView.
  try{
    if(window.ZikirNative&&ZikirNative.vibrate){
      navigator.vibrate=function(p){ try{ ZikirNative.vibrate(JSON.stringify(p)); }catch(e){} return true; };
    }
  }catch(e){}
  function readState(){
    try{var s=JSON.parse(localStorage.getItem(KEY)||'{}');
      var z=(s.zikirs||[]).find(function(x){return x.id===s.activeId;})||(s.zikirs||[])[0];
      if(!z)return null;
      var darkThemes=['nocturne','okyanus','zumrut','kehribar','yakut'];
      return {activeId:z.id,name:z.name,count:z.count,target:z.target||0,
        volumeKeys:s.volumeKeys!==false,haptic:s.haptic!==false,lang:s.lang||'tr',
        dark:darkThemes.indexOf(s.theme||'nocturne')>=0,
        reminders:(s.reminders||[]).map(function(r){return {id:r.id,time:r.time,on:!!r.on,label:r.label||''};})};
    }catch(e){return null;}
  }
  var last='';
  function push(){
    var c=readState(); if(!c)return;
    var j=JSON.stringify(c);
    document.documentElement.dir = (c.lang==='ar') ? 'rtl' : 'ltr';
    if(j!==last){last=j; try{ if(window.ZikirNative&&ZikirNative.onState) ZikirNative.onState(j); }catch(e){} }
  }
  // native -> web: perform a real tap (fires haptics, milestones, persistence)
  window.__zikirTap=function(n){
    n=n||1; var b=document.getElementById('zk-tapbtn');
    if(!b)return false;
    for(var i=0;i<n;i++){ b.click(); }
    setTimeout(push,60);
    return true;
  };
  // native -> web: apply a pending delta accumulated while app was closed
  window.__zikirApplyPending=function(n){ if(n>0) window.__zikirTap(n); };
  setInterval(push, 400);
  document.addEventListener('DOMContentLoaded', function(){ setTimeout(push, 800); });
})();
</script>`;

const out = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<script src="support.js"></script>
</head>
<body>
<x-dc>
${helmet}
${fillCss}
<div id="zk-root">
${appTpl}
</div>
</x-dc>
${scriptBlock}
${bridge}
</body>
</html>
`;

fs.writeFileSync(path.join(assets, 'app.html'), out);
console.log('wrote app.html', out.length, 'bytes');
console.log('appTpl lines', appStart + 1, '-', appEnd + 1, '| script lines', scriptStart + 1, '-', scriptEnd + 1);
