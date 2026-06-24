# Lignage des Données (Data Lineage)

**Version :** 1.0
**Date :** 2026-06-01
**Référentiel :** DAMA-DMBOK

---

## 1. Introduction

Le **lignage des données** (data lineage) est la traçabilité complète du parcours d'une donnée depuis sa source d'origine jusqu'à son utilisation finale, en documentant toutes les transformations, validations et déplacements intermédiaires.

### 1.1 Pourquoi le lignage ?

- **Débogage et résolution d'incidents :** Identifier rapidement d'où vient une donnée erronée
- **Analyse d'impact :** Savoir quels rapports et systèmes sont affectés si une source change
- **Conformité RGPD-like :** Tracer où vont les données personnelles et qui y accède
- **Confiance dans les données :** Les utilisateurs comprennent l'origine des données utilisées
- **Audit :** Justifier l'exactitude des chiffres présentés dans les rapports officiels

### 1.2 Niveaux de lignage

| Niveau | Granularité | Usage |
|--------|-------------|-------|
| Système | Source → Destination (niveau application) | Vue d'ensemble architecturale |
| Entité | Table → Table (avec transformations) | Analyse d'impact par table |
| Attribut | Champ → Champ (transformation détaillée) | Débogage, certification de chiffre |

---

## 2. Diagrammes de lignage — Vue système

### 2.1 Architecture générale des flux de données

```
╔══════════════════════════════════════════════════════════════════════════╗
║                     SOURCES OPÉRATIONNELLES                             ║
╠══════════════════════════════════════════════════════════════════════════╣
║  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  ┌──────────────┐   ║
║  │     CRM     │  │     ERP     │  │   LEGACY   │  │   AGENCES    │   ║
║  │(Clients,    │  │(Stocks,     │  │ SYSTEM     │  │  (Terrain,   │   ║
║  │ Prospects)  │  │ Commandes,  │  │(Historique │  │  Mobile)     │   ║
║  │             │  │ Facturation)│  │ pré-2020)  │  │              │   ║
║  └──────┬──────┘  └──────┬──────┘  └─────┬──────┘  └──────┬───────┘   ║
╚═════════╪════════════════╪════════════════╪════════════════╪═══════════╝
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                    │
                                    ▼
╔══════════════════════════════════════════════════════════════════════════╗
║                          ZONE DE STAGING                                ║
║  ┌──────────────────────────────────────────────────────────────────┐  ║
║  │   Extraction brute — Copie conforme des données sources          │  ║
║  │   Aucune transformation — données brutes préservées              │  ║
║  └──────────────────────────────────────────────────────────────────┘  ║
╚════════════════════════════════════╪═════════════════════════════════════╝
                                    │
                                    ▼
╔══════════════════════════════════════════════════════════════════════════╗
║                       ZONE DE TRANSFORMATION (ETL)                      ║
║  ┌─────────────────────────────────────────────────────────────────┐   ║
║  │  • Nettoyage et standardisation                                 │   ║
║  │  • Application des règles de qualité                            │   ║
║  │  • Déduplication et réconciliation                              │   ║
║  │  • Enrichissement (géocodage, scoring, etc.)                    │   ║
║  │  • Mise en conformité des formats                               │   ║
║  └─────────────────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════╪══════════════════════════════════════╝
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
╔═══════════════════════╗       ╔══════════════════════════════╗
║    HUB MDM            ║       ║    DATA WAREHOUSE            ║
║ ┌──────────────────┐  ║       ║ ┌──────────────────────────┐ ║
║ │  Données Maîtres │  ║       ║ │  Données historisées et  │ ║
║ │  (Golden Records)│  ║       ║ │  modélisées pour analyse │ ║
║ │  Client, Produit,│  ║       ║ │  (schéma en étoile)      │ ║
║ │  Géographie,     │  ║       ║ └──────────────────────────┘ ║
║ │  Organisation    │  ║       ╚══════════════╪═══════════════╝
║ └──────────────────┘  ║                      │
╚═══════════════════════╝                      ▼
          │                    ╔══════════════════════════════╗
          │                    ║    COUCHE ANALYTIQUE         ║
          └──────────────────► ║ ┌──────────────────────────┐ ║
                               ║ │  Tableaux de bord        │ ║
                               ║ │  Rapports réglementaires │ ║
                               ║ │  Analyses ad hoc         │ ║
                               ║ │  Exports et extractions  │ ║
                               ║ └──────────────────────────┘ ║
                               ╚══════════════════════════════╝
```

