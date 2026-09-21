# -*- coding: utf-8 -*-
"""Controle des traductions arabes des articles (build/articles_ar/).

Pour chaque article : traduction presente, metadonnees completes, titre de
recherche de 60 caracteres au plus, description de 90 a 170 caracteres, chaque
mot-cle present dans le texte (diacritiques neutralises), HTML equilibre.
"""
import json, os, re, sys, html, unicodedata
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AR = os.path.join(ROOT, "build", "articles_ar")
DIACRITIQUES = re.compile("[ً-ْٰـ]")   # harakat, alif suscrit, tatwil


def norm(s):
    return DIACRITIQUES.sub("", unicodedata.normalize("NFC", s))


class Equilibre(HTMLParser):
    VIDES = {"br", "img"}

    def __init__(self):
        super().__init__()
        self.pile, self.erreurs = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VIDES:
            self.pile.append(tag)

    def handle_endtag(self, tag):
        if self.pile and self.pile[-1] == tag:
            self.pile.pop()
        else:
            self.erreurs.append(tag)


def main():
    articles = json.load(open(os.path.join(ROOT, "build", "articles.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(AR, "meta.json"), encoding="utf-8"))
    erreurs = []
    for a in articles:
        slug = a["slug"]
        chemin = os.path.join(AR, slug + ".html")
        if not os.path.exists(chemin):
            erreurs.append("%s : pas de traduction" % slug)
            continue
        m = meta.get(slug)
        if not m or any(k not in m for k in ("title", "seo_title", "description", "keywords", "alt")):
            erreurs.append("%s : metadonnees incompletes" % slug)
            continue
        corps = open(chemin, encoding="utf-8").read()
        texte = norm(html.unescape(re.sub(r"<[^>]+>", " ", corps)) + " " + m["title"])
        if len(m["seo_title"]) > 60:
            erreurs.append("%s : titre de recherche de %d caracteres" % (slug, len(m["seo_title"])))
        if not 90 <= len(m["description"]) <= 170:
            erreurs.append("%s : description de %d caracteres" % (slug, len(m["description"])))
        for k in m["keywords"]:
            if norm(k) not in texte:
                erreurs.append("%s : mot-cle absent : %s" % (slug, k))
        eq = Equilibre()
        eq.feed(corps)
        eq.close()
        if eq.erreurs or eq.pile:
            erreurs.append("%s : HTML desequilibre %s %s" % (slug, eq.erreurs[:3], eq.pile[-3:]))
        mots = len(texte.split())
        print("  %-34s %5d mots | titre %2d | description %3d | %d mots-cles"
              % (slug, mots, len(m["seo_title"]), len(m["description"]), len(m["keywords"])))
    if erreurs:
        print("\nPROBLEMES :")
        for e in erreurs:
            print("  - " + e)
        sys.exit(1)
    print("\n  %d traductions conformes" % len(articles))


if __name__ == "__main__":
    main()
