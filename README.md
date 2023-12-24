# keneric

## Version Française :
### Description :
keneric est un générateur de vignettes pour plasma KDE5 qui utilise un script (bash ou python) pour créer ces vignettes.

Il a été créé par Rog131 <samrog131@hotmail.com>.

Voici les modifications apportées par mes soins :
 - Le nom de la vignette temporaire est maintenant le hash md5 du fichier de la vignette finale.
 - Le script exécuté a été renommé de stripPicture à keneric.
 - Ajout de l'utilisation d'un fichier conf.

### Installation :
#### Depuis les sources :
Pour les dérivés d'Ubuntu, la compilation necessite les paquets : **cmake extra-cmake-modules libkf5kio-dev build-essential kio-dev**.

Une fois dans le dossier, le plus simple est de procéder ainsi :
```
mkdir builddir
cd builddir
cmake ..
sudo make install
```
Le fichier **/usr/lib/x86_64-linux-gnu/qt5/plugins/keneric.so** est créé.

#### Depuis le binaire :
Extraire le binaire du fichier tar.gz : **https://github.com/Hizoka76/keneric/releases/latest**.

Le déplacer dans le dossier **/usr/lib/x86_64-linux-gnu/qt5/plugins/**.

#### Depuis le dépôt :
Installer le ppa pour les dérivés d'Ubuntu et installer le paquet :
```
sudo add-apt-repository ppa:hizo/service-menus
sudo apt-get update
sudo apt install keneric
```

#### Souci avec Dolphin :
Si ça ne fonctionne pas avec le navigateur de fichiers Dolphin, supprimer le groupe [PreviewSettings] du fichier ~/.config/dolphinrc.

### Principe de fonctionnement :
#### Fichiers desktop:
Ces fichiers font le lien entre le navigateur de fichiers (comme Dolphin ou Konqueror) et keneric.

Le navigateur de fichiers reconnait ces fichiers desktop comme des générateurs de vignettes, ils sont (dés)activables dans Dolphin : Configurer > Configurer Dolphin > Genéral > Aperçu

Lorsque le navigateur verra un élément au mimetype déclaré dans un de ces fichiers desktop, il appelera keneric afin qu'il lui fournisse une vignette.

Les fichiers desktop doivent être placés dans un dossier défini par la commande :
```
kf5-config --path services
```
Le [dossier desktop](desktop) contient des fichiers fonctionnels.

#### Fichier keneric.so :
Voir ci-dessus pour son installation.

Il appelle le script keneric et attent que celui-ci lui rende la main et lui fournisse une vignette.

Si la vignette est valide, elle sera chargée et fournie au navigateur de fichiers qui l'affichera.

La vignette temporaire fournie par le script à keneric.so est déplacée dans le dossier cache.

#### Script keneric :
Ce script est appelé par keneric.so qui lui fourni les arguments suivants :
 - Le fichier en attente de vignette.
 - Le mimetype du fichier en attente de vignette.
 - L'emplacement et le nom de la vignette que doit être retournée à keneric.so.

Le script doit être placé dans un dossier du path :
```
echo "$PATH"
```

#### Scripts sourcés par keneric :
Afin de faciliter le développement de nouvelles fonctionnalités, keneric charge des sous-scripts.
Toutes les explications sur le fonctionnement des sous-scripts sont dans le [dossier script](scripts).


#### Fichier keneric.conf :
Fichier présent à l'adresse ~/.config/keneric.conf.
Il est utilisé par keneric.so et par le script keneric.

Toutes les informations sur le fichier sont dans le [dossier config](config)


### Exemples de rendus possibles :
#### Script Directory-Covert : Avec un fichier "cover" dans le dossier.
![Directory-Cover](/readme/Directory-Cover.png)


#### Script Directory-Disk : Avec un fichier "disk" dans le dossier.
![Directory-Disk](/readme/Directory-Disk.png)


#### Script Directory-Full : Avec un fichier "full" dans le dossier.
![Directory-Full](/readme/Directory-Full.png)


#### Script Video-mkv-Cover : Avec une image dans un fichier mkv.
La couleur du contour s'adapte à la résolution de la vidéo et à la 3D.
![Video-mkv-Cover](/readme/Video-mkv-Cover.png)


### Services :
Des services en liens sont égalements proposés :
 - Le [dossier KenericHashFile](KenericHashFile) propose de copier le hash d'un élément.
 - Le [dossier KenericRemoveThumbnails](KenericRemoveThumbnails) propose de supprimer les vignettes d'éléments.
 - Le [dossier KenericCustomIcon](KenericCustomIcon) propose de facilité l'utilisation de vignettes personnalisées.
 - Le [dossier KenericDeleteCustomIcon](KenericDeleteCustomIcon) propose de supprimer les vignettes personnalisées.


## English version:
### Description:
keneric is a thumbnail generator for KDE5 plasma that uses a script (bash or python) to create these thumbnails.

It was created by Rog131 <samrog131@hotmail.com>.

Here are the changes I made:
 - The name of the temporary thumbnail is now the md5 hash of the final thumbnail file.
 - The executed script has been renamed from stripPicture to keneric.
 - Added the use of a conf file.

### Installation:
#### From source:
For Ubuntu derivatives, compilation requires the following packages: **cmake extra-cmake-modules libkf5kio-dev build-essential kio-dev**.

Once in the folder, the easiest way is to proceed as follows:
```
mkdir builddir
cd builddir
cmake .
sudo make install
```
The file **/usr/lib/x86_64-linux-gnu/qt5/plugins/keneric.so** is created.

