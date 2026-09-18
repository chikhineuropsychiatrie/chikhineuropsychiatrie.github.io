# Cabinet du Dr F. Chikhi Bengougam — site statique

Site du cabinet de neuropsychiatrie, psychothérapie et relaxation thérapeutique
de Draria (Alger). Site **statique** (HTML/CSS/JS), sans base de données,
sans PHP, prêt pour GitHub Pages.

---

## Pourquoi cette reconstruction

L'ancien site tournait sous **WordPress 4.9.3** (janvier 2018) avec le thème Enfold.
Au moment de la reprise, il présentait deux problèmes indépendants :

**1. Mise en page effondrée.** Le contenu des pages stocké en base commençait par des
balises `</div>` orphelines (`</div></div></div><!-- close content main div -->`).
Ces fermetures parasites refermaient prématurément les conteneurs du thème : toute la
page s'écroulait en colonnes de quelques dizaines de pixels, avec du texte qui débordait.
S'ajoutaient des attributs corrompus par `wptexturize` (`style= »text-align: center; »`,
guillemets typographiques à la place des guillemets droits) et du balisage doublement
échappé affiché littéralement.

**2. Contenu parasite.** L'installation, sans mise à jour depuis plusieurs années,
contenait des articles et des paragraphes publicitaires sans rapport avec le cabinet,
ajoutés à son insu.

Le contenu légitime a été récupéré via l'API REST de WordPress, nettoyé, puis
republié sous forme de pages statiques. Le reste a été écarté.

Passer au statique supprime la surface d'attaque : plus de PHP, plus de base de
données, plus d'interface d'administration à maintenir ou à corriger.

## Ce qui a été conservé

- **6 pages** : Accueil, Le cabinet, Horaires, Cursus, Articles, Contact
- **10 articles** du Dr Chikhi (2017 → 2023), intégralement
- **15 images** de la médiathèque d'origine (logo, favicon, visuels d'articles)

