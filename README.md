# keneric

## Version Française :
### Description :
keneric est un générateur de vignettes pour plasma KDE5 qui utilise un script (bash ou python) pour créer ces vignettes.

Il a été créé par Rog131 <samrog131@hotmail.com>.

Voici les modifications apportées :
 - Le nom de la vignette temporaire est maintenant le hash md5 du fichier de la vignette finale.
 - Le script exécuté a été renommé de stripPicture à keneric.
 - L'utilisation d'un fichier conf est maintenant ajoutée.

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
Extraire le contenu d'un fichier deb depuis le ppa : **https://launchpad.net/~hizo/+archive/ubuntu/service-menus/+packages**.

Le déplacer dans le dossier **/usr/lib/x86_64-linux-gnu/qt5/plugins/**.

#### Depuis le dépôt :
Installer le ppa pour les dérivés d'Ubuntu et installé le paquet :
```
sudo add-apt-repository ppa:hizo/service-menus
sudo apt-get update
sudo apt install keneric
```

### Principe de fonctionnement :
#### Fichiers desktop:
Ces fichiers font le lien entre le navigateur de fichier (comme Dolphin ou Konqueror) et keneric.

Lorsque le navigateur verra un élément au mimetype déclaré dans un de ces fichiers desktop, il appelera keneric afin qu'il lui fournisse une vignette.

Ils doivent être placés dans un dossier défini par la commande :
```
kf5-config --path services
```
Des fichiers desktop d'exemples sont visibles dans le dossier desktop des sources ici-présentes.

#### Fichier keneric.so :
Voir ci-dessus pour son installation.

Il appelle le script keneric et attent que celui-ci lui rende la main et lui fournisse une vignette.

Si la vignette est valide, elle sera chargée et fournie au navigateur de fichier qui l'affichera.

La vignette temporaire fournie par le script est supprimée.

Une vignette finale est créée dans le dossier cache.

#### Script keneric :
Ce script est appelé par keneric.so qui lui fourni les arguments suivants :
 - Le fichier en attente de vignette.
 - Le mimetype du fichier en attente de vignette.
 - L'emplacement et le nom de la vignette que doit fournir le script à keneric.so.

   => Le nom de la vignette est le même que celui qui sera utilisé pour la vignette finale.

Ce script n'a pas d'extension afin de permettre l'utilisation de plusieurs langages comme python ou bash.

Le script doit être déplacé dans un dossier du path :
```
echo "$PATH"
```

Des exemples de scripts sont disponibles dans le dossier scripts des sources ici-présentes.

### Exemples :
![01](https://user-images.githubusercontent.com/48289933/150208006-e48bb97d-a754-47b0-ac8f-a8050734962f.png)

Le dossier n'affiche qu'un seul élément en fonction de son nom et le met dans un cadre.

Le fichier mkv affiche une image qu'il contient.


## English version:
### Description:
keneric is a thumbnail generator for KDE5 plasma that uses a script (bash or python) to create these thumbnails.

It was created by Rog131 <samrog131@hotmail.com>.

Here are the changes made:
 - The name of the temporary thumbnail is now the md5 hash of the final thumbnail file.
 - The script being run has been renamed from stripPicture to keneric.
 - The use of a conf file is now added.

### Installation:
#### From source:
For Ubuntu derivatives, the compilation requires the packages: **cmake extra-cmake-modules libkf5kio-dev build-essential kio-dev**.

Once in the folder, the easiest way is to proceed as follows:
```
mkdir builddir
cd builddir
cmake ..
sudo make install
```
The file **/usr/lib/x86_64-linux-gnu/qt5/plugins/keneric.so** is created.

#### From the binary :
Extract the contents of a deb file from the ppa: **https://launchpad.net/~hizo/+archive/ubuntu/service-menus/+packages**.

Move it into the folder **/usr/lib/x86_64-linux-gnu/qt5/plugins/**.

#### From the repository :
Install the ppa for Ubuntu derivatives and install the package:
```
sudo add-apt-repository ppa:hizo/service-menus
sudo apt-get update
sudo apt install keneric
```

### How it works :
#### Desktop files:
These files are the link between the file browser (like Dolphin or Konqueror) and keneric.

When the browser sees an element with the declared mimetype in one of these desktop files, it will call keneric to provide a thumbnail.

They must be placed in a folder defined by the command :
```
kf5-config --path services
```
Example desktop files are visible in the desktop folder of the sources here.

#### File keneric.so :
See above for its installation.

It calls the keneric script and waits for it to give it a thumbnail.

If the thumbnail is valid, it will be loaded and provided to the file browser which will display it.

The temporary thumbnail provided by the script is deleted.

A final thumbnail is created in the cache folder.

#### keneric script:
This script is called by keneric.so which provides it with the following arguments:
 - The file waiting for the thumbnail.
 - The mimetype of the file waiting for the thumbnail.
 - The location and the name of the thumbnail that the script must provide to keneric.so.

   => The name of the thumbnail is the same as the one that will be used for the final thumbnail.

This script has no extension to allow the use of several languages like python or bash.

The script must be moved to a folder in the path :
```
echo "$PATH"
```

Examples of scripts are available in the scripts folder of the sources here.

### Examples:
![01](https://user-images.githubusercontent.com/48289933/150208006-e48bb97d-a754-47b0-ac8f-a8050734962f.png)

The folder displays only one item based on its name and puts it in a frame.

The mkv file displays an image it contains.

