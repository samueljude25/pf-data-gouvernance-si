# Classification des Données

**Version :** 1.0
**Date :** 2026-06-01
**Référentiel :** ISO 27001, Loi n° 29-2019 Congo, DAMA-DMBOK

---

## 1. Introduction

La classification des données est le processus par lequel chaque donnée ou actif de données se voit attribuer un niveau de sensibilité, déterminant les mesures de protection à appliquer. Elle constitue le fondement de toute politique de sécurité des données.

**Principe :** Chaque donnée doit être classifiée au niveau le plus élevé applicable. En cas de doute, classer au niveau supérieur.

---

## 2. Les quatre niveaux de classification

### Niveau 1 — PUBLIC

**Code couleur :** Vert
**Icône :** [P]

**Définition :** Données dont la divulgation au grand public est autorisée et ne présente aucun risque pour l'organisation, ses partenaires ou les individus.

**Exemples concrets :**
- Rapport annuel publié sur le site web de l'organisation
- Communiqués de presse et publications officielles
- Données statistiques agrégées sans identification individuelle
- Catalogue public des produits et services avec tarifs publics
- Coordonnées de contact générales de l'organisation (adresse, téléphone standard)
- Offres d'emploi publiées
- Données ouvertes sur les infrastructures (nombre d'écoles par département, etc.)
- Résultats d'appels d'offres publiés au Journal Officiel

**Mesures de protection minimales :**
- Aucune restriction d'accès interne
- Pas de chiffrement requis en transit ou au repos
- Partage externe autorisé sans processus de validation
- Conservation selon les politiques standard

**Qui peut y accéder :** Tout le monde (interne et externe)

---

### Niveau 2 — INTERNE

**Code couleur :** Jaune
**Icône :** [I]

**Définition :** Données destinées à un usage interne à l'organisation. Leur divulgation externe n'est pas autorisée mais ne causerait pas de préjudice grave.

**Exemples concrets :**
- Procédures et manuels internes d'exploitation
- Listes du personnel (nom, poste, service) — sans informations personnelles détaillées
- Plans stratégiques généraux non sensibles
- Budgets globaux approuvés et non détaillés
- Données de performance commerciale (CA global, part de marché)
- Comptes rendus de réunion internes sans information confidentielle
- Données de stock et inventaire (quantités générales)
- Organigramme de l'organisation
- Informations sur les projets en cours (statut général)

**Mesures de protection :**
- Accès limité aux agents de l'organisation
- Chiffrement recommandé pour l'envoi par email
- Pas de partage sur des outils cloud non approuvés
- Mention "INTERNE" ou "Usage interne uniquement" sur les documents
- Verrouillage des sessions après inactivité

**Qui peut y accéder :** Agents de l'organisation selon leur besoin d'en connaître

---

### Niveau 3 — CONFIDENTIEL

**Code couleur :** Orange
**Icône :** [C]

**Définition :** Données sensibles dont la divulgation non autorisée pourrait causer un préjudice significatif à l'organisation, à ses partenaires ou à des individus.

**Exemples concrets :**
- **Données clients** : coordonnées complètes, historique d'achats, informations contractuelles
- **Données financières détaillées** : bilans, comptes de résultat, prévisions budgétaires détaillées
- **Données RH** : salaires, évaluations individuelles, dossiers disciplinaires
- **Données médicales et de santé** : fiches patients, diagnostics, traitements
- **Données personnelles identifiantes** : numéro d'identification national (NNI), passeport, numéro de sécurité sociale
- Propositions commerciales et offres en cours de négociation
- Données des fournisseurs avec conditions tarifaires
- Plans d'affaires et études de marché détaillées
- Données judiciaires et contentieux
- Informations sur les incidents de sécurité

**Mesures de protection :**
- Accès strictement limité aux personnes ayant besoin d'en connaître
- Chiffrement obligatoire en transit et au repos
- Authentification renforcée (MFA recommandé)
- Journalisation de tous les accès
- Mention "CONFIDENTIEL" obligatoire sur tous les documents
- Interdiction de stockage sur appareils personnels ou cloud non approuvé
- Transmission sécurisée uniquement (SFTP, email chiffré, VPN)
- Accord de confidentialité requis pour accès par des tiers

**Qui peut y accéder :** Agents autorisés nominativement, avec traçabilité des accès

---

### Niveau 4 — SECRET

**Code couleur :** Rouge
**Icône :** [S]

**Définition :** Données hautement sensibles dont la divulgation non autorisée pourrait causer un préjudice grave et irréversible à l'organisation, compromettre des intérêts stratégiques nationaux ou violer gravement la vie privée d'individus.

**Exemples concrets :**
- Données biométriques (empreintes digitales, données ADN, reconnaissance faciale)
- Mots de passe, clés cryptographiques, secrets d'authentification
- Données de renseignement ou de sécurité nationale
- Informations classifiées par l'État (défense, sécurité)
- Données sur la santé mentale, les addictions, les antécédents judiciaires
- Secrets commerciaux et formules propriétaires
- Plans de continuité d'activité détaillés
- Données de vulnérabilité des systèmes d'information
- Informations sur les témoins protégés ou personnes en danger
- Numéros de comptes bancaires complets + codes de validation

**Mesures de protection :**
- Accès nominatif avec habilitation formelle signée par la Direction
- Chiffrement de haut niveau obligatoire (AES-256 minimum)
- Authentification multi-facteurs obligatoire
- Journalisation complète et surveillance en temps réel des accès
- Aucune copie autorisée sans approbation écrite du Data Owner
- Stockage sur systèmes dédiés et isolés
- Accès physique contrôlé (salles sécurisées, coffres-forts)
- Destruction certifiée obligatoire (certificat de destruction)
- Tout accès externe interdit sauf exception formellement approuvée

**Qui peut y accéder :** Personnes habilitées nominativement, nombre minimal, avec supervision

---

## 3. Matrice de classification par domaine

| Entité / Donnée | Exemples | Classification |
|----------------|----------|----------------|
| Rapport d'activité publié | CA annuel, effectifs globaux | [P] PUBLIC |
| Coordonnées de contact | Téléphone standard, email info@ | [P] PUBLIC |
| Procédures internes | Manuels de travail, processus | [I] INTERNE |
| Données personnelles basiques | Nom, prénom, poste (annuaire interne) | [I] INTERNE |
| Données clients | Coordonnées, historique, contrats | [C] CONFIDENTIEL |
| Données de paie | Salaires, primes, indemnités | [C] CONFIDENTIEL |
| Données médicales | Diagnostics, traitements, ordonnances | [C] CONFIDENTIEL |
| Données de santé globale | Statistiques épidémio. agrégées | [I] INTERNE |
| Numéros NNI / passeport | Identifiants nationaux | [C] CONFIDENTIEL |
| Données biométriques | Empreintes, iris, photo ID | [S] SECRET |
| Mots de passe systèmes | Credentials, API keys | [S] SECRET |
| Données de vulnérabilité SI | Failles, audits de sécurité | [S] SECRET |
| Données judiciaires | Casiers, condamnations | [S] SECRET |
| Données financières agrégées | CA par département | [I] INTERNE |
| Données financières détaillées | Bilans complets, budgets unitaires | [C] CONFIDENTIEL |
| Secrets commerciaux | Formules, algorithmes propriétaires | [S] SECRET |

---

## 4. Processus de classification

### 4.1 Qui classifie ?

| Acteur | Rôle dans la classification |
|--------|-----------------------------|
| Data Owner | Décide du niveau de classification de son domaine |
| Data Steward | Applique et documente la classification dans le catalogue |
| Data Custodian | Met en oeuvre les mesures techniques de protection |
| CDO | Arbitre en cas de désaccord et valide les classifications Secret |
| Direction Générale | Co-signe les habilitations pour le niveau Secret |

### 4.2 Étapes de classification

```
1. Identification → Lister toutes les entités et attributs de données
2. Évaluation → Analyser la sensibilité et l'impact potentiel d'une divulgation
3. Classification → Attribuer le niveau approprié (principe de précaution)
4. Documentation → Enregistrer dans le catalogue de données
5. Protection → Mettre en place les mesures techniques correspondantes
6. Révision → Revoir la classification lors de tout changement significatif
```

### 4.3 Critères d'évaluation

**Questions à se poser pour classer une donnée :**

1. Quel est l'impact si cette donnée est divulguée à une personne non autorisée ?
   - Aucun impact → PUBLIC
   - Impact limité → INTERNE
   - Impact significatif → CONFIDENTIEL
   - Impact grave et irréversible → SECRET

2. Cette donnée permet-elle d'identifier une personne physique ?
   - Non → ajouter aux critères ci-dessus
   - Oui, indirectement → INTERNE au minimum
   - Oui, directement → CONFIDENTIEL au minimum

3. Cette donnée relève-t-elle d'une catégorie sensible (santé, origine ethnique, données judiciaires) ?
   - Oui → CONFIDENTIEL au minimum, souvent SECRET

---

## 5. Cas particuliers

### 5.1 Données agrégées et anonymisées

Des données individuellement CONFIDENTIELLES peuvent être classifiées INTERNE ou PUBLIC après agrégation et anonymisation irréversible, sous réserve que l'anonymisation ait été vérifiée.

**Exemple :** Les diagnostics individuels de patients sont CONFIDENTIELS. Les statistiques de prévalence des maladies par département, sans aucune information permettant d'identifier un individu, peuvent être classifiées INTERNE ou PUBLIC.

### 5.2 Données héritées

Les données importées depuis d'anciens systèmes sans classification doivent être classifiées selon le processus standard dans les **90 jours** suivant la migration.

### 5.3 Données de test et développement

Les données réelles ne doivent jamais être utilisées en environnement de développement ou de test sans anonymisation préalable. Les données de test doivent être classifiées INTERNE.

### 5.4 Données partagées avec des tiers

Le niveau de classification ne diminue pas lors du partage avec un tiers. Les tiers doivent signer un accord de traitement des données adapté au niveau de classification.

---

## 6. Marquage des documents

Tout document contenant des données classifiées doit être marqué visiblement :

```
[P] PUBLIC                — En-tête et pied de page verts
[I] INTERNE               — En-tête et pied de page jaunes  
[C] CONFIDENTIEL          — En-tête et pied de page oranges, caractères gras
[S] SECRET                — En-tête et pied de page rouges, caractères gras + numérotation des exemplaires
```

Pour les fichiers numériques : préfixer le nom du fichier avec le niveau de classification.
Exemple : `CONFIDENTIEL_liste_clients_brazzaville_2026.xlsx`

---

## 7. Révision de la classification

La classification d'une donnée est révisée :
- Annuellement par le Data Steward du domaine
- Lors de tout changement de contexte réglementaire
- Lors de tout changement significatif de l'usage de la donnée
- Suite à tout incident de sécurité impliquant la donnée

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
*Adapté au cadre réglementaire congolais — Loi n° 29-2019*
