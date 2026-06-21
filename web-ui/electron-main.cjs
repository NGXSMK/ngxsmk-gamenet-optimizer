const { app, BrowserWindow, shell, ipcMain } = require('electron');
const path = require('node:path');
const url = require('node:url');
const { spawn } = require('node:child_process');
const isDev = !app.isPackaged;

let pyProc = null;

function startPython() {
  const script = path.join(__dirname, '../src/ngx_optimizer/api.py');
  pyProc = spawn('python', [script], {
    cwd: path.join(__dirname, '..')
  });

  pyProc.stdout.on('data', (data) => console.log(`Python: ${data}`));
  pyProc.stderr.on('data', (data) => console.error(`Python Error: ${data}`));
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
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });

  if (isDev) {
    // Optional: mainWindow.webContents.openDevTools();
  }
}

app.whenReady().then(() => {
  startPython();
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (pyProc) pyProc.kill();
  if (process.platform !== 'darwin') app.quit();
});

