# -*- coding: utf-8 -*-
"""Genere le site statique du cabinet a partir de build/articles.json."""
import json, os, io, html, datetime, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Empreinte du contenu de la feuille de style et du script, ajoutee a leur adresse.
# GitHub Pages laisse les navigateurs les garder 10 minutes en cache : sans cela, une
# page neuve peut s'afficher avec une feuille de style perimee apres une mise a jour.
def _empreinte(chemin):
    with open(os.path.join(ROOT, chemin), "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:10]

ASSET_V = {"css": _empreinte("assets/css/style.css"), "js": _empreinte("assets/js/main.js")}
SITE_URL = "https://chikhineuropsychiatrie.github.io"   # adresse de publication ; voir README

# Code de validation Google Search Console. Vide = aucune balise emise.
# Le code se recupere dans Search Console, methode "Balise HTML".
GOOGLE_VERIFICATION = "NoFKglLWocQ3Qggm3pVqNF6FOyC3WvYvR712uhxYlXg"

DOC   = "Dr F. Chikhi Bengougam"
SPEC  = "Neuropsychiatre — Psychothérapeute"
TEL_DISPLAY = "05 49 14 36 48"
TEL_HREF    = "+213549143648"
EMAIL = "chikhifatiha@hotmail.fr"
ADDR1 = "Lotissement des Jeunes Aveugles, Lot 100"
ADDR2 = "Draria, Alger"
YEAR  = 2026

# Nom du site affiche par Google au-dessus de l'URL.
SITE_NAME = "Dr Chikhi Neuropsychiatrie"

# Position du cabinet : epingle de sa fiche Google (CID 0xaf08c0f369c65df1),
# la meme que celle qu'utilisent deja les patients pour venir.
GEO_LAT, GEO_LON = 36.7119136, 2.9960607
GMAPS_URL = "https://maps.google.com/?cid=12612542908135267825"
_DLON, _DLAT = 0.006, 0.0035   # cadrage de la carte autour du cabinet
MAP_EMBED = ("https://www.openstreetmap.org/export/embed.html"
             "?bbox=%.5f%%2C%.5f%%2C%.5f%%2C%.5f&amp;layer=mapnik&amp;marker=%.7f%%2C%.7f"
             % (GEO_LON - _DLON, GEO_LAT - _DLAT, GEO_LON + _DLON, GEO_LAT + _DLAT, GEO_LAT, GEO_LON))
OSM_URL = ("https://www.openstreetmap.org/?mlat=%.7f&amp;mlon=%.7f#map=18/%.7f/%.7f"
           % (GEO_LAT, GEO_LON, GEO_LAT, GEO_LON))

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

def fr_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, MOIS[m - 1], y)

NAV = [
    ("index.html",    "Accueil"),
    ("cabinet.html",  "Le cabinet"),
    ("horaires.html", "Horaires"),
    ("cursus.html",   "Cursus"),
    ("articles.html", "Articles"),
    ("contact.html",  "Contact"),
]

# ---- Version arabe : pages traduites sous /ar/ (voir build/pages_ar.py).
# Les articles traduits sont sous /ar/articles/ (build/articles_ar/).
AR_PAGES = ["index.html", "cabinet.html", "horaires.html", "cursus.html", "contact.html"]
NAV_AR = [
    ("index.html",       "الرئيسية"),
    ("cabinet.html",     "العيادة"),
    ("horaires.html",    "أوقات العمل"),
    ("cursus.html",      "المسار المهني"),
    ("articles.html",    "المقالات"),
    ("contact.html",     "اتصل بنا"),
]
DOC_AR   = "الدكتورة ف. شيخي بن قوقام"
ADDR2_AR = "الدرارية، الجزائر العاصمة"
# Numeros et adresses latines forces de gauche a droite : dans un texte arabe,
# « 05 49 14 36 48 » s'afficherait sinon groupes inverses.
TEL_LTR   = '<span dir="ltr">%s</span>' % TEL_DISPLAY
ADDR1_LTR = '<span dir="ltr">%s</span>' % ADDR1
EMAIL_LTR = '<span dir="ltr">%s</span>' % EMAIL

FONTS = {
    "fr": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Lora:wght@500;600&display=swap",
    "ar": "https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@500;600&family=Noto+Sans+Arabic:wght@400;500;600&display=swap",
}

UI = {
    "fr": {
        "skip": "Aller au contenu",
        "rdv_top": "Prendre rendez-vous&nbsp;:",
        "brand_sub": "Neuropsychiatrie · Draria",
        "menu": "Ouvrir le menu",
        "nav_label": "Navigation principale",
        "rdv_btn": "Rendez-vous",
        "switch": "العربية",
        "f_cabinet": "Le cabinet",
        "f_tag": "Prise en charge des troubles psychologiques, psychiatriques et neurologiques.",
        "f_nav": "Navigation",
        "f_coord": "Coordonnées",
        "f_hours": "Horaires",
        "f_hours_list": ["Samedi – Jeudi&nbsp;: 08:00 – 17:30", "Pause&nbsp;: 12:00 – 13:00",
                         "Mardi &amp; vendredi&nbsp;: fermé"],
        "f_detail": "Voir le détail",
        "f_rights": "© {year} Cabinet du {doc}. Tous droits réservés.",
        "f_disclaimer": "Ce site ne remplace pas une consultation médicale.",
    },
    "ar": {
        "skip": "انتقل إلى المحتوى",
        "rdv_top": "لحجز موعد:",
        "brand_sub": "الطب العصبي النفسي · الدرارية",
        "menu": "فتح القائمة",
        "nav_label": "القائمة الرئيسية",
        "rdv_btn": "احجز موعدا",
        "switch": "Français",
        "f_cabinet": "العيادة",
        "f_tag": "التكفل بالاضطرابات النفسية والعقلية والعصبية.",
        "f_nav": "روابط",
        "f_coord": "معلومات الاتصال",
        "f_hours": "أوقات العمل",
        "f_hours_list": ["من السبت إلى الخميس: من 08:00 إلى 17:30", "الاستراحة: من 12:00 إلى 13:00",
                         "الثلاثاء والجمعة: مغلق"],
        "f_detail": "التفاصيل",
        "f_rights": "© {year} عيادة {doc}. جميع الحقوق محفوظة.",
        "f_disclaimer": "هذا الموقع لا يغني عن الاستشارة الطبية.",
    },
}

