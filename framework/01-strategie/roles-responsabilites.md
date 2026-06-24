# Rôles et Responsabilités — Gouvernance des Données

**Version :** 1.0
**Date :** 2026-06-01
**Statut :** Approuvée

---

## 1. Vue d'ensemble des rôles

La gouvernance des données repose sur une organisation claire où chaque acteur a des responsabilités définies. Le modèle adopté s'inspire de DAMA-DMBOK et est adapté aux structures organisationnelles des institutions africaines.

```
Direction Générale
      |
      v
Chief Data Officer (CDO)
      |
      +-- Data Owner (par domaine métier)
      |         |
      |         +-- Data Steward (par domaine)
      |
      +-- Data Custodian (DSI)
      |
      +-- Data Engineer (DSI / Data Team)
      |
      +-- Data Analyst
      |
      +-- Data Consumer (tous les utilisateurs)
```

---

## 2. Descriptions des rôles

### 2.1 Chief Data Officer (CDO) / Responsable Gouvernance des Données

**Niveau hiérarchique :** Direction / N-1 de la Direction Générale

**Mission :** Piloter la stratégie de gouvernance des données de l'organisation, en assurer la cohérence et la mise en œuvre opérationnelle.

**Profil :** Cadre supérieur avec double compétence métier et technique, maîtrise des référentiels de gouvernance (DAMA-DMBOK, ISO 8000), aptitude au leadership transversal.

**Responsabilités :**
- Définir et faire évoluer la stratégie de gouvernance des données
- Animer le Comité de Gouvernance des Données
- Coordonner les Data Owners, Stewards et Custodians
- Piloter les projets de qualité des données et de MDM
- Assurer la conformité réglementaire (protection des données personnelles)
- Produire le rapport de gouvernance mensuel pour la Direction
- Représenter l'organisation sur les questions de gouvernance des données

**Indicateurs de performance :**
- Score qualité global des données (cible ≥ 85/100)
- Taux de couverture du catalogue de données (cible 100%)
- Nombre d'incidents de gouvernance par trimestre (cible 0)
- Taux de conformité aux politiques d'accès (cible 100%)

---

### 2.2 Data Owner (Propriétaire de la Donnée)

**Niveau hiérarchique :** Directeur / Responsable de département métier

**Mission :** Assumer la responsabilité complète d'un domaine de données, de sa définition à sa qualité, en passant par les droits d'accès et les règles d'utilisation.

**Exemples de Data Owners :**
- Directeur Commercial → données clients, prospects, contrats
- Directeur Financier → données comptables, facturation, budgets
- DRH → données ressources humaines, paie, compétences
- Directeur des Opérations → données logistique, stocks, fournisseurs

**Responsabilités :**
- Définir les règles métier applicables à son domaine de données
- Valider les définitions dans le catalogue de données et le glossaire
- Approuver les droits d'accès aux données de son domaine
- Prioriser les actions de qualité pour son périmètre
- Valider les critères de rétention et d'archivage
- Participer aux décisions d'arbitrage en cas de conflit de données
- Signer les analyses d'impact relatives à la protection des données (AIPD)

**Indicateurs de performance :**
- Taux de complétude du catalogue pour son domaine (cible 100%)
- Score qualité de son domaine (cible ≥ 85/100)
- Délai de traitement des demandes d'accès (cible ≤ 5 jours ouvrés)

---

### 2.3 Data Steward (Intendant de la Donnée)

**Niveau hiérarchique :** Expert métier / Analyste senior

**Mission :** Opérer quotidiennement la gouvernance au sein d'un domaine de données, sous l'autorité du Data Owner. Le Data Steward est le garant opérationnel de la qualité et de la conformité.

**Responsabilités :**
- Maintenir à jour les définitions et métadonnées dans le catalogue
- Surveiller la qualité des données via les tableaux de bord
- Identifier, documenter et escalader les problèmes de qualité
- Appliquer et faire respecter les règles de validation
- Former et accompagner les utilisateurs métier de son domaine
- Participer aux projets de migration et d'intégration de données
- Maintenir le glossaire métier pour son domaine
- Coordonner la résolution des doublons avec le Data Engineer
- Participer aux audits de conformité