---

## 3. Lignage par entité — Données Clients

### 3.1 Flux complet de la donnée client

```
SOURCES (3 systèmes)
│
├─ [CRM] → Table: crm.contacts
│          Champs: contact_id, full_name, phone, email, city
│          Fréquence: Temps réel (API webhook)
│          Qualité: Score 82/100
│
├─ [ERP] → Table: erp.business_partners
│          Champs: bp_id, company_name, phone, address, city, country
│          Fréquence: Quotidienne (batch nuit, J+1 à 02h00)
│          Qualité: Score 88/100
│
└─ [LEGACY] → Fichier: legacy_clients_historique.csv
              Champs: id_anc, nom_prenom, tel, ville, dept
              Fréquence: Migration unique (données pré-2020)
              Qualité: Score 71/100

           ▼ ÉTAPE 1 : STAGING (00h00-02h00)
           ┌─────────────────────────────────┐
           │ stg.crm_contacts                │
           │ stg.erp_business_partners       │
           │ stg.legacy_clients              │
           │                                 │
           │ Opération : Copie brute         │
           │ Transformation : Aucune         │
           │ Durée de rétention : 7 jours    │
           └─────────────────┬───────────────┘
                             │
           ▼ ÉTAPE 2 : NETTOYAGE (02h00-03h00)
           ┌─────────────────────────────────┐
           │ clean.clients_standardises      │
           │                                 │
           │ Transformations appliquées :    │
           │  • Normalisation nom (MAJUSC.)  │
           │  • Standardisation tel (+242XX) │
           │  • Validation format email      │
           │  • Nettoyage espaces/accents     │
           │  • Mapping codes départements   │
           └─────────────────┬───────────────┘
                             │
           ▼ ÉTAPE 3 : DÉDUPLICATION MDM (03h00-04h00)
           ┌─────────────────────────────────┐
           │ mdm.clusters_clients            │
           │                                 │
           │ Algorithmes appliqués :         │
           │  • Matching exact sur NNI/RCCM  │
           │  • Fuzzy matching nom+téléphone │
           │  • Score de similarité Jaro-W.  │
           │  • Seuil de fusion : 0.85       │
           └─────────────────┬───────────────┘
                             │
           ▼ ÉTAPE 4 : GOLDEN RECORD (04h00-05h00)
           ┌─────────────────────────────────┐
           │ mdm.t_client_maitre             │
           │                                 │
           │ Règles de survivorship :        │
           │  • id : généré par MDM          │
           │  • nom : CRM > ERP > Legacy     │
           │  • tel : source la + récente    │
           │  • email : source la + récente  │
           │  • adresse : CRM > ERP          │
           │                                 │
           │ Score confiance calculé         │
           └─────────────────┬───────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
    [DW analytique]   [CRM (référence  [API Service
    dw.dim_client      enrichie)]       client]
    Pour analyses      Pour usage        Pour appli
    décisionnelles     commercial       mobile
```

---

## 4. Lignage par entité — Données Financières

### 4.1 Flux de la donnée de transaction

```
SAISIE OPÉRATIONNELLE
        │
        ├─ [Point de vente] → POST /api/transactions
        │                     Validation temps réel
        │
        └─ [Virement bancaire] → Fichier MT940 (SWIFT)
                                 Import quotidien 09h00

        ▼ VALIDATION TEMPS RÉEL
   ┌────────────────────────────────┐
   │ Règles appliquées :            │
   │  • Montant > 0                 │
   │  • Client existant (FK check)  │
   │  • Devise dans liste autorisée │
   │  • Signature électronique OK   │
   │                                │
   │ Si KO → Table: txn_rejetees    │
   │ Si OK → Table: txn_en_attente  │
   └──────────────┬─────────────────┘
                  │
        ▼ VALIDATION MÉTIER (J+1, 08h00)
   ┌────────────────────────────────┐
   │ Contrôles :                   │
   │  • Rapprochement bancaire     │
   │  • Validation contrôleur       │
   │  • Détection anomalies (ML)   │
   │                                │
   │ → t_transaction (VALIDEE)     │
   └──────────────┬─────────────────┘
                  │
        ▼ AGRÉGATION (J+1, 20h00)
   ┌────────────────────────────────┐
   │ dw.fact_transactions          │
   │                                │
   │ Granularité : 1 ligne/txn     │
   │ Historique : 10 ans           │
   └──────────────┬─────────────────┘
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
[Rapport CA   [Tableau    [Rapport
 mensuel]      de bord     fiscal
               DG]         annuel]
```

