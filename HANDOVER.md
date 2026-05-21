# SPECTRAL SCANNER // INSTRUCTOR HANDOVER

*EPIC Aerospace Recon Division — Camo Generator Tool*
*Last updated: 2026-05-20 by Will Kurtz (wkurtz97@gmail.com)*

> This file lives in two places:
> - GitHub repo: https://github.com/wkur-z/spectral-scanner/blob/main/HANDOVER.md
> - Shared Drive folder (same place student submissions land)

This document is written for a future instructor who didn't build the app
and may not be a coder. It covers running camp, basic maintenance, and
what to do if Will (the original author) leaves and you're taking over.

---

## WHAT THIS IS

A web app middle-school summer camp students use to generate
camouflage patterns from hex codes their Arduino RGB sensor reads. They
generate a pattern, click TRANSMIT, and a print-ready 8.5x11" PDF lands
in a shared Google Drive folder. The instructor batch-prints them onto
sticker paper at the end of camp — students apply them to model planes
to take home.

The hidden EPIC Campus mountain silhouette is embedded in every camo
pattern so students remember the project came from EPIC.

---

## LINKS YOU NEED

| Thing | URL |
|---|---|
| Live student site | https://wkur-z.github.io/spectral-scanner/ |
| Source code (GitHub) | https://github.com/wkur-z/spectral-scanner |
| Submissions folder | https://drive.google.com/drive/folders/16fs4H13M3xmJf5ZM-tKcxu-VAyD23ADU |
| Apps Script editor | https://script.google.com/ (project: "SPECTRAL SCANNER") |

---

## WHO OWNS WHAT

| Thing | Account |
|---|---|
| GitHub repo | github user `wkur-z` (Will Kurtz) |
| Drive folder | `wkurtz97@gmail.com` (Will Kurtz) |
| Apps Script | `wkurtz97@gmail.com` (Will Kurtz) |

These three accounts are linked together by URLs hard-coded in the app.
If any of them are deactivated without transferring access first, the
TRANSMIT button stops working. See "**IF YOU'RE TAKING OVER**" below.

---

## HOW STUDENTS USE IT (paint mode — the primary workflow)

1. Go to **https://wkur-z.github.io/spectral-scanner/**
2. Wait for the boot sequence (the "POWER-ON SELF TEST" text).
3. Type your **operative callsign** — format is `FIRST LAST :: CALLSIGN`,
   e.g. `JANE DOE :: BEARCAT` or `SAM SMITH :: AIRMASTER`.
4. Type the **4 hex codes** from your Arduino RGB sensor reading.
   - Or click the amber **`▶ LOAD EPIC TEST PALETTE`** button to fill in
     EPIC's brand colors (white, orange, navy, green) for a quick demo.
     This also auto-fills the callsign with `OPERATIVE_TEST` if blank.
5. Pick one of the **4 paintable camo patterns**:
   - WOODLAND-7B (~100 organic blobs)
   - FRACTAL-G (~300 triangles)
   - HEXFIELD-6 (~150 hexagons)
   - DRAGONSCALE-V (~120 Voronoi cells)
6. The canvas shows the pattern in **grayscale with numbered shapes**.
   Pick a color from the palette panel on the right (or press keys
   **1–4** to switch active color).
7. **Click / tap each shape** to fill it with the active color. The
   counter shows progress: `PAINTED :: 47 / 312`.
8. Helpful buttons on the right:
   - **FILL ALL** — set every shape to the active color (good starting
     base coat).
   - **UNDO** — revert the last shape change. Cmd/Ctrl+Z also works.
   - **RESET** — clear everything back to unpainted gray.
   - **RANDOMIZE** — auto-assign random colors (escape hatch if a kid
     is overwhelmed).
9. When happy, click `▲ TRANSMIT TO COMMAND ▲` — your PDF lands in the
   camp's Drive folder. Or `DOWNLOAD LOCAL COPY` for a local save.

Students never sign in to Google.

### The EPIC logo stamp

Every generated camo has 4 copies of the official EPIC Campus logo
stamped on it (mountain icon + "EPIC CAMPUS" wordmark + "EXPLORATIVE
PATHWAYS FOR INNOVATIVE CAREERS" tagline). When students take their
sticker-decorated planes home, the EPIC branding goes with them.

### Hidden motif templates

A `▓ HIDDEN MOTIFS ▓` section in the palette panel has three buttons
that pre-paint the canvas into recognizable shapes using the student's
own colors:

- **▶ SMILEY :)** — circular face, eyes, and a U-shaped smile
- **▶ SNOWY PEAKS** — three mountain peaks with snow caps and sky
- **▶ EPIC BADGE** — mimics the EPIC mountain logo across the whole sheet

