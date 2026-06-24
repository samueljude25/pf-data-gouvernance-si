# Dimensions de la Qualité des Données

**Version :** 1.0
**Date :** 2026-06-01
**Référentiel :** DAMA-DMBOK, ISO 8000

---

## Introduction

La qualité des données est évaluée selon six dimensions fondamentales, chacune mesurant un aspect distinct de l'adéquation des données à leur usage. Ce cadre s'applique à tous les domaines de données de l'organisation et constitue la base du score qualité global.

**Score qualité global = Σ (Score dimension × Poids dimension)**

| Dimension | Poids |
|-----------|-------|
| Complétude | 25% |
| Exactitude | 25% |
| Cohérence | 20% |
| Actualité | 15% |
| Unicité | 10% |
| Validité | 5% |
| **Total** | **100%** |

---

## Dimension 1 — Complétude (Completeness)

### Définition
La complétude mesure le degré auquel toutes les données requises sont présentes. Une donnée est complète lorsque tous les champs obligatoires sont renseignés avec une valeur non nulle et non vide.

### Formule de calcul

```
Taux de complétude = (Nombre de champs obligatoires renseignés / Nombre total de champs obligatoires attendus) × 100
```

Pour un dataset :
```
Score complétude = (1 - Taux de valeurs manquantes dans les champs obligatoires) × 100
```

### Niveaux de complétude

| Score | Niveau | Interprétation |
|-------|--------|----------------|
| 95-100% | Excellent | Données prêtes pour l'utilisation opérationnelle |
| 85-94% | Bon | Utilisable avec attention aux exceptions |
| 70-84% | Acceptable | Amélioration requise avant usage critique |
| < 70% | Insuffisant | Action corrective urgente nécessaire |

### Exemple Congo-Brazzaville

**Entité : Fiche patient — Centre de santé de Makélékélé (Brazzaville)**

| Champ | Obligatoire | Taux de renseignement observé |
|-------|-------------|-------------------------------|
| Nom et prénom | Oui | 99,2% |
| Date de naissance | Oui | 87,4% |
| Numéro de téléphone | Oui | 76,1% |
| Adresse (quartier) | Oui | 91,3% |
| Groupe sanguin | Non | 43,2% |
| Numéro d'assuré social | Non | 12,8% |

Score complétude (champs obligatoires uniquement) :
```
Score = (99,2 + 87,4 + 76,1 + 91,3) / 4 = 88,5%
```

**Problème identifié :** Le numéro de téléphone est trop souvent manquant, ce qui empêche les rappels de rendez-vous. Action : rendre ce champ obligatoire à la saisie.

### Règles de mesure
- Les champs avec valeur par défaut générique ("N/A", "Inconnu", "0000") sont traités comme manquants
- Les espaces blancs seuls sont considérés comme des valeurs manquantes
- La complétude est calculée séparément pour les champs obligatoires et optionnels

---

## Dimension 2 — Exactitude (Accuracy)

### Définition
L'exactitude mesure le degré de correspondance entre les données enregistrées et la réalité qu'elles sont censées représenter. Une donnée est exacte lorsqu'elle reflète fidèlement l'état réel de l'entité.

### Formule de calcul

```
Score exactitude = (Nombre d'enregistrements exacts / Nombre total d'enregistrements vérifiés) × 100
```

L'exactitude nécessite une source de vérité de référence (visite terrain, document officiel, enquête).

### Types d'inexactitude

| Type | Description | Exemple |
|------|-------------|---------|
| Erreur de saisie | Faute de frappe, inversion de chiffres | Téléphone "06" au lieu de "06" → "60" |
| Données obsolètes | Réalité a changé depuis la saisie | Adresse après déménagement |
| Valeur approximative | Arrondi ou estimation excessive | Âge estimé vs date de naissance exacte |
| Valeur incorrecte | Erreur factuelle | Montant de transaction erroné |

### Exemple Congo-Brazzaville

**Entité : Registre des fournisseurs — Direction des marchés publics**

Lors d'un audit par échantillonnage (100 fournisseurs tirés au sort, vérification des coordonnées) :

| Vérification | Conformes | Non conformes | Taux exactitude |
|--------------|-----------|---------------|-----------------|
| Numéro RCCM | 87 | 13 | 87% |
| Adresse du siège | 79 | 21 | 79% |
| Numéro de téléphone | 91 | 9 | 91% |
| Représentant légal | 83 | 17 | 83% |

