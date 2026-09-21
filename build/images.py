"""Versions WebP des images du site, creees au besoin a chaque generation.

Pour chaque JPEG ou PNG de assets/img : une copie WebP a la meme taille et, pour
les grandes images, des variantes plus etroites (suffixes -800, -1200) parmi
lesquelles le navigateur choisit selon la largeur d'affichage (attribut sizes).
Les originaux restent en place : navigateurs anciens, apercus de partage.

Les images sont suivies par empreinte de contenu (build/images-webp.json), pas par
date de fichier : une generation sur une copie neuve du depot ne refait rien. Une
image nouvelle ou remplacee est d'abord nettoyee (voir nettoyer).
"""
import hashlib, json, os
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


def empreinte(chemin):
    with open(chemin, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()


def nettoyer(src):
    """Photo deposee telle quelle (telephone) : orientation appliquee, metadonnees
    retirees (dont la position GPS), plus grand cote ramene a 1600 px."""
    with Image.open(src) as im:
        if not im.getexif() and max(im.size) <= 2000:
            return
        fmt, icc = im.format, im.info.get("icc_profile")
        v = ImageOps.exif_transpose(im)
        v.thumbnail((1600, 1600), Image.LANCZOS)
    opts = {"icc_profile": icc} if icc else {}
    if fmt == "PNG":
        v.save(src, "PNG", optimize=True, **opts)
    else:
        v.convert("RGB").save(src, "JPEG", quality=85, optimize=True, progressive=True, **opts)


def preparer(dossier, manifeste):
    """Cree les WebP manquants ou perimes ; renvoie {original: [largeurs, croissantes]}."""
    connu = json.load(open(manifeste, encoding="utf-8")) if os.path.exists(manifeste) else None
    table, suivi = {}, {}
    for nom in sorted(os.listdir(dossier)):
        base, ext = os.path.splitext(nom)
        if ext.lower() not in (".jpg", ".jpeg", ".png") or nom in EXCLUS or nom.startswith("og-"):
            continue
        src = os.path.join(dossier, nom)
        change = connu is not None and connu.get(nom) != empreinte(src)   # nouvelle ou remplacee
        if change:
            nettoyer(src)
        with Image.open(src) as im:
            w, h = im.size
            if im.getexif().get(0x0112, 1) in (5, 6, 7, 8):   # photo tournee d'un quart de tour
                w, h = h, w
            dispo = largeurs(w)
            a_faire = [lw for lw in dispo
                       if change or not os.path.exists(os.path.join(dossier, nom_webp(base, lw, w)))]
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
        suivi[nom] = empreinte(src)
    # WebP produits ici pour une image depuis retiree : supprimes avec elle (jamais un
    # .webp depose tel quel, qui n'a pas d'original suivi).
    for n in connu or {}:
        if n not in table:
            for suffixe in ("", "-800", "-1200"):
                p = os.path.join(dossier, os.path.splitext(n)[0] + suffixe + ".webp")
                if os.path.exists(p):
                    os.remove(p)
    with open(manifeste, "w", encoding="utf-8", newline="\n") as f:
        json.dump(suivi, f, indent=1, sort_keys=True)
        f.write("\n")
    return table