ICONS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .3 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.4 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "map":   '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "mail":  '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/>',
    "brain": '<path d="M9.5 3a3 3 0 0 0-3 3 3 3 0 0 0-2 5.2A3 3 0 0 0 6 16.5 3 3 0 0 0 9 20a2.5 2.5 0 0 0 3-2.4V5.5A2.5 2.5 0 0 0 9.5 3z"/><path d="M14.5 3a3 3 0 0 1 3 3 3 3 0 0 1 2 5.2 3 3 0 0 1-1.5 5.3A3 3 0 0 1 15 20a2.5 2.5 0 0 1-3-2.4V5.5A2.5 2.5 0 0 1 14.5 3z"/>',
    "chat":  '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 8.9 8.9 0 0 1-3.9-.9L3 20.5l1.6-4.8A8.4 8.4 0 0 1 3.6 11 8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/>',
    "leaf":  '<path d="M11 20A7 7 0 0 1 4 13c0-6 5-9 16-10 0 10-4 15-9 16z"/><path d="M4.5 20.5 12 13"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "cap":   '<path d="m12 3 10 5-10 5L2 8z"/><path d="M6 10.5V16c0 1.5 2.7 3 6 3s6-1.5 6-3v-5.5"/>',
    "star":  '<path d="m12 3 2.7 5.6 6.3.9-4.5 4.3 1 6.2-5.5-3-5.5 3 1-6.2L3 9.5l6.3-.9z"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5.5A1.5 1.5 0 0 1 10.5 4h3A1.5 1.5 0 0 1 15 5.5V7"/><path d="M3 12.5h18"/>',
    "award": '<circle cx="12" cy="9" r="5.5"/><path d="M8.8 13.5 7.5 21l4.5-2.6 4.5 2.6-1.3-7.5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M15.5 4.8a3.5 3.5 0 0 1 0 6.4"/><path d="M17.5 14.3c2.1.8 3.5 2.9 3.5 5.7"/>',
}

