
// Ce script renderer.js est celui qui nous permet de gérer la logique de l'interface
// C'est lui qui crée les composants React de la page et gere leur fonctionnement internet
import React from 'react'
import { render } from 'react-dom'
import { Component } from 'react'
import Dropzone from 'react-dropzone' //librairie pour le composant DRAG AND DROP
import { Player } from 'react-easy-audio' // Librairie pour le Player
import { exec }    from 'child_process'; // Librairies pour executer un sous process a partir de nodejs

class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      files: [],
      current: null,
      loading: false
    }
  }

  onDrop = (files) => {
    const mp3s = files.filter(file => {
      if (file.type === 'audio/mp3') return true
      return false
    })
    //console.log(mp3s)
    const newMp3s = mp3s.map(file => file.path)
    require('fs').writeFile(

    './newMp3s.json',

    JSON.stringify(newMp3s),

    function (err) {
        if (err) {
            console.error('Crap happens');
        }
    }
);
    // On peut remplacer `python ./recommend.py` par un exécutable .exe `python ./recommend.py -l '${JSON.stringify(newMp3s)}'`
    //`python ./recommend.py --l '${JSON.stringify(newMp3s)}'`
    //./build/exe.win-amd64-3.5/recommend.exe  python ./recommend.py
    this.setState({ loading: true })
    exec(`python ./recommend.py `, (err, std) => {
		console.log(err);
		if (err){
			console.log("Echec du traitement Python");
			console.log(err.signal+"erreur");
		}
    console.log(std);
	  console.log("TESTTTTT");

      //const clustered = JSON.parse(JSON.parse(JSON.stringify(std)));
      const clustered = JSON.parse(std)
	  console.log(clustered);
      // Ajoute les numeros de clusters dans le tableau de fichiers mp3 initial
      const clustFiles = mp3s.map(file => {
        const { cluster } = clustered.filter(elem => elem.index === file.name)[0]
        // ajoute au fichier courant la propriété cluster qui est égale à son numéro de cluster
        return {
          name: file.name,
          path: file.path,
          cluster: cluster
        }
      })

      console.log(clustFiles)
      this.setState({ files: clustFiles, current: clustFiles[0], loading: false })
    })
  }

  renderPlayer() {
    if (this.state.current !== null) {
      return <Player
        src={this.state.current.path}
        author={null}
        title={this.state.current.name}
        cover="./iconeplayer.png"
      />
    }
    return null
  }

// Pour le moment on fige le nombre de groupes à 3 tout le temps
  renderListOrDropZone() {
    if (this.state.files.length !== 0)
      return (
          <div>
          <h3>Playist 1</h3>

          <ul>
            {this.state.files.filter(file => file.cluster === 0).map(file => <li key={file.path}   onClick={() => this.setState({ current: file })}>{file.name.slice(0,-4)}</li>)}
          </ul>

          <h3>Playist 2</h3>

          <ul>
            {this.state.files.filter(file => file.cluster === 1).map(file => <li key={file.path}   onClick={() => this.setState({ current: file })}>{file.name.slice(0,-4)}</li>)}
          </ul>

          <h3>Playist 3</h3>

          <ul>
            {this.state.files.filter(file => file.cluster === 2).map(file => <li key={file.path}   onClick={() => this.setState({ current: file })}>{file.name.slice(0,-4)}</li>)}
          </ul>
         </div>

      )
    else if (this.state.loading) {
      // Au moment ou l'utilisateur ajoute son dossier , on affiche
      //un petit message pour indiquer que les calculs sont en cours
      return (<div style={{color:'blue'}}> Création des playlists en cours... </div>)
    }
    return (
      <Dropzone onDrop={this.onDrop}>
        <button>Ajoutez votre dossier de mp3s</button>
		<div className="dropzone"> <h2 style={{color:'blue'}}> SMART PLAYER </h2> </div>
      </Dropzone>
    )
  }

  render() {
    return (
      <div>
        {this.renderPlayer()}
        {this.renderListOrDropZone()}

      </div>
    )
  }

}

render(<App />, document.getElementById('root'));
