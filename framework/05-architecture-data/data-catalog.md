# Catalogue de Données

**Version :** 1.0
**Date :** 2026-06-01
**Référentiel :** DAMA-DMBOK, ISO 8000

---

## 1. Introduction

Le **catalogue de données** est l'inventaire centralisé et documenté de tous les actifs de données de l'organisation. Il constitue la "carte" du patrimoine data — permettant à tout utilisateur de trouver rapidement quelle donnée existe, où elle se trouve, qui en est responsable, et comment l'utiliser de manière appropriée.

### 1.1 Objectifs du catalogue

- Rendre les données **découvrables** : tout agent peut trouver les données dont il a besoin
- Assurer la **compréhension** : définitions claires, contexte métier documenté
- Gérer la **confiance** : qualité certifiée, propriétaire identifié, score de confiance
- Garantir la **conformité** : classification, droits d'accès, règles RGPD-like
- Faciliter la **collaboration** : commentaires, tags, partage de connaissances

### 1.2 Structure du catalogue

```
Catalogue de données
    │
    ├── Domaines métier
    │       ├── Commercial
    │       ├── Finance
    │       ├── RH
    │       └── Opérations
    │
    ├── Entités (Tables / Fichiers / API)
    │       ├── Fiche entité complète
    │       ├── Dictionnaire des attributs
    │       └── Liens de lignage
    │
    └── Métadonnées
            ├── Techniques (schéma, types, stats)
            ├── Métier (définition, propriétaire, usage)
            └── Opérationnelles (qualité, fraîcheur)
```

---

## 2. Structure d'une fiche entité

Chaque entité documentée dans le catalogue comprend les sections suivantes :

### 2.1 En-tête de fiche

| Champ | Description |
|-------|-------------|
| Identifiant catalogue | Code unique (ex : CAT-COM-001) |
| Nom de l'entité | Nom technique de la table/fichier/API |
| Nom métier | Libellé compréhensible par les non-techniciens |
| Domaine métier | Domaine de rattachement |
| Type | Table BDD / Fichier CSV / API / Vue / Rapport |
| Statut | Actif / Deprecated / En cours de migration |
| Version du catalogue | Version de la documentation |
| Date de création | Date de premier enregistrement dans le catalogue |
| Date de mise à jour | Dernière mise à jour de la documentation |

### 2.2 Propriété et gouvernance

| Champ | Description |
|-------|-------------|
| Data Owner | Propriétaire métier de l'entité |
| Data Steward | Intendant opérationnel |
| Data Custodian | Responsable technique du stockage |
| Niveau de classification | Public / Interne / Confidentiel / Secret |
| Droits d'accès | Résumé des profils autorisés |
| Contient des données personnelles | Oui / Non / Partiellement |
| Référence registre traitements | ID dans le registre des traitements |

### 2.3 Description métier

| Champ | Description |
|-------|-------------|
| Description | Explication claire de ce que contient l'entité |
| Finalité d'usage | À quoi servent ces données |
| Utilisateurs typiques | Qui utilise typiquement ces données |
| Termes du glossaire associés | Liens vers le glossaire métier |
| Données associées | Entités liées (références, dépendances) |
| Contraintes métier | Règles importantes à connaître |

### 2.4 Localisation technique

| Champ | Description |
|-------|-------------|
| Système source | Application ou base d'origine |
| Environnement | Production / Préproduction / Test |
| Serveur / Host | Localisation technique |
| Base de données | Nom de la base |
| Schéma | Schéma de la base |
| Nom technique | Nom exact de la table/fichier |
| Format | Relationnel / Parquet / CSV / JSON / etc. |
| Volumétrie actuelle | Nombre d'enregistrements et taille |
| Croissance estimée | Taux de croissance mensuel |

### 2.5 Qualité des données

| Champ | Description |
|-------|-------------|
| Score qualité global | Score pondéré sur 100 (lien vers scoring) |
| Score complétude | % champs obligatoires renseignés |
| Score exactitude | % de valeurs exactes |
| Score cohérence | % de règles cohérence respectées |
| Score actualité | % d'enregistrements à jour |
| Score unicité | % d'enregistrements non dupliqués |
| Score validité | % de valeurs au format valide |
| Dernière évaluation qualité | Date du dernier calcul de score |
| Fréquence d'évaluation | Quotidienne / Hebdomadaire / Mensuelle |