def icon(name, size=24):
    return ('<svg viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (size, size, ICONS[name]))

def canon_path(page):
    """Chemin canonique : une page d'accueil se reference par son dossier."""
    return page[:-len("index.html")] if page.endswith("index.html") else page


def head(title, desc, page, depth=0, og_image="assets/img/2017_12_intestinCerveau.jpg", extra=""):
    lang = "ar" if page.startswith("ar/") else "fr"
    up = "../" * depth
    canon = "%s/%s" % (SITE_URL, canon_path(page))
    verif = ('\n<meta name="google-site-verification" content="%s">' % GOOGLE_VERIFICATION
             if GOOGLE_VERIFICATION else "")
    # Pages disponibles dans les deux langues : on le signale a Google (hreflang).
    base = page[3:] if lang == "ar" else page
    alts = ""
    if base in AR_PAGES:
        fr_u = "%s/%s" % (SITE_URL, canon_path(base))
        ar_u = "%s/%s" % (SITE_URL, canon_path("ar/" + base))
        alts = ('\n<link rel="alternate" hreflang="fr" href="%s">'
                '\n<link rel="alternate" hreflang="ar" href="%s">'
                '\n<link rel="alternate" hreflang="x-default" href="%s">'
                '\n<meta property="og:locale:alternate" content="%s">'
                % (fr_u, ar_u, fr_u, "fr_FR" if lang == "ar" else "ar_DZ"))
    rtl = ' dir="rtl"' if lang == "ar" else ""
    locale = "ar_DZ" if lang == "ar" else "fr_FR"
    return f"""<!DOCTYPE html>
<html lang="{lang}"{rtl}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">{alts}
<meta property="og:type" content="website">
<meta property="og:locale" content="{locale}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE_URL}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f6094">{verif}
<link rel="icon" href="{up}favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" type="image/png" sizes="96x96" href="{up}assets/img/icon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="{up}assets/img/icon-192.png">
<link rel="apple-touch-icon" href="{up}assets/img/icon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS[lang]}">
<link rel="stylesheet" href="{up}assets/css/style.css?v={ASSET_V['css']}">
{extra}</head>
<body>
<a class="skip" href="#contenu">{UI[lang]["skip"]}</a>
"""

def header(page, depth=0, lang="fr", switch_to=None):
    ui = UI[lang]
    up = "../" * depth
    # Les liens du menu arabe sont relatifs a /ar/ ; ceux du menu francais, a la page.
    navp = "../" * (depth - 1) if lang == "ar" else up
    items = []
    for href, label in (NAV_AR if lang == "ar" else NAV):
        cur = ' aria-current="page"' if href == page else ""
        items.append(f'        <li><a href="{navp}{href}"{cur}>{label}</a></li>')
    links = "\n".join(items)
    if lang == "ar":
        switch_href, other = "../" + page, "fr"
        addr, tel, name = ADDR2_AR, TEL_LTR, DOC_AR
    else:
        # Page sans equivalent arabe (articles, 404) : on renvoie vers l'accueil arabe.
        switch_href, other = up + "ar/" + (page if page in AR_PAGES else "index.html"), "ar"
        addr, tel, name = ADDR2, TEL_DISPLAY, DOC
    if switch_to:   # article : on renvoie vers sa traduction plutot que vers la liste
        switch_href = switch_to
    return f"""<div class="topbar">
  <div class="wrap">
    <span>{icon('map', 15)} {addr}</span>
    <span>{ui["rdv_top"]} <a class="tel-link" href="tel:{TEL_HREF}">{tel}</a>
      <a class="lang-switch" href="{switch_href}" lang="{other}" hreflang="{other}">{ui["switch"]}</a></span>
  </div>
</div>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{navp}index.html">
      <img src="{up}assets/img/2017_12_logo3.png" alt="" width="180" height="47">
      <span class="brand-txt">
        <strong>{name}</strong>
        <span>{ui["brand_sub"]}</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="{ui["menu"]}">
      <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="nav" id="menu" aria-label="{ui["nav_label"]}">
      <ul>
{links}
        <li><a class="btn-rdv" href="{navp}contact.html">{ui["rdv_btn"]}</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="contenu">
"""

def footer(depth=0, lang="fr"):
    ui = UI[lang]
    up = "../" * depth
    navp = "../" * (depth - 1) if lang == "ar" else up
    nav_links = "\n".join(f'          <li><a href="{navp}{h}">{l}</a></li>'
                          for h, l in (NAV_AR if lang == "ar" else NAV))
    hours = "\n".join("          <li>%s</li>" % h for h in ui["f_hours_list"])
    if lang == "ar":
        name, spec = DOC_AR, "الطب العصبي النفسي — العلاج النفسي"
        addr, tel, mail = "%s<br>%s" % (ADDR1_LTR, ADDR2_AR), TEL_LTR, EMAIL_LTR
    else:
        name, spec = DOC, SPEC
        addr, tel, mail = "%s<br>%s" % (ADDR1, ADDR2), TEL_DISPLAY, EMAIL
    rights = ui["f_rights"].format(year=YEAR, doc=name)
    return f"""</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>{ui["f_cabinet"]}</h4>
        <p class="tagline">{name}<br>{spec}</p>
        <p class="tagline">{ui["f_tag"]}</p>
      </div>
      <div>
        <h4>{ui["f_nav"]}</h4>
        <ul>
{nav_links}
        </ul>
      </div>
      <div>
        <h4>{ui["f_coord"]}</h4>
        <ul>
          <li>{addr}</li>
          <li><a class="tel-link" href="tel:{TEL_HREF}">{tel}</a></li>
          <li><a href="mailto:{EMAIL}">{mail}</a></li>
        </ul>
      </div>
      <div>
        <h4>{ui["f_hours"]}</h4>
        <ul>
{hours}
          <li><a href="{navp}horaires.html">{ui["f_detail"]}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>{rights}</span>
      <span>{ui["f_disclaimer"]}</span>
    </div>
  </div>
</footer>

<script src="{up}assets/js/main.js?v={ASSET_V['js']}"></script>
</body>
</html>
"""

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with io.open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return len(content)


# --------------------------------------------------------------- donnees

articles = json.load(open(os.path.join(ROOT, "build/articles.json"), encoding="utf-8"))
AR_ARTICLES = [a["slug"] for a in articles
               if os.path.exists(os.path.join(ROOT, "build", "articles_ar", a["slug"] + ".html"))]
AR_PAGES += ["articles.html"] + ["articles/%s.html" % s for s in AR_ARTICLES]

SERVICES = [
    ("brain", "Neuropsychiatrie",
     "Diagnostic et prise en charge des troubles neurologiques et psychiatriques : dépression, anxiété, troubles bipolaires, épilepsie, céphalées, addictions aux drogues douces."),
    ("chat", "Psychothérapie",
     "Entretiens réguliers dans une relation de confiance et de confidentialité, seuls ou en complément d’un traitement."),
    ("leaf", "Relaxation thérapeutique",
     "Relaxation musculaire progressive et hypnose ericksonienne, pour apaiser le stress, l’anxiété et les tensions."),
]

DEMARCHE = [
    "Diagnostic basé sur un entretien, des examens et des tests complémentaires",
    "Prise en charge adaptée à chaque situation",
    "Suivi régulier, disponibilité et conseils",
    "Relaxation thérapeutique",
]

HORAIRES = [
    ("Samedi",   "08:00 – 12:00 · 13:00 – 17:30", False),
    ("Dimanche", "08:00 – 12:00 · 13:00 – 17:30", False),
    ("Lundi",    "08:00 – 12:00 · 13:00 – 17:30", False),
    ("Mardi",    "Fermé", True),
    ("Mercredi", "08:00 – 12:00 · 13:00 – 17:30", False),
    ("Jeudi",    "08:00 – 12:00 · 13:00 – 17:30", False),
    ("Vendredi", "Fermé", True),
]

def post_card(a, depth=0):
    up = "../" * depth
    img = (f'<div class="thumb"><img src="{up}assets/img/{a["image"]}" alt="" loading="lazy" width="600" height="375"></div>'
           if a["image"] else "")
    return f"""        <article class="post-card">
{img}
          <div class="body">
            <p class="meta">{fr_date(a['date'])}</p>
            <h3><a href="{up}articles/{a['slug']}.html">{html.escape(a['title'])}</a></h3>
            <p>{html.escape(a['excerpt'])}</p>
            <a class="more" href="{up}articles/{a['slug']}.html">Lire l’article →</a>
          </div>
        </article>"""


# --------------------------------------------------------------- accueil

cards = "\n".join(
    f"""        <div class="card">
          <div class="ico">{icon(ic)}</div>
          <h3>{t}</h3>
          <p>{d}</p>
        </div>""" for ic, t, d in SERVICES)

demarche = "\n".join(f"          <li>{x}</li>" for x in DEMARCHE)
# ---- Videos du Dr Chikhi : entretiens pour le media sante algerien 37° degres.
# Textes tires des titres et descriptions officiels des videos, sans rien y
# ajouter. La vignette est hebergee ici ; le lecteur YouTube (sans cookies) ne se
# charge qu'au clic (assets/js/main.js).
MEDIA_URL = "https://www.37degres.dz/"
VIDEOS = {
    "depression": {
        "id": "uVGxKyq7iy0", "img": "video-depression.jpg", "secondes": 1450,
        "date": "2023-08-04", "upload": "2023-08-04T06:16:46-07:00",
        "article": "depression-nerveuse", "position": "haut",
        "fr": {
            "titre": "La dépression : diagnostic précoce et stratégies thérapeutiques efficaces",
            "desc": "Dans cet entretien pour le média santé algérien 37° degrés, le Dr Chikhi fait le tour "
                    "de la dépression : comment on la diagnostique, comment se déroule le suivi, et quels "
                    "traitements sont efficaces.",
            "intro": "<strong>En vidéo.</strong> Le Dr Chikhi aborde aussi ce sujet dans un entretien de "
                     "24 minutes, du diagnostic au traitement.",
        },
        "ar": {
            "titre": "الاكتئاب: تشخيص مبكر واستراتيجيات علاجية فعالة",
            "desc": "في هذا اللقاء مع منبر الصحة الجزائري «37 درجة»، تشرح " + DOC_AR + " كل ما يتعلق "
                    "بالاكتئاب، من طريقة التشخيص والمتابعة إلى مرحلة العلاج.",
            "intro": "<strong>فيديو.</strong> تتناول " + DOC_AR + " هذا الموضوع أيضا في لقاء مصور بالفرنسية مدته "
                     "24 دقيقة، من التشخيص إلى العلاج.",
        },
    },
    "addiction": {
        "id": "ZQg9iiENrl0", "img": "video-addiction.jpg", "secondes": 1031,
        "date": "2023-08-20", "upload": "2023-08-20T02:42:22-07:00",
        "article": "medicaments-psychotropes", "position": "bas",
        "fr": {
            "titre": "L’addiction : ses causes et ses effets",
            "desc": "L’addiction, c’est l’usage nocif de substances comme l’alcool, les médicaments "
                    "psychotropes ou les drogues illicites (cannabis, cocaïne), qui peut devenir un besoin "
                    "irrésistible et agit sur le cerveau et le comportement. Le Dr Chikhi en détaille les "
                    "causes : curiosité, influence de l’entourage, fuite des problèmes, recherche de "
                    "performance ou soulagement de troubles psychiques.",
            "intro": "<strong>Pour aller plus loin.</strong> Le Dr Chikhi consacre un entretien vidéo à "
                     "l’addiction, dont le mauvais usage des médicaments psychotropes fait partie. "
                     "Le cabinet prend en charge les addictions aux drogues douces.",
        },
        "ar": {
            "titre": "الإدمان: أسبابه وتأثيره",
            "desc": "الإدمان هو إساءة استخدام مواد ضارة بالصحة، مثل الكحول والأدوية النفسية والمخدرات غير "
                    "المشروعة كالقنب والكوكايين، وقد يتحول إلى حاجة لا تقاوم إلى تعاطيها تؤثر في الدماغ "
                    "والسلوك. وتعرض " + DOC_AR + " أسبابه المتعددة: الفضول، والتأثير الاجتماعي، والهروب "
                    "من المشكلات، والرغبة في تحسين الأداء، أو التخفيف من اضطرابات نفسية.",
            "intro": "<strong>للتعمق أكثر.</strong> خصصت " + DOC_AR + " لقاء مصورا بالفرنسية للإدمان، ومن صوره "
                     "سوء استعمال الأدوية النفسية. وتتكفل العيادة بحالات الإدمان على المخدرات الخفيفة.",
        },
    },
}
MOIS_AR = ["جانفي", "فيفري", "مارس", "أفريل", "ماي", "جوان", "جويلية", "أوت",
           "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]


def ar_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return "%d %s %d" % (d, MOIS_AR[m - 1], y)


def video_card(v, lang, up):
    """Carte video : vignette cliquable (lecteur charge au clic), titre, description."""
    t = v[lang]
    minutes = round(v["secondes"] / 60)
    duree = "%d:%02d" % (v["secondes"] // 60, v["secondes"] % 60)
    if lang == "ar":
        label = "تشغيل الفيديو: " + t["titre"]
        meta = 'فيديو بالفرنسية · %d دقيقة · %s · <a href="%s" target="_blank" rel="noopener">«37 درجة»</a>' % (
            minutes, ar_date(v["date"]), MEDIA_URL)
    else:
        label = "Lire la vidéo : " + t["titre"]
        meta = 'Vidéo · %d min · %s · <a href="%s" target="_blank" rel="noopener">37° degrés</a>' % (
            minutes, fr_date(v["date"]), MEDIA_URL)
    return f"""      <figure class="video">
        <a class="video-facade" href="https://www.youtube.com/watch?v={v['id']}" data-yt="{v['id']}"
           aria-label="{html.escape(label)}" target="_blank" rel="noopener">
          <img src="{up}assets/img/{v['img']}" alt="" loading="lazy" width="960" height="540">
          <span class="video-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.5v13l11-6.5z"/></svg></span>
          <span class="video-duree" dir="ltr">{duree}</span>
        </a>
        <figcaption>
          <p class="meta">{meta}</p>
          <h3>{t['titre']}</h3>
          <p>{t['desc']}</p>
        </figcaption>
      </figure>"""


def video_ld(v, lang):
    """Donnees structurees VideoObject (resultats video de Google)."""
    t = v[lang]
    return '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps({
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": t["titre"],
        "description": t["desc"],
        "thumbnailUrl": ["%s/assets/img/%s" % (SITE_URL, v["img"])],
        "uploadDate": v["upload"],
        "duration": "PT%dM%dS" % (v["secondes"] // 60, v["secondes"] % 60),
        "embedUrl": "https://www.youtube-nocookie.com/embed/" + v["id"],
        "url": "https://www.youtube.com/watch?v=" + v["id"],
        "inLanguage": "fr",
        "publisher": {"@type": "Organization", "name": "37° degrés", "url": MEDIA_URL},
    }, ensure_ascii=False, indent=1)


def video_blocks(slug, lang, up):
    """Blocs video d'un article (haut, bas) et leurs donnees structurees."""
    haut = bas = ld = ""
    for v in VIDEOS.values():
        if v["article"] != slug:
            continue
        bloc = f"""  <div class="narrow">
    <aside class="article-video">
      <p class="article-video-intro">{v[lang]['intro']}</p>
{video_card(v, lang, up)}
    </aside>
  </div>
"""
        if v["position"] == "haut":
            haut += bloc
        else:
            bas += bloc
        ld += video_ld(v, lang)
    return haut, bas, ld


def section_videos(lang, up):
    """Section « En video » des pages d'accueil."""
    if lang == "ar":
        head_ = (f'<p class="eyebrow">فيديو</p>\n      <h2>{DOC_AR} تجيب عن أسئلة «37 درجة»</h2>\n'
                 f'      <p>لقاءان مصوران باللغة الفرنسية مع منبر الصحة الجزائري '
                 f'<a href="{MEDIA_URL}" target="_blank" rel="noopener">«37 درجة»</a>.</p>')
    else:
        head_ = ('<p class="eyebrow">En vidéo</p>\n      <h2>Le Dr Chikhi répond aux questions de 37° degrés</h2>\n'
                 f'      <p>Deux entretiens filmés pour le média santé algérien '
                 f'<a href="{MEDIA_URL}" target="_blank" rel="noopener">37° degrés</a>.</p>')
    cards = "\n".join(video_card(v, lang, up) for v in VIDEOS.values())
    return f"""
<section>
  <div class="wrap">
    <div class="section-head">
      {head_}
    </div>
    <div class="videos">
{cards}
    </div>
  </div>
</section>
"""


# L'accueil met en avant les derniers articles du Dr Chikhi elle-meme : la section
# s'intitule « Articles du Dr ... » et doit porter sur la psychiatrie.
recent = "\n".join(post_card(a) for a in [x for x in articles if not x.get("author")][:3])

SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "@id": SITE_URL + "/#cabinet",
    "name": "Cabinet du " + DOC,
    "alternateName": "عيادة " + DOC_AR,
    "description": "Cabinet de neuropsychiatrie, psychothérapie et relaxation thérapeutique à Draria, Alger.",
    "url": SITE_URL,
    "telephone": "+213 549 14 36 48",
    "email": EMAIL,
    "medicalSpecialty": ["Psychiatric", "Neurologic"],
    "geo": {"@type": "GeoCoordinates", "latitude": GEO_LAT, "longitude": GEO_LON},
    "hasMap": GMAPS_URL,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": ADDR1,
        "addressLocality": "Draria",
        "addressRegion": "Alger",
        "addressCountry": "DZ",
    },
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Saturday", "Sunday", "Monday", "Wednesday", "Thursday"],
        "opens": "08:00", "closes": "17:30",
    }],
}, ensure_ascii=False, indent=1)

