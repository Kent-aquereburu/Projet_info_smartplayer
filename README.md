# PROJET INFORMATIQUE ENSAE 2017 : Kent AQUEREBURU

**SMART PLAYER : RECOMMENDATION DE MUSIQUES PAR CREATION AUTOMATIQUE DE PLAYLISTS**

Cette application SMART PLAYER a ete réalisée dans le cadre d'un projet informatique.


**Le dossier de cette application contient les fichiers indispensables suivants:**:

- `package.json` - C'est un fichier json qui liste les libraires dependantes a installer.
- `main.js` - Ce script est le **point d'entrée** de l'application: il ouvre le processus principal .
- `index.html` - Une page HTML classique qui est la page principale de l'application
- `renderer.js` - Ce script gère toute la logique de **l'interface** de l'application: il ouvre le processus principal .
- `recommend.py` - Ce script **python** est le moteur de l'application: il lance tous les calculs : extraction des features et application de l'algorithme de regroupement. Il faut donc avoir python installé sur son pc avec les librairies  **pandas** et **sklearn**
Toutes les autres librairies sont installées par défaut avec Python (version 3 et plus)
- `newMp3s.json` - Ce fichier est un fichier temporaire qui est ecrasé et recrée à chaque fois qu'un dossier de mp3s est rajouté dans l'application
- `sox-14.4.0` - C'est dossier qui contient une petite appli utilisee pour convertir les fichiers .mp3 en .wav


## Pour exécuter l'application

Si vous n'avez pas le dossier en local Vous aurez besoin de cloner ce repository [Git](https://git-scm.com) et
Vous aurez aussi besoin d'installer [Node.js](https://nodejs.org/en/download/) afin d'avoir acces a **npm** qui est un package manager permettant d'installer facilement toutes les dependences.
Lancez les commandes suivantes dans votre terminal préféré pour executer l'application (ici on utilise bash):

```bash
# Cloner le repository
git clone https://github.com/electron/electron-quick-start
# Aller dans le repertoire smartplayer
cd smartplayer
# la commande suivante install les dependences mentionnees dans le package.json
npm install
# la comande
npm start
```


## Liens vers les sites des librairies utilisees pour ce projet

- [electron.atom.io/docs](http://electron.atom.io/docs) - ELECTRON
- [react](https://facebook.github.io/react/)
