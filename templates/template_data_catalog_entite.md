# Fiche Catalogue — [NOM DE L'ENTITÉ]

> *Instructions : Compléter tous les champs. Les champs marqués [OBLIGATOIRE] doivent être renseignés avant publication.*

---

## En-tête

| Champ | Valeur |
|-------|--------|
| **ID Catalogue** [OBLIGATOIRE] | CAT-XXX-000 |
| **Nom de l'entité (technique)** [OBLIGATOIRE] | [nom_table_ou_fichier] |
| **Nom métier** [OBLIGATOIRE] | [Libellé compréhensible] |
| **Domaine métier** [OBLIGATOIRE] | [Commercial / Finance / RH / Opérations / Référentiel] |
| **Type** [OBLIGATOIRE] | [Table BDD / Fichier CSV / API / Vue / Rapport] |
| **Statut** [OBLIGATOIRE] | [Actif / Deprecated / En migration] |
| **Version catalogue** | 1.0 |
| **Date création fiche** | [AAAA-MM-JJ] |
| **Date dernière mise à jour** | [AAAA-MM-JJ] |
| **Auteur de la fiche** | [Prénom NOM — Data Steward] |

---

## Gouvernance

| Champ | Valeur |
|-------|--------|
| **Data Owner** [OBLIGATOIRE] | [Titre — Prénom NOM] |
| **Data Steward** [OBLIGATOIRE] | [Prénom NOM] |
| **Data Custodian** | [Prénom NOM — DSI] |
| **Classification** [OBLIGATOIRE] | [PUBLIC / INTERNE / CONFIDENTIEL / SECRET] |
| **Contient des données personnelles** [OBLIGATOIRE] | [Oui / Non / Partiellement] |
| **Référence registre traitements** | [TRT-XXX si applicable] |
| **Accord de traitement requis** | [Oui / Non] |

---

## Description Métier

### Définition
*[Expliquer clairement et simplement ce que contient cette entité, en langage accessible aux non-techniciens.]*

### Finalité d'usage
*[À quoi servent ces données ? Quelles décisions permettent-elles ?]*

### Utilisateurs typiques
*[Qui utilise typiquement ces données et dans quel but ?]*

- [Rôle 1] : [Usage]
- [Rôle 2] : [Usage]

### Termes du glossaire associés
- [Terme 1] — voir glossaire-metier.md
- [Terme 2] — voir glossaire-metier.md

### Données associées
*[Quelles autres entités sont liées à celle-ci ?]*

- Liée à : [Entité A] (via [champ de jointure])
- Alimente : [Entité B]
- Source de : [Entité C]

### Contraintes métier importantes
*[Règles importantes que tout utilisateur doit connaître]*

- [Contrainte 1]
- [Contrainte 2]

---

## Localisation Technique

| Champ | Valeur |
|-------|--------|
| **Système source** | [CRM / ERP / LEGACY / etc.] |
| **Environnement** | [Production / Préproduction / Test] |
| **Serveur / Host** | [nom-serveur.domaine] |
| **Base de données** | [nom_base] |
| **Schéma** | [nom_schema] |
| **Nom technique** | [nom_exact_table_ou_fichier] |
| **Format** | [MySQL / PostgreSQL / Parquet / CSV / etc.] |
| **Volumétrie actuelle** | [X enregistrements — X MB/GB] |
| **Croissance estimée** | [X enregistrements/mois] |
| **URL / Connexion** | [à renseigner par le Data Custodian] |

---

## Dictionnaire des Attributs

| Nom champ | Type | Taille | Obligatoire | Clé | Description | Format | Exemple |
|-----------|------|--------|-------------|-----|-------------|--------|---------|
| [champ_1] | VARCHAR | 10 | Oui | PK | [Description] | [Format] | [Exemple] |
| [champ_2] | VARCHAR | 100 | Oui | - | [Description] | [Format] | [Exemple] |
| [champ_3] | DATE | - | Non | - | [Description] | YYYY-MM-DD | 2026-01-15 |
| [champ_4] | DECIMAL | 10,2 | Oui | - | [Description] | NNN.NN | 45000.00 |
| [champ_5] | INTEGER | - | Non | FK | [Description] | [Format] | [Exemple] |

---

## Qualité des Données

*[Compléter après exécution du script scoring.py]*

| Dimension | Score | Cible | Statut |
|-----------|-------|-------|--------|
| Complétude | [X]% | 95% | [OK / ALERTE / CRITIQUE] |
| Exactitude | [X]% | 90% | [OK / ALERTE / CRITIQUE] |
| Cohérence | [X]% | 99% | [OK / ALERTE / CRITIQUE] |
| Actualité | [X]% | 85% | [OK / ALERTE / CRITIQUE] |
| Unicité | [X]% | 98% | [OK / ALERTE / CRITIQUE] |
| Validité | [X]% | 95% | [OK / ALERTE / CRITIQUE] |
| **Score global** | **[X]/100** | **85/100** | **[Niveau]** |

**Date de dernière évaluation qualité :** [AAAA-MM-JJ]
**Fréquence d'évaluation :** [Quotidienne / Hebdomadaire / Mensuelle]

---

## Cycle de Vie

| Champ | Valeur |
|-------|--------|
| **Fréquence de mise à jour** | [Temps réel / Quotidienne / Hebdomadaire / Mensuelle] |
| **Délai de disponibilité** | [Délai entre production et disponibilité] |
| **Durée de rétention active** | [X ans] |
| **Durée d'archivage** | [X ans] |
| **Durée totale de conservation** | [X ans] |
| **Politique de destruction** | [Méthode d'effacement certifié] |
| **Base légale de conservation** | [OHADA / Contrat / Légal / etc.] |

---

## Lignage (Data Lineage)

### Sources
```
[Source 1] ──► [Ce dataset]
[Source 2] ──► [Ce dataset]
```

### Consommateurs
```
[Ce dataset] ──► [Consommateur 1]
[Ce dataset] ──► [Consommateur 2]
```

### Transformations principales
*[Décrire les principales transformations appliquées entre les sources et ce dataset]*

---

## Historique des modifications

| Date | Version | Auteur | Description |
|------|---------|--------|-------------|
| [AAAA-MM-JJ] | 1.0 | [Auteur] | Création initiale de la fiche |

---

## Tags

`[domaine]` `[classification]` `[entite-maitre / transactionnel / referentiel]` `[confidentiel si applicable]`

---

*Fiche catalogue produite dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
