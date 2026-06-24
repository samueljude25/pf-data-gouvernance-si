# Méthode de Calcul du Score Qualité Global

**Version :** 1.0
**Date :** 2026-06-01
**Référentiel :** DAMA-DMBOK, ISO 8000

---

## 1. Principe général

Le score qualité global est un indicateur synthétique sur 100 points permettant d'évaluer en un coup d'œil la fiabilité d'un jeu de données. Il est calculé comme la **moyenne pondérée** des scores obtenus sur les six dimensions de qualité.

```
Score Global = Σ (Score_dimension_i × Poids_i)
```

Ce score est calculé automatiquement par le script `scripts/qualite/scoring.py` et intégré dans les rapports produits par `scripts/qualite/rapport_qualite.py`.

---

## 2. Pondération des dimensions

Les poids reflètent l'importance relative de chaque dimension pour la prise de décision. Ils sont définis par le Bureau de Gouvernance des Données et peuvent être ajustés par domaine métier.

| # | Dimension | Poids | Justification |
|---|-----------|-------|---------------|
| 1 | Complétude | 25% | Des données manquantes rendent les analyses incomplètes et biaisées |
| 2 | Exactitude | 25% | Des données inexactes conduisent à de mauvaises décisions |
| 3 | Cohérence | 20% | Des incohérences signalent des problèmes d'intégration inter-systèmes |
| 4 | Actualité | 15% | Des données obsolètes peuvent être dangereuses dans certains contextes |
| 5 | Unicité | 10% | Les doublons faussent les indicateurs (ex : double comptage) |
| 6 | Validité | 5% | La validité est souvent contrôlée en amont à la saisie |
| | **Total** | **100%** | |

---

## 3. Calcul de chaque dimension

### 3.1 Score de complétude

```python
def score_completude(df, champs_obligatoires):
    """
    Calcule le taux de renseignement des champs obligatoires.
    Valeurs considérées comme manquantes : None, NaN, '', ' ', 'N/A', 'null'
    """
    valeurs_vides = [None, float('nan'), '', ' ', 'N/A', 'null', 'NULL']
    total_cellules = len(df) * len(champs_obligatoires)
    cellules_renseignees = 0
    
    for champ in champs_obligatoires:
        cellules_renseignees += df[champ].apply(
            lambda x: 0 if x in valeurs_vides or pd.isna(x) else 1
        ).sum()
    
    return (cellules_renseignees / total_cellules) * 100
```

### 3.2 Score d'exactitude

L'exactitude nécessite une source de vérité externe ou des règles de plausibilité :

```python
def score_exactitude(df, regles_plausibilite):
    """
    Applique des règles de plausibilité et calcule le taux de conformité.
    En l'absence de source de vérité, utilise des règles statistiques
    (détection des outliers par IQR).
    """
    total = len(df)
    conformes = 0
    
    for regle in regles_plausibilite:
        conformes += df.query(regle['condition']).shape[0]
    
    return (conformes / (total * len(regles_plausibilite))) * 100
```

### 3.3 Score de cohérence

```python
def score_coherence(df, regles_coherence):
    """
    Vérifie les règles de cohérence intra-enregistrement.
    """
    total_controles = len(df) * len(regles_coherence)
    violations = 0
    
    for regle in regles_coherence:
        violations += df.query(regle['violation_condition']).shape[0]
    
    return ((total_controles - violations) / total_controles) * 100
```

### 3.4 Score d'actualité

```python
def score_actualite(df, champ_date_maj, delai_fraicheur_jours):
    """
    Mesure le % d'enregistrements mis à jour dans le délai de fraîcheur.
    """
    date_limite = pd.Timestamp.now() - pd.Timedelta(days=delai_fraicheur_jours)
    actuels = (df[champ_date_maj] >= date_limite).sum()
    return (actuels / len(df)) * 100
```

### 3.5 Score d'unicité

```python
def score_unicite(df, champs_cles):
    """
    Calcule le taux d'enregistrements non dupliqués sur les champs clés.
    """
    total = len(df)
    doublons = df.duplicated(subset=champs_cles, keep='first').sum()
    return ((total - doublons) / total) * 100
```

### 3.6 Score de validité

```python
def score_validite(df, regles_format):
    """
    Vérifie la conformité aux formats et listes de valeurs autorisées.
    """
    total_controles = 0
    conformes = 0
    
    for regle in regles_format:
        champ = regle['champ']
        if regle['type'] == 'format':
            mask = df[champ].astype(str).str.match(regle['pattern'])
        elif regle['type'] == 'liste':
            mask = df[champ].isin(regle['valeurs'])
        elif regle['type'] == 'plage':
            mask = (df[champ] >= regle['min']) & (df[champ] <= regle['max'])
        
        total_controles += len(df[champ].dropna())
        conformes += mask.sum()
    
    return (conformes / total_controles) * 100 if total_controles > 0 else 100
```

---

## 4. Calcul du score global

```python
POIDS = {
    'completude': 0.25,
    'exactitude': 0.25,
    'coherence': 0.20,
    'actualite': 0.15,
    'unicite': 0.10,
    'validite': 0.05
}

def score_global(scores_dimensions):
    """
    Calcule le score qualité global pondéré.
    
    Args:
        scores_dimensions (dict): {'completude': 88.5, 'exactitude': 85.0, ...}
    
    Returns:
        float: Score global sur 100
    """
    score = 0
    for dimension, poids in POIDS.items():
        score += scores_dimensions.get(dimension, 0) * poids
    return round(score, 2)
```