Les articles parasites et les 19 images de démonstration du thème Enfold
(photos de cabinet dentaire, d'immeubles de bureaux, etc., sans rapport avec le cabinet)
ont été écartés. Elles restent archivées hors dépôt, dans `../chikhi-src/`.

## Ce qui a changé

- HTML sémantique, responsive, sans dépendance JavaScript pour lire le contenu
- Navigation accessible (menu clavier, `aria-current`, lien d'évitement, focus visible)
- Métadonnées SEO et Open Graph par page, `sitemap.xml`, `robots.txt`,
  données structurées JSON-LD (`MedicalBusiness` et `Article`)
- Images redimensionnées et recompressées : **7,8 Mo → 0,8 Mo**
- Carte OpenStreetMap (sans clé d'API ni traceur) à la place de l'ancien embed
- Le formulaire de contact de l'ancien site n'a **pas** été repris : un site statique
  ne peut pas envoyer d'e-mail. La prise de rendez-vous se fait par téléphone, ce que
  le texte d'origine indiquait déjà. Voir « Ajouter un formulaire » plus bas.

---

## Structure

```
index.html          Accueil
cabinet.html        Le cabinet
horaires.html       Horaires
cursus.html         Cursus
articles.html       Liste des articles
contact.html        Contact
404.html            Page d'erreur
articles/*.html     Les 10 articles
assets/css/         Feuille de style unique
assets/js/          Menu mobile (~30 lignes)
assets/img/         Images
build/              Générateur et contenu des articles (voir ci-dessous)
```

## Régénérer le site

Les pages HTML sont **générées** par un script Python. Pour modifier un texte de page,
éditez `build/generate.py` puis relancez :

```bash
python build/generate.py
```

Les articles vivent dans `build/articles.json` (titre, date, visuel, corps HTML).
Pour corriger un article, éditez ce fichier puis relancez `generate.py`.

Les réglages globaux (téléphone, adresse, e-mail, nom, URL du site) sont en haut de
`build/generate.py`.

## Prévisualiser en local

```bash
python -m http.server 8124 --directory .
```

Puis ouvrir http://localhost:8124

---

## Déployer sur GitHub Pages

L'adresse `xxx.github.io` vient du **nom du compte** GitHub, pas du nom du dépôt.
Le site est publié depuis un compte dédié au cabinet, nommé `chikhineuropsychiatrie`
et enregistré à l'adresse e-mail du cabinet. Le site appartient donc au cabinet et
non à un compte personnel ; les personnes qui interviennent dessus sont ajoutées
comme collaborateurs.

1. Sur le compte `chikhineuropsychiatrie`, créer un dépôt **public** nommé
   `chikhineuropsychiatrie.github.io`. Le dépôt doit être public : GitHub Pages
   n'est gratuit que sur les dépôts publics. Sans importance ici, le site est
   de toute façon destiné à être lu par tous, et ne contient rien de confidentiel.
2. **Settings → Collaborators** : ajouter les comptes qui doivent pouvoir publier
   (par exemple `RayaneChikhi`), en accès *Write*. Ils poussent alors avec leur
   propre clé SSH, sans partager le mot de passe du compte du cabinet.
3. Le relier et pousser :

```bash
git remote add origin git@github.com:chikhineuropsychiatrie/chikhineuropsychiatrie.github.io.git
git push -u origin main
```

4. Dans le dépôt : **Settings → Pages → Source : Deploy from a branch**,
   branche `main`, dossier `/ (root)`.

Le site est alors en ligne sur `https://chikhineuropsychiatrie.github.io/`, servi à la
racine — d'où des liens internes relatifs qui fonctionnent sans réglage de chemin de base.
Le fichier `.nojekyll` est présent pour que GitHub serve les fichiers tels quels.

Comptez quelques minutes avant la première mise en ligne.

### Sécurité des comptes

La double authentification doit être active sur le compte GitHub du cabinet et sur
l'adresse e-mail qui lui sert de récupération, et les codes de secours conservés
hors de cette boîte mail.

### Garder le domaine chikhineuropsychiatrie.com

Le **domaine** (l'adresse) et l'**hébergement** (le serveur WordPress) sont deux
prestations distinctes, même si elles sont souvent facturées ensemble. On peut résilier
l'hébergement et garder le domaine : GitHub Pages héberge gratuitement, il ne reste que
le renouvellement annuel du domaine (~10–15 €/an).

À vérifier au préalable : le domaine doit être enregistré **au nom du cabinet**, pas à
celui du prestataire, et il faut un accès au compte du registrar. Si le prestataire est
aussi le registrar, le domaine peut être transféré ailleurs (OVH, Gandi, Cloudflare)
sans être perdu.

Ensuite, chez le registrar, remplacer les enregistrements DNS par :

```
Type    Nom     Valeur
A       @       185.199.108.153
A       @       185.199.109.153
A       @       185.199.110.153
A       @       185.199.111.153
CNAME   www     chikhineuropsychiatrie.github.io.
```

Puis créer à la racine du dépôt un fichier `CNAME` contenant une seule ligne :

```
www.chikhineuropsychiatrie.com
```

et renseigner ce domaine dans **Settings → Pages → Custom domain**, en cochant
**Enforce HTTPS** une fois le certificat émis (quelques minutes à quelques heures).

La variable `SITE_URL` en haut de `build/generate.py` doit correspondre à l'adresse
finale ; elle alimente les balises `canonical`, Open Graph et le `sitemap.xml`.
Après changement, relancer `python build/generate.py`.

> **Ne coupez pas l'hébergement avant** que le nouveau site réponde sur le domaine :
> la propagation DNS peut prendre jusqu'à 48 h.

---

## Ajouter un formulaire de contact

GitHub Pages ne sert que des fichiers statiques : aucun code ne s'exécute côté serveur,
donc pas d'envoi d'e-mail. Deux options si un formulaire devient nécessaire :

- **Formspree** ou **Web3Forms** — l'attribut `action` du formulaire pointe vers leur
  service, qui relaie vers la boîte du cabinet. Offre gratuite suffisante ici.
- **Netlify** — héberge le site (gratuitement aussi) et gère les formulaires nativement.

En l'état, la page Contact met en avant le téléphone et l'adresse e-mail, ce qui
correspond au fonctionnement décrit sur le site d'origine : « une assistante répondra
à vos appels pour fixer un rendez-vous ».

## Licence et contenu

Textes et images appartiennent au cabinet du Dr F. Chikhi Bengougam.
Les articles de 2023 citent leur source d'origine (`semapharma.fr`), comme sur
le site initial.
