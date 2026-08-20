# App Store — App Review Information Notes

Paste-ready reply for the **Resolution Center** message *and* the permanent
**App Store Connect → App Review Information → Notes** field. Written in English
(the review team reads English). Answers every point of the Guideline 2.1
"Information Needed" rejection, in the same order Apple asked.

App: **Dhikrer** (`com.fxerkan.dhikrer`, Apple ID 6803203796). Keep this file in
sync every release — it is a permanent Notes field, not a one-time reply.

---

## ⚠️ You must do by hand (Apple cannot be answered by text alone)

1. **Screen recording on a physical device** — record the flow in the shot list
   below on a real iPhone running the latest iOS, then attach it in the
   Resolution Center reply. A simulator recording is NOT accepted.
2. **Confirm the device/OS list** in point 2 below matches what you actually
   tested on (edit if you tested on more/other devices).

Everything else is the copy/paste text that follows.

---

## Paste this into the Notes field / Resolution Center reply

```
Dhikrer is a simple, fully offline dhikr (tasbih / prayer-bead) counter. 
Below is the information requested, point by point.

1) SCREEN RECORDING
A screen recording captured on a physical iPhone 14 (iOS 18.6.2) see attached demonstrates the
typical flow: launch → reset counter → tap the counter to increment → set target → reach a target and feel the
haptic milestone → switch dhikr via dhkirs page → reset again counter → set lower target → change theme → lock buttons and unlock → open Settings and change language → Change haptics, sound alerts → Change preset, design of the counter and button, customize look and feel → open Settings add a Reminder → open Statistics → click the Developer name (FXerkan) opens an external portfolio web page → click until Target achieved no more counter increase.

The app has NO account registration, login, or account-deletion flow; NO paid content, purchases, or subscriptions;
NO user-generated content, sharing, or social features. 

The only permission prompt is the standard iOS notification prompt, and it appears ONLY if the user
enables a daily reminder in Settings — it is shown in the recording.

2) DEVICES & OS TESTED
- iPhone 14, iOS 18.6.2 (physical device)
- iPad mini (6th gen), iPadOS 26.5.2
- iPad Air (4th gen), iPadOS 26.5.2
- iPhone 17 simulator, iOS 26 (smoke test only)

3) WHAT THE APP DOES & WHO IT IS FOR
Dhikrer is a digital tasbih: a counter for repeating dhikr (short Islamic remembrance phrases such as SubhanAllah, Alhamdulillah, Allahu Akbar). 
It replaces physical prayer beads. 

The problem it solves: counting repetitions by hand or with physical beads is easy to lose track of; Dhikrer counts reliably,
remembers your progress, shows daily/total statistics, and lets you set gentle
reminders. 

Target audience: Muslim users of any age who perform dhikr and want a
clean, ad-free, private counter. Core value: fast one-tap counting, haptic
feedback at each target, 10 themes, and everything stored locally on the device.

4) HOW TO SET UP & ACCESS THE MAIN FEATURES
No setup, no login, no credentials, no sample files needed. 
The app is fully functional the moment it launches, offline. 

Main features:
- Counter tab: tap the large ring/button to count; it shows count, percentage,
  and remaining to the target. Long-press or the reset control clears it.
- Dhikr list tab: pick which dhikr to count; add your own custom dhikr.
- Statistics tab: daily and total counts.
- Settings tab: switch UI language (Turkish / English / Arabic), pick one of 10
  themes, and optionally set daily reminders (this is the only feature that asks for the iOS notification permission).

5) EXTERNAL SERVICES / TOOLS / PLATFORMS
None. The app is 100% offline and self-contained. 
There is NO backend server, NO account system, NO analytics, NO advertising SDK, NO tracking, NO AI service, and NO payment processor. 
All data (counts, custom dhikr, settings) is stored only on the device (local storage). 

The only third-party code is the open-source Capacitor runtime and two of its first-party plugins: Haptics (vibration on
count/milestone) and Local Notifications (on-device daily reminders). 
Neither sends any data off the device.

6) REGIONAL DIFFERENCES
None. The app behaves identically in every region and country. 
The only variation is the in-app UI language (Turkish, English, Arabic), which the user
selects manually in Settings and which also follows the device language for the
home-screen name. 
No content, feature, or availability differs by region.

7) REGULATED INDUSTRY / PROTECTED THIRD-PARTY MATERIAL
Not applicable. Dhikrer is not in a regulated industry (no health, finance, or similar). 
The dhikr phrases are short, universally used Islamic remembrance words in the public domain; no copyrighted or licensed third-party material is
included, so no authorization or documentation is required.

CONTACT: dhikrer@fxerkan.com
```

---

## Screen-recording shot list (record on a real iPhone, ~40–60s)

Record with the device screen recorder (Control Center) — not the simulator.

1. **Launch** — open Dhikrer from the home screen; let the app fully render.
2. **Count** — tap the counter ~5–10 times; show count / % / remaining updating.
3. **Milestone** — reach the target so the haptic + ring-complete fires.
4. **Switch dhikr** — Dhikr list tab → pick a different dhikr → back to counter.
5. **Statistics** — open the Statistics tab (daily / total).
6. **Settings** — change theme, change language (show tr↔en↔ar), then enable a
   **daily reminder** so the **iOS notification permission prompt** appears on
   camera (this is the one and only permission the app ever requests).
7. End on the counter screen. No login, no paywall, no data prompts exist to show.

Keep it real-time and continuous (Apple wants the genuine flow, not a montage).

---

## Why this rejection happened & how to avoid it next time

Guideline 2.1 "Information Needed" on a **new app** is Apple's default when the
**App Review Information → Notes** field is empty or thin. It is not a bug
finding. The fix is: always ship the Notes text above with the first submission
of any new app (and re-confirm it on major updates). See `RELEASE.md` step 8.