# Nom du site affiche par Google au-dessus de l'URL. Sans ce signal, il retombe
# sur le proprietaire du domaine parent, et affiche « GitHub ».
WEBSITE_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": SITE_NAME,
    "alternateName": [DOC, "Cabinet du Dr Chikhi"],
    "url": SITE_URL + "/",
}, ensure_ascii=False, indent=1)

index = head(
    f"Psychiatre à Draria, Alger — {DOC}",
    "Cabinet de neuropsychiatrie, psychothérapie et relaxation thérapeutique à Draria, Alger. "
    "Stress, anxiété, dépression, troubles bipolaires, épilepsie et céphalées.",
    "index.html",
    extra=(f'<script type="application/ld+json">\n{SCHEMA}\n</script>\n'
           f'<script type="application/ld+json">\n{WEBSITE_SCHEMA}\n</script>\n'
           + video_ld(VIDEOS["depression"], "fr") + video_ld(VIDEOS["addiction"], "fr")),
) + header("index.html") + f"""
<section class="hero">
  <img class="hero-bg" src="assets/img/2017_12_intestinCerveau.jpg" alt="" width="1500" height="630" fetchpriority="high">
  <div class="wrap">
    <div class="hero-inner">
      <p class="eyebrow">Cabinet médical · Draria, Alger</p>
      <h1>Pour sortir de la souffrance et vivre en paix</h1>
      <p class="lede">
        Le cabinet du {DOC}, neuropsychiatre et psychothérapeute, accueille les personnes
        confrontées à une souffrance mentale, psychologique ou neurologique.
      </p>
      <div class="btn-row">
        <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} {TEL_DISPLAY}</a>
        <a class="btn btn-ghost" href="cabinet.html">Découvrir le cabinet</a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Consultations</p>
      <h2>Ce que nous prenons en charge</h2>
      <p>
        Stress, anxiété, dépression nerveuse, troubles bipolaires, épilepsie, céphalées,
        addictions aux drogues douces et autres troubles psychiatriques ou neurologiques.
      </p>
    </div>
    <div class="grid grid-3">
{cards}
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="split">
      <div class="body">
        <p class="eyebrow">Le cabinet</p>
        <h2>Bienvenue sur mon site</h2>
        <p>
          Le cabinet médical de neuropsychiatrie et psychothérapie est situé au centre de Draria,
          sur l’artère principale, à quelques encablures de la Daïra et de l’APC.
        </p>
        <p>
          Vous pouvez faire confiance à sa longue expérience dans la prise en charge des personnes
          en souffrance mentale ou psychologique.
        </p>
        <h3>Notre démarche</h3>
        <ul class="list-check">
{demarche}
        </ul>
      </div>
      <div class="media">
        <img src="assets/img/2017_12_lotus-zen1.jpg" alt="Fleur de lotus posée sur l’eau" loading="lazy" width="1500" height="630">
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Carte de visite</p>
      <h2>{DOC}</h2>
      <p>{SPEC} et relaxation thérapeutique.</p>
    </div>
    <div class="grid grid-3">
      <div class="card">
        <div class="ico">{icon('cap')}</div>
        <h3>Formation</h3>
        <ul class="list-check">
          <li>Diplôme de neurologie — Université de médecine de Kiev, 2004</li>
          <li>D.E.M.S. en psychiatrie — Université d’Alger, 1992</li>
          <li>Docteur en médecine — Université d’Alger, 1988</li>
        </ul>
      </div>
      <div class="card">
        <div class="ico">{icon('star')}</div>
        <h3>Sociétés savantes</h3>
        <ul class="list-check">
          <li>Membre de la Société Algérienne de Psychiatrie (S.A.P)</li>
          <li>Membre de l’Association Algérienne des Psychiatres d’Exercice Privé (AAPEP)</li>
        </ul>
      </div>
      <div class="card">
        <div class="ico">{icon('map')}</div>
        <h3>Adresse</h3>
        <p>{ADDR1}<br>{ADDR2}</p>
        <p>Pour prendre rendez-vous, appelez le<br>
          <a class="tel-link" href="tel:{TEL_HREF}"><strong>{TEL_DISPLAY}</strong></a>
        </p>
      </div>
    </div>
    <p style="margin-top:2rem"><a class="btn btn-outline" href="cursus.html">Voir le cursus complet</a></p>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Actualité &amp; lecture</p>
      <h2>Articles du {DOC}</h2>
      <p>Repères et explications sur les troubles psychiatriques et neurologiques.</p>
    </div>
    <div class="posts">
{recent}
    </div>
    <p style="margin-top:2.2rem"><a class="btn btn-outline" href="articles.html">Tous les articles</a></p>
  </div>
</section>
{section_videos('fr', '')}
<section class="cta-band">
  <div class="wrap">
    <h2>Prendre un rendez-vous</h2>
    <p>
      Vous pouvez nous contacter par téléphone. Une assistante répondra à vos appels
      pour fixer un rendez-vous.
    </p>
    <div class="btn-row">
      <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} {TEL_DISPLAY}</a>
      <a class="btn btn-ghost" href="contact.html">Voir les coordonnées</a>
    </div>
  </div>
</section>
""" + footer()

