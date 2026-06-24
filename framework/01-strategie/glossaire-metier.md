# Glossaire Métier — Gouvernance des Données

**Version :** 1.0
**Date :** 2026-06-01
**Domaine :** Gouvernance des Données / Data Management
**Référentiels :** DAMA-DMBOK, ISO 8000, RGPD

---

## Introduction

Ce glossaire centralise les définitions des termes utilisés dans le cadre de la gouvernance des données de l'organisation. Il est maintenu par le Bureau de Gouvernance des Données et constitue la référence officielle pour toute documentation, rapport ou échange relatif à la gestion des données.

**Légende :**
- **(T)** : Terme technique
- **(M)** : Terme métier
- **(R)** : Terme réglementaire
- **(G)** : Terme de gouvernance

---

## A

**Actif de données (Data Asset)** *(M/G)*
Ensemble de données ayant une valeur pour l'organisation et nécessitant une gestion structurée. Exemple : la base clients constitue un actif de données stratégique pour une entreprise commerciale à Brazzaville.

**Actualité (Timeliness)** *(G)*
Dimension de qualité mesurant le degré auquel les données reflètent la réalité à un moment donné. Une donnée d'adresse d'un client mise à jour il y a 5 ans peut ne plus être actuelle.

**Analyse d'Impact sur la Protection des Données (AIPD)** *(R)*
Évaluation systématique des risques qu'un traitement de données personnelles fait peser sur les droits et libertés des personnes. Obligatoire pour les traitements à risque élevé selon le RGPD et la loi congolaise n° 29-2019.

**Anonymisation** *(R/T)*
Technique irréversible rendant impossible l'identification d'une personne à partir de ses données. Différent de la pseudonymisation. Les données anonymisées ne sont plus soumises aux règles de protection des données personnelles.

**Archivage** *(G)*
Phase du cycle de vie des données consistant à déplacer des données inactives vers un stockage de longue durée, avec des conditions d'accès restreintes mais une possibilité de restauration.

**Architecture de données** *(T/G)*
Ensemble des modèles, règles et standards qui définissent la structure, le stockage, l'intégration et la sécurité des données dans un système d'information.

**AUPC** *(R)*
Acte Uniforme sur la Protection des données à caractère personnel de l'OHADA. Cadre juridique africain harmonisant la protection des données dans l'espace OHADA, complémentaire aux législations nationales.

---

## B

**Base de données maîtres** *(T)*
Référentiel centralisé contenant les données maîtres validées et officielles de l'organisation. Exemple : la base clients maîtres contenant les 50 000 clients officiellement enregistrés.

**Big Data** *(T)*
Ensemble de technologies et pratiques permettant de gérer des volumes de données très importants, à haute vélocité et grande variété, dépassant les capacités des outils traditionnels.

**Business Glossary** *(G)*
Voir *Glossaire métier*.

---

## C

**Cardinalité** *(T)*
Nombre de valeurs distinctes dans un champ d'un jeu de données. Une cardinalité faible indique peu de valeurs différentes (ex : champ genre : 2 valeurs), une cardinalité haute indique beaucoup de valeurs (ex : identifiant client).

**Catalogue de données (Data Catalog)** *(G)*
Inventaire centralisé et documenté de tous les actifs de données d'une organisation, incluant les métadonnées techniques et métier, le propriétaire, la classification et la localisation.

**Champ** *(T)*
Unité élémentaire d'information dans un enregistrement ou une table. Synonyme : colonne, attribut, variable.

**Chiffrement** *(T)*
Transformation cryptographique des données les rendant illisibles sans la clé de déchiffrement. Technique de protection des données en transit et au repos.

**Classification des données** *(G)*
Organisation des données en catégories selon leur sensibilité et leur criticité. Le cadre adopte quatre niveaux : Public, Interne, Confidentiel, Secret.

**Cohérence (Consistency)** *(G)*
Dimension de qualité mesurant l'absence de contradictions entre des données liées entre elles ou stockées dans différents systèmes.

**Complétude (Completeness)** *(G)*
Dimension de qualité mesurant le taux de renseignement des champs obligatoires d'un enregistrement. Formule : Champs renseignés / Champs attendus × 100.

**Conformité (Compliance)** *(G/R)*
Respect des règles, réglementations, politiques internes et standards applicables à la gestion des données.

**Consentement** *(R)*
Accord libre, éclairé, spécifique et univoque d'une personne physique pour le traitement de ses données personnelles. Fondement légal prévu par la loi congolaise n° 29-2019.

**Custodian** *(G)*
Voir *Data Custodian*.

---

## D

