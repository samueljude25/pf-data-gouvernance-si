# Master Data Management (MDM)

**Version :** 1.0
**Date :** 2026-06-01
**Référentiel :** DAMA-DMBOK, ISO 8000

---

## 1. Introduction au MDM

### 1.1 Définition

Le **Master Data Management (MDM)** est l'ensemble des processus, politiques, gouvernance, standards et outils permettant de créer et maintenir une version unique, cohérente, exacte et autorisée des données maîtres de l'organisation.

Les **données maîtres** (ou Master Data) représentent les entités fondamentales du business — les "qui", "quoi" et "où" de l'organisation — qui sont partagées et référencées par l'ensemble des systèmes d'information.

### 1.2 Problématique sans MDM

Sans stratégie MDM, les organisations africaines font face à des problèmes récurrents :

| Problème | Impact | Exemple Congo |
|----------|--------|---------------|
| Doublons clients | Surcoûts, mauvaise relation client | Un client enregistré 3 fois avec 3 numéros différents dans le CRM |
| Référentiels divergents | Incohérence des rapports | Le rapport commercial dit 12 500 clients actifs, le rapport financier dit 11 800 |
| Données obsolètes | Décisions incorrectes | Adresses client incorrectes → taux d'échec livraison > 20% |
| Silos de données | Impossibilité de vision à 360° | Service client ne voit pas les achats récents du client |
| Qualité insuffisante | Conformité réglementaire compromise | Impossibilité d'exercer les droits RGPD-like faute d'identification certaine |

### 1.3 Bénéfices du MDM

- Vision client unique et cohérente à travers tous les canaux et systèmes
- Réduction des doublons et des erreurs de données
- Amélioration de la qualité et de la fiabilité des rapports
- Conformité réglementaire facilitée
- Meilleure expérience client (personnalisation, service cohérent)
- Efficacité opérationnelle accrue (moins de corrections manuelles)

---

## 2. Entités maîtres de l'organisation

### 2.1 Cartographie des entités maîtres

```
                    ENTITÉS MAÎTRES
                          |
         +----------------+----------------+
         |                |                |
      CLIENT          PRODUIT        GÉOGRAPHIE
         |                |                |
    +----+----+      +----+----+     +-----+-----+
    |         |      |         |     |           |
Particulier Entreprise Bien  Service Lieu      Zone
                              |
                     ORGANISATION
                          |
                   +------+------+
                   |             |
               Service      Département
```

### 2.2 Description des entités maîtres

#### Entité : CLIENT

**Périmètre :** Toute personne physique ou morale en relation commerciale avec l'organisation.

**Attributs clés du golden record :**

| Attribut | Description | Obligatoire | Source prioritaire |
|----------|-------------|-------------|-------------------|
| id_client_maitre | Identifiant MDM unique | Oui | Généré par MDM |
| type_client | Particulier / Entreprise / ONG / Administration | Oui | CRM |
| nom_complet | Nom et prénom ou raison sociale | Oui | CRM prioritaire |
| date_naissance | Pour personnes physiques | Non | Système d'enregistrement |
| nni | Numéro National d'Identification | Non | Source officielle |
| telephone_principal | Numéro de contact principal | Oui | Dernier système ayant mis à jour |
| telephone_secondaire | Numéro secondaire | Non | CRM |
| email | Adresse email principale | Non | CRM |
| adresse_complete | Adresse postale complète | Oui | Dernier adresse vérifiée |
| ville | Ville de résidence/siège | Oui | CRM |
| departement | Département Congo | Oui | CRM |
| pays | Pays de résidence/siège | Oui | CRM |
| statut | Actif / Inactif / Prospect / Bloqué | Oui | CRM |
| date_creation_maitre | Date de création dans MDM | Oui | MDM |
| date_derniere_maj | Dernière mise à jour du golden record | Oui | MDM |
| score_confiance | Score de confiance dans les données (0-100) | Oui | MDM calculé |
| sources_consolidees | Liste des systèmes sources | Oui | MDM |

#### Entité : PRODUIT

**Périmètre :** Biens et services proposés par l'organisation.

**Attributs clés du golden record :**