write("index.html", index)


# --------------------------------------------------------------- le cabinet

cabinet = head(
    "Le cabinet — " + DOC,
    "Le cabinet de neuropsychiatrie du " + DOC + ", au centre de Draria, Alger. "
    "Consultations, psychothérapie et relaxation thérapeutique.",
    "cabinet.html",
) + header("cabinet.html") + f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Le cabinet</p>
    <h1>Notre cabinet</h1>
    <p>
      Le cabinet du Dr Chikhi vous accueillera si vous êtes à la recherche d’une consultation
      en neuropsychiatrie et/ou en psychothérapie.
    </p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="split">
      <div class="body">
        <h2>Un lieu au centre de Draria</h2>
        <p>
          Le cabinet médical de neuropsychiatrie et psychothérapie est situé au centre de Draria,
          sur l’artère principale, à quelques encablures de la Daïra et de l’APC.
        </p>
        <p>
          Nous prenons en charge les troubles psychologiques, psychiatriques et neurologiques :
          stress, anxiété, dépression nerveuse, troubles bipolaires, épilepsie, céphalées,
          addictions aux drogues douces et autres troubles psychiatriques ou neurologiques.
        </p>
        <p>
          Vous pouvez faire confiance à sa longue expérience dans la prise en charge des personnes
          en souffrance mentale ou psychologique.
        </p>
      </div>
      <figure class="media">
        <img src="assets/img/draria-chateau.jpg" alt="Le château de Draria et ses deux tourelles pointues, sous un ciel bleu" width="1200" height="804" loading="lazy">
        <figcaption>
          Le château de Draria. Photo&nbsp;:
          <a href="https://commons.wikimedia.org/wiki/File:Photo_chateau_draria_30052016.jpg" target="_blank" rel="noopener">Sandervalya</a>,
          <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.fr" target="_blank" rel="noopener">CC BY-SA 4.0</a>,
          via Wikimedia Commons.
        </figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Consultations</p>
      <h2>Nos services</h2>
    </div>
    <div class="grid grid-3">
{cards}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div class="body">
        <h2>Le déroulement d’une prise en charge</h2>
        <ul class="list-check">
{demarche}
        </ul>
        <p style="margin-top:1.6rem">
          <a class="btn btn-outline" href="horaires.html">Consulter les horaires</a>
        </p>
      </div>
      <div class="body">
        <div class="callout">
          <p><strong>Ce site ne peut remplacer une consultation.</strong></p>
          <p>
            Il renseigne sur le fonctionnement du cabinet, sur l’adresse et les horaires.
            En cas d’urgence, contactez les services d’urgence ou rendez-vous à l’hôpital le plus proche.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2>Prendre un rendez-vous</h2>
    <p>Une assistante répondra à vos appels pour fixer un rendez-vous.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} {TEL_DISPLAY}</a>
      <a class="btn btn-ghost" href="contact.html">Nous trouver</a>
    </div>
  </div>