**Data Catalog** *(G)*
Voir *Catalogue de données*.

**Data Consumer** *(G)*
Toute personne utilisant des données dans le cadre de son activité professionnelle, sans nécessairement participer à leur production ou à leur gestion.

**Data Custodian** *(G)*
Acteur responsable de la garde technique des données : stockage sécurisé, sauvegarde, disponibilité, gestion des droits d'accès techniques.

**Data Domain** *(G)*
Périmètre regroupant un ensemble cohérent de données sous la responsabilité d'un Data Owner. Exemple : le domaine "Clients" regroupe toutes les données relatives aux clients.

**Data Engineer** *(G)*
Spécialiste technique en charge de la conception et du maintien des pipelines de données, des processus ETL et des architectures de stockage.

**Data Governance** *(G)*
Voir *Gouvernance des données*.

**Data Lake** *(T)*
Référentiel centralisé permettant de stocker des données structurées et non structurées à grande échelle, sans transformation préalable. Permet des analyses exploratoires flexibles.

**Data Lineage** *(G)*
Voir *Lignage des données*.

**Data Mart** *(T)*
Sous-ensemble d'un entrepôt de données orienté vers un domaine métier spécifique (exemple : data mart commercial, data mart RH).

**Data Mesh** *(T)*
Architecture décentralisée de gestion des données où chaque domaine métier est propriétaire et producteur de ses propres données, exposées comme des produits.

**Data Owner** *(G)*
Responsable métier ayant la pleine responsabilité d'un domaine de données : définition des règles métier, validation des accès, garantie de la qualité.

**Data Product** *(G)*
Données gérées comme un produit, avec propriétaire, documentation, SLA de qualité et interface d'accès standardisée.

**Data Quality** *(G)*
Voir *Qualité des données*.

**Data Steward** *(G)*
Expert opérationnel chargé de la gestion quotidienne de la qualité, de la documentation et de la conformité des données d'un domaine, sous l'autorité du Data Owner.

**Data Warehouse (Entrepôt de données)** *(T)*
Système de stockage centralisé des données historisées, structurées et intégrées, utilisé pour l'analyse décisionnelle.

**Déduplication** *(T/G)*
Processus d'identification et de suppression ou fusion des enregistrements en double dans un jeu de données.

**Dictionnaire de données** *(G)*
Documentation technique décrivant chaque champ d'une entité de données : nom, type, format, contraintes, description, source, propriétaire.

**Disponibilité (Availability)** *(G)*
Capacité à accéder aux données quand elles sont nécessaires, dans des délais acceptables et selon les droits accordés.

**Donnée maître** *(M/G)*
Voir *Master Data*.

**Donnée personnelle** *(R)*
Toute information permettant d'identifier directement ou indirectement une personne physique (nom, numéro de téléphone, adresse, numéro d'identification national, etc.).

**Donnée sensible** *(R)*
Catégorie particulière de données personnelles dont le traitement est soumis à des protections renforcées : données de santé, origine ethnique, opinions politiques, données biométriques, etc.

---

## E

**Entité** *(T/M)*
Objet du monde réel représenté dans un système d'information. Exemples d'entités maîtres : Client, Produit, Fournisseur, Employé, Site géographique.

**ETL (Extract, Transform, Load)** *(T)*
Processus d'extraction de données depuis des sources, de transformation selon des règles métier, et de chargement dans un système cible.

**ELT (Extract, Load, Transform)** *(T)*
Variante du processus ETL où les données sont d'abord chargées dans le système cible avant d'être transformées, exploitant la puissance de calcul du système cible.

**Exactitude (Accuracy)** *(G)*
Dimension de qualité mesurant le degré de correspondance entre les données et la réalité qu'elles représentent. Exemple : l'adresse enregistrée correspond-elle à l'adresse réelle du client ?

---

## F

**Fiche de données** *(G)*
Document standardisé décrivant une entité de données dans le catalogue : définition, attributs, propriétaire, classification, source, règles de qualité.

**Fuzzy Matching** *(T)*
Technique de correspondance approximative permettant de rapprocher des enregistrements dont les valeurs sont similaires mais non identiques. Utilisée dans la déduplication.

---

## G

**Golden Record** *(G)*
Enregistrement unique, officiel et de référence pour une entité maître, construit par fusion et réconciliation de plusieurs sources. Représente la "meilleure version de la vérité".

**Glossaire métier** *(G)*
Inventaire des définitions officielles des termes métier utilisés dans l'organisation, validé par les Data Owners. Garantit un langage commun entre métier et technique.

**Gouvernance des données** *(G)*
Ensemble des processus, règles, rôles et responsabilités assurant la gestion efficace et sécurisée des données tout au long de leur cycle de vie.