Score exactitude global = (87 + 79 + 91 + 83) / 4 = **85%**

**Problème identifié :** 21% des adresses de sièges sont incorrectes — souvent en raison du manque de mise à jour après déménagement. Action : mettre en place une vérification annuelle des coordonnées fournisseurs.

---

## Dimension 3 — Cohérence (Consistency)

### Définition
La cohérence mesure l'absence de contradictions entre des données liées, qu'elles soient dans le même enregistrement, dans des tables différentes ou dans des systèmes différents.

### Types d'incohérence

| Type | Description | Exemple |
|------|-------------|---------|
| Incohérence intra-enregistrement | Contradiction au sein d'un même enregistrement | Date de fin < Date de début |
| Incohérence inter-tables | Contradiction entre tables liées | Montant facture ≠ Somme des lignes |
| Incohérence inter-systèmes | Même entité avec valeurs différentes dans deux systèmes | Solde client différent entre CRM et ERP |
| Incohérence temporelle | Évolution illogique dans le temps | Solde négatif sans autorisation |

### Formule de calcul

```
Score cohérence = (1 - Nombre de violations de règles de cohérence / Nombre total de contrôles) × 100
```

### Exemple Congo-Brazzaville

**Contrôles de cohérence — Système de gestion des permis (DGTT)**

| Règle de cohérence | Violations détectées | Total contrôles | Taux |
|-------------------|---------------------|-----------------|------|
| Date délivrance ≤ Date expiration | 12 | 5 000 | 99,76% |
| Catégorie permis ∈ liste officielle | 8 | 5 000 | 99,84% |
| Âge titulaire ≥ âge légal (18 ans pour B) | 3 | 5 000 | 99,94% |
| Numéro permis format conforme | 47 | 5 000 | 99,06% |

Score cohérence global = Moyenne = **99,65%** — Excellent

**Problème identifié :** 47 numéros de permis au format non conforme. Cela suggère une migration de l'ancien système avec des formats hérités. Action : normaliser et corriger les anciens formats.

---

## Dimension 4 — Actualité (Timeliness)

### Définition
L'actualité mesure le degré auquel les données reflètent l'état actuel de la réalité qu'elles représentent. Une donnée est actuelle si elle a été mise à jour dans un délai acceptable pour son usage.

### Formule de calcul

```
Score actualité = (Nombre d'enregistrements mis à jour dans le délai requis / Total enregistrements) × 100
```

Chaque domaine définit son **délai de fraîcheur acceptable** (DFA) :

| Domaine | DFA recommandé |
|---------|---------------|
| Données de stocks | Temps réel à J+1 |
| Données clients (coordonnées) | Vérification annuelle |
| Données financières (cours) | Quotidien |
| Données RH (effectifs) | Mensuel |
| Référentiel géographique | Triennal |

### Exemple Congo-Brazzaville

**Référentiel clients — Opérateur de télécommunications**

Analyse de l'ancienneté des données de contact :

| Ancienneté de la dernière mise à jour | Nombre clients | Pourcentage |
|--------------------------------------|----------------|-------------|
| < 6 mois | 45 230 | 62,1% |
| 6 mois à 1 an | 14 870 | 20,4% |
| 1 an à 2 ans | 8 450 | 11,6% |
| > 2 ans | 4 210 | 5,9% |

DFA défini : 1 an. Données "actuelles" = mises à jour il y a moins de 1 an.

```
Score actualité = (45 230 + 14 870) / 72 760 × 100 = 82,5%
```

**Problème identifié :** 14 660 clients (20%) ont des données non mises à jour depuis plus d'un an. Action : campagne de mise à jour via SMS et au point de vente.

---

## Dimension 5 — Unicité (Uniqueness)

### Définition
L'unicité mesure l'absence de doublons dans un jeu de données. Chaque entité réelle doit être représentée par un seul et unique enregistrement dans le système de référence.

### Formule de calcul

```
Score unicité = ((N - D) / N) × 100
```
Avec :
- N = Nombre total d'enregistrements
- D = Nombre d'enregistrements en doublon (copies supplémentaires)

### Types de doublons

