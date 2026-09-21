# -*- coding: utf-8 -*-
"""Version arabe du site, sous /ar/ : pages pratiques et articles traduits.

Appele par generate.py, qui lui passe ses globales (gabarits, constantes).
Articles : traductions dans build/articles_ar/<slug>.html (corps HTML) et
build/articles_ar/meta.json (titre, titre de recherche, description, mots-cles,
texte alternatif). Chaque traduction renvoie vers son original francais.

Conventions : usage algerien (« التكفل » pour la prise en charge, mois
maghrebins جانفي/فيفري/ماي...), noms de lieux sous leur forme courante.
Numeros, e-mail et adresse officielle en caracteres latins, forces de gauche
a droite (TEL_LTR, EMAIL_LTR, ADDR1_LTR).
"""
import json, os


def build(g):
    head, header, footer, write, icon = g["head"], g["header"], g["footer"], g["write"], g["icon"]
    TEL, TEL_HREF, MAIL, MAIL_LTR = g["TEL_LTR"], g["TEL_HREF"], g["EMAIL"], g["EMAIL_LTR"]
    ADDR1, ADDR2, DOC = g["ADDR1_LTR"], g["ADDR2_AR"], g["DOC_AR"]

    def page(name, title, desc, body, extra=""):
        write("ar/" + name, head(title, desc, "ar/" + name, depth=1, extra=extra)
              + header(name, depth=1, lang="ar") + body + footer(depth=1, lang="ar"))

    def cards(items, cls="grid-3"):
        out = "\n".join(f"""        <div class="card">
          <div class="ico">{icon(ic)}</div>
          <h3>{t}</h3>
          <p>{d}</p>
        </div>""" for ic, t, d in items)
        return f'    <div class="grid {cls}">\n{out}\n    </div>'

    def checklist(items, indent="          "):
        return "\n".join("%s<li>%s</li>" % (indent, x) for x in items)

    def cta(title, text, second_label, second_href):
        return f"""
<section class="cta-band">
  <div class="wrap">
    <h2>{title}</h2>
    <p>{text}</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} {TEL}</a>
      <a class="btn btn-ghost" href="{second_href}">{second_label}</a>
    </div>
  </div>
</section>
"""

    SERVICES = [
        ("brain", "الطب العصبي النفسي",
         "تشخيص الاضطرابات العصبية والنفسية والتكفل بها: الاكتئاب، القلق، الاضطراب ثنائي القطب، الصرع، الصداع."),
        ("chat", "العلاج النفسي",
         "مقابلات منتظمة في جو من الثقة والسرية، بمفردها أو إلى جانب العلاج الدوائي."),
        ("leaf", "الاسترخاء العلاجي",
         "الاسترخاء العضلي التدريجي والتنويم الإيحائي الإريكسوني، للتخفيف من التوتر والقلق."),
    ]
    DEMARCHE = [
        "تشخيص يقوم على مقابلة وفحوصات واختبارات تكميلية",
        "تكفل ملائم لكل حالة",
        "متابعة منتظمة، مع الإصغاء والنصح",
        "الاسترخاء العلاجي",
    ]
    SOCIETES = [
        "عضو في الجمعية الجزائرية للطب النفسي (SAP)",
        "عضو في الجمعية الجزائرية للأطباء النفسيين الممارسين في القطاع الخاص (AAPEP)",
    ]
    LIEU = ("تقع عيادة الطب العصبي النفسي والعلاج النفسي في وسط الدرارية، على الطريق الرئيسي، "
            "على بعد خطوات من مقر الدائرة والبلدية.")
    CONFIANCE = "يمكنكم الوثوق في خبرتها الطويلة في التكفل بالأشخاص الذين يعانون نفسيا أو ذهنيا."
    ASSISTANTE = "ستتولى مساعدة الرد على مكالماتكم لتحديد موعد."
    AVERTISSEMENT = ("<strong>هذا الموقع لا يغني عن الاستشارة الطبية.</strong> "
                     "هو يعرّف بطريقة عمل العيادة وعنوانها وأوقات عملها. في حالة الطوارئ، "
                     "اتصلوا بمصالح الاستعجالات أو توجهوا إلى أقرب مستشفى.")
    HEURES = "من 08:00 إلى 12:00 ومن 13:00 إلى 17:30"

    # ------------------------------------------------------------ articles traduits
    AR_DIR = os.path.join(g["ROOT"], "build", "articles_ar")
    META = json.load(open(os.path.join(AR_DIR, "meta.json"), encoding="utf-8"))
    TRAD = {s: open(os.path.join(AR_DIR, s + ".html"), encoding="utf-8").read() for s in g["AR_ARTICLES"]}
    MOIS_AR = ["جانفي", "فيفري", "مارس", "أفريل", "ماي", "جوان", "جويلية", "أوت",
               "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
    AUTEURS_AR = {"Roza": ("روزا", "صيدلانية")}

    def ar_date(iso):
        y, m, d = (int(x) for x in iso.split("-"))
        return "%d %s %d" % (d, MOIS_AR[m - 1], y)

    def signature(a):
        if a.get("author"):
            return "%s، %s" % AUTEURS_AR[a["author"]]
        return DOC

    def card(a):
        """Carte d'article depuis /ar/ : traduite si possible, sinon la carte francaise, marquee comme telle."""
        if a["slug"] not in TRAD:
            return g["post_card"](a, 1).replace('<article class="post-card">',
                                                '<article class="post-card" lang="fr" dir="ltr">')
        m, href = META[a["slug"]], "articles/%s.html" % a["slug"]
        img = (f'<div class="thumb"><img src="../assets/img/{a["image"]}" alt="" loading="lazy" '
               f'width="600" height="375"></div>' if a["image"] else "")
        return f"""        <article class="post-card">
{img}
          <div class="body">
            <p class="meta">{ar_date(a["date"])}</p>
            <h3><a href="{href}">{m["title"]}</a></h3>
            <p>{m["description"]}</p>
            <a class="more" href="{href}">اقرأ المقال ←</a>
          </div>
        </article>"""

    # ------------------------------------------------------------ accueil
    doctor_articles = [a for a in g["articles"] if not a.get("author")][:3]
    recent = "\n".join(card(a) for a in doctor_articles)

    page("index.html",
         f"طبيب نفسي بالدرارية — {DOC}",
         f"عيادة {DOC}، طبيبة نفسانية وطبيبة أعصاب بالدرارية، الجزائر العاصمة: "
         "التوتر، القلق، الاكتئاب، الاضطراب ثنائي القطب، الصرع والصداع.",
         f"""
<section class="hero">
  <img class="hero-bg" src="../assets/img/2017_12_intestinCerveau.jpg" alt="" width="1500" height="630" fetchpriority="high">
  <div class="wrap">
    <div class="hero-inner">
      <p class="eyebrow">عيادة طبية · الدرارية، الجزائر العاصمة</p>
      <h1>للخروج من المعاناة والعيش في سلام</h1>
      <p class="lede">
        تستقبل عيادة {DOC}، الأخصائية في الطب النفسي وطب الأعصاب والمعالجة النفسية،
        الأشخاص الذين يمرون بمعاناة نفسية أو عصبية.
      </p>
      <div class="btn-row">
        <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} {TEL}</a>
        <a class="btn btn-ghost" href="cabinet.html">تعرّفوا على العيادة</a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">الاستشارات</p>
      <h2>مجالات التكفل</h2>
      <p>التوتر، القلق، الاكتئاب، الاضطراب ثنائي القطب، الصرع، الصداع، وغيرها من الاضطرابات النفسية والعصبية.</p>
    </div>
{cards(SERVICES)}
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="split">
      <div class="body">
        <p class="eyebrow">العيادة</p>
        <h2>مرحبا بكم</h2>
        <p>{LIEU}</p>
        <p>{CONFIANCE}</p>
        <h3>طريقة العمل</h3>
        <ul class="list-check">
{checklist(DEMARCHE)}
        </ul>
      </div>
      <div class="media">
        <img src="../assets/img/2017_12_lotus-zen1.jpg" alt="زهرة لوتس على سطح الماء" loading="lazy" width="1500" height="630">
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">بطاقة تعريف</p>
      <h2>{DOC}</h2>
      <p>أخصائية في الطب العصبي النفسي، معالجة نفسية، والاسترخاء العلاجي.</p>
    </div>
    <div class="grid grid-3">
      <div class="card">
        <div class="ico">{icon('cap')}</div>
        <h3>التكوين</h3>
        <ul class="list-check">
          <li>شهادة في طب الأعصاب — جامعة الطب بكييف، 2004</li>
          <li>شهادة الدراسات الطبية المتخصصة في الطب النفسي — جامعة الجزائر، 1992</li>
          <li>دكتوراه في الطب — جامعة الجزائر، 1988</li>
        </ul>
      </div>
      <div class="card">
        <div class="ico">{icon('star')}</div>
        <h3>الجمعيات العلمية</h3>
        <ul class="list-check">
{checklist(SOCIETES)}
        </ul>
      </div>
      <div class="card">
        <div class="ico">{icon('map')}</div>
        <h3>العنوان</h3>
        <p>{ADDR1}<br>{ADDR2}</p>
        <p>لحجز موعد، اتصلوا على<br>
          <a class="tel-link" href="tel:{TEL_HREF}"><strong>{TEL}</strong></a>
        </p>
      </div>
    </div>
    <p style="margin-top:2rem"><a class="btn btn-outline" href="cursus.html">المسار المهني كاملا</a></p>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">قراءات</p>
      <h2>مقالات {DOC}</h2>
      <p>شروحات حول الاضطرابات النفسية والعصبية.</p>
    </div>
    <div class="posts">
{recent}
    </div>
    <p style="margin-top:2.2rem"><a class="btn btn-outline" href="articles.html">جميع المقالات</a></p>
  </div>
</section>
""" + cta("احجزوا موعدا", "يمكنكم الاتصال بنا هاتفيا. " + ASSISTANTE, "معلومات الاتصال", "contact.html"),
         extra='<script type="application/ld+json">\n%s\n</script>\n' % g["SCHEMA"])

    # ------------------------------------------------------------ cabinet
    page("cabinet.html",
         f"العيادة — {DOC}، الدرارية",
         f"عيادة {DOC} للطب العصبي النفسي والعلاج النفسي في وسط الدرارية، الجزائر العاصمة: "
         "استشارات، علاج نفسي واسترخاء علاجي.",
         f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">العيادة</p>
    <h1>عيادتنا</h1>
    <p>تستقبلكم عيادة {DOC} إذا كنتم تبحثون عن استشارة في الطب العصبي النفسي أو العلاج النفسي.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="split">
      <div class="body">
        <h2>في قلب الدرارية</h2>
        <p>{LIEU}</p>
        <p>
          نتكفل بالاضطرابات النفسية والعقلية والعصبية: التوتر، القلق، الاكتئاب، الاضطراب ثنائي القطب،
          الصرع، الصداع، وغيرها من الاضطرابات النفسية أو العصبية.
        </p>
        <p>{CONFIANCE}</p>
      </div>
      <figure class="media">
        <img src="../assets/img/draria-chateau.jpg" alt="قصر الدرارية ببرجيه المدببين تحت سماء زرقاء" width="1200" height="804" loading="lazy">
        <figcaption>
          قصر الدرارية. تصوير:
          <a href="https://commons.wikimedia.org/wiki/File:Photo_chateau_draria_30052016.jpg" target="_blank" rel="noopener">Sandervalya</a>،
          رخصة <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ar" target="_blank" rel="noopener">CC BY-SA 4.0</a>،
          عبر ويكيميديا كومنز.
        </figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">الاستشارات</p>
      <h2>خدماتنا</h2>
    </div>
{cards(SERVICES)}
  </div>
</section>

<section>
  <div class="wrap">
    <div class="split">
      <div class="body">
        <h2>مراحل التكفل</h2>
        <ul class="list-check">
{checklist(DEMARCHE)}
        </ul>
        <p style="margin-top:1.6rem">
          <a class="btn btn-outline" href="horaires.html">أوقات العمل</a>
        </p>
      </div>
      <div class="body">
        <div class="callout">
          <p>{AVERTISSEMENT}</p>
        </div>
      </div>
    </div>
  </div>
</section>
""" + cta("احجزوا موعدا", ASSISTANTE, "كيف تصلون إلينا", "contact.html"))

    # ------------------------------------------------------------ horaires
    JOURS = [("السبت", HEURES, False), ("الأحد", HEURES, False), ("الإثنين", HEURES, False),
             ("الثلاثاء", "مغلق", True), ("الأربعاء", HEURES, False), ("الخميس", HEURES, False),
             ("الجمعة", "مغلق", True)]
    rows = "\n".join('        <tr%s><th scope="row">%s</th><td>%s</td></tr>'
                     % (' class="closed"' if closed else "", d, h) for d, h, closed in JOURS)

    page("horaires.html",
         f"أوقات العمل — {DOC}، الدرارية",
         f"أوقات عمل عيادة {DOC} بالدرارية: من السبت إلى الخميس، من 08:00 إلى 17:30. "
         "مغلقة يومي الثلاثاء والجمعة. الاستشارات بموعد مسبق.",
         f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">معلومات عملية</p>
    <h1>أوقات عمل العيادة</h1>
    <p>تتم الاستشارات بموعد مسبق. لتحديد موعد، اتصلوا على {TEL}.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="body">
        <table class="hours">
          <caption>العيادة مغلقة يومي الثلاثاء والجمعة.</caption>
          <thead>
            <tr><th scope="col">اليوم</th><th scope="col">الأوقات</th></tr>
          </thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
      <div class="body">
        <h2>للعلم</h2>
        <ul class="list-check">
          <li><strong>الاستراحة</strong> — من 12:00 إلى 13:00</li>
          <li><strong>فترات بموعد مسبق</strong> — من 08:00 إلى 09:00 ومن 16:30 إلى 17:30</li>
          <li><strong>أيام الإغلاق</strong> — الثلاثاء والجمعة</li>
        </ul>
        <div class="callout" style="margin-top:1.8rem">
          <p>
            <strong>حجز المواعيد.</strong> يمكنكم الاتصال بنا على
            <a class="tel-link" href="tel:{TEL_HREF}">{TEL}</a>. {ASSISTANTE}
          </p>
        </div>
        <p style="margin-top:1.8rem">
          <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} اتصلوا بالعيادة</a>
        </p>
      </div>
    </div>
  </div>
</section>
""")

    # ------------------------------------------------------------ cursus
    def timeline(items, ic):
        return "\n".join(f"""        <div class="card">
          <div class="ico">{icon(ic)}</div>
          <p class="meta">{when}</p>
          <h3>{what}</h3>
          <p>{where}</p>
        </div>""" for when, what, where in items)

    FORMATION = [
        ("2004", "شهادة في طب الأعصاب", "جامعة الطب بكييف، أوكرانيا"),
        ("1992", "شهادة الدراسات الطبية المتخصصة في الطب النفسي", "جامعة الطب بالجزائر"),
        ("1988", "دكتوراه في الطب", "جامعة الطب بالجزائر"),
    ]
    EXPERIENCE = [
        ("منذ ماي 2015", "طبيبة أعصاب ونفسية، معالجة نفسية", "عيادة خاصة، الدرارية"),
        ("فيفري 2005", "طبيبة أعصاب ونفسية، معالجة نفسية",
         "عيادة جماعية (الطب العصبي النفسي – جراحة الأعصاب)، الرويبة"),
        ("فيفري 1993", "أخصائية مساعدة في الطب النفسي",
         "المؤسسة الاستشفائية المتخصصة في الطب النفسي بالشراقة"),
        ("1988 – 1992", "طبيبة مقيمة في الطب النفسي",
         "المؤسسة الاستشفائية المتخصصة في الطب النفسي بالقبة"),
    ]
    CERTIFICATS = [
        "معالجة ممارسة بالتنويم الإيحائي — Psynapse (معتمدة من FFHTB)، 2021",
        "شهادة في الاسترخاء العلاجي — المؤسسة الاستشفائية المتخصصة بالشراقة، 1997",
        "شهادة في العلاجات المعرفية السلوكية المطبقة على الاكتئاب والرهاب والقلق — "
        "Renaissance Life Therapies (Libby Seery)، نوفمبر 2017",
        "مدخل إلى التنويم الإيحائي الإريكسوني — البروفيسور ف. كاشا، المؤسسة الاستشفائية المتخصصة بالشراقة، 2017",
        "<bdi>Hypnotherapy Practitioner Diploma</bdi> — Kain Ramsey (Academy of Modern Applied Psychology) "
        "و Steven Burns، المملكة المتحدة",
        "<bdi>Hypnosis Induction Mastery</bdi> — Steven Burns، المملكة المتحدة",
        "<bdi>Ericksonian Hypnosis</bdi> — Daniel Johns، المملكة المتحدة",
    ]

    page("cursus.html",
         f"المسار المهني — {DOC}",
         f"مسار {DOC}: التكوين والشهادات والخبرة المهنية في الطب العصبي النفسي "
         "والعلاج النفسي والتنويم الإيحائي.",
         f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">المسار</p>
    <h1>المسار المهني</h1>
    <p>
      {DOC} — الطب العصبي النفسي، العلاج النفسي والاسترخاء العلاجي.
      تمارس حاليا كطبيبة أعصاب ونفسية ومعالجة نفسية في عيادتها الخاصة بالدرارية.
    </p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">الشهادات</p>
      <h2>التكوين</h2>
    </div>
    <div class="grid grid-3">
{timeline(FORMATION, "cap")}
    </div>
  </div>
</section>

<section class="soft">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">المسار المهني</p>
      <h2>الخبرة المهنية</h2>
      <p>
        عملت في المؤسسة الاستشفائية المتخصصة في الطب النفسي بالشراقة، قبل أن أنضم إلى عيادة جماعية
        (طب الأعصاب، الطب النفسي، جراحة الأعصاب) بالرويبة.
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
      <p class="eyebrow">التكوين المستمر</p>
      <h2>الشهادات والجمعيات العلمية</h2>
    </div>
    <div class="grid grid-2" style="align-items:start">
      <div class="card">
        <div class="ico">{icon('award')}</div>
        <h3>الشهادات</h3>
        <ul class="list-check">
{checklist(CERTIFICATS)}
        </ul>
      </div>
      <div class="card">
        <div class="ico">{icon('users')}</div>
        <h3>الجمعيات العلمية</h3>
        <ul class="list-check">
{checklist(SOCIETES)}
        </ul>
      </div>
    </div>
  </div>
</section>
""" + cta("احجزوا موعدا",
          "يمكنكم الوثوق في سنوات خبرتها الطويلة في التكفل بالأشخاص الذين يعانون نفسيا أو ذهنيا.",
          "اتصلوا بنا", "contact.html"))

    # ------------------------------------------------------------ contact
    page("contact.html",
         f"اتصل بنا — {DOC}، الدرارية",
         f"للاتصال بعيادة {DOC} بالدرارية، الجزائر العاصمة: الهاتف %s، العنوان، "
         "أوقات العمل والخريطة." % g["TEL_DISPLAY"],
         f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">للتواصل</p>
    <h1>اتصل بنا</h1>
    <p>لحجز موعد، اتصلوا على {TEL}. {ASSISTANTE}</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="split" style="align-items:start">
      <div class="body">
        <h2>معلومات</h2>
        <ul class="info-list">
          <li>
            <span class="ico">{icon('phone', 21)}</span>
            <span><strong>الهاتف</strong>
              <a class="tel-link" href="tel:{TEL_HREF}">{TEL}</a><br>
              <span style="color:var(--ink-faint);font-size:.9rem" dir="ltr">(+213) 549 14 36 48</span>
            </span>
          </li>
          <li>
            <span class="ico">{icon('mail', 21)}</span>
            <span><strong>البريد الإلكتروني</strong><a href="mailto:{MAIL}">{MAIL_LTR}</a></span>
          </li>
          <li>
            <span class="ico">{icon('map', 21)}</span>
            <span><strong>العنوان</strong>{ADDR1}<br>{ADDR2}</span>
          </li>
          <li>
            <span class="ico">{icon('clock', 21)}</span>
            <span><strong>أوقات العمل</strong>
              من السبت إلى الخميس: من 08:00 إلى 17:30<br>
              بموعد مسبق: من 08:00 إلى 09:00 ومن 16:30 إلى 17:30<br>
              الاستراحة: من 12:00 إلى 13:00<br>
              الثلاثاء والجمعة: مغلق
            </span>
          </li>
        </ul>
        <div class="btn-row" style="margin-top:2rem">
          <a class="btn btn-primary" href="tel:{TEL_HREF}">{icon('phone', 18)} اتصلوا بالعيادة</a>
          <a class="btn btn-outline" href="mailto:{MAIL}">راسلونا بالبريد الإلكتروني</a>
        </div>
      </div>
      <div class="body">
        <h2>كيف تصلون إلينا</h2>
        <p>{LIEU}</p>
        <iframe
          class="map-embed"
          title="خريطة: موقع العيادة بالدرارية"
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          src="{g["MAP_EMBED"]}"></iframe>
        <p style="margin-top:1rem;font-size:.9rem">
          <a href="{g["GMAPS_URL"]}" target="_blank" rel="noopener">الاتجاهات عبر خرائط Google ←</a>
          &nbsp;·&nbsp;
          <a href="{g["OSM_URL"]}" target="_blank" rel="noopener">فتح في OpenStreetMap ←</a>
        </p>
      </div>
    </div>

    <div class="callout" style="margin-top:3rem">
      <p>{AVERTISSEMENT}</p>
    </div>
  </div>
</section>
""")

    # ------------------------------------------------------------ liste des articles
    page("articles.html",
         f"المقالات — {DOC}",
         f"مقالات {DOC} حول الاكتئاب، العلاج النفسي، التنويم الإيحائي، الاسترخاء، "
         "الأدوية النفسية والصحة النفسية.",
         f"""
<div class="page-head">
  <div class="wrap">
    <p class="eyebrow">قراءات</p>
    <h1>المقالات</h1>
    <p>شروحات حول الاضطرابات النفسية والعصبية، مترجمة عن الأصل الفرنسي.</p>
  </div>
</div>

<section>
  <div class="wrap">
    <div class="posts">
{chr(10).join(card(a) for a in g["articles"])}
    </div>
  </div>
</section>
""")

    # ------------------------------------------------------------ pages des articles
    traduits = [a for a in g["articles"] if a["slug"] in TRAD]
    for i, a in enumerate(traduits):
        slug, m = a["slug"], META[a["slug"]]
        older = traduits[i + 1] if i + 1 < len(traduits) else None
        newer = traduits[i - 1] if i > 0 else None
        nav = "\n".join([
            f'      <a href="{older["slug"]}.html">→ {META[older["slug"]]["title"]}</a>' if older else "      <span></span>",
            f'      <a href="{newer["slug"]}.html">{META[newer["slug"]]["title"]} ←</a>' if newer else "",
        ])
        hero = (f"""  <div class="wrap article-hero">
    <img src="../../assets/img/{a['image']}" alt="{m['alt']}" width="1200" height="440">
  </div>""" if a["image"] else "")
        auteur = ({"@type": "Person", "name": a["author"], "alternateName": AUTEURS_AR[a["author"]][0],
                   "jobTitle": a["author_role"].capitalize()} if a.get("author") else
                  {"@type": "Person", "name": g["DOC"], "alternateName": DOC})
        ld = json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": m["title"],
            "description": m["description"],
            "keywords": m["keywords"],
            "inLanguage": "ar",
            **({"image": "%s/assets/img/%s" % (g["SITE_URL"], a["image"])} if a["image"] else {}),
            "datePublished": a["date"],
            "author": auteur,
            "publisher": {"@type": "Organization", "name": "Cabinet du " + g["DOC"]},
            "mainEntityOfPage": "%s/ar/articles/%s.html" % (g["SITE_URL"], slug),
            "translationOfWork": {"@id": "%s/articles/%s.html" % (g["SITE_URL"], slug)},
        }, ensure_ascii=False, indent=1)
        body = f"""
<article>
  <div class="article-head">
    <div class="narrow">
      <p class="breadcrumb"><a href="../index.html">الرئيسية</a> / <a href="../articles.html">المقالات</a></p>
      <p class="meta">{ar_date(a['date'])} · {signature(a)}</p>
      <h1>{m['title']}</h1>
      <p class="translation-note">
        ترجمة عن الأصل الفرنسي —
        <a href="../../articles/{slug}.html" lang="fr" hreflang="fr">Lire l’original en français</a>
      </p>
    </div>
  </div>
{hero}
  <div class="prose">
    <div class="narrow">
{TRAD[slug]}
    </div>
  </div>
  <div class="narrow" style="padding-bottom:3.5rem">
    <div class="callout">
      <p>
        <strong>هذا الموقع لا يغني عن الاستشارة الطبية.</strong> للحصول على رأي يناسب حالتكم،
        احجزوا موعدا على <a class="tel-link" href="tel:{TEL_HREF}">{TEL}</a>.
      </p>
    </div>
    <nav class="article-nav" aria-label="المقال السابق والتالي">
{nav}
    </nav>
  </div>
</article>
"""
        write("ar/articles/%s.html" % slug,
              head(m["seo_title"], m["description"], "ar/articles/%s.html" % slug, depth=2,
                   og_image="assets/img/" + a["image"] if a["image"] else "assets/img/2017_12_intestinCerveau.jpg",
                   extra='<script type="application/ld+json">\n%s\n</script>\n' % ld)
              + header("articles.html", depth=2, lang="ar", switch_to="../../articles/%s.html" % slug)
              + body + footer(depth=2, lang="ar"))
