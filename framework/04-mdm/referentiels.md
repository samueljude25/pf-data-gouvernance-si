# Référentiels de Données

**Version :** 1.0
**Date :** 2026-06-01
**Maintenu par :** Bureau de Gouvernance des Données

---

## 1. Introduction

Un **référentiel de données** est un jeu de données de référence validé et officiel, utilisé comme source de vérité pour un type d'entité ou une liste de valeurs. Les référentiels garantissent la cohérence entre les systèmes et sont la base de la validation des données opérationnelles.

### Principes de gestion des référentiels

- **Source unique de vérité :** Un seul référentiel officiel par entité
- **Versionnage :** Toute modification est versionnée et datée
- **Gouvernance :** Modifications soumises à validation du Data Owner
- **Disponibilité :** Accessibles à tous les systèmes autorisés
- **Qualité certifiée :** Score qualité ≥ 90/100 requis

---

## 2. Référentiel Clients

### 2.1 Description

**Finalité :** Source de vérité pour toutes les entités clientes de l'organisation
**Data Owner :** Directeur Commercial
**Data Steward :** Responsable CRM
**Système maître :** CRM (hub MDM pour la consolidation)
**Classification :** Confidentiel

### 2.2 Structure du référentiel clients

| Champ | Type | Description | Obligatoire |
|-------|------|-------------|-------------|
| id_client | VARCHAR(10) | Identifiant unique MDM (CLI-XXXXXX) | Oui |
| type_client | VARCHAR(20) | Particulier/Entreprise/Administration/ONG | Oui |
| nom | VARCHAR(100) | Nom de famille ou raison sociale | Oui |
| prenom | VARCHAR(100) | Prénom(s) — personnes physiques | Non |
| date_naissance | DATE | Date de naissance — personnes physiques | Non |
| nni | VARCHAR(20) | Numéro National d'Identification | Non |
| numero_rccm | VARCHAR(30) | Numéro RCCM — personnes morales | Non |
| telephone_1 | VARCHAR(15) | Téléphone principal | Oui |
| telephone_2 | VARCHAR(15) | Téléphone secondaire | Non |
| email | VARCHAR(100) | Adresse email | Non |
| adresse_ligne_1 | VARCHAR(200) | Adresse postale | Non |
| quartier | VARCHAR(100) | Quartier | Non |
| ville | VARCHAR(100) | Ville | Oui |
| departement | VARCHAR(50) | Département Congo | Oui |
| pays | VARCHAR(50) | Pays (défaut : Congo) | Oui |
| statut | VARCHAR(20) | Actif/Inactif/Prospect/Bloqué | Oui |
| segment | VARCHAR(50) | Segment commercial | Non |
| date_creation | DATE | Date de création du compte | Oui |
| date_derniere_maj | TIMESTAMP | Dernière modification | Oui |
| source_creation | VARCHAR(50) | Système ayant créé la fiche | Oui |
| score_confiance | DECIMAL(5,2) | Score MDM de confiance (0-100) | Oui |

### 2.3 Règles de gestion

- Un client ne peut exister qu'une seule fois (unicité sur NNI ou numéro RCCM)
- La déduplication est effectuée mensuellement
- Le statut "Bloqué" nécessite une validation du Directeur Commercial
- Les données des clients inactifs depuis 5 ans sont archivées

---

## 3. Référentiel Produits

### 3.1 Description

**Finalité :** Catalogue officiel des biens et services
**Data Owner :** Directeur Marketing
**Système maître :** ERP / Catalogue produit
**Classification :** Interne

### 3.2 Structure du référentiel produits

| Champ | Type | Description | Obligatoire |
|-------|------|-------------|-------------|
| id_produit | VARCHAR(12) | Identifiant MDM (PRD-CAT-NNNN) | Oui |
| code_interne | VARCHAR(20) | Code ERP interne | Oui |
| code_barres | VARCHAR(20) | Code EAN/UPC si applicable | Non |
| libelle_court | VARCHAR(50) | Libellé abrégé | Oui |
| libelle_long | VARCHAR(500) | Description complète | Non |
| categorie_n1 | VARCHAR(50) | Catégorie principale | Oui |
| categorie_n2 | VARCHAR(50) | Sous-catégorie | Non |
| unite_mesure | VARCHAR(20) | Unité de vente | Oui |
| conditionnement | VARCHAR(50) | Description du conditionnement | Non |
| prix_achat_fcfa | DECIMAL(12,2) | Prix d'achat moyen en FCFA | Non |
| prix_vente_fcfa | DECIMAL(12,2) | Prix de vente de référence en FCFA | Oui |
| tva_taux | DECIMAL(5,2) | Taux de TVA applicable | Oui |
| fournisseur_principal | VARCHAR(10) | ID fournisseur principal | Non |
| origine | VARCHAR(50) | Pays d'origine | Non |
| actif | BOOLEAN | Produit actif dans le catalogue | Oui |
| date_lancement | DATE | Date de mise au catalogue | Oui |
| date_fin | DATE | Date de fin de commercialisation | Non |
| poids_kg | DECIMAL(8,3) | Poids en kg | Non |
| classification_douaniere | VARCHAR(20) | Code douanier (nomenclature) | Non |

---

## 4. Référentiel Géographie

### 4.1 Description

**Finalité :** Référentiel officiel des entités géographiques
**Data Owner :** CDO (données transverses)
**Maintenu par :** Architecte de données
**Classification :** Public (pour le découpage officiel) / Interne (pour les données internes)

### 4.2 Découpage géographique — Congo-Brazzaville

#### Niveau Départements

