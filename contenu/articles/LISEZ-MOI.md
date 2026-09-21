# Publier un article sur le site

Chaque article est un fichier texte de ce dossier, dont le nom se termine par
`.md`. Une fois enregistré sur GitHub, il apparaît sur le site **en 2 à 3
minutes**, dans la liste des articles et sur la page d'accueil. Rien à installer.

## Écrire un nouvel article

1. Sur GitHub, ouvrez ce dossier : `contenu` → `articles`.
2. Cliquez sur **Add file**, puis **Create new file**.
3. Donnez au fichier le nom du sujet, en minuscules, avec des tirets à la place
   des espaces, par exemple `trouble-anxieux.md`. Ce nom devient l'adresse de
   l'article : `chikhineuropsychiatrie.github.io/articles/trouble-anxieux.html`.
4. Collez le modèle ci-dessous, puis remplacez les exemples par votre texte.
5. L'onglet **Preview** montre la mise en forme.
6. Cliquez sur **Commit changes**, puis encore sur **Commit changes**.

**Ajouter une image** : déposez-la d'abord dans le dossier `assets/img`
(**Add file** → **Upload files**), puis écrivez son nom exact dans l'en-tête
(`image: ...`). Une photo de téléphone convient : elle est redressée, allégée et
débarrassée de ses informations cachées (dont le lieu de prise de vue).

## Le modèle à copier

```
---
titre: Le trouble anxieux généralisé
date: 2026-10-05
resume: Deux ou trois phrases qui donnent envie de lire l'article. Elles apparaissent dans la liste des articles.
image: anxiete.jpg
legende_image: Une femme assise près d'une fenêtre, l'air pensif
mots_cles: anxiété, angoisse, inquiétude, psychiatre Draria
---

Le texte commence ici. Pour changer de paragraphe, laissez une ligne vide.

## Un intertitre

Du texte en **gras** ou en *italique*.

- une liste
- à puces

1. une liste
2. numérotée

> Une citation.

Un [lien vers un autre site](https://www.who.int/fr).
```

## Les lignes de l'en-tête

| Ligne | Obligatoire | À quoi elle sert |
|---|---|---|
| `titre` | oui | Le titre de l'article. |
| `date` | oui | Date de publication : `2026-10-05` ou `05/10/2026`. |
| `resume` | non | Texte de la liste des articles. Par défaut : le début du premier paragraphe. |
| `image` | non | Nom d'une image déposée dans `assets/img`. |
| `legende_image` | non | Description de l'image, lue aux personnes malvoyantes. |
| `mots_cles` | non | Mots séparés par des virgules, pour les moteurs de recherche. |
| `auteur` | non | Laisser absent pour le Dr Chikhi. Sinon le prénom, par exemple `Roza`. |
| `fonction_auteur` | non | Avec `auteur`, par exemple `pharmacienne`. |
| `description` | non | Texte affiché par Google sous le titre (160 caractères). Par défaut : le résumé. |
| `titre_seo` | non | Titre affiché par Google, s'il doit différer du titre. |
| `brouillon` | non | `oui` : l'article n'est pas publié. |

## Modifier ou retirer un article

- **Modifier** : ouvrez le fichier, cliquez sur le crayon (**Edit**), corrigez,
  puis **Commit changes**.
- **Retirer** : ouvrez le fichier, menu **…** en haut à droite, **Delete file**.
  La page disparaît du site.

## Bon à savoir

- Ce dépôt est **public** : un brouillon enregistré ici n'est pas sur le site,
  mais reste lisible sur GitHub. Préparez les textes sensibles ailleurs.
- Jamais de témoignage ni de détail permettant de reconnaître un patient
  (secret médical).
- Si l'en-tête contient une erreur, le site n'est simplement pas mis à jour.
  L'onglet **Actions** du dépôt affiche alors une croix rouge ; en cliquant
  dessus, le message indique le fichier et la ligne à corriger.
- Les fichiers dont le nom commence par `_` sont ignorés : `_modele.md` sert de
  point de départ.
