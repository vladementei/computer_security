const {app, BrowserWindow, Menu} = require('electron')
const path = require('path');
const debug = require('electron-debug');
const prompt = require('electron-prompt');

//Uncomment if you need debug mode
//debug();


const template = [
    {
        label: 'File',
        submenu: [
            {
                label: 'Open',
                click: async () => {
                    prompt({
                        title: 'Open File',
                        label: 'File name',
                        value: 'file.txt',
                        type: 'input',
                        height: 180
                    })
                        .then((result) => {
                            if (!!result) {
                                template[0].submenu[2].visible = true;
                                updateMenu();
                                BrowserWindow.getAllWindows()[0].webContents.send('openFile', result);
                            }
                        })
                        .catch(console.error);
                }
            },
            {
                label: 'Save as',
                click: async () => {
                    prompt({
                        title: 'Save file as',
                        label: 'File name',
                        value: 'file.txt',
                        type: 'input',
                        height: 180
                    })
                        .then((result) => {
                            if (!!result) {
                                template[0].submenu[2].visible = true;
                                updateMenu();
                                BrowserWindow.getAllWindows()[0].webContents.send('saveFile', result);
                            }
                        })
                        .catch(console.error);
                }
            },
            {
                label: 'Save',
                visible: false,
                click: async () => {
                    BrowserWindow.getAllWindows()[0].webContents.send('updateFile');
                }
            },
            {
                label: 'Delete',
                click: async () => {
                    prompt({
                        title: 'Delete File',
                        label: 'File name',
                        value: 'file.txt',
                        type: 'input',
                        height: 180
                    })
                        .then((result) => {
                            if (!!result) {
                                BrowserWindow.getAllWindows()[0].webContents.send('deleteFile', result);
                            }
                        })
                        .catch(console.error);
                }
            }
        ]
    },
    {
        label: 'Key manager',
        submenu: [
            {
                label: 'generate RSA',
                click: async () => {
                    console.log(BrowserWindow.getAllWindows());
                    BrowserWindow.getAllWindows()[0].webContents.send('generateRSA');
                }
            },
            {
                label: 'get session key',
                click: async () => {
                    BrowserWindow.getAllWindows()[0].webContents.send('getSessionKey');
                }
            },
        ]
    }
];

function updateMenu() {
    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

function createWindow() {
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    });
    //Create custom menu bar
    updateMenu();

    // and load the index.html of the app.
    mainWindow.loadFile('index.html');
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        // On macOS it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
})