**Profil :** Bonne connaissance métier du domaine, appétence pour la qualité des données, capacité de communication transversale.

**Indicateurs de performance :**
- Délai de résolution des anomalies de qualité (cible ≤ 48h)
- Taux de documentation des entités de son domaine (cible 100%)
- Nombre de formations dispensées par trimestre (cible ≥ 2)

---

### 2.4 Data Custodian (Gardien de la Donnée)

**Niveau hiérarchique :** Responsable / Expert DSI

**Mission :** Assurer la garde technique des données — leur stockage sécurisé, leur disponibilité, leur sauvegarde et leur protection physique et logique.

**Responsabilités :**
- Mettre en œuvre les politiques de sécurité et de chiffrement
- Gérer les droits d'accès techniques (comptes, profils, permissions)
- Assurer la sauvegarde, la restauration et la continuité d'activité
- Implémenter les politiques de rétention et d'archivage
- Surveiller les performances et la disponibilité des systèmes de données
- Gérer les environnements (production, test, développement)
- Produire les rapports d'audit technique
- Maintenir la documentation technique des systèmes de stockage

**Profil :** Administrateur base de données, architecte infrastructure, administrateur systèmes. Maîtrise des technologies de stockage et de sécurité.

**Indicateurs de performance :**
- Disponibilité des systèmes de données (cible ≥ 99,5%)
- Délai de restauration après incident (cible ≤ RTO défini)
- Conformité des droits d'accès techniques (cible 100%)
- Réalisation des sauvegardes (cible 100%)

---

### 2.5 Data Engineer (Ingénieur de la Donnée)

**Niveau hiérarchique :** Expert technique / Ingénieur DSI ou Data Team

**Mission :** Concevoir, développer et maintenir les pipelines de collecte, de transformation et de chargement des données (ETL/ELT). Garantir la qualité technique des flux de données.

**Responsabilités :**
- Concevoir et développer les pipelines ETL/ELT
- Implémenter les règles de qualité dans les traitements
- Assurer la traçabilité (data lineage) des transformations
- Développer et maintenir les scripts de profiling et de validation
- Gérer les données maîtres (MDM) : déduplication, golden record
- Intégrer les nouvelles sources de données
- Optimiser les performances des traitements
- Documenter les flux et architectures techniques

**Profil :** Maîtrise de Python/SQL, ETL (Talend, Informatica, dbt), bases de données relationnelles et NoSQL. Connaissance des principes de gouvernance des données.

---

### 2.6 Data Analyst (Analyste de la Donnée)

**Niveau hiérarchique :** Expert analytique

**Mission :** Exploiter les données pour produire des analyses, des tableaux de bord et des insights au service des décisions métier. Première ligne de détection des anomalies de qualité.

**Responsabilités :**
- Analyser et interpréter les données pour répondre aux besoins métier
- Signaler les anomalies de qualité détectées lors des analyses
- Contribuer à la définition des règles métier et des indicateurs
- Créer et maintenir les tableaux de bord analytiques
- Respecter les politiques de classification et d'accès
- Documenter les analyses et les définitions des indicateurs
- Participer à la validation des données issues des migrations

---

### 2.7 Data Consumer (Utilisateur de la Donnée)

**Niveau hiérarchique :** Tous niveaux

**Mission :** Utiliser les données dans le cadre de ses activités professionnelles, en respectant les règles définies par la gouvernance.

**Responsabilités :**
- Accéder uniquement aux données autorisées par son profil
- Signaler toute anomalie détectée au Data Steward de son domaine
- Respecter les règles de confidentialité et de sécurité
- Ne pas partager de données sensibles en dehors des canaux autorisés
- Suivre les formations de sensibilisation obligatoires
- Respecter les politiques d'utilisation des données

---

## 3. Matrice RACI

*R = Responsable (fait le travail) | A = Approbateur (valide) | C = Consulté | I = Informé*

### 3.1 Processus de gouvernance des données

