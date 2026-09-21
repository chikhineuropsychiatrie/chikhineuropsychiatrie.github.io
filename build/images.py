"""Versions WebP des images du site, creees au besoin a chaque generation.

Pour chaque JPEG ou PNG de assets/img : une copie WebP a la meme taille et, pour
les grandes images, des variantes plus etroites (suffixes -800, -1200) parmi
lesquelles le navigateur choisit selon la largeur d'affichage (attribut sizes).
Les originaux restent en place : navigateurs anciens, apercus de partage.
"""
import os
from PIL import Image, ImageOps

# Icones d'onglet et images de partage (og-*) : jamais affichees par une balise <img>.
EXCLUS = {"icon-96.png", "icon-192.png"}


def largeurs(w):
    l = {w}
    if w > 900:
        l.add(800)
    if w >= 1500:
        l.add(1200)
    return sorted(l)


def nom_webp(base, lw, w):
    return "%s%s.webp" % (base, "" if lw == w else "-%d" % lw)


def preparer(dossier):
    """Cree les WebP manquants ou perimes ; renvoie {original: [largeurs, croissantes]}."""
    table = {}
    for nom in sorted(os.listdir(dossier)):
        base, ext = os.path.splitext(nom)
        if ext.lower() not in (".jpg", ".jpeg", ".png") or nom in EXCLUS or nom.startswith("og-"):
            continue
        src = os.path.join(dossier, nom)
        with Image.open(src) as im:
            w, h = im.size
            if im.getexif().get(0x0112, 1) in (5, 6, 7, 8):   # photo tournee d'un quart de tour
                w, h = h, w
            dispo = largeurs(w)
            a_faire = [lw for lw in dispo
                       if not os.path.exists(os.path.join(dossier, nom_webp(base, lw, w)))
                       or os.path.getmtime(os.path.join(dossier, nom_webp(base, lw, w))) < os.path.getmtime(src)]
            if a_faire:
                icc = im.info.get("icc_profile")
                im = ImageOps.exif_transpose(im)      # l'orientation EXIF n'est pas reprise en WebP
                for lw in a_faire:
                    v = im if lw == w else im.resize((lw, round(h * lw / w)), Image.LANCZOS)
                    opts = {"method": 6}
                    if icc:
                        opts["icc_profile"] = icc
                    if ext.lower() == ".png":
                        opts["lossless"] = True
                    else:
                        v, opts["quality"] = v.convert("RGB"), 80
                    v.save(os.path.join(dossier, nom_webp(base, lw, w)), "WEBP", **opts)
        table[nom] = dispo
    return table