| Attribut | Description | Obligatoire | Source prioritaire |
|----------|-------------|-------------|-------------------|
| id_produit_maitre | Identifiant MDM unique | Oui | Généré par MDM |
| code_produit_interne | Code interne de référence | Oui | ERP |
| libelle_court | Libellé abrégé (50 car. max) | Oui | ERP |
| libelle_long | Description complète | Non | Catalogue produit |
| categorie_n1 | Catégorie principale | Oui | Référentiel catégories |
| categorie_n2 | Sous-catégorie | Non | Référentiel catégories |
| unite_mesure | Unité de vente | Oui | ERP |
| prix_reference_fcfa | Prix de référence en FCFA HT | Oui | Finance |
| actif | Disponible à la vente | Oui | ERP |
| date_creation | Date d'introduction au catalogue | Oui | ERP |
| fournisseur_principal | Identifiant du fournisseur principal | Non | ERP/Achats |

#### Entité : GÉOGRAPHIE

**Périmètre :** Référentiel des zones géographiques, adapté au contexte Congo et Afrique centrale.

**Hiérarchie :**
```
Continent → Région → Pays → Province/Département → Ville/Chef-lieu → Quartier/Zone
```

**Exemples de valeurs (Congo-Brazzaville) :**

| Département | Chef-lieu | Superficie (km²) | Population estimée |
|-------------|-----------|-----------------|-------------------|
| Brazzaville | Brazzaville | 100 | 2 388 000 |
| Pointe-Noire | Pointe-Noire | 45 | 1 042 000 |
| Bouenza | Madingou | 12 265 | 342 000 |
| Cuvette | Owando | 74 850 | 198 000 |
| Cuvette-Ouest | Ewo | 26 600 | 75 000 |
| Kouilou | Hinda | 13 694 | 112 000 |
| Lékoumou | Sibiti | 20 950 | 107 000 |
| Likouala | Impfondo | 66 044 | 185 000 |
| Niari | Dolisie | 25 942 | 267 000 |
| Plateaux | Djambala | 38 400 | 186 000 |
| Pool | Kinkala | 33 955 | 221 000 |
| Sangha | Ouesso | 55 795 | 99 000 |

#### Entité : ORGANISATION

**Périmètre :** Structure organisationnelle interne (directions, services, sites).

**Attributs clés :**

| Attribut | Description |
|----------|-------------|
| id_organisation | Identifiant unique |
| libelle | Nom de l'entité |
| type | Direction / Département / Service / Agence / Site |
| parent_id | Référence vers l'entité parente |
| responsable | Agent responsable de l'entité |
| localisation | Référence vers l'entité géographique |
| actif | Entité active ou non |
| date_creation | Date de création |

---

## 3. Architecture MDM

### 3.1 Modèles d'implémentation

#### Modèle centralisé (Registry)

```
Source 1 (CRM)  ──┐
Source 2 (ERP)  ──┤──► HUB MDM (Golden Record) ──► Systèmes consommateurs
Source 3 (Agence)─┘         (Référentiel central)
```

**Avantages :** Vision unique, gouvernance simplifiée, cohérence garantie
**Inconvénients :** Point unique de défaillance, complexité d'implémentation
**Recommandé pour :** Organisations avec DSI centralisée et peu de systèmes legacy

#### Modèle fédéré (Hub and Spoke)

```
Source 1 ─► MDM Hub ◄─ Source 2
                │
                ▼
         Golden Record
                │
       ┌────────┴────────┐
       ▼                 ▼
 Système A          Système B
```

**Avantages :** Flexibilité, tolérance aux systèmes legacy
**Recommandé pour :** Organisations avec plusieurs systèmes hétérogènes

#### Modèle de coexistence (Recommandé pour le contexte africain)

```
Source 1 ────────────────────────────────► Consommateur 1
   │            ▲         │               
   └──► MDM Hub ─┘    Cross-reference     
Source 2 ────────────────────────────────► Consommateur 2
```

Chaque système source garde ses données. Le MDM maintient les identifiants croisés et le golden record de référence sans remplacer les systèmes existants.

**Recommandé pour :** Phase de transition, ressources limitées, systèmes legacy nombreux.

---

## 4. Golden Record — Construction et maintenance

### 4.1 Définition

Le **golden record** est la version unique, officielle et faisant autorité d'une entité maître. Il est construit par fusion et réconciliation de plusieurs sources de données.

### 4.2 Processus de construction