| Type | Description | Méthode de détection |
|------|-------------|----------------------|
| Doublon exact | Enregistrements identiques sur tous les champs | Comparaison stricte |
| Doublon quasi-exact | Légères variations (orthographe, format) | Fuzzy matching (Levenshtein) |
| Doublon fonctionnel | Même entité avec identifiants différents | Rapprochement multi-attributs |

### Exemple Congo-Brazzaville

**Base de bénéficiaires — Programme social national**

Lors d'une campagne de déduplication :

| Méthode de détection | Doublons trouvés |
|---------------------|------------------|
| Même NNI (numéro national d'identification) | 234 |
| Même nom + prénom + date naissance | 1 847 |
| Fuzzy matching nom/prénom + village | 3 412 |
| **Total doublons estimés** | **5 493** |
| **Base totale** | **87 500** |

```
Score unicité = (87 500 - 5 493) / 87 500 × 100 = 93,7%
```

**Problème identifié :** 6,3% de doublons, soit 5 493 enregistrements. Impact : double paiement des prestations sociales. Action urgente : campagne de déduplication et mise en place d'un contrôle d'unicité à la saisie.

---

## Dimension 6 — Validité (Validity)

### Définition
La validité mesure la conformité des données aux formats, plages de valeurs, listes de référence et contraintes métier définies. Une donnée valide respecte toutes les règles de format et de domaine.

### Types de règles de validité

| Type | Description | Exemple |
|------|-------------|---------|
| Format | Respect d'un pattern défini | Téléphone Congo : 06XXXXXXX ou 05XXXXXXX |
| Plage | Valeur dans un intervalle défini | Âge : 0-120 ans |
| Liste de référence | Valeur appartenant à une liste officielle | Département : liste des 12 départements du Congo |
| Contrainte métier | Règle logique complexe | Date naissance < Date embauche |

### Formule de calcul

```
Score validité = (Nombre de valeurs conformes / Nombre total de valeurs vérifiées) × 100
```

### Exemple Congo-Brazzaville

**Contrôles de validité — Registre du commerce (RCCM)**

| Règle de validité | Conformes | Violations | Taux |
|-------------------|-----------|------------|------|
| Format RCCM : BRAZZA-YYYY-B-NNNNN | 4 782 | 218 | 95,6% |
| Département ∈ 12 départements officiels | 4 951 | 49 | 99,0% |
| Capital social > 0 | 4 989 | 11 | 99,8% |
| Date création ≤ aujourd'hui | 5 000 | 0 | 100,0% |
| Format téléphone : 0[56]XXXXXXX | 3 841 | 1 159 | 76,8% |

Score validité global = Moyenne pondérée = **94,2%**

**Problème identifié :** 23,2% des numéros de téléphone ne respectent pas le format officiel (souvent anciens formats ou indicatifs étrangers non documentés). Action : mise à jour des règles de validation pour accepter les formats internationaux légitimes.

---

## Récapitulatif — Tableau de bord qualité type

```
╔══════════════════════════════════════════════════════════════╗
║              SCORE QUALITÉ GLOBAL : 87,3 / 100              ║
╠══════════════╦════════════╦════════╦══════════════════════════╣
║ Dimension    ║ Score      ║ Poids  ║ Contribution             ║
╠══════════════╬════════════╬════════╬══════════════════════════╣
║ Complétude   ║ 88,5%      ║ 25%    ║ 22,1                     ║
║ Exactitude   ║ 85,0%      ║ 25%    ║ 21,3                     ║
║ Cohérence    ║ 99,7%      ║ 20%    ║ 19,9                     ║
║ Actualité    ║ 82,5%      ║ 15%    ║ 12,4                     ║
║ Unicité      ║ 93,7%      ║ 10%    ║  9,4                     ║
║ Validité     ║ 94,2%      ║  5%    ║  4,7                     ║
╠══════════════╬════════════╬════════╬══════════════════════════╣
║ TOTAL        ║            ║ 100%   ║ 89,8                     ║
╚══════════════╩════════════╩════════╩══════════════════════════╝
```

**Interprétation :**
- Score ≥ 90 : Excellent — données fiables pour tous usages critiques
- Score 80-89 : Bon — amélioration ciblée recommandée
- Score 70-79 : Acceptable — plan d'action qualité requis
- Score < 70 : Insuffisant — blocage des usages critiques jusqu'à correction

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
