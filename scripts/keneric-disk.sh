#!/bin/bash

#############
## Version ##
#############
# Création de dossier CD pour les fichiers ~ disk.png, necessite le fichier baseDisk.png

# Utilisation : keneric FullName mime exportPicture

FullName="$1"
MimeType="$2"
ExportPicture="$3"
Thumb="${ExportPicture##*/}"

# Si on veut un peu mieux comprendre
# echo "keneric $1 $2 $3 $Thumb" >> /tmp/hizo.txt


# Si la vignette existe déjà, on ne fait rien, n'est pas sensé se produire
[[ -e "${HOME}/.cache/thumbnails/large/${Thumb}.png" || -e "${HOME}/.cache/thumbnails/normal/${Thumb}.png" ]] && exit


function Dependencies
{
    # ${@} : Les arguments doivent être de type : commande:paquet ou commande (si paquet = commande)

    local Command

    # Vérification des dépendances
    for Command in "${@}"
    do
        # Si la commande n'existe pas
        [[ -z $(which ${Command}) ]] && return 1
    done

    return 0
}


# En fonction du type des fichiers
case "${MimeType}" in
    inode/directory)
        Dependencies convert identify || exit 1

        # S'il y a un fichier NoKeneric, on ne fait rien
        Image="$(find "${FullName}" -maxdepth 1 ! -type d -iregex "${FullName/%\/}/\.?NoKeneric" -print -quit)"
        [[ -f "${Image}" ]] && exit 0

        # S'il y a un fichier disk, on l'utilise comme image pour créer une pochette CD
        Image="$(find "${FullName}" -maxdepth 1 ! -type d -iregex "${FullName/%\/}/\.?disk.\(jpg\|png\|jpeg\|webp\)" -print -quit)"

        if [[ -f "${Image}" ]]
        then
            # Il faut obligatoirement mettre une extension png pour le convert
            convert -size 228x228 canvas:transparent \( "${Image}" -resize 200!x200! -bordercolor black -border 2 \) -geometry +0+12 -composite "baseDisk.png" -geometry +166+48 -composite -format png "${ExportPicture}.png" 2>> /tmp/keneric.log

            # Suppression de l'extension
            mv "${ExportPicture}.png" "${ExportPicture}"
        fi

        exit 0 ;;
esac