| Code | Département | Chef-lieu | Code INSEE | Superficie km² |
|------|-------------|-----------|------------|---------------|
| CG-BZV | Brazzaville | Brazzaville | 8 | 100 |
| CG-PNR | Pointe-Noire | Pointe-Noire | 16 | 45 |
| CG-BOU | Bouenza | Madingou | 11 | 12 265 |
| CG-CUV | Cuvette | Owando | 14 | 74 850 |
| CG-CUO | Cuvette-Ouest | Ewo | 15 | 26 600 |
| CG-KOU | Kouilou | Hinda | 5 | 13 694 |
| CG-LEK | Lékoumou | Sibiti | 2 | 20 950 |
| CG-LIK | Likouala | Impfondo | 7 | 66 044 |
| CG-NIA | Niari | Dolisie | 9 | 25 942 |
| CG-PLA | Plateaux | Djambala | 12 | 38 400 |
| CG-POO | Pool | Kinkala | 6 | 33 955 |
| CG-SAN | Sangha | Ouesso | 13 | 55 795 |

#### Niveau Villes/Communes principales

| Code | Ville | Département | Statut |
|------|-------|-------------|--------|
| CG-BZV-001 | Brazzaville | Brazzaville | Capitale nationale |
| CG-PNR-001 | Pointe-Noire | Pointe-Noire | Capitale économique |
| CG-NIA-001 | Dolisie | Niari | Chef-lieu département |
| CG-BOU-001 | Madingou | Bouenza | Chef-lieu département |
| CG-CUV-001 | Owando | Cuvette | Chef-lieu département |
| CG-PLA-001 | Djambala | Plateaux | Chef-lieu département |
| CG-POO-001 | Kinkala | Pool | Chef-lieu département |
| CG-LIK-001 | Impfondo | Likouala | Chef-lieu département |
| CG-SAN-001 | Ouesso | Sangha | Chef-lieu département |
| CG-LEK-001 | Sibiti | Lékoumou | Chef-lieu département |
| CG-KOU-001 | Hinda | Kouilou | Chef-lieu département |
| CG-CUO-001 | Ewo | Cuvette-Ouest | Chef-lieu département |
| CG-NIA-002 | Nkayi | Niari | Ville secondaire |
| CG-BOU-002 | Loutété | Bouenza | Ville secondaire |

### 4.3 Afrique centrale — Pays CEMAC

| Code ISO | Pays | Capitale | Langue officielle | Monnaie |
|----------|------|----------|-------------------|---------|
| CG | Congo-Brazzaville | Brazzaville | Français | XAF (FCFA) |
| CM | Cameroun | Yaoundé | Français / Anglais | XAF (FCFA) |
| CF | Centrafrique | Bangui | Français | XAF (FCFA) |
| TD | Tchad | N'Djamena | Français / Arabe | XAF (FCFA) |
| GQ | Guinée équatoriale | Malabo | Espagnol / Français | XAF (FCFA) |
| GA | Gabon | Libreville | Français | XAF (FCFA) |
| CD | RD Congo | Kinshasa | Français | CDF |
| AO | Angola | Luanda | Portugais | AOA |
| RW | Rwanda | Kigali | Kinyarwanda / Français / Anglais | RWF |
| BI | Burundi | Gitega | Kirundi / Français | BIF |

---

## 5. Référentiel Organisation

### 5.1 Description

**Finalité :** Structure organisationnelle officielle de l'organisation
**Data Owner :** DRH
**Système maître :** SIRH
**Classification :** Interne

### 5.2 Structure organisationnelle type

```
Direction Générale
├── Direction Financière et Comptable (DFC)
│   ├── Service Comptabilité
│   ├── Service Contrôle de Gestion
│   └── Service Trésorerie
├── Direction des Systèmes d'Information (DSI)
│   ├── Service Développement
│   ├── Service Infrastructure
│   └── Service Support Utilisateurs
├── Direction Commerciale (DC)
│   ├── Service Commercial Brazzaville
│   ├── Service Commercial Pointe-Noire
│   └── Service Après-Vente
├── Direction des Ressources Humaines (DRH)
│   ├── Service Recrutement et Formation
│   └── Service Administration du Personnel
└── Direction des Opérations (DO)
    ├── Service Logistique
    └── Service Production
```

---

## 6. Référentiel Devises et Taux

### 6.1 Devises actives

| Code ISO | Devise | Pays principaux | Zone |
|----------|--------|-----------------|------|
| XAF | Franc CFA BEAC | Congo, Cameroun, Gabon, etc. | CEMAC |
| XOF | Franc CFA BCEAO | Sénégal, Côte d'Ivoire, etc. | UEMOA |
| EUR | Euro | France et zone euro | Europe |
| USD | Dollar américain | États-Unis, usage international | Mondial |
| GBP | Livre sterling | Royaume-Uni | Europe |
| NGN | Naira | Nigeria | Afrique de l'Ouest |
| ZAR | Rand | Afrique du Sud | Afrique Australe |
| CDF | Franc congolais | RD Congo | Afrique centrale |

---

## 7. Gouvernance des référentiels

### 7.1 Processus de mise à jour

```
1. Demande de modification → Formulaire standardisé
2. Validation Data Steward → Vérification cohérence
3. Approbation Data Owner → Validation métier
4. Mise en oeuvre technique → Data Custodian
5. Notification des systèmes → Via API ou notification
6. Archivage de l'ancienne version → Conservation 7 ans
```

### 7.2 SLA de disponibilité

- Référentiels critiques (Client, Produit) : disponibilité ≥ 99,9%
- Référentiels standards (Géographie, Organisation) : disponibilité ≥ 99,5%
- Temps de propagation des mises à jour : ≤ 4 heures vers tous les systèmes

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