The motif uses each student's 4 colors mapped by brightness (lightest →
darkest), so it always reads correctly regardless of which colors they
picked. They can keep painting on top of the motif or hit RESET to
start fresh.

### Auto-field (AUTOBOTS ROLL OUT) mode — for short classes

If the class is running short on time, type **`AUTOBOTS ROLL OUT`** at
the start of the callsign field (followed by the student's name), e.g.
`AUTOBOTS ROLL OUT JANE DOE :: BEARCAT`. The codephrase gets stripped
automatically. The Step 03 section flips to the older one-click
auto-generation flow:

- Two additional patterns appear (`MARPAT-D` digital camo and
  `TERRAIN-X` topographic) that aren't paintable.
- One `EXECUTE` button generates the entire camo in seconds.
- `RECALIBRATE` rolls a new random version with the same colors.

Refreshing the page returns to paint mode by default.

---

## HOW THE INSTRUCTOR BATCH-PRINTS

1. Open the **submissions folder** (link above) on a computer.
2. Sort by date so newest are on top.
3. Select all the PDFs you want to print (Cmd/Ctrl+click or Shift+click).
4. Right-click → **Open with → Adobe Acrobat** (or Preview, any desktop
   PDF reader). Don't use Drive's built-in viewer — it prints one at a
   time.
5. From Acrobat: **File → Print → All open documents**.
6. Printer settings that matter:
   - **Paper size:** US Letter (8.5 × 11)
   - **Scaling:** "Actual size" or "100%" — **NEVER** "Fit to page"
   - **Margins:** None
   - **Orientation:** Portrait
7. Use **full-sheet white sticker paper** (Avery 8165 or equivalent —
   no pre-cut shapes).

---

## BETWEEN CAMP SESSIONS

The Drive folder accumulates submissions over time. To clear it:

1. Open the submissions folder.
2. Select all files (Cmd/Ctrl + A).
3. Move to trash. They stay recoverable for 30 days.

You don't have to clear it — Drive has plenty of space for hundreds of
PDFs. Just makes batch-print selection easier next time.

---

## THE EPIC TEST PALETTE BUTTON

There's an amber "LOAD EPIC TEST PALETTE" button next to the hex
inputs. One click fills them with EPIC's brand colors (white, orange,
navy, green). Useful for:

- Demoing the app before students have sensor readings
- Showing what camo looks like with high-contrast inputs
- A backup if a student's sensor isn't working

A persistent warning underneath reminds students to override with their
own sensor readings.

---

## IF SOMETHING BREAKS

### "COMMAND CHANNEL OFFLINE" appears in the status bar

- Means: the app can't reach the Apps Script receiver.
- Fix: the Apps Script URL might be wrong in the code, or the script
  was deleted. See **REDEPLOYING THE APPS SCRIPT** below.

### "TRANSMISSION FAILED // CODE [HTTP_401]" or [HTTP_403]

- Means: Apps Script's "Who has access" setting got changed away from
  "Anyone".
- Fix: Open script.google.com → SPECTRAL SCANNER project → **Deploy →
  Manage deployments** → Edit (pencil icon) → set "Who has access:
  Anyone" → save and deploy a new version.

### "TRANSMISSION FAILED // CODE [Exception: ... not found]"

- Means: the Drive folder ID baked into the script is wrong, or the
  folder was deleted.
- Fix:
  1. Confirm the folder still exists. If it's in Trash, restore it.
  2. If the folder was recreated, copy the new ID from the URL (the
     long string after `/folders/`).
  3. Open the Apps Script, update the `FOLDER_ID` line near the top.
  4. Save, then redeploy (see **REDEPLOYING** below).

### Students see a Google sign-in prompt

- Means: the Apps Script's "Execute as" got changed.
- Fix: **Deploy → Manage deployments** → Edit → set "Execute as: Me"
  → redeploy a new version.

### PDF prints small with a white margin

- Printer is using "Fit to page". Change to **Actual size / 100%** and
  set margins to **None**.

### Boot sequence runs but EXECUTE button never enables

