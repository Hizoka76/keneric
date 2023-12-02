# keneric

## Version Française :
Si ça ne fonctionne pas avec le navigateur Dolphin, supprimer le groupe [PreviewSettings] du fichier ~/.config/dolphinrc.

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
Extraire le binaire du fichier tar.gz : **https://github.com/Hizoka76/keneric/releases/latest**.

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
![01](https://user-images.githubusercontent.com/48289933/150758696-587cdf89-2abb-4936-8792-16f18d5f1a03.png)

Le dossier Animaux affiche seulement une image portant un nom spécifique et le met en valeur dans un cadre.

Le fichier Test.mkv affiche une image qu'il contient.

Le fichier Test2.mkv affiche une icône personnalisée via le fichier keneric.conf.

![border-exemples](https://github.com/Hizoka76/keneric/assets/48289933/91746874-6615-4f0d-8be2-cd2ebd41c4a6)

Adaptation du contour de la vidéo à sa qualité : script/keneric-border-color

![05](https://github.com/Hizoka76/keneric/assets/48289933/f8974a59-eb0f-4495-b11c-d66c09244593)

Dossier d'un album musical : script/keneric-disk

![06](https://github.com/Hizoka76/keneric/assets/48289933/61d04a94-cae2-449a-a022-1f0ad2a1c625)

Dossier d'une saison d'une série : script/keneric-full

### Plus d'informations :
 - Le dossier conf présente le fonctionnement du fichier de configuration et donne des exemples.
 - Le dossier KenericHashFile présente un service menu copiant le hash d'un élément.
 - Le dossier KenericRemoveThumbnails présente un service menu supprimant les vignettes d'éléments.
 - Le dossier KenericCustomIcon présente un service menu facilitant l'utilisation de vignettes personnalisées.
 - Le dossier KenericDeleteCustomIcon présente un service menu facilitant la suppression de vignettes personnalisées.

##

## English version:
If it doesn't work with the Dolphin browser, remove the [PreviewSettings] group from the ~/.config/dolphinrc file.

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
Extract the binary from the tar.gz file : **https://github.com/Hizoka76/keneric/releases/latest**.

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
![01](https://user-images.githubusercontent.com/48289933/150758696-587cdf89-2abb-4936-8792-16f18d5f1a03.png)

The Animaux folder displays only one item based on its name and puts it in a frame.

The Test.mkv file displays an image it contains.

The Test2.mkv file displays an custom icon via the keneric.conf file.

![border-exemples](https://github.com/Hizoka76/keneric/assets/48289933/91746874-6615-4f0d-8be2-cd2ebd41c4a6)

Adapt video contour to video quality: script/keneric-border-color

![05](https://github.com/Hizoka76/keneric/assets/48289933/f8974a59-eb0f-4495-b11c-d66c09244593)

Musical album folder: script/keneric-disk

![06](https://github.com/Hizoka76/keneric/assets/48289933/61d04a94-cae2-449a-a022-1f0ad2a1c625)

Series season file: script/keneric-full

### More information:
 - The conf folder presents how the configuration file works and gives examples.
 - The KenericHashFile folder presents a menu service copying the hash of an item.
 - The KenericRemoveThumbnails folder presents a menu service deleting thumbnails of items.
 - The KenericCustomIcon folder presents a menu service to facilitate the use of custom icons.
 - The KenericDeleteCustomIcon folder presents a menu service to facilitate the deletion of custom thumbnails.

