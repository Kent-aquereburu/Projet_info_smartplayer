// Ce script  main.js est le point d'entree de l'application
// Il ouvre le processus principal qui gere la fenetre de l'app et lance la vue avec renderer.js

const electron = require('electron')
// On cree l'instance Electron qui gère l'application
const app = electron.app
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow

const path = require('path')
const url = require('url')

// Keep a global reference of the window object, if you don't, the window will
// On crée l'objet qui va contenir la fenetre Windows
let mainWindow

function createWindow () {
  // On instancie la fenetre Windows
  mainWindow = new BrowserWindow({width: 800, height: 600})

  // On affiche la page index.html comme page d'acceuil de l'application
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))



  // Lorsque que l'application se ferme, on fait disparaitre la fenetre
  mainWindow.on('closed', function () {

    mainWindow = null
  })
}

// This method will be called when Electron has finished

app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // Sur les systèmes OS X, il faut forcer l'application à se fermer pour tuer le processus
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function () {
  // On OS X it's common to re-create a window in the app when the

  if (mainWindow === null) {
    createWindow()
  }
})
