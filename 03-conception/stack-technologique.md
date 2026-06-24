# Stack technologique — Gouvernance de la donnée

## DAMA-DMBOK (référentiel méthodologique)
Le Data Management Body of Knowledge est le référentiel de référence mondial pour la gouvernance et le management des données. Il définit 11 domaines de connaissance (qualité, sécurité, architecture, modélisation, intégration, documents, référentiels, entrepôt, métadonnées, gouvernance). Il sert de cadre conceptuel pour structurer la démarche.

## ISO 8000
Norme internationale sur la qualité des données maîtres. Elle définit les exigences pour les données échangées entre systèmes et garantit leur interopérabilité. Particulièrement utile pour les projets MDM et les échanges de données inter-organisationnels (administrations, chaînes de valeur).

## Apache Atlas
Plateforme open source de gouvernance des métadonnées (Apache Software Foundation). Fonctionnalités clés :
- Catalogue de données (inventaire des tables, colonnes, pipelines)
- Classification et étiquetage des données sensibles
- Lineage automatique (traçabilité des flux)
- Intégration native avec Hadoop, Hive, HBase, Kafka, Spark

Alternative open source : OpenMetadata, DataHub (LinkedIn).

## Great Expectations
Framework Python pour la validation automatique de la qualité des données. Génère des rapports HTML détaillés. S'intègre dans les pipelines Airflow et dbt pour une qualité continue.

## dbt (data build tool)
En plus de la transformation SQL, dbt génère une documentation automatique du modèle de données et des tests de qualité intégrés. Le `dbt docs serve` produit un site web de documentation navigable — un catalogue de données léger.

## Comparatif outils de catalogage

| Outil | Coût | Richesse | Facilité | Intégration |
|---|---|---|---|---|
| **Apache Atlas** | Gratuit | Élevée | Moyenne | Hadoop/Spark |
| OpenMetadata | Gratuit | Élevée | Bonne | Universelle |
| DataHub | Gratuit | Élevée | Bonne | Universelle |
| Collibra | Payant | Très élevée | Bonne | Universelle |
| Alation | Payant | Élevée | Très bonne | Universelle |
| dbt docs | Gratuit | Limitée | Excellente | dbt uniquement |

**Recommandation Afrique centrale** : OpenMetadata ou DataHub pour les organisations disposant d'une équipe IT structurée. Pour les organisations plus petites, dbt docs + Great Expectations forment un catalogue léger mais suffisant.
