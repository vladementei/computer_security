// Modules to control application life and create native browser window
const {app, BrowserWindow, Menu} = require('electron')
const path = require('path');
const debug = require('electron-debug');
const prompt = require('electron-prompt');
debug();


const template = [
  {
    label: 'File',
    submenu: [
      {
        label: 'Open',
        id: 'as',
        click: async () => {
          prompt({
            title: 'Open File',
            label: 'File name',
            value: 'file.txt',
            type: 'input',
            height: 180
          })
              .then((result) => {
                if (result === null) {
                  console.log('user cancelled');
                } else {
                  BrowserWindow.getAllWindows()[0].webContents.send('openFile', result);
                }
              })
              .catch(console.error);
        }
      },
      {
        label: 'Save',
        click: async () => {
          console.log('save');
        }
      },
      {
        label: 'Delete',
        click: async () => {
          console.log('delete');
        }
      }
    ]
  }
];

function createWindow () {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }
  });
  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);


  // and load the index.html of the app.
  mainWindow.loadFile('index.html');

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow();
  
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