---

## I

**Identifiant unique** *(T)*
Valeur permettant d'identifier sans ambiguïté un enregistrement dans un système. Clé primaire garantissant l'unicité.

**Impact Assessment** *(R)*
Voir *Analyse d'Impact sur la Protection des Données (AIPD)*.

**Intégrité des données** *(G)*
Garantie que les données sont exactes, complètes et non altérées, qu'elles soient stockées, transmises ou traitées.

**Interopérabilité** *(T)*
Capacité de systèmes différents à échanger et utiliser des données de manière cohérente, grâce à des formats et des standards communs.

---

## K

**KPI (Key Performance Indicator)** *(M)*
Indicateur clé de performance permettant de mesurer l'atteinte d'un objectif. En gouvernance des données : score qualité, taux de complétude, taux de conformité.

---

## L

**Lignage des données (Data Lineage)** *(G)*
Traçabilité complète du parcours d'une donnée depuis sa source jusqu'à son utilisation finale, documentant toutes les transformations intermédiaires.

**Loi n° 29-2019** *(R)*
Loi congolaise portant protection des données à caractère personnel, adoptée en République du Congo (Congo-Brazzaville). Définit les droits des personnes et les obligations des responsables de traitement.

---

## M

**Master Data (Donnée maître)** *(G)*
Données de référence fondamentales et partagées de l'organisation, représentant les entités clés du business (clients, produits, fournisseurs, employés, lieux).

**Master Data Management (MDM)** *(G)*
Ensemble des processus, outils et politiques permettant de créer et maintenir une version unique, cohérente et autorisée des données maîtres.

**Métadonnées** *(G)*
Données décrivant d'autres données. Exemples : nom du champ, type de données, date de création, propriétaire, classification de sécurité, source.

**Métadonnées techniques** *(G)*
Informations techniques sur les données : type, taille, format, contraintes, index, statistiques de distribution.

**Métadonnées métier** *(G)*
Informations métier sur les données : définition, propriétaire, règles d'utilisation, classification, termes du glossaire associés.

**Modèle de données** *(T)*
Représentation structurée des données et de leurs relations, utilisée pour la conception et la documentation des systèmes d'information.

---

## N

**Niveau de classification** *(G)*
Catégorie de sensibilité attribuée à une donnée ou un actif de données. Les quatre niveaux du cadre : Public, Interne, Confidentiel, Secret.

**Norme ISO 8000** *(G)*
Norme internationale sur la qualité des données et des données maîtres. Définit les exigences et les bonnes pratiques pour la gestion de la qualité des données.

**Nullité** *(T)*
Absence de valeur pour un champ donné. Le taux de nullité mesure la proportion de valeurs manquantes.

---

## O

**OHADA** *(R)*
Organisation pour l'Harmonisation en Afrique du Droit des Affaires. Produit des actes uniformes applicables dans 17 États membres, dont le Congo-Brazzaville.

**Ontologie** *(T/G)*
Représentation formelle des concepts d'un domaine et de leurs relations, permettant une compréhension commune et le partage de la connaissance.

**Outlier (Valeur aberrante)** *(T)*
Valeur qui s'écarte significativement de la distribution normale des données. Peut indiquer une erreur de saisie ou un cas exceptionnel légitime.

---

## P

**Pipeline de données** *(T)*
Séquence automatisée de traitements permettant de collecter, transformer et charger les données d'une source vers une destination.

**Politique de données** *(G)*
Règles et directives définissant comment les données doivent être gérées, utilisées et protégées dans l'organisation.

**Privacy by Design** *(R)*
Principe de protection des données personnelles intégrée dès la conception des systèmes et des processus, et non ajoutée a posteriori.

**Profilage des données (Data Profiling)** *(T/G)*
Analyse statistique automatisée d'un jeu de données pour en comprendre la structure, la qualité, les distributions et les anomalies.

**Pseudonymisation** *(R)*
Technique remplaçant les identifiants directs d'une personne par un pseudonyme, réduisant les risques tout en permettant une ré-identification dans des conditions contrôlées.

---

## Q

**Qualité des données** *(G)*
Degré auquel les données répondent aux exigences des utilisateurs pour un usage particulier. Mesurée selon six dimensions : complétude, exactitude, cohérence, actualité, unicité, validité.

---

## R

**RACI** *(G)*
Matrice de partage des responsabilités : Responsable (fait), Approbateur (valide), Consulté (avisé), Informé (notifié).

**Réconciliation** *(T/G)*
Processus de résolution des conflits entre données provenant de sources différentes, pour déterminer la valeur officielle à retenir dans le golden record.

