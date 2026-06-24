# Gouvernance de la Donnée — Cadre pour Organisations Africaines

**Portfolio de compétences — Samuel Jude Sendzi, Chef de Projet Digital & Consultant SI**

---

## Présentation du projet

Ce projet présente la conception d'un **cadre complet de gouvernance de la donnée** adapté aux organisations publiques et privées d'Afrique centrale. Il couvre la politique qualité des données, la sécurité, le Master Data Management (MDM), la conformité réglementaire et les outils de mise en œuvre.

---

## Pourquoi la gouvernance de la donnée ?

Dans de nombreuses organisations africaines, les données sont gérées de façon informelle, dispersée et non documentée. Cette situation génère des risques concrets :

- **Risque décisionnel** : des rapports basés sur des données de mauvaise qualité conduisent à de mauvaises décisions
- **Risque opérationnel** : des données clients ou fournisseurs incorrectes créent des erreurs coûteuses
- **Risque de conformité** : l'absence de documentation des données rend difficile tout audit ou certification
- **Risque de sécurité** : sans inventaire des données sensibles, leur protection est impossible à garantir

Un cadre de gouvernance structuré répond à ces risques en définissant qui est responsable de quelles données, selon quelles règles et avec quels outils.

---

## Référentiels utilisés

| Référentiel | Description |
|---|---|
| **DAMA-DMBOK** | Data Management Body of Knowledge — référentiel de référence mondial |
| **ISO 8000** | Norme internationale sur la qualité des données |
| **COBIT 2019** | Gouvernance et management des systèmes d'information |
| **RGPD (adaptation)** | Bonnes pratiques européennes adaptées au contexte africain |

---

## Outils couverts

| Outil | Rôle |
|---|---|
| **Apache Atlas** | Catalogue de données et lineage |
| **Great Expectations** | Tests automatiques de qualité des données |
| **dbt** | Transformation et documentation des modèles |
| **Collibra / OpenMetadata** | Gouvernance enterprise (alternative open source) |

---

## Structure du dépôt

```
01-avant-projet/
   etude-opportunite.md
   etude-faisabilite.md
   analyse-swot.md
   analyse-pestel.md

02-cahier-des-charges/
   cahier-des-charges.md

03-conception/
   architecture-technique.md
   stack-technologique.md

04-roadmap/
   phases-projet.md
```

---

## Composantes du cadre

1. **Politique de gouvernance** : vision, principes, rôles et responsabilités
2. **Catalogue de données** : inventaire de toutes les données de l'organisation
3. **Qualité des données** : règles, métriques, processus de correction
4. **Sécurité et confidentialité** : classification, accès, chiffrement
5. **Master Data Management** : référentiels uniques (clients, fournisseurs, produits)
6. **Conformité** : adaptation des bonnes pratiques RGPD au contexte local