</section>
""" + footer()

write("cabinet.html", cabinet)


# --------------------------------------------------------------- horaires

rows = "\n".join(
    '        <tr class="closed"><th scope="row">%s</th><td>%s</td></tr>' % (d, h)
    if closed else
    '        <tr><th scope="row">%s</th><td>%s</td></tr>' % (d, h)
    for d, h, closed in HORAIRES)

horaires = head(
    "Horaires — " + DOC,
    "Horaires du cabinet du " + DOC + " à Draria : samedi à jeudi, 08:00 – 17:30. "
    "Fermé le mardi et le vendredi. Consultations sur rendez-vous.",
    "horaires.html",
) + header("horaires.html") + f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Informations pratiques</p>
    <h1>Horaires du cabinet</h1>
    <p>Les consultations se font sur rendez-vous. Pour en fixer un, appelez le {TEL_DISPLAY}.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="body">
        <table class="hours">
          <caption>Le cabinet est fermé le mardi et le vendredi.</caption>
          <thead>
            <tr><th scope="col">Jour</th><th scope="col">Ouverture</th></tr>
          </thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
      <div class="body">
        <h2>Bon à savoir</h2>
        <ul class="list-check">
          <li><strong>Pause</strong> — de 12:00 à 13:00</li>
          <li><strong>Créneaux sur rendez-vous</strong> — de 08:00 à 09:00 et de 16:30 à 17:30</li>
          <li><strong>Fermeture</strong> — mardi et vendredi</li>
        </ul>
        <div class="callout" style="margin-top:1.8rem">
          <p>
            <strong>Prise de rendez-vous.</strong> Vous pouvez nous contacter par téléphone au
            <a class="tel-link" href="tel:{TEL_HREF}">{TEL_DISPLAY}</a>. Une assistante répondra
            à vos appels pour fixer un rendez-vous.
          </p>
        </div>
        <p style="margin-top:1.8rem">
          <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} Appeler le cabinet</a>
        </p>
      </div>
    </div>
  </div>
</section>
""" + footer()

write("horaires.html", horaires)


# --------------------------------------------------------------- cursus

