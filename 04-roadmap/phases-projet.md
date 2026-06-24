# Roadmap — Cadre de gouvernance de la donnée

## Vue d'ensemble

| Phase | Durée | Objectif |
|---|---|---|
| Phase 0 — Diagnostic | 3 semaines | Audit maturité, inventaire données |
| Phase 1 — Fondations | 6 semaines | Politique, rôles, catalogue initial |
| Phase 2 — Qualité & MDM | 6 semaines | Métriques qualité, référentiels |
| Phase 3 — Sécurité & conformité | 4 semaines | Classification, accès, registre traitements |
| Phase 4 — Outillage | 4 semaines | Apache Atlas / OpenMetadata, GE |
| Phase 5 — Ancrage | Récurrent | Formation continue, amélioration |

---

## Phase 0 — Diagnostic de maturité (S1–S3)

**Objectifs :**
- Évaluer le niveau de maturité data actuel (niveau 1 à 5)
- Inventorier les principales sources de données et leurs propriétaires
- Identifier les 3 à 5 problèmes de qualité les plus coûteux
- Cartographier les flux de données entre systèmes
- Interviewer les parties prenantes clés (direction, IT, métier)

**Livrables :**
- Rapport de diagnostic de maturité data
- Inventaire des sources de données (catalogue embryonnaire)
- Cartographie des flux (data lineage initial)
- Plan de gouvernance priorisé

---

## Phase 1 — Fondations organisationnelles (S4–S9)

**Objectifs :**
- Rédiger et faire valider la politique de gouvernance de la donnée
- Désigner et former les Data Owners (un par domaine métier)
- Former les Data Stewards (un par domaine, rôle opérationnel)
- Créer le Data Council (instance de décision mensuelle)
- Définir le glossaire métier (termes clés, définitions officielles)

**Livrables :**
- Politique de gouvernance validée par la direction
- Matrice RACI des rôles data
- Charte du Data Council
- Glossaire métier (50 à 100 termes)
- Supports de formation Data Stewards

**Point clé :** Organiser un atelier de lancement (kick-off) avec toutes les parties prenantes pour marquer l'engagement officiel de la direction.

---

## Phase 2 — Qualité des données & MDM (S10–S15)

**Objectifs :**
- Définir les règles de qualité par domaine et par dimension
- Implémenter les premières suites de tests Great Expectations
- Identifier et construire le référentiel clients (golden record)
- Mettre en place le processus de déduplication
- Publier le premier tableau de bord qualité

**Livrables :**
- Dictionnaire des règles qualité par domaine
- Suites Great Expectations déployées
- Référentiel clients nettoyé et dédupliqué
- Tableau de bord qualité Power BI
- SLA de qualité par domaine

---

## Phase 3 — Sécurité & conformité (S16–S19)

**Objectifs :**
- Classer toutes les données selon 4 niveaux de sensibilité
- Auditer les droits d'accès existants et les corriger
- Rédiger le registre des traitements de données personnelles
- Réaliser un Privacy Impact Assessment (PIA) sur les traitements à risque
- Définir la politique de conservation et de suppression

**Livrables :**
- Matrice de classification des données
- Audit des habilitations et plan de remédiation
- Registre des traitements (format CNIL adapté)
- PIAs sur les traitements sensibles
- Politique de conservation et de purge

---

## Phase 4 — Outillage (S20–S23)

**Objectifs :**
- Déployer Apache Atlas ou OpenMetadata
- Charger le catalogue initial dans l'outil
- Configurer le lineage automatique
- Intégrer Great Expectations dans les pipelines
- Former les utilisateurs à l'outil de catalogage

**Livrables :**
- Instance Apache Atlas / OpenMetadata déployée
- Catalogue peuplé (données maîtres + entrepôt)
- Guide d'utilisation du catalogue
- Formation utilisateurs (1 journée)

---

## Phase 5 — Ancrage et amélioration continue (récurrent)

**Mensuellement :**
- Réunion du Data Council (30 min) : revue des incidents qualité, décisions
- Mise à jour du catalogue pour les nouveaux systèmes
- Rapport qualité des données aux Data Owners

**Trimestriellement :**
- Revue de la politique de gouvernance
- Évaluation du niveau de maturité (progression)
- Formation de nouveaux Data Stewards si turnover

**Annuellement :**
- Audit complet de gouvernance (interne ou externe)
- Mise à jour du registre des traitements
- Révision de la classification des données
