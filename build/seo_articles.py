# -*- coding: utf-8 -*-
"""Metadonnees de referencement des articles, fusionnees dans build/articles.json.

Pour chaque article : le titre affiche par Google (le titre visible de la page ne
change pas), la description sous le resultat, des mots-cles pour les donnees
structurees, et le texte alternatif du visuel. Relancer ce script apres
modification, puis generate.py.

Le script refuse d'ecrire si un titre depasse 60 caracteres, si une description
sort de 110-160 caracteres, ou si un mot-cle n'apparait nulle part dans l'article.
"""
import json, io, os, re, html, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "build", "articles.json")

SEO = {
    "depression-nerveuse": {
        "seo_title": "Dépression nerveuse : symptômes et traitements — Dr Chikhi",
        "description": "Tristesse profonde, perte de plaisir, troubles de l’humeur : comment "
                       "reconnaître une dépression nerveuse, et quels traitements existent.",
        "keywords": ["dépression", "dépression nerveuse", "symptômes", "traitement",
                     "troubles de l’humeur", "prise en charge"],
        "alt": "Silhouette d’une personne assise, recroquevillée, la tête entre les mains, au bord de la mer",
    },
    "hypnose-ericksonienne": {
        "seo_title": "Hypnose ericksonienne : principe et bienfaits — Dr Chikhi",
        "description": "Qu’est-ce que l’hypnose ericksonienne, en quoi diffère-t-elle de l’hypnose "
                       "de spectacle, et comment aide-t-elle contre le stress ou les phobies ?",
        "keywords": ["hypnose ericksonienne", "hypnose thérapeutique", "séance d’hypnose",
                     "stress", "anxiété", "phobies"],
        "alt": "Nuage de mots autour des termes hypnosis, psychology, therapy et patient",
    },
    "covid-19-et-sante-mentale": {
        "seo_title": "COVID-19 et santé mentale : les conseils d’un psychiatre",
        "description": "Peur, stress, confinement : comment préserver sa santé mentale et celle "
                       "de sa famille pendant la pandémie de COVID-19. Conseils du Dr Chikhi.",
        "keywords": ["COVID-19", "santé mentale", "confinement", "stress", "pandémie", "famille"],
        "alt": "Vue microscopique de particules du coronavirus",
    },
    "relaxation-musculaire-progressive": {
        "seo_title": "Relaxation musculaire progressive : stress et anxiété",
        "description": "Une méthode simple et efficace pour maîtriser le stress et l’anxiété : "
                       "principe de la relaxation musculaire progressive et indications.",
        "keywords": ["relaxation musculaire progressive", "relaxation", "stress", "anxiété",
                     "crises d’angoisses", "détente"],
        "alt": "Homme allongé dans l’herbe, les bras derrière la tête, sous un ciel bleu",
    },
    "psychotherapie": {
        "seo_title": "Psychothérapie : définition, indications et méthodes",
        "description": "Qu’est-ce qu’une psychothérapie, pour quels troubles consulter "
                       "(stress, angoisses, phobies, deuil, dépression) et quelles approches existent.",
        "keywords": ["psychothérapie", "psychothérapeute", "soutien", "cognitive et comportementale",
                     "phobies", "dépression"],
        "alt": "Patient allongé sur un divan pendant qu’un praticien prend des notes",
    },
    "neurologique-ou-psychiatrique": {
        "seo_title": "Neurologue ou psychiatre : quelle différence ? — Dr Chikhi",
        "description": "Neurologue ou psychiatre ? Ce qui distingue les deux spécialités, et "
                       "pourquoi elles étaient autrefois réunies en neuropsychiatrie.",
        "keywords": ["neurologue", "psychiatre", "neuropsychiatrie", "neurologie", "psychiatrie",
                     "maladies mentales"],
        "alt": "Représentation en trois dimensions d’un cerveau lumineux sur fond sombre",
    },
    "medicaments-psychotropes": {
        "seo_title": "Médicaments psychotropes : faut-il en avoir peur ?",
        "description": "Comment agissent les médicaments psychotropes, que penser de leurs effets "
                       "secondaires, et pourquoi un traitement bien suivi ne doit pas faire peur.",
        "keywords": ["médicaments psychotropes", "psychotropes", "effets secondaires", "traitement",
                     "cerveau"],
        "alt": "Comprimés et gélules de couleurs variées disposés sur une surface claire",
    },
    "ameliorer-sa-concentration": {
        "seo_title": "Comment améliorer sa concentration pendant les révisions ?",
        "description": "Nuits blanches, compléments alimentaires : ce qui aide vraiment à se "
                       "concentrer pendant les révisions, par une pharmacienne. Conseils concrets.",
        "keywords": ["concentration", "révisions", "efficacité", "étudiant", "compléments alimentaires"],
        "alt": "Écran d’ordinateur portable affichant une visioconférence d’étudiants coiffés de toques de diplôme",
    },
    "prise-de-parole-en-public": {
        "seo_title": "Prise de parole en public : comment se préparer ?",
        "description": "Accroche, plan, choix des mots : les conseils d’une pharmacienne pour "
                       "préparer une présentation orale et captiver son auditoire, timide ou non.",
        "keywords": ["prise de parole en public", "présentation", "oral", "timides", "auditoire"],
        "alt": "Scène de théâtre vide aux rideaux rouges, éclairée par un projecteur",
    },
    "etre-president-association": {
        "seo_title": "Être président d’association étudiante : témoignage",
        "description": "Une pharmacienne raconte son mandat de présidente d’association étudiante "
                       "à Montpellier : ce qu’il apporte, ses difficultés, et pourquoi se lancer.",
        "keywords": ["association", "président", "mandat", "étudiants", "Montpellier",
                     "industrie pharmaceutique"],
        "alt": "Illustration d’une réunion d’association : un auditoire assis face à une intervenante présentant des graphiques",
    },
}


def norm(s):
    """Minuscules, apostrophes unifiees, accents conserves."""
    return unicodedata.normalize("NFC", s.lower().replace("’", "'"))


def main():
    arts = json.load(open(PATH, encoding="utf-8"))
    errors = []
    for a in arts:
        meta = SEO.get(a["slug"])
        if not meta:
            errors.append("%s : aucune metadonnee" % a["slug"])
            continue
        text = norm(html.unescape(re.sub(r"<[^>]+>", " ", a["body"])) + " " + a["title"])
        t, d = meta["seo_title"], meta["description"]
        if len(t) > 60:
            errors.append("%s : titre de %d caracteres (> 60)" % (a["slug"], len(t)))
        if not 110 <= len(d) <= 160:
            errors.append("%s : description de %d caracteres (110-160)" % (a["slug"], len(d)))
        for k in meta["keywords"]:
            if norm(k) not in text:
                errors.append("%s : mot-cle absent du texte : %s" % (a["slug"], k))
        print("  %-34s titre %2d | description %3d | %d mots-cles" % (a["slug"], len(t), len(d), len(meta["keywords"])))
    if errors:
        print("\nREFUS :")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    for a in arts:
        a.update(SEO[a["slug"]])
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(json.dumps(arts, ensure_ascii=False, indent=1))
    print("\n  articles.json mis a jour")


if __name__ == "__main__":
    main()