#### From the binary :
Extract binary from tar.gz file: **https://github.com/Hizoka76/keneric/releases/latest**.

Move it to the **/usr/lib/x86_64-linux-gnu/qt5/plugins/** folder.

#### From the repository:
Install the ppa for Ubuntu derivatives and install its package:
```
sudo add-apt-repository ppa:hizo/service-menus
sudo apt-get update
sudo apt install keneric
```

#### Dolphin problem:
If it doesn't work with the Dolphin file browser, remove the [PreviewSettings] group from the ~/.config/dolphinrc file.

### How it works:
#### Desktop files:
These files form the link between the file browser (such as Dolphin or Konqueror) and keneric.

The file browser recognizes these desktop files as thumbnail generators, and they can be (des)activated in Dolphin: Configure > Configure Dolphin > General > Preview.

When the browser sees an element with the declared mimetype in one of these desktop files, it will call keneric to provide a thumbnail.

Desktop files must be placed in a folder defined by the command:
```
kf5-config --path services
```
The [desktop folder](desktop) contains functional files.

#### keneric.so file:
See above for installation.

It calls the keneric script and waits for it to give it a thumbnail.

If the thumbnail is valid, it will be loaded and supplied to the file browser, which will display it.

The temporary thumbnail supplied by the script to keneric.so is moved to the cache folder.

#### Script keneric :
This script is called by keneric.so, which supplies it with the following arguments:
 - The file to be thumbnailed.
 - The mimetype of the file awaiting thumbnailing.
 - The location and name of the thumbnail to be returned to keneric.so.

The script must be placed in a folder of path :
```
echo "$PATH"
```

#### Scripts sourced by keneric :
To facilitate the development of new features, keneric loads sub-scripts.
A full explanation of how sub-scripts work can be found in the [script folder](scripts).


#### keneric.conf file:
File located at ~/.config/keneric.conf.
It is used by keneric.so and by the keneric script.

All information on the file is in the [config folder](config).


### Examples of possible renderings :
#### Directory-Covert script: With a "cover" file in the folder.
![Directory-Cover](/readme/Directory-Cover.png)


#### Script Directory-Disk: With a "disk" file in the folder.
![Directory-Disk](/readme/Directory-Disk.png)


#### Script Directory-Full: With a "full" file in the folder.
![Directory-Full](/readme/Directory-Full.png)


#### Script Video-mkv-Cover: With an image in an mkv file.
Contour color adapts to video resolution and 3D.
![Video-mkv-Cover](/readme/Video-mkv-Cover.png)


### Services :
Linked services are also available:
 - The [KenericHashFile](KenericHashFile) folder lets you copy an element's hash.
 - The [KenericRemoveThumbnails folder](KenericRemoveThumbnails) lets you delete thumbnails.
 - The [KenericCustomIcon folder](KenericCustomIcon) facilitates the use of custom thumbnails.
 - The [KenericDeleteCustomIcon](KenericDeleteCustomIcon) folder lets you delete custom thumbnails.