**Exemple de calcul :**

```
Score global = (88.5 × 0.25) + (85.0 × 0.25) + (99.7 × 0.20)
             + (82.5 × 0.15) + (93.7 × 0.10) + (94.2 × 0.05)

           = 22.13 + 21.25 + 19.94 + 12.38 + 9.37 + 4.71

           = 89.78 / 100
```

---

## 5. Interprétation du score

### 5.1 Niveaux de qualité

| Plage | Niveau | Couleur | Signification |
|-------|--------|---------|---------------|
| 95-100 | Excellent | Vert foncé | Données certifiées, prêtes pour tous usages |
| 85-94 | Bon | Vert | Données fiables, amélioration ciblée recommandée |
| 70-84 | Acceptable | Orange | Plan d'action qualité requis, usage limité aux rapports non critiques |
| 50-69 | Insuffisant | Rouge | Blocage des usages critiques, action corrective urgente |
| < 50 | Critique | Rouge foncé | Données non utilisables, arrêt et correction complète |

### 5.2 Décisions par niveau

| Niveau | Rapports décisionnels | Opérations clients | Export réglementaire |
|--------|----------------------|-------------------|---------------------|
| Excellent | Autorisé | Autorisé | Autorisé |
| Bon | Autorisé | Autorisé avec réserves | Autorisé avec déclaration |
| Acceptable | Avec avertissement | Limité | Interdit sauf dérogation |
| Insuffisant | Interdit | Suspendu | Interdit |
| Critique | Interdit | Suspendu | Interdit |

---

## 6. Pondérations par domaine métier

Les poids peuvent être adaptés selon le domaine. Les valeurs ci-dessous remplacent les poids par défaut pour certains contextes :

### Domaine Santé / Données patients

| Dimension | Poids standard | Poids santé |
|-----------|---------------|-------------|
| Complétude | 25% | 30% |
| Exactitude | 25% | 35% |
| Cohérence | 20% | 20% |
| Actualité | 15% | 10% |
| Unicité | 10% | 5% |
| Validité | 5% | 0% |

*Justification : en santé, l'exactitude des données (diagnostic, dosage, allergie) est critique. La complétude également car une donnée manquante peut avoir des conséquences graves.*

### Domaine Financier / Transactions

| Dimension | Poids standard | Poids financier |
|-----------|---------------|-----------------|
| Complétude | 25% | 20% |
| Exactitude | 25% | 30% |
| Cohérence | 20% | 25% |
| Actualité | 15% | 15% |
| Unicité | 10% | 10% |
| Validité | 5% | 0% |

*Justification : la cohérence et l'exactitude des montants et des références sont primordiales pour la conformité financière.*

### Domaine RH / Données employés

| Dimension | Poids standard | Poids RH |
|-----------|---------------|----------|
| Complétude | 25% | 25% |
| Exactitude | 25% | 25% |
| Cohérence | 20% | 15% |
| Actualité | 15% | 25% |
| Unicité | 10% | 10% |
| Validité | 5% | 0% |

*Justification : l'actualité est cruciale en RH (postes, responsabilités, formations, contrats évoluent fréquemment).*

---

## 7. Évolution temporelle du score

Le score qualité est calculé à fréquence régulière pour suivre l'évolution :

```
Fréquence de calcul par domaine :
- Données opérationnelles (transactions, stocks) : Quotidien
- Données clients et fournisseurs : Hebdomadaire
- Données RH : Mensuel
- Données de référence (géographie, produits) : Mensuel
- Rapport global de gouvernance : Mensuel
```

### Exemple de tableau de suivi

```
Domaine Clients — Score qualité mensuel 2026

Mois       | Complét. | Exact.  | Cohér.  | Actual. | Unicité | Valid.  | GLOBAL
-----------|----------|---------|---------|---------|---------|---------|--------
Janvier    |  82,1%   |  80,5%  |  97,3%  |  78,2%  |  91,4%  |  88,7%  |  84,1
Février    |  83,7%   |  81,2%  |  98,0%  |  79,1%  |  92,8%  |  90,1%  |  85,2
Mars       |  85,4%   |  82,9%  |  98,5%  |  80,7%  |  93,1%  |  91,4%  |  86,5
Avril      |  87,2%   |  84,0%  |  99,1%  |  81,5%  |  94,2%  |  92,8%  |  87,8
Mai        |  88,5%   |  85,0%  |  99,7%  |  82,5%  |  93,7%  |  94,2%  |  89,8
```

**Tendance :** amélioration constante de +1,1 point/mois suite au plan d'action qualité lancé en janvier.

---

## 8. Alertes automatiques

```
Règles d'alerte intégrées au script scoring.py :

SI score_global < 70   → Alerte CRITIQUE → Email CDO + Data Owner + Data Steward
SI score_global < 85   → Alerte WARNING  → Email Data Steward
SI score_dimension < seuil_dimension → Alerte par dimension au Data Steward concerné
SI amélioration < -5 points vs mois précédent → Alerte dégradation soudaine
```

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