---

## 5. Lignage attribut — Exemple détaillé

### Champ : `chiffre_affaires_mensuel` dans le rapport de direction

```
Origine des données :

t_transaction.montant          (ERP Production)
       │
       ├─ Filtre : statut = 'VALIDEE'
       ├─ Filtre : type_transaction IN ('VENTE', 'FACTURE')
       ├─ Filtre : date_transaction BETWEEN debut_mois AND fin_mois
       │
       ▼
SOMME(montant)                 (Agrégation SQL)
       │
       ├─ Conversion devise : XAF uniquement
       │  (Taux BCEAofficiel du 1er du mois)
       │
       ▼
dw.fact_ca_mensuel.ca_fcfa    (Data Warehouse)
       │
       ├─ Arrondissement : 2 décimales
       ├─ Division par 1 000 000 pour affichage en millions FCFA
       │
       ▼
rapport_direction.ca_mois     (Rapport Excel / Dashboard)
       │
       Libellé : "Chiffre d'affaires du mois (M FCFA)"
       Exemple : 1 247,83 M FCFA

Certification : validé par le Contrôleur de gestion le 2026-06-01
```

---

## 6. Gestion du lignage

### 6.1 Outillage

| Outil | Usage | Niveau |
|-------|-------|--------|
| Documentation manuelle (ce fichier) | Lignage stratégique et pédagogique | Système, Entité |
| Commentaires SQL (source → destination) | Lignage technique dans les scripts | Entité, Attribut |
| OpenLineage / Marquez | Lignage automatique des pipelines | Entité, Attribut |
| dbt lineage graph | Lignage des modèles de transformation | Entité, Attribut |
| Catalogue de données (champ source) | Référence rapide | Système |

### 6.2 Conventions de documentation

Chaque script ETL doit inclure un en-tête documentant le lignage :

```sql
-- ============================================================
-- SCRIPT : chargement_dim_client.sql
-- SOURCE : stg.crm_contacts + stg.erp_business_partners
-- DESTINATION : dw.dim_client
-- TRANSFORMATION :
--   - Déduplication sur telephone_normalise
--   - Enrichissement departement depuis ref.geographie
--   - Calcul score_confiance MDM
-- DATA OWNER : Directeur Commercial
-- DATA STEWARD : Responsable CRM
-- FRÉQUENCE : Quotidienne à 05h30
-- DERNIÈRE MODIF : 2026-06-01 — S. J. SENDZI
-- ============================================================
```

### 6.3 Analyse d'impact (impact analysis)

Avant toute modification d'une source de données, l'analyse d'impact identifie tous les objets en aval affectés :

```
Exemple : Modification du format du champ "telephone" dans CRM
│
▼ Systèmes impactés :
├─ stg.crm_contacts.phone → transformation standardisation tel
├─ clean.clients_standardises.telephone_normalise → règle nettoyage
├─ mdm.t_client_maitre.telephone_1 → golden record
├─ dw.dim_client.telephone → dimension analytique
├─ rapport_relance_clients.xlsx → export mensuel
└─ api_service_client → appel API externe

Délai minimum avant modification : 5 jours ouvrés
(pour mise à jour de tous les scripts et tests)
```

---

## 7. Traçabilité des données personnelles (RGPD-like)

Le lignage joue un rôle essentiel dans la conformité RGPD-like : il permet de répondre aux questions :
- "Où vont les données personnelles de ce client ?" → Analyse des flux descendants
- "D'où viennent ces données personnelles ?" → Remontée aux sources
- "Qui a accédé à ces données ?" → Journaux d'audit couplés au lignage

```
Données personnelles client Jean MOUYABI (id: CLI-001234)
│
├─ CRM (source) → contrat de service (base légale : Contrat)
│
├─ MDM Hub → Golden record (traiteur : Data Engineer MDM)
│
├─ DW analytique → Analyses agrégées UNIQUEMENT (pseudonymisation)
│
├─ Service client → Consultation lors d'appels (accès tracé)
│
└─ NON transmis à des tiers (sauf réquisition légale)

Durée de conservation : 5 ans après fin de relation (archivage 10 ans)
Droit à l'effacement : applicable — procédure documentée dans conformite-rgpd.md
```

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