```
Étape 1 : COLLECTE
    Extraire les enregistrements de toutes les sources sources
    
Étape 2 : STANDARDISATION
    Normaliser les formats (majuscules, espaces, codes pays, etc.)
    
Étape 3 : DÉDUPLICATION
    Identifier les enregistrements représentant la même entité réelle
    (matching exact + fuzzy matching)
    
Étape 4 : CLUSTERING
    Regrouper les enregistrements dupliqués en clusters
    
Étape 5 : SURVIVORSHIP (Règles de survie)
    Appliquer les règles pour choisir la meilleure valeur par attribut
    
Étape 6 : GOLDEN RECORD
    Créer l'enregistrement consolidé
    
Étape 7 : DISTRIBUTION
    Diffuser le golden record aux systèmes consommateurs
    
Étape 8 : MAINTENANCE
    Monitorer les nouvelles entrées et mettre à jour le golden record
```

### 4.3 Règles de survivorship

Les règles de survivorship déterminent, pour chaque attribut, quelle source "gagne" lors de la consolidation :

| Règle | Description | Exemple d'application |
|-------|-------------|----------------------|
| Source la plus fiable | Une source est désignée autoritaire pour un attribut | État civil pour le NNI |
| Valeur la plus récente | La mise à jour la plus récente l'emporte | Numéro de téléphone |
| Valeur la plus complète | La valeur non nulle l'emporte | Adresse complète vs partielle |
| Consensus | La valeur présente dans la majorité des sources | Nom et prénom |
| Règle métier | Logique métier spécifique | Prix : valeur validée par Finance |
| Score de confiance | La source avec le meilleur score qualité | Toute valeur discordante |

### 4.4 Score de confiance MDM

```python
def calculer_score_confiance_golden_record(sources):
    """
    Score de confiance global du golden record (0-100).
    Basé sur : nombre de sources concordantes, fraîcheur, qualité des sources.
    """
    score_sources = len(sources) / MAX_SOURCES * 30        # Max 30 pts
    score_concordance = taux_concordance_sources * 40      # Max 40 pts
    score_fraicheur = score_fraicheur_donnees * 20         # Max 20 pts
    score_completude = taux_completude_attributs * 10      # Max 10 pts
    
    return round(score_sources + score_concordance + score_fraicheur + score_completude, 1)
```

---

## 5. Gouvernance MDM

### 5.1 Rôles MDM

| Rôle | Responsabilités MDM |
|------|---------------------|
| CDO | Définir la stratégie MDM, arbitrage des conflits de golden record |
| Data Owner Entité | Valider les règles de survivorship, approuver les fusions |
| Data Steward MDM | Gérer les conflits non résolus automatiquement, superviser la déduplication |
| Data Engineer MDM | Développer et maintenir les pipelines MDM |
| Utilisateurs | Signaler les doublons détectés, valider les demandes de fusion |

### 5.2 Processus de gestion des conflits

```
Conflit détecté (valeurs discordantes sur un attribut clé)
        │
        ▼
Application des règles de survivorship automatiques
        │
     [Résolu ?]
      /       \
    Oui        Non
     │          │
     ▼          ▼
Golden record  Escalade au Data Steward MDM
mis à jour          │
                    ▼
           Arbitrage manuel (Data Steward + Data Owner)
                    │
                    ▼
           Décision documentée + mise à jour golden record
```

### 5.3 KPIs MDM

| Indicateur | Formule | Cible |
|------------|---------|-------|
| Taux de couverture MDM | Entités dans MDM / Total entités connues | 100% |
| Taux de doublons résiduels | Doublons détectés / Total golden records | < 0,5% |
| Délai de synchronisation | Temps entre modification source et mise à jour golden record | < 24h |
| Score confiance moyen | Moyenne des scores de confiance | > 80/100 |
| Taux de conflits résolus auto | Conflits résolus / Conflits totaux | > 85% |

---

## 6. Feuille de route MDM

### Phase 1 — Fondations (Mois 1-3)
- Inventaire des systèmes sources
- Définition des entités maîtres prioritaires (Client en premier)
- Design du modèle de données MDM
- Sélection du modèle d'implémentation

### Phase 2 — Déduplication initiale (Mois 4-6)
- Extraction et profilage des données existantes
- Campagne de déduplication manuelle assistée
- Établissement des premières règles de survivorship
- Formation des Data Stewards MDM

### Phase 3 — MDM opérationnel (Mois 7-12)
- Déploiement du hub MDM
- Connexion des systèmes sources prioritaires
- Génération des premiers golden records
- Tableau de bord MDM en production

### Phase 4 — Consolidation (Mois 13-18)
- Extension à toutes les entités maîtres
- Automatisation des processus de déduplication
- Intégration avec le catalogue de données
- Optimisation des règles de survivorship

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