### 2.6 Cycle de vie

| Champ | Description |
|-------|-------------|
| Fréquence de mise à jour | Temps réel / Quotidien / Hebdomadaire / etc. |
| Délai de disponibilité | Après quel délai les données sont accessibles |
| Durée de rétention active | Durée de conservation en production |
| Durée d'archivage | Durée de conservation en archive |
| Politique de destruction | Méthode de suppression certifiée |

---

## 3. Exemples de fiches entités

### Fiche CAT-COM-001 — Table Clients

```
═══════════════════════════════════════════════════════════════
CATALOGUE DE DONNÉES — FICHE ENTITÉ
ID : CAT-COM-001 | Version : 1.2 | Date MAJ : 2026-06-01
═══════════════════════════════════════════════════════════════

NOM MÉTIER       : Référentiel Clients
NOM TECHNIQUE    : t_client_maitre
DOMAINE          : Commercial
TYPE             : Table base de données relationnelle
STATUT           : Actif [●]

GOUVERNANCE
───────────
Data Owner       : Directeur Commercial
Data Steward     : Responsable CRM
Data Custodian   : DBA Production (DSI)
Classification   : [C] CONFIDENTIEL
Données perso.   : Oui — Référence registre : TRT-001

DESCRIPTION MÉTIER
──────────────────
Contient les informations de référence de tous les clients
actifs et inactifs de l'organisation. Constitue la table
maître utilisée par le CRM, la facturation et le service
client. Golden record consolidé depuis 3 systèmes sources.

Finalité : Gestion de la relation client, facturation,
           analyses commerciales, conformité RGPD.

Utilisateurs : Service commercial, service client, marketing
               (lecture masquée), finance (lecture partielle)

LOCALISATION TECHNIQUE
──────────────────────
Système source   : CRM Salesforce + ERP SAP + Agence Legacy
Environnement    : Production
Serveur          : db-prod-01.organisation.cg
Base de données  : PROD_DW
Schéma           : mdm
Table            : t_client_maitre
Format           : Relationnel (MySQL 8.0)
Volumétrie       : 87 450 enregistrements | 42 MB
Croissance       : ~500 nouveaux clients/mois

QUALITÉ DES DONNÉES (évaluation du 2026-06-01)
───────────────────────────────────────────────
Score global     : 87,3 / 100  [BON ●]
  Complétude     : 88,5%
  Exactitude     : 85,0%
  Cohérence      : 99,7%
  Actualité      : 82,5%
  Unicité        : 93,7%
  Validité       : 94,2%

CYCLE DE VIE
────────────
Mise à jour      : Temps réel (via API MDM)
Rétention active : 5 ans après fin de relation
Archivage        : 10 ans
Destruction      : Effacement certifié + journalisation

ATTRIBUTS PRINCIPAUX (voir dictionnaire complet)
─────────────────────────────────────────────────
id_client        VARCHAR(10)   PK    Identifiant MDM unique
type_client      VARCHAR(20)   NN    Particulier/Entreprise/...
nom              VARCHAR(100)  NN    Nom ou raison sociale
prenom           VARCHAR(100)        Prénom(s)
telephone_1      VARCHAR(15)   NN    Téléphone principal
email            VARCHAR(100)        Email
departement      VARCHAR(50)   NN    Département Congo (FK)
statut           VARCHAR(20)   NN    Actif/Inactif/...
date_creation    DATE          NN    Date création fiche
score_confiance  DECIMAL(5,2)  NN    Score MDM (0-100)

LIGNAGE
───────
Sources → [CRM] → [ERP] → [Agence Legacy]
              ↓
       [MDM HUB (déduplication + golden record)]
              ↓
       [t_client_maitre]
              ↓
  → [DW analytique] → [Tableaux de bord commercial]
  → [Facturation]
  → [Service client]

TAGS : clients | MDM | golden-record | confidentiel | RGPD
═══════════════════════════════════════════════════════════════
```

### Fiche CAT-FIN-001 — Table Transactions