- Means: a hex code is invalid (it's flashing amber) or the callsign
  field is empty. Both must be filled in valid form before EXECUTE
  unlocks.

---

## REDEPLOYING THE APPS SCRIPT

Do this if you change the script's code, OR if you need to re-grant
Google permissions.

1. Open https://script.google.com/, click the **SPECTRAL SCANNER**
   project.
2. Make your changes. Press Cmd/Ctrl+S (or the floppy disk icon) to
   save.
3. Click **Deploy → Manage deployments** (NOT "New deployment" — that
   creates a different URL and you'd have to update the code in
   GitHub).
4. Click the ✏️ pencil icon next to the existing deployment.
5. In the "Version" dropdown, select **"New version"**.
6. Click **Deploy**.
7. The Web app URL stays the same. Done.

---

## MAKING CHANGES TO THE APP ITSELF

The student-facing app is one file: `index.html` in the GitHub repo.
The repo also has:

- `apps-script/Code.gs` — the Drive receiver script
- `samples/` — example outputs of the four pattern styles
- `README.md` — technical docs for developers
- `HANDOVER.md` — this file

**Small changes** (changing button text, tweaking colors, swapping the
test palette): you can do this through GitHub's web editor without
installing anything. Open a file → click the ✏️ pencil → make changes →
"Commit changes" at the bottom. The site rebuilds in ~30 seconds.

**Bigger changes** (new patterns, bug fixes, new features): hand it to
a coder. Will built it with the help of Claude (Anthropic's AI
assistant) and a coder can do the same thing.

---

## IF YOU'RE TAKING OVER (and Will is leaving)

Before Will's accounts get deactivated, these things need to happen.
Without them, the TRANSMIT button stops working when his account is
disabled.

### 1. Drive folder ownership

1. Will opens the submissions folder, **Share** → add your Google
   account as **Editor**.
2. Then change your permission to **Owner** (Will demotes himself).
3. Confirm the change in Drive's prompt.

### 2. Apps Script (must be recreated in your account — scripts aren't transferable)

1. Open https://script.google.com/ signed in as YOU.
2. Click **+ New project**.
3. Rename it to `SPECTRAL SCANNER`.
4. Open the GitHub repo's `apps-script/Code.gs` file, copy all of it,
   paste it into the new project (replacing whatever's there).
5. On the line that says `const FOLDER_ID = '...'`, paste in the folder
   ID from your submissions folder.
6. Save.
7. **Deploy → New deployment** → gear icon → **Web app**.
8. Settings:
   - Execute as: **Me (your-email)**
   - Who has access: **Anyone**
9. Click Deploy, authorize when prompted ("Advanced → Go to SPECTRAL
   SCANNER (unsafe) → Allow"). This is safe — it's your own code.
10. Copy the **Web app URL** that appears.

### 3. Update the app to point at your new script

1. Open `index.html` in the GitHub repo (use the web editor).
2. Near the top of the `<script>` section, find:
   ```
   const CONFIG = {
     APPS_SCRIPT_URL: 'https://script.google.com/macros/s/.../exec'
   };
   ```
3. Replace the URL with your new Web app URL from step 2.10.
4. Commit. GitHub Pages rebuilds in ~30 seconds.

### 4. GitHub repo access (optional)

The repo lives under github user `wkur-z`. You have two options:

- **Easy:** Will adds you as a Collaborator (Settings → Collaborators →
  add your username). You don't need ownership. The student-facing URL
  stays the same: `https://wkur-z.github.io/spectral-scanner/`.
- **Full transfer:** Settings → Transfer ownership. The URL changes to
  `https://YOUR-USERNAME.github.io/spectral-scanner/`. You'd need to
  share the new URL with students.

The easy option is recommended unless you have a strong reason to own
the repo outright.

---

## QUICK REFERENCE — TEST PALETTES

For demos, troubleshooting, or "the sensor isn't working" scenarios:

```
EPIC Campus brand:   #FFFFFF  #E87722  #1B3D5E  #3E9D43
Classic Woodland:    #4A7C2B  #8B6F47  #2D3E1F  #C4B896
Desert / Tan:        #C2A878  #8B6F3F  #E8D7A7  #5C4A2A
Urban Gray:          #3C3C3C  #7A7A7A  #1A1A1A  #C8C8C8
Naval Blue:          #1F3A5F  #4A6B8C  #0A1929  #B0C4D8
Arctic / Snow:       #E8EBED  #B5BCC2  #6C7480  #F5F6F7
```

---

## CREDITS

Built May 2026 by Will Kurtz with the help of Claude (Anthropic).
For EPIC Campus, Littleton Public Schools, Colorado.
Original purpose: middle-school aerospace summer camp.
