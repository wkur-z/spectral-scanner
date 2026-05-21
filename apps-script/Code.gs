/**
 * SPECTRAL SCANNER — Drive drop receiver
 *
 * This script is deployed as a Google Apps Script Web App. The terminal
 * page POSTs a base64-encoded PDF here, and this script saves it into a
 * specific Drive folder owned by YOU (the instructor).
 *
 * Students never sign in to Google. The script runs as your account, so
 * all submissions land in your folder regardless of who's clicking.
 *
 * ============== INSTRUCTOR: ONE-TIME SETUP =====================
 * 1. Create a Drive folder for student submissions, e.g. "EPIC Camo Submissions"
 * 2. Open the folder. Look at the URL:
 *      https://drive.google.com/drive/folders/1aBcDeFgHi...
 *    Copy the long ID after /folders/.
 * 3. Paste that ID into FOLDER_ID below (replace PASTE_FOLDER_ID_HERE).
 * 4. Click Deploy → New deployment → Type: Web app
 *      Description: "SPECTRAL SCANNER receiver"
 *      Execute as: Me
 *      Who has access: Anyone
 *    Click Deploy. Authorize when prompted.
 * 5. Copy the Web app URL. Paste it into index.html CONFIG.APPS_SCRIPT_URL.
 * ===============================================================
 */

const FOLDER_ID = 'PASTE_FOLDER_ID_HERE';

/**
 * POST handler — receives a JSON payload with a base64-encoded file.
 * Sent as Content-Type: text/plain to avoid CORS preflight.
 *
 * Payload fields:
 *   filename   — required, used as the Drive file name
 *   pdfBase64  — required, base64-encoded file bytes (kept this
 *                name for backward compatibility; works for any
 *                file type, not just PDFs)
 *   mimeType   — optional, defaults to 'application/pdf'. Examples:
 *                'text/markdown', 'text/plain', 'image/png'.
 */
function doPost(e) {
  try {
    if (FOLDER_ID === 'PASTE_FOLDER_ID_HERE') {
      throw new Error('FOLDER_ID_UNCONFIGURED');
    }
    if (!e || !e.postData || !e.postData.contents) {
      throw new Error('NO_BODY');
    }
    const data = JSON.parse(e.postData.contents);
    const rawName = data.filename || 'CAMO_UNKNOWN.pdf';
    // Strip anything weird; allow only A-Z a-z 0-9 . _ -
    const filename = String(rawName).replace(/[^A-Za-z0-9._-]/g, '_').slice(0, 120);
    const b64 = data.pdfBase64;
    if (!b64) throw new Error('NO_FILE_DATA');
    const mimeType = data.mimeType || 'application/pdf';

    const bytes = Utilities.base64Decode(b64);
    const blob = Utilities.newBlob(bytes, mimeType, filename);
    const folder = DriveApp.getFolderById(FOLDER_ID);
    const file = folder.createFile(blob);

    return ContentService
      .createTextOutput(JSON.stringify({
        ok: true,
        id: file.getId(),
        name: file.getName(),
        url: file.getUrl()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({
        ok: false,
        error: String((err && err.message) || err)
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * GET handler — lets you sanity-check the deployed URL in a browser.
 */
function doGet(e) {
  return ContentService
    .createTextOutput('SPECTRAL SCANNER RECEIVER :: ONLINE')
    .setMimeType(ContentService.MimeType.TEXT);
}
