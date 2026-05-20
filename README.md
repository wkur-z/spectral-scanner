# SPECTRAL SCANNER // CAMO GENERATION TERMINAL

A single-page web app for the EPIC Aerospace Recon Division summer camp.
Students enter four hex codes captured from their Arduino RGB sensor,
pick a camo algorithm, generate a print-ready 8.5x11" pattern, and
transmit it to a shared Google Drive folder for the instructor to batch
print on sticker paper.

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
- Uploads the PDF to a shared Google Drive folder via the student's
  Google sign-in, OR offers a local-only `DOWNLOAD LOCAL COPY` fallback.

The whole thing is one `index.html` file. No build step, no server,
no frameworks. It runs from a static host (GitHub Pages) and works
fine on Chromebooks.

---

## HOW STUDENTS USE IT

1. Watch the boot sequence (`POWER-ON SELF TEST… OK`).
2. Type a callsign — any name or codename, letters and numbers only.
3. Enter the four hex codes from their Arduino RGB sensor. A live
   color swatch appears next to each one. Bad codes flash amber with
   `INVALID HEX // RETRY`.
4. Pick a camo algorithm from the four cards.
5. Click `EXECUTE >> GENERATE PATTERN`. The preview renders inside
   the CRT frame.
6. Click `RECALIBRATE >> NEW SEED` as many times as they like.
7. Click `▲ TRANSMIT TO COMMAND ▲` to upload the PDF to the shared
   Drive folder, OR `DOWNLOAD LOCAL COPY` to save it themselves.

On first transmit, a Google sign-in popup appears. After that the
session caches the token, so resubmits are one-click.

---

## INSTRUCTOR SETUP — GOOGLE CLOUD

You only do this **once** before camp. The app needs three things from
Google: a **Client ID**, an **API Key**, and the **ID of the shared
Drive folder** where student PDFs will land. Paste all three at the
top of `index.html`.

### 1. Create a Google Cloud project

1. Go to **https://console.cloud.google.com/**.
2. Click the project dropdown at top-left → **NEW PROJECT**.
3. Name it `EPIC Spectral Scanner` (or whatever you like). Create.

### 2. Enable the Google Drive API

1. In the left menu: **APIs & Services → Library**.
2. Search for `Google Drive API`. Click it. Click **ENABLE**.

### 3. Configure the OAuth consent screen

1. **APIs & Services → OAuth consent screen**.
2. User type: **External**. Create.
3. App name: `EPIC Spectral Scanner`. User support email: yours.
   Developer contact: yours. Save and continue through the rest with
   defaults (you do not need to add scopes here — the app requests
   `drive.file` at runtime).
