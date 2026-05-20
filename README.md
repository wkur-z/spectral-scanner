# SPECTRAL SCANNER // CAMO GENERATION TERMINAL

A single-page web app for the EPIC Aerospace Recon Division summer camp.
Students enter four hex codes captured from their Arduino RGB sensor,
pick a camo algorithm, generate a print-ready 8.5x11" pattern, and
transmit it to a shared Google Drive folder for the instructor to batch
print on sticker paper.

**Live:** https://wkur-z.github.io/spectral-scanner/

---

## WHAT THE APP DOES

- Accepts a callsign (the student's name) and four hex color codes
  (with or without `#`, 3-char shorthand like `F0A` auto-expands).
- Renders one of four camouflage algorithms using **only** the four
  colors the student supplied:
  - **MARPAT-D :: DIGITAL TESSELLATION** — blocky pixel-cluster camo.
  - **WOODLAND-7B :: ORGANIC BLOB** — classic painted blob camo.
  - **FRACTAL-G :: GEOMETRIC SHATTER** — triangular shatter pattern.
  - **TERRAIN-X :: TOPOGRAPHIC FIELD** — aerial-recon noise bands.
- Lets the student `RECALIBRATE` for a new random seed any number of
  times.
- Exports a full-bleed 8.5x11 inch PDF at 300 DPI.
- Submits the PDF directly to a Drive folder you (the instructor) own —
  students never sign in to Google — OR offers `DOWNLOAD LOCAL COPY`
  as a fallback.

The whole thing is one `index.html` file. No build step, no server,
no frameworks. Runs from GitHub Pages and works fine on Chromebooks.

---

## HOW STUDENTS USE IT

1. Watch the boot sequence (`POWER-ON SELF TEST… OK`).
2. Type a callsign — any name or codename.
3. Enter the four hex codes from their Arduino RGB sensor. A live
   color swatch appears next to each one. Bad codes flash amber with
   `INVALID HEX // RETRY`.
4. Pick a camo algorithm from the four cards.
5. Click `EXECUTE >> GENERATE PATTERN`. Preview renders in the CRT frame.
6. Click `RECALIBRATE >> NEW SEED` as many times as they like.
7. Click `▲ TRANSMIT TO COMMAND ▲` — the PDF lands in your Drive folder.

---

## INSTRUCTOR SETUP — APPS SCRIPT PROXY

The app uses a Google Apps Script as a tiny upload receiver. You deploy
it once, paste one URL into `index.html`, done. The script runs **as your
account**, so all student submissions land in your folder regardless of
who clicks the button. Students never sign in to Google.

### 1. Create the Drive folder

1. In Google Drive, click **New → Folder**, e.g. `EPIC Camo Submissions`.
2. Open it. The URL looks like:
   `https://drive.google.com/drive/folders/1aBcDeFgHiJkLmNoPqRsTuVwXyZ`
3. Copy the long ID at the end (everything after `/folders/`).

### 2. Create the Apps Script

1. Open **https://script.google.com/** in the same Google account that
   owns the folder.
2. Click **New project** (top-left).
3. Rename the project from "Untitled project" to `SPECTRAL SCANNER`
   (click the title at the top to rename).
4. Delete the placeholder `function myFunction() { ... }` and paste in
   the entire contents of [`apps-script/Code.gs`](apps-script/Code.gs).
5. Find the line `const FOLDER_ID = 'PASTE_FOLDER_ID_HERE';` near the
   top and replace `PASTE_FOLDER_ID_HERE` with the folder ID from step 1.
6. Click the 💾 **Save** icon (or `Ctrl+S`).

### 3. Deploy the script as a Web App

1. Top-right, click **Deploy → New deployment**.
2. Click the gear icon next to "Select type" → choose **Web app**.
3. Fill in:
   - **Description:** `SPECTRAL SCANNER receiver`
   - **Execute as:** `Me (your-email)`  ← important — this is why
     students don't need to sign in.
   - **Who has access:** `Anyone`  ← the script verifies its own
     folder; nobody can write anywhere else.
4. Click **Deploy**.
5. First time only: a permissions dialog appears. Click **Authorize
   access** → pick your account → "Advanced" → "Go to SPECTRAL SCANNER
   (unsafe)" → **Allow**. (Google calls it "unsafe" because the app
   isn't published; it's your own code running in your own account.)
