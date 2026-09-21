# -*- coding: utf-8 -*-
"""Images d'apercu des partages (og:image : WhatsApp, Facebook...), 1200 x 630.

Composees en HTML avec la photo du bureau et les polices du site, puis
photographiees par Chrome sans interface. A relancer seulement si le nom, la
specialite ou le telephone changent :   python build/partage.py
"""
import base64, os, pathlib, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TEL = "05 49 14 36 48"
PHONE_SVG = ('<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#fff" stroke-width="1.8" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 '
             '1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .3 1.9.7 '
             '2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.4 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>')

VERSIONS = {
    "og-cabinet.jpg": {
        "lang": "fr", "dir": "ltr", "angle": "90deg", "pos": "72% 50%",
        "sans": '"Inter", sans-serif', "serif": '"Lora", serif', "ls": ".14em", "tt": "uppercase", "h1": 62,
        "eyebrow": "Cabinet médical · Draria, Alger",
        "nom": "Dr F. Chikhi Bengougam",
        "role": "Neuropsychiatre et psychothérapeute",
        "rdv": "Rendez-vous&nbsp;:",
    },
    "og-cabinet-ar.jpg": {
        "lang": "ar", "dir": "rtl", "angle": "270deg", "pos": "20% 50%",
        "sans": '"Noto Sans Arabic", "Inter", sans-serif', "serif": '"Noto Naskh Arabic", serif',
        "ls": "0", "tt": "none", "h1": 60,
        "eyebrow": "عيادة طبية · الدرارية، الجزائر العاصمة",
        "nom": "الدكتورة ف. شيخي بن قوقام",
        "role": "الطب العصبي النفسي والعلاج النفسي",
        "rdv": "لحجز موعد:",
    },
}

GABARIT = """<!DOCTYPE html>
<html lang="{lang}" dir="{dir}"><head><meta charset="utf-8"><style>
@font-face {{ font-family: "Inter"; font-weight: 400 600; src: url("{f_inter}"); }}
@font-face {{ font-family: "Lora"; font-weight: 500 600; src: url("{f_lora}"); }}
@font-face {{ font-family: "Noto Sans Arabic"; font-weight: 400 600; src: url("{f_nsa}");
  unicode-range: U+0600-06FF, U+200C-200E, U+2010-2011, U+FB50-FDFF, U+FE70-FEFC; }}
@font-face {{ font-family: "Noto Naskh Arabic"; font-weight: 500 600; src: url("{f_nna}");
  unicode-range: U+0600-06FF, U+200C-200E, U+2010-2011, U+FB50-FDFF, U+FE70-FEFC; }}
* {{ box-sizing: border-box; margin: 0; }}
html, body {{ width: 1200px; height: 630px; overflow: hidden; background: #12314a; }}
.og {{ position: relative; width: 1200px; height: 630px; overflow: hidden; }}
.photo {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: {pos}; }}
.voile {{ position: absolute; inset: 0; background: linear-gradient({angle}, rgba(18,49,74,.97) 0%,
  rgba(18,49,74,.93) 44%, rgba(18,49,74,.55) 68%, rgba(18,49,74,.06) 90%); }}
.txt {{ position: absolute; top: 0; bottom: 0; inset-inline-start: 76px; width: 700px; display: flex;
  flex-direction: column; justify-content: center; color: #fff; font-family: {sans}; }}
.eyebrow {{ font-weight: 600; font-size: 22px; letter-spacing: {ls}; text-transform: {tt}; color: #9cc4e4; }}
h1 {{ font-family: {serif}; font-weight: 600; font-size: {h1}px; line-height: 1.15; margin: 18px 0 14px; }}
.role {{ font-weight: 500; font-size: 31px; line-height: 1.4; color: #dce9f4; }}
.filet {{ width: 72px; height: 4px; background: #3fa3a3; border-radius: 2px; margin: 34px 0 30px; }}
.rdv {{ display: flex; align-items: center; gap: 18px; font-size: 29px; font-weight: 500; }}
.ico {{ width: 60px; height: 60px; border-radius: 50%; background: #1f6094; display: grid; place-items: center; flex: none; }}
.tel {{ font-family: "Inter", sans-serif; font-weight: 600; font-size: 34px; letter-spacing: .02em; }}
</style></head>
<body><div class="og">
<img class="photo" src="{photo}" alt="">
<div class="voile"></div>
<div class="txt">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{nom}</h1>
  <p class="role">{role}</p>
  <div class="filet"></div>
  <p class="rdv"><span class="ico">{phone}</span><span>{rdv} <span class="tel" dir="ltr">{tel}</span></span></p>
</div></div></body></html>
"""


def photographier(html_txt, png):
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "og.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(html_txt)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1200,630",
                        "--virtual-time-budget=4000", "--user-data-dir=" + os.path.join(tmp, "profil"),
                        "--screenshot=" + png, pathlib.Path(page).as_uri()],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def main():
    img = os.path.join(ROOT, "assets", "img")
    # Polices integrees a la page : aucune dependance aux regles d'acces aux fichiers locaux.
    def data(nom):
        with open(os.path.join(ROOT, "assets", "fonts", nom + ".woff2"), "rb") as f:
            return "data:font/woff2;base64," + base64.b64encode(f.read()).decode()
    fonts = {"f_inter": data("inter-latin"), "f_lora": data("lora-latin"),
             "f_nsa": data("noto-sans-arabic-arabic"), "f_nna": data("noto-naskh-arabic-arabic")}
    photo = pathlib.Path(img, "cabinet-bureau.jpg").as_uri()
    for nom, v in VERSIONS.items():
        png = os.path.join(tempfile.gettempdir(), nom + ".png")
        if os.path.exists(png):
            os.remove(png)
        photographier(GABARIT.format(photo=photo, **fonts, phone=PHONE_SVG, tel=TEL, **v), png)
        with Image.open(png) as im:
            assert im.size == (1200, 630), im.size
            im.convert("RGB").save(os.path.join(img, nom), "JPEG", quality=86, optimize=True, progressive=True)
        os.remove(png)
        print("  %-20s %5.1f Ko" % (nom, os.path.getsize(os.path.join(img, nom)) / 1024))


if __name__ == "__main__":
    sys.exit(main())