```
═══════════════════════════════════════════════════════════════
CATALOGUE DE DONNÉES — FICHE ENTITÉ
ID : CAT-FIN-001 | Version : 1.0 | Date MAJ : 2026-06-01
═══════════════════════════════════════════════════════════════

NOM MÉTIER       : Journal des Transactions
NOM TECHNIQUE    : t_transaction
DOMAINE          : Finance / Commercial
TYPE             : Table base de données relationnelle
STATUT           : Actif [●]

GOUVERNANCE
───────────
Data Owner       : Directeur Financier
Data Steward     : Contrôleur de gestion
Classification   : [C] CONFIDENTIEL

DESCRIPTION MÉTIER
──────────────────
Enregistre toutes les transactions commerciales et financières
de l'organisation. Chaque ligne représente une opération
atomique (vente, paiement, remboursement, transfert).
Table de faits principale pour les analyses financières.

LOCALISATION TECHNIQUE
──────────────────────
Serveur          : db-prod-01.organisation.cg
Base de données  : PROD_DW
Schéma           : finance
Table            : t_transaction
Volumétrie       : 2 450 000 enregistrements | 1,2 GB
Croissance       : ~15 000 transactions/jour

QUALITÉ DES DONNÉES (évaluation du 2026-06-01)
───────────────────────────────────────────────
Score global     : 93,2 / 100  [BON ●●]
  Complétude     : 95,1%
  Exactitude     : 91,0%
  Cohérence      : 99,5%
  Actualité      : 99,9%
  Unicité        : 99,8%
  Validité       : 97,2%

TAGS : transactions | finance | facturation | confidentiel
═══════════════════════════════════════════════════════════════
```

---

## 4. Dictionnaire de données type

Le dictionnaire de données détaille chaque attribut d'une entité :

| Nom_champ | Type | Longueur | Obligatoire | Clé | Description | Format_attendu | Exemple | Valeurs_autorisees | Source | Propriétaire | Classification | Règle_qualité |
|-----------|------|----------|-------------|-----|-------------|---------------|---------|-------------------|--------|--------------|----------------|---------------|
| id_client | VARCHAR | 10 | Oui | PK | Identifiant unique MDM du client | CLI-NNNNNN | CLI-001234 | Pattern: ^CLI-[0-9]{6}$ | MDM | DirCom | CONFIDENTIEL | CLI-001 |
| type_client | VARCHAR | 20 | Oui | - | Catégorie juridique du client | Liste de valeurs | Entreprise | Particulier,Entreprise,Administration,ONG | CRM | DirCom | CONFIDENTIEL | CLI-012 |
| nom | VARCHAR | 100 | Oui | - | Nom de famille ou raison sociale | Texte libre | MOUYABI | Non vide | CRM | DirCom | CONFIDENTIEL | CLI-002 |

---

## 5. Processus d'alimentation du catalogue

### 5.1 Catalogue automatique (metadata harvesting)

```
Connexion aux sources de données
        │
        ▼
Extraction automatique des métadonnées techniques
(schéma, types, statistiques, relations)
        │
        ▼
Enrichissement manuel par les Data Stewards
(description métier, propriétaire, classification)
        │
        ▼
Validation par le Data Owner
        │
        ▼
Publication dans le catalogue
        │
        ▼
Mise à jour continue (planifiée ou événementielle)
```

### 5.2 SLA de documentation

| Type d'entité | Délai de documentation |
|---------------|----------------------|
| Nouvelle entité en production | ≤ 5 jours ouvrés |
| Modification significative | ≤ 3 jours ouvrés |
| Révision périodique | Annuelle minimum |
| Entité critique (score qualité < 70) | Documentation complète obligatoire avant usage |

---

## 6. KPIs du catalogue

| Indicateur | Formule | Cible |
|------------|---------|-------|
| Taux de couverture | Entités documentées / Entités totales | 100% |
| Complétude des fiches | Fiches complètes / Fiches totales | ≥ 95% |
| Fraîcheur | Fiches mises à jour dans l'année / Total | ≥ 90% |
| Utilisation | Consultations mensuelles uniques | KPI croissance |
| Score qualité moyen des entités | Moyenne des scores qualité | ≥ 85/100 |

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