**Référentiel** *(M/G)*
Jeu de données de référence utilisé comme source de vérité pour un type d'entité. Exemples : référentiel des communes de la République du Congo, référentiel des catégories de produits.

**Registre des traitements** *(R)*
Document obligatoire (article 30 du RGPD, équivalent congolais) listant tous les traitements de données personnelles réalisés par l'organisation.

**Responsable de traitement** *(R)*
Personne morale ou physique qui détermine les finalités et les moyens du traitement des données personnelles.

**Rétention des données** *(G)*
Durée pendant laquelle les données sont conservées, selon leur catégorie et les obligations légales applicables.

**RGPD** *(R)*
Règlement Général sur la Protection des Données (UE 2016/679). Référence internationale en matière de protection des données personnelles, utilisée comme modèle pour les législations africaines.

**Règle de qualité** *(G)*
Critère formel définissant une condition que doit satisfaire une donnée pour être considérée comme valide. Exemple : le numéro de téléphone doit comporter 9 chiffres pour le Congo-Brazzaville (indicatif +242).

---

## S

**Score qualité** *(G)*
Indicateur synthétique (0-100) mesurant la qualité globale d'un jeu de données, calculé comme la moyenne pondérée des scores sur les six dimensions de qualité.

**Sensitivity Level** *(G)*
Voir *Niveau de classification*.

**Sous-traitant** *(R)*
Entité traitant des données personnelles pour le compte d'un responsable de traitement. Soumis aux mêmes obligations de protection.

**Source de données** *(T/G)*
Système, application ou fichier d'où proviennent les données. La traçabilité (lignage) documente toutes les sources.

**Survivorship** *(G)*
Règles déterminant quelle valeur est retenue lors de la fusion de plusieurs enregistrements pour construire le golden record.

---

## T

**Traçabilité** *(G)*
Voir *Lignage des données*.

**Traitement de données** *(R)*
Toute opération effectuée sur des données personnelles : collecte, enregistrement, modification, extraction, consultation, transmission, effacement.

---

## U

**Unicité (Uniqueness)** *(G)*
Dimension de qualité mesurant l'absence de doublons dans un jeu de données. Formule : (Total enregistrements - Doublons) / Total enregistrements × 100.

---

## V

**Validité (Validity)** *(G)*
Dimension de qualité mesurant la conformité des données aux formats, règles et contraintes définis. Exemple : une date de naissance ne peut pas être dans le futur.

**Valeur par défaut** *(T)*
Valeur attribuée automatiquement à un champ lorsqu'aucune valeur n'est fournie. Peut masquer des problèmes de complétude si mal utilisée.

**Violation de données** *(R)*
Incident de sécurité entraînant la destruction, la perte, l'altération, la divulgation non autorisée ou l'accès non autorisé à des données.

**Volume de données** *(T)*
Quantité de données stockées ou traitées, exprimée en nombre d'enregistrements, d'octets ou d'autres unités. L'un des critères caractérisant le Big Data.

---

## W

**Workflow de validation** *(G)*
Processus formalisé de vérification et d'approbation des données avant leur utilisation ou leur publication, impliquant les rôles définis dans la gouvernance.

---

## Z

**Zone de confiance** *(T)*
Espace de stockage où les données ont été validées, nettoyées et certifiées conformes aux standards de qualité. Utilisée dans les architectures Data Lake (zone brute → zone validée → zone certifiée).

---

## Annexe — Index des acronymes

| Acronyme | Définition |
|----------|-----------|
| AIPD | Analyse d'Impact sur la Protection des Données |
| AUPC | Acte Uniforme sur la Protection des données à caractère personnel |
| BGD | Bureau de Gouvernance des Données |
| CDO | Chief Data Officer |
| CGD | Comité de Gouvernance des Données |
| CEMAC | Communauté Économique et Monétaire de l'Afrique Centrale |
| DAMA | Data Management Association |
| DMBOK | Data Management Body of Knowledge |
| DPO | Data Protection Officer |
| ELT | Extract, Load, Transform |
| ETL | Extract, Transform, Load |
| KPI | Key Performance Indicator |
| MDM | Master Data Management |
| OHADA | Organisation pour l'Harmonisation en Afrique du Droit des Affaires |
| RACI | Responsible, Accountable, Consulted, Informed |
| RGPD | Règlement Général sur la Protection des Données |
| SLA | Service Level Agreement |
| SQL | Structured Query Language |

---

*Glossaire maintenu par le Bureau de Gouvernance des Données*
*Dernière mise à jour : 2026-06-01 — Version 1.0*