FORMATION = [
    ("2004", "Diplôme de neurologie", "Université de médecine de Kiev, Ukraine"),
    ("1992", "Diplôme d’études médicales spécialisées en psychiatrie", "Université de médecine d’Alger"),
    ("1988", "Diplôme de Docteur en médecine", "Université de médecine d’Alger"),
]
EXPERIENCE = [
    ("Depuis mai 2015", "Neuropsychiatre, psychothérapeute", "Cabinet privé, Draria"),
    ("Février 2005", "Neuropsychiatre, psychothérapeute",
     "Cabinet de groupe (neuropsychiatrie – neurochirurgie), Rouiba"),
    ("Février 1993", "Assistante spécialiste en psychiatrie",
     "Établissement spécialisé en psychiatrie de Chéraga"),
    ("1988 – 1992", "Médecin résidente en psychiatrie",
     "Établissement spécialisé en psychiatrie de Kouba"),
]
CERTIFICATS = [
    "Hypnothérapeute praticienne — Psynapse (certifié FFHTB), 2021",
    "Certificat en relaxation thérapeutique — EHS de Chéraga, 1997",
    "Certificat en thérapies cognitivo-comportementales appliquées aux dépressions, phobies et anxiété — Renaissance Life Therapies (Libby Seery), novembre 2017",
    "Initiation à l’hypnose ericksonienne — Pr F. Kacha, EHS de Chéraga, 2017",
    "Hypnotherapy Practitioner Diploma — Kain Ramsey (Academy of Modern Applied Psychology) et Steven Burns, Royaume-Uni",
    "Hypnosis Induction Mastery — Steven Burns, Royaume-Uni",
    "Ericksonian Hypnosis — Daniel Johns, Royaume-Uni",
]

def timeline(items, ico):
    out = []
    for when, what, where in items:
        out.append(f"""        <div class="card">
          <div class="ico">{icon(ico)}</div>
          <p class="meta">{when}</p>
          <h3>{what}</h3>
          <p>{where}</p>
        </div>""")
    return "\n".join(out)

certs = "\n".join(f"          <li>{c}</li>" for c in CERTIFICATS)

cursus = head(
    "Cursus — " + DOC,
    "Parcours du " + DOC + " : formations, diplômes, certificats et expériences professionnelles "
    "en neuropsychiatrie, psychothérapie et hypnose.",
    "cursus.html",
) + header("cursus.html") + f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Parcours</p>
    <h1>Cursus</h1>
    <p>
      {DOC} — neuropsychiatrie, psychothérapie et relaxation thérapeutique.
      Actuellement neuropsychiatre psychothérapeute d’exercice libéral à Draria.
    </p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Diplômes</p>
      <h2>Formations</h2>
    </div>
    <div class="grid grid-3">
{timeline(FORMATION, "cap")}
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Parcours professionnel</p>
      <h2>Expériences</h2>
      <p>
        J’ai exercé à l’EHS de psychiatrie de Chéraga avant de m’associer en cabinet de groupe
        (neurologie, psychiatrie, neurochirurgie) à Rouiba.
      </p>
    </div>
    <div class="grid grid-2">
{timeline(EXPERIENCE, "briefcase")}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Formation continue</p>
      <h2>Certificats et sociétés savantes</h2>
    </div>
    <div class="grid grid-2" style="align-items:start">
      <div class="card">
        <div class="ico">{icon('award')}</div>
        <h3>Certificats</h3>
        <ul class="list-check">
{certs}
        </ul>
      </div>
      <div class="card">
        <div class="ico">{icon('users')}</div>
        <h3>Sociétés savantes</h3>
        <ul class="list-check">
          <li>Membre de la Société Algérienne de Psychiatrie (S.A.P)</li>
          <li>Membre de l’Association Algérienne des Psychiatres d’Exercice Privé (AAPEP)</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <h2>Rendez-vous</h2>
    <p>
      Vous pouvez faire confiance à ses longues années d’expérience dans la prise en charge
      de personnes en souffrance mentale ou psychologique.
    </p>
    <div class="btn-row">
      <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} {TEL_DISPLAY}</a>
      <a class="btn btn-ghost" href="contact.html">Nous contacter</a>
    </div>
  </div>
</section>
""" + footer()

write("cursus.html", cursus)


# --------------------------------------------------------------- liste articles

all_cards = "\n".join(post_card(a) for a in articles)

liste = head(
    "Articles — " + DOC,
    "Articles du " + DOC + " : dépression, psychothérapie, hypnose ericksonienne, relaxation, "
    "médicaments psychotropes, santé mentale et COVID-19.",
    "articles.html",
) + header("articles.html") + f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Lecture</p>
    <h1>Articles</h1>
    <p>Actualité médicale, repères et explications sur les troubles psychiatriques et neurologiques.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="posts">
{all_cards}
    </div>
  </div>
</section>
""" + footer()

write("articles.html", liste)


# --------------------------------------------------------------- contact

contact = head(
    "Contact — " + DOC,
    "Contacter le cabinet du " + DOC + " à Draria, Alger. Téléphone " + TEL_DISPLAY +
    ", " + ADDR1 + ", " + ADDR2 + ".",
    "contact.html",
) + header("contact.html") + f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">Nous joindre</p>
    <h1>Contact</h1>
    <p>Pour prendre rendez-vous, appelez le {TEL_DISPLAY}. Une assistante répondra à vos appels.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="body">
        <h2>Informations</h2>
        <ul class="info-list">
          <li>
            <span class="ico">{icon('phone', 21)}</span>
            <span><strong>Téléphone</strong>
              <a class="tel-link" href="tel:{TEL_HREF}">{TEL_DISPLAY}</a><br>
              <span style="color:var(--ink-faint);font-size:.9rem">(+213) 549 14 36 48</span>
            </span>
          </li>
          <li>
            <span class="ico">{icon('mail', 21)}</span>
            <span><strong>E-mail</strong><a href="mailto:{EMAIL}">{EMAIL}</a></span>
          </li>
          <li>
            <span class="ico">{icon('map', 21)}</span>
            <span><strong>Adresse</strong>{ADDR1}<br>{ADDR2}</span>
          </li>
          <li>
            <span class="ico">{icon('clock', 21)}</span>
            <span><strong>Horaires de travail</strong>
              Samedi – jeudi&nbsp;: 08:00 – 17:30<br>
              Sur RDV&nbsp;: 08:00 – 09:00 / 16:30 – 17:30<br>
              Pause&nbsp;: 12:00 – 13:00<br>
              Mardi &amp; vendredi&nbsp;: fermé
            </span>
          </li>
        </ul>
        <div class="btn-row" style="margin-top:2rem">
          <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} Appeler le cabinet</a>
          <a class="btn btn-outline" href="mailto:{EMAIL}">Écrire un e-mail</a>
        </div>
      </div>
      <div class="body">
        <h2>Nous trouver</h2>
        <p>
          Le cabinet se situe au centre de Draria, sur l’artère principale,
          à quelques encablures de la Daïra et de l’APC.
        </p>
        <iframe
          class="map-embed"
          title="Carte : emplacement du cabinet à Draria, Alger"
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          src="{MAP_EMBED}"></iframe>
        <p style="margin-top:1rem;font-size:.9rem">
          <a href="{GMAPS_URL}" target="_blank" rel="noopener">Itinéraire avec Google Maps →</a>
          &nbsp;·&nbsp;
          <a href="{OSM_URL}" target="_blank" rel="noopener">Ouvrir dans OpenStreetMap →</a>
        </p>
      </div>
    </div>

    <div class="callout" style="margin-top:3rem">
      <p>
        <strong>Ce site ne peut remplacer une consultation.</strong> Il renseigne sur le fonctionnement
        du cabinet, sur l’adresse et les horaires. En cas d’urgence, contactez les services d’urgence
        ou rendez-vous à l’hôpital le plus proche.
      </p>
    </div>
  </div>