6. You land on a "Deployment successfully updated" screen. **Copy the
   Web app URL.** It looks like:
   `https://script.google.com/macros/s/AKfycby.../exec`

### 4. Paste the URL into the app

Open `index.html`. Near the top of the `<script>` block:

```js
const CONFIG = {
  APPS_SCRIPT_URL: 'PASTE_YOUR_APPS_SCRIPT_URL_HERE'
};
```

Replace the placeholder with the Web app URL from step 3.6. Commit and
push. That's it.

### Updating the script later

If you edit `Code.gs`, you must redeploy:
1. **Deploy → Manage deployments** (NOT "New deployment" — that would
   give you a different URL).
2. Click the ✏️ pencil icon next to your existing deployment.
3. **Version: New version**. Click **Deploy**.

The Web app URL stays the same, so you don't need to touch `index.html`.

---

## DEPLOY TO GITHUB PAGES

(Already done — repo lives at https://github.com/wkur-z/spectral-scanner
and the site is live at https://wkur-z.github.io/spectral-scanner/.)

For future updates: just push to `main` and Pages rebuilds in ~30 seconds.

---

## PRINTER SETTINGS — STICKER PAPER

Every printer dialog needs the same answer:

- **Paper size:** US Letter, 8.5 x 11 inches.
- **Scaling:** **Actual size** (also called **100%** / **None**).
  Do **not** use "Fit to page" — it will shrink the pattern and leave
  white margins.
- **Margins:** **None** (or "Minimum" if your printer can't go
  borderless). The PDF is already full-bleed.
- **Orientation:** Portrait.
- **Color:** Color, normal quality is fine for 300 DPI bitmaps.

### Batch print from the Drive folder

1. Open the shared Drive folder on the instructor's computer.
2. Sort by date so the newest submissions are on top.
3. Select all the PDFs you want to print (Cmd/Ctrl-click or Shift-click).
4. Right-click → **Open with → Adobe Acrobat / Preview / a desktop PDF
   reader** (Drive's built-in viewer prints one at a time).
5. From the desktop reader: **File → Print → All open documents**
   (Acrobat), or print each one with the settings above.

---

## FILES IN THIS REPO

```
index.html              # the whole app
apps-script/
  Code.gs               # paste this into script.google.com
generate_samples.py     # helper that rebuilds samples/*.png from the
                        # same algorithms (Python + PIL); not used at runtime
samples/
  MARPAT-D.png          # example output for each pattern, generated
  WOODLAND-7B.png       # with the test palette
  FRACTAL-G.png         # #4A7C2B, #8B6F47, #2D3E1F, #C4B896
  TERRAIN-X.png
README.md               # this file
```

---

## TROUBLESHOOTING

- **`COMMAND CHANNEL OFFLINE`:** `APPS_SCRIPT_URL` in `index.html` is
  still the placeholder, OR the device is offline. Local download still
  works.
- **`TRANSMISSION FAILED // CODE [HTTP_401]` or `[HTTP_403]`:** the Apps
  Script wasn't deployed with **Who has access: Anyone**. Redeploy.
- **`TRANSMISSION FAILED // CODE [FOLDER_ID_UNCONFIGURED]`:** you forgot
  to paste the folder ID into `Code.gs`. Edit, save, **Manage
  deployments → New version**.
- **`TRANSMISSION FAILED // CODE [Exception: ... not found]`:** the
  folder ID is wrong, or the script's account doesn't have access to
  that folder. Make sure the folder lives in the same Google account
  the script is deployed under.
- **Submissions are landing in the wrong folder:** you put a different
  folder's ID in `Code.gs`. Fix it and redeploy a new version.
- **PDF prints with white margin:** printer is using "Fit to page".
  Re-select **Actual size** / **100%**.
- **Pattern looks the same after RECALIBRATE:** unlikely — each click
  reseeds. If you see identical output, refresh the page.
