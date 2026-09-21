# -*- coding: utf-8 -*-
"""Articles rediges en Markdown : un fichier par article dans contenu/articles/.

Un en-tete entre deux lignes « --- » (titre, date, image...), puis le texte.
Mode d'emploi : contenu/articles/LISEZ-MOI.md. Sont ignores les fichiers dont le
nom commence par « _ » (le modele) et ceux marques « brouillon: oui ».
"""
import html, os, re, unicodedata
import markdown

CHAMPS = {"titre", "date", "resume", "image", "legende_image", "mots_cles", "auteur",
          "fonction_auteur", "description", "titre_seo", "brouillon"}


def slug(texte):
    s = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def couper(texte, n):
    """Coupe a n caracteres au plus, sur une fin de mot."""
    if len(texte) <= n:
        return texte
    return texte[:n].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"


def lire(chemin):
    texte = open(chemin, encoding="utf-8-sig").read().replace("\r\n", "\n")
    m = re.match(r"\s*---[ \t]*\n(.*?)\n---[ \t]*\n(.*)", texte, re.S)
    if not m:
        raise ValueError("l'en-tête doit être encadré par deux lignes ---")
    meta = {}
    for ligne in m.group(1).splitlines():
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            continue
        cle, sep, val = ligne.partition(":")
        cle = slug(cle).replace("-", "_")          # « Mots clés » -> mots_cles
        if not sep or cle not in CHAMPS:
            raise ValueError("ligne d'en-tête non reconnue : %r" % ligne.strip())
        meta[cle] = val.strip()
    return meta, m.group(2)


def date_iso(val):
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", val) or re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", val)
    if not m:
        raise ValueError("date attendue sous la forme 2026-10-05 (ou 05/10/2026) : %r" % val)
    a, b, c = m.groups()
    return "%s-%s-%s" % ((a, b, c) if len(a) == 4 else (c, b, a))


def corps_html(texte):
    h = markdown.markdown(texte, extensions=["sane_lists"], output_format="html")
    # Le titre de l'article est le seul <h1> de la page : les intertitres commencent a <h2>.
    if re.search(r"<h1\b", h):
        h = re.sub(r"<(/?)h([1-5])\b", lambda m: "<%sh%d" % (m.group(1), int(m.group(2)) + 1), h)
    if "<pre" in h:
        return h
    return "\n".join("    " + l if l.strip() else l for l in h.splitlines())


def article(chemin, dossier_img):
    meta, texte = lire(chemin)
    if meta.get("brouillon", "").lower() in ("oui", "o", "yes", "true", "1"):
        return None
    for requis in ("titre", "date"):
        if not meta.get(requis):
            raise ValueError("champ « %s » manquant" % requis)
    image = meta.get("image", "")
    if image and not os.path.exists(os.path.join(dossier_img, image)):
        raise ValueError("image introuvable dans assets/img : %r" % image)
    corps = corps_html(texte)
    premier = re.search(r"<p>(.*?)</p>", corps, re.S)
    brut = html.unescape(re.sub(r"<[^>]+>", "", premier.group(1))).strip() if premier else ""
    resume = meta.get("resume") or couper(" ".join(brut.split()), 215)
    auteur = meta.get("auteur", "")
    if re.search(r"bengougam|^(la-)?(dr|docteur|docteure)-(f-)?chikhi$", slug(auteur)):
        auteur = ""                                 # le Dr Chikhi : auteur par defaut
    a = {
        "slug": slug(os.path.splitext(os.path.basename(chemin))[0]),
        "title": meta["titre"],
        "date": date_iso(meta["date"]),
        "image": image,
        "alt": meta.get("legende_image", ""),
        "excerpt": resume,
        "body": corps,
        "description": meta.get("description") or couper(resume, 160),
        "keywords": [k.strip() for k in meta.get("mots_cles", "").split(",") if k.strip()],
    }
    if meta.get("titre_seo"):
        a["seo_title"] = meta["titre_seo"]
    if auteur:
        a["author"] = auteur
        if meta.get("fonction_auteur"):
            a["author_role"] = meta["fonction_auteur"]
    return a


def fusionner(articles, dossier, dossier_img):
    """Ajoute les articles Markdown a ceux de articles.json, du plus recent au plus ancien."""
    if not os.path.isdir(dossier):
        return articles
    nouveaux = []
    for nom in sorted(os.listdir(dossier)):
        if not nom.lower().endswith(".md") or nom.startswith("_") or nom.upper().startswith("LISEZ"):
            continue
        try:
            a = article(os.path.join(dossier, nom), dossier_img)
        except ValueError as e:
            raise SystemExit("contenu/articles/%s : %s" % (nom, e))
        if a:
            nouveaux.append(a)
    remplaces = {a["slug"] for a in nouveaux}
    tous = [a for a in articles if a["slug"] not in remplaces] + nouveaux
    return sorted(tous, key=lambda a: a["date"], reverse=True)