4. **Test users**: add the gmail addresses of every student account
   that will use the app (or your camp's Google Workspace domain).
   Without this, students will see an "unverified app" wall.

### 4. Create the OAuth 2.0 Client ID

1. **APIs & Services → Credentials → CREATE CREDENTIALS → OAuth client ID**.
2. Application type: **Web application**.
3. Name: `Spectral Scanner Web`.
4. **Authorized JavaScript origins** — add your GitHub Pages URL
   (root only, no path). Examples:
   - `https://USERNAME.github.io`
   - `https://your-camp-domain.org`
   If you'll also test locally, add `http://localhost:8000`.
5. **Authorized redirect URIs** — leave blank. (GIS uses the
   implicit token flow.)
6. Create. **Copy the Client ID** that appears.

### 5. Create the API Key

1. **APIs & Services → Credentials → CREATE CREDENTIALS → API key**.
2. **Copy the key**.
3. (Recommended) Click the new key → **Edit API key** →
   **Application restrictions: HTTP referrers** → add your GitHub
   Pages URL with `/*` (e.g. `https://USERNAME.github.io/*`).
   **API restrictions: Restrict key → Google Drive API**.

### 6. Create and share the Drive folder

1. In Google Drive, create a folder, e.g. `EPIC Camo Submissions`.
2. Open the folder. The URL looks like:
   `https://drive.google.com/drive/folders/1aBcDeFgHiJkLmNoPqRsTuVwXyZ`
   That long ID at the end is the **Drive folder ID**.
3. Click **Share** on the folder.
   - **Easy mode:** set "Anyone with the link" to **Editor**.
     Students do not need to be added individually.
   - **Locked mode:** add your students' Google accounts as Editors.
4. Either way, students still authenticate as themselves — they
   only get access to files **the app creates** (the `drive.file`
   scope is narrow).

### 7. Paste the three values into the app

Open `index.html` and find the `CONFIG` block near the top of the
script section:

```js
const CONFIG = {
  GOOGLE_CLIENT_ID:   'PASTE_YOUR_CLIENT_ID_HERE',
  GOOGLE_API_KEY:     'PASTE_YOUR_API_KEY_HERE',
  DRIVE_FOLDER_ID:    'PASTE_YOUR_SHARED_FOLDER_ID_HERE'
};
```

Replace each string with the value from steps 4, 5, and 6. Commit and
push. That's it.

If any of the three are left as `PASTE_…` placeholders, the
`TRANSMIT TO COMMAND` button stays disabled with `COMMAND CHANNEL
OFFLINE. USE LOCAL DOWNLOAD.` — the rest of the app still works.

---

## DEPLOY TO GITHUB PAGES

1. Push this folder to a GitHub repository.
2. On the repo page: **Settings → Pages**.
3. **Source: Deploy from a branch**.
4. **Branch: main**, **Folder: / (root)**. Save.
5. Wait ~30 seconds. Your site appears at
   `https://USERNAME.github.io/REPO/`.
6. **Important:** that URL (the origin, without the `/REPO/` path)
   must be listed in **Authorized JavaScript origins** in step 4
   above. If you used the project-page form, the origin is
   `https://USERNAME.github.io`.

For a custom domain, point a `CNAME` at GitHub Pages and add that
domain to Authorized JavaScript origins.

---

## PRINTER SETTINGS — STICKER PAPER

When you batch-print, every printer dialog needs the same answer:

- **Paper size:** US Letter, 8.5 x 11 inches.
- **Scaling:** **Actual size** (also called **100%** / **None**).
  Do **not** use "Fit to page" — it will shrink the pattern and
  leave white margins.
- **Margins:** **None** (or "Minimum" if your printer can't go
  borderless). The PDF is already full-bleed.
- **Orientation:** Portrait.
- **Color:** Color, normal quality is fine for 300 DPI bitmaps.

### Batch print from the Drive folder

1. Open the shared Drive folder on the instructor's computer.
2. Sort by date so the newest student submissions are on top.
3. Select all the PDFs you want to print (Cmd/Ctrl-click or
   Shift-click).
4. Right-click → **Open with → Adobe Acrobat / Preview / a desktop
   PDF reader** (Drive's built-in viewer prints one at a time).
5. From the desktop reader: **File → Print → All open documents**
   (Acrobat), or print each one with the settings above.

Tip: Acrobat's **Print → All open files in this window** is the
fastest path for batches of 20+.

---

## FILES IN THIS REPO

```
index.html              # the whole app
generate_samples.py     # helper that rebuilds samples/*.png from the
                        # same algorithms (Python + PIL); not needed
                        # to deploy the app
samples/
  MARPAT-D.png          # example output for each pattern,
  WOODLAND-7B.png       # generated with test palette
  FRACTAL-G.png         # #4A7C2B, #8B6F47, #2D3E1F, #C4B896
  TERRAIN-X.png
README.md               # this file
```

---

## TROUBLESHOOTING

- **"unverified app" warning on Google sign-in:** the student's
  account is not in the Test Users list (step 3.4). Add them, or
  publish the OAuth consent screen.
- **`origin_mismatch` error:** the URL the app is served from is not
  in **Authorized JavaScript origins**. Check step 4 and re-save.
- **403 from Drive on upload:** the student is signed in to a
  different Google account than the one with folder access, OR the
  folder isn't shared (step 6).
- **`COMMAND CHANNEL OFFLINE`:** one of the three CONFIG values is
  still `PASTE_…`, or the device is offline. Local download still
  works.
- **PDF prints with white margin:** printer is using "Fit to page".
  Re-select **Actual size** / **100%**.
- **Pattern looks the same after RECALIBRATE:** unlikely — each
  click reseeds. If you're seeing identical output, refresh the
  page; some Chromebook kiosk modes pin RNG state.