| Activité | CDO | Data Owner | Data Steward | Data Custodian | Data Engineer | Data Analyst | Data Consumer |
|----------|-----|-----------|--------------|----------------|---------------|--------------|---------------|
| Définir la politique de gouvernance | A | C | C | I | I | I | I |
| Identifier et nommer les Data Owners | R | A | I | I | I | I | I |
| Définir les règles métier d'un domaine | I | A | R | I | C | C | I |
| Maintenir le catalogue de données | C | A | R | I | C | I | I |
| Maintenir le glossaire métier | C | A | R | I | I | C | I |
| Valider les droits d'accès | A | R | C | C | I | I | I |
| Gérer les droits d'accès techniques | I | I | I | R | C | I | I |
| Surveiller la qualité des données | A | C | R | I | C | C | I |
| Résoudre les anomalies de qualité | C | A | R | I | R | C | I |
| Signaler une anomalie de qualité | I | I | A | I | I | R | R |
| Développer les pipelines ETL | I | C | C | C | R | I | I |
| Assurer les sauvegardes | I | I | I | R | I | I | I |
| Produire les rapports de gouvernance | R | C | C | C | I | C | I |
| Former les utilisateurs | R | C | R | I | I | I | I |
| Gérer les incidents de données | R | A | R | C | C | I | I |
| Approuver les AIPD | A | R | C | C | C | I | I |
| Archiver / détruire les données | A | R | C | R | C | I | I |

### 3.2 Cycle de vie des données

| Phase | CDO | Data Owner | Data Steward | Data Custodian | Data Engineer | Data Consumer |
|-------|-----|-----------|--------------|----------------|---------------|---------------|
| Création / Collecte | I | A | C | I | R | I |
| Stockage | I | A | I | R | C | I |
| Transformation / Traitement | I | C | C | I | R | I |
| Accès / Utilisation | I | A | I | R | I | R |
| Archivage | I | A | C | R | I | I |
| Destruction | I | R | C | R | I | I |

---

## 4. Domaines de données et Data Owners associés

| Domaine | Entités principales | Data Owner | Data Steward |
|---------|---------------------|-----------|--------------|
| Clients & Partenaires | Client, Prospect, Fournisseur, Contact | Directeur Commercial | Responsable CRM |
| Finances & Comptabilité | Compte, Facture, Budget, Transaction | Directeur Financier | Contrôleur de gestion |
| Ressources Humaines | Agent, Contrat, Compétence, Paie | DRH | Responsable RH |
| Produits & Services | Produit, Service, Tarif, Catalogue | Directeur Marketing | Chef de produit |
| Opérations & Logistique | Stock, Commande, Livraison, Site | Directeur des Opérations | Responsable logistique |
| Géographie & Référentiels | Région, Ville, Site, Zone | CDO | Architecte de données |
| Systèmes & Infrastructure | Serveur, Application, Utilisateur SI | DSI | Admin systèmes |

---

## 5. Procédure de nomination et de délégation

### 5.1 Nomination des Data Owners

1. Le CDO identifie les domaines de données critiques
2. En accord avec la Direction Générale, un directeur métier est désigné Data Owner
3. La nomination est formalisée par une lettre de mission signée de la Direction Générale
4. Le Data Owner est formé à ses responsabilités dans les 30 jours suivant sa nomination

### 5.2 Délégation

Un Data Owner peut déléguer certaines tâches opérationnelles à son Data Steward, mais ne peut pas déléguer :
- La validation finale des droits d'accès de niveau Confidentiel et Secret
- L'approbation des analyses d'impact sur la protection des données
- Les décisions d'archivage ou de destruction

### 5.3 Intérim

En cas d'absence du Data Owner, un intérimaire est désigné par le CDO pour une durée maximale de 3 mois.

---

## 6. Révision des rôles

Les descriptions de rôles et la matrice RACI sont révisées :
- Annuellement lors de la révision de la politique de gouvernance
- Lors de toute réorganisation structurelle significative
- À la suite de retours d'expérience identifiant des lacunes dans la couverture des responsabilités

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
