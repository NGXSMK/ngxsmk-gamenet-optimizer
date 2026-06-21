const { app, BrowserWindow, shell, ipcMain } = require('electron');
const path = require('node:path');
const url = require('node:url');
const { spawn } = require('node:child_process');
const http = require('node:http');
const isDev = !app.isPackaged;

let pyProc = null;

function startPython() {
  if (isDev) {
    const script = path.join(__dirname, '../src/ngx_optimizer/api.py');
    pyProc = spawn('python', [script], {
      cwd: path.join(__dirname, '..')
    });
  } else {
    // In production, spawn the bundled PyInstaller backend executable
    const exePath = path.join(process.resourcesPath, 'backend/NGXSMK_GameNet_Optimizer.exe');
    pyProc = spawn(exePath, ['--background'], {
      cwd: path.dirname(exePath)
    });
  }

  pyProc.stdout.on('data', (data) => console.log(`Python: ${data}`));
  pyProc.stderr.on('data', (data) => console.error(`Python Error: ${data}`));
}

/**
 * Poll http://localhost:5000/api/health until Flask responds (or we give up).
 * @param {number} maxRetries - Maximum number of attempts
 * @param {number} intervalMs - Milliseconds between retries
 * @returns {Promise<boolean>} - Resolves true when Flask is ready, false on timeout
 */
function waitForFlask(maxRetries = 30, intervalMs = 500) {
  return new Promise((resolve) => {
    let attempts = 0;

    function tryPing() {
      attempts++;
      const req = http.get('http://127.0.0.1:5000/api/health', (res) => {
        if (res.statusCode === 200) {
          console.log(`[Electron] Flask is ready after ${attempts} attempt(s).`);
          resolve(true);
        } else {
          scheduleRetry();
        }
      });

      req.on('error', () => {
        scheduleRetry();
      });

      req.setTimeout(400, () => {
        req.destroy();
        scheduleRetry();
      });
    }

    function scheduleRetry() {
      if (attempts >= maxRetries) {
        console.warn(`[Electron] Flask not ready after ${maxRetries} attempts — loading UI anyway.`);
        resolve(false);
        return;
      }
      setTimeout(tryPing, intervalMs);
    }

    tryPing();
  });
}

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1300,
    height: 850,
    minWidth: 1000,
    minHeight: 700,
    frame: false, // Frameless for custom premium title bar look
    transparent: true,
    backgroundColor: '#00000000', // Transparent background for rounded corners effect
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs'),
    },
    title: "NGXSMK Neural Optimizer",
    icon: path.join(__dirname, 'public/vite.svg') // Placeholder icon
  });

  // Window control handlers
  ipcMain.on('window-minimize', () => mainWindow.minimize());
  ipcMain.on('window-maximize', () => {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  });
  ipcMain.on('window-close', () => mainWindow.close());

  // Hide default menu bar
  mainWindow.setMenuBarVisibility(false);

  // Load the app
  const startUrl = isDev
    ? 'http://localhost:5173'
    : url.pathToFileURL(path.join(__dirname, 'dist/index.html')).toString();

  mainWindow.loadURL(startUrl);

  // Open links in external browser
  mainWindow.webContents.setWindowOpenHandler(({ url: linkUrl }) => {
    shell.openExternal(linkUrl);
    return { action: 'deny' };
  });
}

app.whenReady().then(async () => {
  startPython();

  // Wait for Flask backend to be ready before creating the window
  // so the UI doesn't load before the API is available.
  if (!isDev) {
    await waitForFlask(40, 500); // up to 20 seconds
  }

  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (pyProc) pyProc.kill();
  if (process.platform !== 'darwin') app.quit();
});
