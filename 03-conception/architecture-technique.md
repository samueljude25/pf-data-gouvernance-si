# Architecture technique — Cadre de gouvernance de la donnée

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CADRE DE GOUVERNANCE                              │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Apache Atlas │  │   Great      │  │  dbt (documentation       │  │
│  │  (catalogue  │  │ Expectations │  │  + tests qualité          │  │
│  │  + lineage)  │  │  (qualité)   │  │  modèles analytiques)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Couche MDM (Master Data)                         │   │
│  │  Référentiels : Clients | Fournisseurs | Produits | Employés  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              Sources de données                               │   │
│  │   ERP | CRM | RH | Comptabilité | Fichiers Excel             │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Apache Atlas — Catalogue de données

Apache Atlas est l'outil open source de référence pour le catalogage des données et la traçabilité (data lineage).

### Concepts clés
- **Entity** : objet catalogué (table, colonne, pipeline, rapport)
- **Classification** : étiquette de sensibilité appliquée à une entité
- **Lineage** : graphe de traçabilité montrant d'où vient une donnée et où elle va
- **Glossary** : dictionnaire métier lié aux entités techniques

### Exemple de classification
```json
{
  "entityType": "hive_table",
  "entityGuid": "xxxx-xxxx-xxxx",
  "classifications": [
    {
      "typeName": "CONFIDENTIEL",
      "attributes": {
        "domaine": "RH",
        "proprietaire": "DRH",
        "duree_retention": "10 ans",
        "chiffrement_requis": true
      }
    }
  ]
}
```

## Great Expectations — Qualité des données

Great Expectations (GE) permet de définir des suites de tests automatiques sur les données.

```python
import great_expectations as ge

# Chargement d'un batch de données
context = ge.data_context.DataContext()
batch = context.get_batch(
    datasource_name="postgresql_prod",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name="dim_clients"
)

# Définition des expectations (règles qualité)
batch.expect_column_values_to_not_be_null("id_client")
batch.expect_column_values_to_be_unique("id_client")
batch.expect_column_values_to_not_be_null("nom")
batch.expect_column_values_to_match_regex("telephone", r"^\+?[0-9]{8,15}$")
batch.expect_column_values_to_be_in_set("pays", ["Congo", "Gabon", "Cameroun", "RCA", "Tchad", "Guinée Equatoriale"])
batch.expect_column_values_to_be_between("age", min_value=18, max_value=120)

# Validation et rapport
results = batch.validate()
print(f"Succès : {results['success']}")
print(f"Tests passés : {results['statistics']['successful_expectations']} / {results['statistics']['evaluated_expectations']}")
```

## Tableau de bord qualité des données (DAX Power BI)

```dax
Taux_Completude_Clients =
DIVIDE(
    COUNTROWS(FILTER(dim_clients, dim_clients[nom] <> BLANK())),
    COUNTROWS(dim_clients),
    0
) * 100

Taux_Doublons_Clients =
1 - DIVIDE(
    DISTINCTCOUNT(dim_clients[id_source]),
    COUNTROWS(dim_clients),
    1
)

Score_Qualite_Global =
(
    [Taux_Completude_Clients] * 0.30 +
    [Taux_Validite_Telephone] * 0.20 +
    (1 - [Taux_Doublons_Clients] * 100) * 0.30 +
    [Taux_Fraicheur_J7] * 0.20
)
```

## Modèle de maturité de gouvernance

| Niveau | Caractéristiques | Actions |
|---|---|---|
| **1 Initial** | Données en silos, pas de règles | Audit, sensibilisation |
| **2 Géré** | Quelques processus définis | Désigner Data Owners |
| **3 Défini** | Politique documentée, rôles établis | Déployer catalogue |
| **4 Maîtrisé** | Métriques qualité suivies | Automatiser les contrôles |
| **5 Optimisé** | Amélioration continue | Culture data ancrée |

La plupart des organisations africaines démarrent au niveau 1. L'objectif réaliste d'un programme de 18 mois est d'atteindre le niveau 3.
