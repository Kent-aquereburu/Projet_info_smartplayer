
import json
import io
import re
from string import printable
import subprocess
import wave
import struct
import numpy as np
import os
import sys, ast, getopt, types
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.metrics import silhouette_samples, silhouette_score

try:
    to_unicode = unicode
except NameError:
    to_unicode = str

def read_wav(wav_file):
    """ Charge un fichier wav et renvoie 2 extraits tires aleatoirement"""
    w = wave.open(wav_file)
    n = 60 * 10000
    if w.getnframes() < n * 2:
        raise ValueError('Le fichier est trop court')
    frames = w.readframes(n)
    wav_data1 = struct.unpack('%dh' % n, frames)
    frames = w.readframes(n)
    wav_data2 = struct.unpack('%dh' % n, frames)
    return wav_data1, wav_data2

def moments(x):
    mean = x.mean()
    std = x.var()**0.5
    skewness = ((x - mean)**3).mean() / std**3
    kurtosis = ((x - mean)**4).mean() / std**4
    return [mean, std, skewness, kurtosis]

def fftfeatures(wavdata):
    f = np.fft.fft(wavdata)
    f = f[2:(f.size / 2 + 1)]
    f = abs(f)
    total_power = f.sum()
    f = np.array_split(f, 10)
    return [e.sum() / total_power for e in f]

def features(x):
    x = np.array(x)
    f = []

    xs = x
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 10).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 100).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    xs = x.reshape(-1, 1000).mean(1)
    diff = xs[1:] - xs[:-1]
    f.extend(moments(xs))
    f.extend(moments(diff))

    f.extend(fftfeatures(x))
    return f


def compute_chunk_features(mp3_file):
    """Fonction qui prend un fichier mp3 calcule les features pour 2 extraits de chaque fichier tires aleatoirement."""
    # On convertit le fichier mp3 en un fichier wav mono, 1avec un sample rate de 10000Hertz: on utilise
    # On utilise l'application sox "c:/Program Files (x86)/sox-14.4.0/sox"

    sox_command = "./sox-14.4.0/sox"
    out_file = 'temp.wav'
    #cmd = sox_command % (out_file, mp3_file)
    temp2 = subprocess.call([sox_command, mp3_file,'-r 10000','-c 1',out_file])
    # Read in chunks of data from WAV file
    wav_data1, wav_data2 = read_wav(out_file)
    # We'll cover how the features are computed in the next section!
    return np.array(features(wav_data1)), np.array(features(wav_data2))



def clustering(files):
  #Fonction globale qui execute toute l'analyse
  filelist=[]
  featurelist1=[  ]
  featurelist2=[]

  for file in files:

      try:
          feature_vec1, feature_vec2 = compute_chunk_features(file)
      except:
          print("erreur d'extraction")
          continue
      tail, track = os.path.split(file)
      tail, dir1 = os.path.split(tail)
      title = str(dir1)+'\\\\'+str(track)
      filelist.append(track)
      featurelist1.append(feature_vec1)
      #featurelist2.append(feature_vec2)

  features_names = ["amp1mean","amp1std","amp1skew","amp1kurt","amp1dmean","amp1dstd","amp1dskew","amp1dkurt","amp10mean","amp10std",
              "amp10skew","amp10kurt",
              "amp10dmean","amp10dstd","amp10dskew","amp10dkurt","amp100mean","amp100std","amp100skew",
              "amp100kurt","amp100dmean","amp100dstd","amp100dskew","amp100dkurt","amp1000mean","amp1000std","amp1000skew",
              "amp1000kurt","amp1000dmean","amp1000dstd","amp1000dskew","amp1000dkurt","power1","power2","power3","power4",
              "power5","power6","power7","power8","power9","power10"]

  #On met les features dans un dataframe
  datatrain1 = pd.DataFrame(index=filelist,data=np.array(featurelist1),columns=features_names)

  #datatrain2 = pd.DataFrame(index=filelist,data=np.array(featurelist2),columns=FeatNames)


  # NORMALISATION DES FEATURES
  data = scale(datatrain1.ix[:,1:])

  # REDUCTION DE LA DIMENSION VIA UNE ACP (ANALYSE EN COMPOSANTES PRINCIPALES)
  reduced_data = PCA(n_components=2).fit_transform(data)

  # CLUSTERING DES DONNEES REDUITES AVEC KMEANS
  #POUR LE MOMENT ON FIGE LE NOMBRE DE CLUSTERS A 3
  kmeans = KMeans(init='k-means++', n_clusters=3,n_init=50,max_iter=600,n_jobs=2,random_state=10)
  kmeans.fit(reduced_data)

  #ON PREDIT LES CLUSTERS DE CHAQUE GROUPES
  pred = kmeans.predict(reduced_data)

  #
  groupes = pd.Series(index=datatrain1.index,data=pred, name="cluster")

  Music_clusters = groupes.reset_index().to_dict(orient='records')

  msc = json.dumps(Music_clusters, indent=4)

  # ON PRINT LE RESULTAT EN JSON DANS LA CONSOLE POUR POUVOIR LE RECUPERER DANS L'INTERFACE EN JAVASCRIPT
  print(msc)



if __name__ == '__main__':
    # On recupere le fichier json contenant les chemins vers les fichiers mp3s a analyser
    # Ce fichier a ete cree par javascript au moment de l'ajout des fichiers par l'utilisateur
    with open('./newMp3s.json') as data_file:
        files = json.load(data_file)

    #print(files)


    clustering(files)
