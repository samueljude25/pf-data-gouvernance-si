# Cahier des charges — Cadre de gouvernance de la donnée

## 1. Objet
Conception et déploiement d'un cadre de gouvernance de la donnée pour une organisation de taille intermédiaire en Afrique centrale. Le cadre couvre la politique qualité, la sécurité, le Master Data Management et la conformité réglementaire.

## 2. Périmètre

### Domaines de données couverts (Phase 1)
- **Données clients / bénéficiaires** : référentiel unique, qualité, accès
- **Données financières** : intégrité, traçabilité, conservation
- **Données ressources humaines** : confidentialité, exactitude, mise à jour

### Extensions prévues (Phase 2 et suivantes)
- Données fournisseurs et partenaires
- Données opérationnelles (stocks, logistique)
- Données analytiques (KPIs, rapports)

## 3. Composantes du cadre

### 3.1 Politique de gouvernance
Document de référence définissant :
- Vision et objectifs de la gouvernance data
- Principes directeurs (qualité, sécurité, accessibilité, conformité)
- Rôles et responsabilités (Data Owner, Data Steward, Data Engineer, DPO)
- Instances de gouvernance (Data Council, comités qualité)
- Processus de gestion des incidents data

### 3.2 Catalogue de données
Inventaire exhaustif des données de l'organisation :
- Description de chaque entité de données
- Source, propriétaire, format, localisation
- Niveau de sensibilité (public, interne, confidentiel, secret)
- Règles de qualité associées
- Flux de données (lineage)

### 3.3 Politique qualité des données
- Définition des 6 dimensions de qualité (complétude, exactitude, cohérence, fraîcheur, unicité, validité)
- Métriques de qualité par domaine et par dimension
- Processus de correction et d'amélioration
- Tableau de bord qualité (scorecard)

### 3.4 Sécurité et classification
- Classification des données selon 4 niveaux de sensibilité
- Politique d'accès et d'habilitation (principe du moindre privilège)
- Politique de chiffrement (au repos et en transit)
- Politique de rétention et d'archivage
- Plan de réponse aux incidents de sécurité data

### 3.5 Master Data Management (MDM)
- Identification des données maîtres (clients, fournisseurs, produits, employés)
- Définition du système de référence (golden record)
- Règles de déduplication et de fusion
- Processus de mise à jour et de synchronisation
- Gouvernance des référentiels (qui peut modifier quoi)

### 3.6 Conformité (RGPD-like)
- Registre des traitements de données personnelles
- Analyse des risques (Privacy Impact Assessment simplifié)
- Procédure de gestion des droits des personnes (accès, rectification, suppression)
- Politique de conservation et de suppression

## 4. Livrables

| Livrable | Format |
|---|---|
| Politique de gouvernance | Document Word/PDF |
| Catalogue de données (initial) | Excel + Apache Atlas |
| Politique qualité + métriques | Document + tableau de bord |
| Classification des données | Document + matrice |
| Charte MDM | Document |
| Registre des traitements | Excel |
| Formation Data Stewards | Supports PPT |
| Guide d'utilisation Apache Atlas | PDF |
