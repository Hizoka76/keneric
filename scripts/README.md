# Scripts
## Version Française :
### Présentation:
Ces sous-scripts doivent être dans le même dossier que le script keneric et être nommés en se basant sur le mimetype qu'ils traitent afin d'être correctement sourcés :
 - Avec un sous-script traitant les "video/x-matroska" : keneric-video-x-matroska-[0-9][0-9][0-9]-nom_script
 - Avec un sous-script traitant les "x-matroska" : keneric-x-matroska-[0-9][0-9][0-9]-nom_script
 - Avec un sous-script traitant les "video" : keneric-video-[0-9][0-9][0-9]-nom_script

Ils seront chargés dans l'ordre ci-dessus puis par nom, d'où l'intérêt des [0-9][0-9][0-9] qui permettent de les prioriser.

Donc, pour un fichier avec un mimetype video/x-matroska :
  Keneric recherche des sous-scripts commençants par keneric-video-x-matroska.
    S'il y en a : keneric-video-x-matroska-**001**-mkv-cover sera chargé avant keneric-video-x-matroska-**010**-mkv-other.
      Si un sous-script crée la vignette attendue, le script s’arrêtera.

  Si la vignette n'est toujours pas créée, keneric recherche des sous-scripts commençants par keneric-x-matroska.
    S'il y en a : keneric-x-matroska-**001**-mkv-cover sera chargé avant keneric-x-matroska-**010**-mkv-other.
      Si un sous-script crée la vignette attendue, le script s’arrêtera.

  Si la vignette n'est toujours pas créée, keneric recherche des sous-scripts commençants par keneric-video.
    S'il y en a : keneric-video-**001**-mkv-cover sera chargé avant keneric-video-**010**-mkv-other.
      Si un sous-script crée la vignette attendue, le script s’arrêtera.

### Explications des sous-scripts :
Ils peuvent utiliser les fonctions partagées suivantes :
    **Dependencies** : À utiliser pour vérifier des dépendances avant d'utiliser les commandes liées.
    **SearchInFolder** : Utile pour la recherche d'un fichier dans un dossier
    **LogFileMessage** : Fonction d'envoi de message au fichier log s'il est actif.
        Ex de message : **LogFileMessage** "NoKeneric file found : ${Image}"
        Ex de message d'erreur : convert ...  **|& LogFileMessage**

Ils peuvent utiliser les variables globales :
    **FullName** : Adresse du fichier/dossier.
    **MimeType** : Mimetype du fichier/dossier.
    **ExportPicture** : Adresse de la vignette du fichier/dossier qui sera reprise par keneric.
    **Thumb** : Nom de la vignette attendue
    **ExecFolder** : Dossier du script keneric.
    **LogRedirection** : Sorite des retours des messages log.

Toujours déclarer les variables (avec leurs valeurs par défaut) avant de les tester afin d'éviter qu'un précédent sous-script ait créé des variables portant le même nom.

Un sous-script ne doit pas faire de return ou d'exit.
Un sous-script ayant créé la vignette doit l'avoir exportée vers **${ExportPicture}** et faire un **ThumbCreated=1** afin de terminer le script keneric.

## English version:
### Introducing:
These sub-scripts must be in the same folder as keneric and named according to the mimetype they handle, in order to be properly sourced:
 - With sub-script processing "video/x-matroska": keneric-video-x-matroska-[0-9][0-9][0-9]-script_name
 - With sub-script processing "x-matroska": keneric-x-matroska-[0-9][0-9][0-9]-script_name
 - With sub-script processing "video": keneric-video-[0-9][0-9][0-9]-script_name

They will be loaded in the above order, then by name, which is why [0-9][0-9][0-9] is useful for prioritizing them.

So, for a file with mimetype video/x-matroska :
  Keneric searches for sub-scripts starting with keneric-video-x-matroska.
    If there are any: keneric-video-x-matroska-**001**-mkv-cover will be loaded before keneric-video-x-matroska-**010**-mkv-other.
      If a sub-script creates the expected thumbnail, the script will stop.

  If the thumbnail is still not created, keneric searches for sub-scripts starting with keneric-x-matroska.
    If there are any, keneric-x-matroska-**001**-mkv-cover will be loaded before keneric-x-matroska-**010**-mkv-other.
      If a sub-script creates the expected thumbnail, the script will stop.

  If the thumbnail is still not created, keneric searches for sub-scripts starting with keneric-video.
    If there are any, keneric-video-**001**-mkv-cover will be loaded before keneric-video-**010**-mkv-other.
      If a sub-script creates the expected thumbnail, the script will stop.

### Sub-scripts explanation:
They can use shared functions:
    **Dependencies**: Use to check dependencies before using linked commands.
    **SearchInFolder**: Useful for searching for a file in a folder.
    **LogFileMessage**: Sends a message to the log file if it is active.
        Example message: **LogFileMessage** "NoKeneric file found: ${Image}".
        Example of error message: convert ...  **|& LogFileMessage**

They can use the global variables :
    **FullName**: File/folder address.
    **MimeType**: Mimetype of the file/folder.
    **ExportPicture**: Address of the file/folder thumbnail to be exported by keneric.
    **Thumb**: Name of the expected thumbnail.
    **ExecFolder**: Folder of the keneric script.
    **LogRedirection**: Output of log message returns.

Always declare variables (with their default values) before testing them, to avoid a previous script having created variables with the same name.

A script must not return or exit.
A script that has created the thumbnail must have exported it to **${ExportPicture}** and done a **ThumbCreated=1** in order to terminate the keneric script.