</section>
""" + footer()

write("contact.html", contact)


# --------------------------------------------------------------- articles

for i, a in enumerate(articles):
    v_haut, v_bas, v_ld = video_blocks(a["slug"], "fr", "../")
    # Auteur : le Dr Chikhi par defaut ; certains articles sont d'une autre plume.
    auteur = a.get("author") or DOC
    signature = "%s, %s" % (auteur, a["author_role"]) if a.get("author_role") else auteur
    person = {"@type": "Person", "name": auteur}
    if a.get("author_role"):
        person["jobTitle"] = a["author_role"].capitalize()
    prev_a = articles[i + 1] if i + 1 < len(articles) else None
    next_a = articles[i - 1] if i > 0 else None
    nav_parts = []
    if prev_a:
        nav_parts.append(f'      <a href="{prev_a["slug"]}.html">← {html.escape(prev_a["title"])}</a>')
    else:
        nav_parts.append("      <span></span>")
    if next_a:
        nav_parts.append(f'      <a href="{next_a["slug"]}.html">{html.escape(next_a["title"])} →</a>')
    nav_html = "\n".join(nav_parts)

    hero_img = (f"""  <div class="wrap article-hero">
    <img src="../assets/img/{a['image']}" alt="{html.escape(a.get('alt', ''))}" width="1200" height="440">
  </div>""" if a["image"] else "")

    ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a["title"],
        "description": a.get("description") or a["excerpt"][:160],
        "keywords": a.get("keywords", []),
        "inLanguage": "fr",
        **({"image": "%s/assets/img/%s" % (SITE_URL, a["image"])} if a["image"] else {}),
        "datePublished": a["date"],
        "author": person,
        "publisher": {"@type": "Organization", "name": "Cabinet du " + DOC},
        "mainEntityOfPage": f"{SITE_URL}/articles/{a['slug']}.html",
    }, ensure_ascii=False, indent=1)

    page = head(
        a.get("seo_title") or a["title"] + " — " + DOC,
        a.get("description") or a["excerpt"][:160],
        "articles/" + a["slug"] + ".html",
        depth=1,
        og_image="assets/img/" + a["image"] if a["image"] else "assets/img/2017_12_intestinCerveau.jpg",
        extra=f'<script type="application/ld+json">\n{ld}\n</script>\n' + v_ld,
    ) + header("articles.html", depth=1,
               switch_to=("../ar/articles/%s.html" % a["slug"]) if a["slug"] in AR_ARTICLES else None) + f"""
<article>
  <div class="article-head">
    <div class="narrow">
      <p class="breadcrumb"><a href="../index.html">Accueil</a> / <a href="../articles.html">Articles</a></p>
      <p class="meta">{fr_date(a['date'])} · {html.escape(signature)}</p>
      <h1>{html.escape(a['title'])}</h1>
    </div>
  </div>
{hero_img}
{v_haut}  <div class="prose">
    <div class="narrow">
{a['body']}
    </div>
  </div>
{v_bas}  <div class="narrow" style="padding-bottom:3.5rem">
    <div class="callout">
      <p>
        <strong>Ce site ne peut remplacer une consultation.</strong> Pour un avis adapté à votre situation,
        prenez rendez-vous au <a class="tel-link" href="tel:{TEL_HREF}">{TEL_DISPLAY}</a>.
      </p>
    </div>
    <nav class="article-nav" aria-label="Articles précédent et suivant">
{nav_html}
    </nav>
  </div>
</article>
""" + footer(depth=1)

    write("articles/%s.html" % a["slug"], page)


# --------------------------------------------------------------- version arabe

import pages_ar
pages_ar.build(globals())


# --------------------------------------------------------------- annexes

pages_for_map = ([h for h, _ in NAV] + ["ar/" + p for p in AR_PAGES]
                 + ["articles/%s.html" % a["slug"] for a in articles])
today = "2026-09-18"
urls = "\n".join(
    "  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>" % (SITE_URL, canon_path(p), today)
    for p in pages_for_map)
write("sitemap.xml",
      '<?xml version="1.0" encoding="UTF-8"?>\n'
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")

# build/ contient les sources (traductions en fragments, generateur) : servies par
# GitHub Pages comme le reste du depot, elles n'ont pas a etre indexees.
write("robots.txt", "User-agent: *\nAllow: /\nDisallow: /build/\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)
write(".nojekyll", "")

write("404.html", head("Page introuvable — " + DOC, "La page demandée n’existe pas.", "404.html",
      extra='<meta name="robots" content="noindex">\n<base href="/">\n')
      + header("") + f"""
<section>
  <div class="narrow" style="text-align:center;padding:3rem 0">
    <p class="eyebrow">Erreur 404</p>
    <h1>Cette page n’existe pas</h1>
    <p style="color:var(--ink-soft)">
      Le lien est peut-être erroné ou la page a été déplacée.
    </p>
    <div class="btn-row" style="justify-content:center;margin-top:2rem">
      <a class="btn btn-primary" href="/index.html">Retour à l’accueil</a>
      <a class="btn btn-outline" href="/contact.html">Contact</a>
    </div>
  </div>
</section>
""" + footer())

print("Pages generees :")
for p in sorted(pages_for_map + ["404.html", "sitemap.xml", "robots.txt"]):
    fp = os.path.join(ROOT, p)
    if os.path.exists(fp):
        print("  %-46s %7d o" % (p, os.path.getsize(fp)))
