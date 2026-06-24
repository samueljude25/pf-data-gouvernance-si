# Politiques de Rétention et d'Archivage des Données

**Version :** 1.0
**Date :** 2026-06-01
**Référentiel :** Loi n° 29-2019 Congo, DAMA-DMBOK

---

## 1. Principes généraux

### 1.1 Principe de minimisation de la durée de conservation

Les données ne doivent pas être conservées plus longtemps que nécessaire à leur finalité. Ce principe, central dans la loi congolaise n° 29-2019 et l'AUPC, protège les personnes et réduit les risques de sécurité.

### 1.2 Cycle de conservation

```
DONNÉES ACTIVES          ARCHIVAGE               DESTRUCTION
(Usage opérationnel)     (Conservation légale)   (Effacement certifié)
      │                        │                        │
      ▼                        ▼                        ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│ Production   │──────►│ Archives     │──────► │ Destruction  │
│ Accès rapide │        │ Accès limité │        │ Certifiée    │
│ Performance  │        │ Coût réduit  │        │ Journalisée  │
└──────────────┘        └──────────────┘        └──────────────┘
```

---

## 2. Tableau de rétention par catégorie

### 2.1 Données clients et commerciales

| Catégorie | Durée rétention active | Durée archivage | Durée totale | Base légale |
|-----------|----------------------|-----------------|--------------|-------------|
| Données clients actifs | Durée de la relation | - | Variable | Contrat |
| Données clients inactifs | 2 ans post-inactivité | 8 ans | 10 ans | Légal + contractuel |
| Historique d'achats | 5 ans | 5 ans | 10 ans | Comptable (OHADA) |
| Données de prospects | 3 ans | - | 3 ans | Consentement/Intérêt légitime |
| Données de contact marketing | 3 ans sans interaction | - | 3 ans | Consentement |
| Contrats et avenants | 5 ans post-expiration | 10 ans | 15 ans | Légal OHADA |
| Factures et pièces comptables | 10 ans | 10 ans | 20 ans | Code de commerce Congo |
| Devis et propositions | 2 ans | 3 ans | 5 ans | Pratique commerciale |
| Réclamations clients | 5 ans | - | 5 ans | Légal |

### 2.2 Données financières et comptables

| Catégorie | Durée rétention active | Durée archivage | Durée totale | Base légale |
|-----------|----------------------|-----------------|--------------|-------------|
| Écritures comptables | 10 ans | 10 ans | 20 ans | OHADA (Acte Uniforme comptable) |
| Livres et journaux comptables | 10 ans | 10 ans | 20 ans | OHADA |
| Pièces justificatives | 10 ans | 10 ans | 20 ans | OHADA |
| Déclarations fiscales | 10 ans | 10 ans | 20 ans | Code des impôts Congo |
| Données bancaires (relevés) | 5 ans | 5 ans | 10 ans | Légal bancaire |
| Données de paie | 5 ans | 15 ans | 20 ans | Code du travail Congo |
| Données de trésorerie | 5 ans | 5 ans | 10 ans | OHADA |
| Budgets et prévisions | 3 ans | 7 ans | 10 ans | Pratique managériale |

### 2.3 Données ressources humaines

| Catégorie | Durée rétention active | Durée archivage | Durée totale | Base légale |
|-----------|----------------------|-----------------|--------------|-------------|
| Dossier employé actif | Durée du contrat | - | Variable | Code du travail Congo |
| Dossier employé (départ) | 2 ans post-départ | 28 ans (retraite) | 30 ans max | Code du travail + CNSS |
| Bulletins de paie | 5 ans | 15 ans | 20 ans | Code du travail Congo |
| Cotisations CNSS | 5 ans | 25 ans | 30 ans | CNSS Congo |
| Évaluations de performance | 5 ans | - | 5 ans | Pratique RH |
| Candidatures non retenues | 2 ans max | - | 2 ans | Loi n° 29-2019 |
| Formations et certifications | Durée du contrat + 5 ans | 5 ans | Variable | Pratique RH |
| Données médicales du travail | Durée du contrat | 30 ans | ~30 ans | Code du travail |
| Données disciplinaires | 3 ans (si sanction non suivie d'effets) | - | 3 ans | Code du travail |

### 2.4 Données opérationnelles et systèmes

| Catégorie | Durée rétention active | Durée archivage | Durée totale | Base légale |
|-----------|----------------------|-----------------|--------------|-------------|
| Logs applicatifs | 3 mois | 9 mois | 1 an | Pratique sécurité |
| Logs d'accès (INTERNE) | 1 an | - | 1 an | Sécurité SI |
| Logs d'accès (CONFIDENTIEL) | 2 ans | - | 2 ans | Conformité |
| Logs d'accès (SECRET) | 5 ans | - | 5 ans | Conformité |
| Logs de sécurité | 2 ans | 3 ans | 5 ans | Sécurité SI |
| Sauvegardes opérationnelles | 30 jours | - | 30 jours | Continuité d'activité |
| Sauvegardes de catastrophe | 1 an | 2 ans | 3 ans | Continuité d'activité |
| Données de test | Durée du projet + 30 jours | - | Variable | Pratique IT |
| Configurations système | Durée d'utilisation + 2 ans | 5 ans | Variable | Pratique IT |

### 2.5 Données de santé (applicable aux structures de santé)

| Catégorie | Durée rétention active | Durée archivage | Durée totale | Base légale |
|-----------|----------------------|-----------------|--------------|-------------|
| Dossier médical adulte | 20 ans | 10 ans | 30 ans | Législation santé Congo |
| Dossier médical mineur | Jusqu'à 28 ans | 10 ans | Variable | Législation santé Congo |
| Imagerie médicale | 10 ans | 10 ans | 20 ans | Pratique médicale |
| Prescriptions médicales | 5 ans | 5 ans | 10 ans | Pratique médicale |
| Données épidémiologiques | 10 ans | 30 ans | 40 ans | Santé publique |

---

## 3. Processus d'archivage

### 3.1 Déclenchement de l'archivage

L'archivage est déclenché automatiquement par le système ou manuellement selon les cas :

| Déclencheur | Type | Responsable |
|------------|------|-------------|
| Échéance de rétention active | Automatique | Data Custodian + Système |
| Fin de relation client | Semi-automatique (validation requise) | Data Steward |
| Départ d'un employé | Semi-automatique | DRH + Data Custodian |
| Migration de système | Manuel | Data Engineer |
| Demande d'effacement RGPD | Manuel | Data Steward + Data Owner |

### 3.2 Procédure d'archivage technique

```
Étape 1 : IDENTIFICATION
    ├─ Détection des données à archiver (requêtes planifiées)
    ├─ Validation de la liste par Data Steward
    └─ Approbation formelle du Data Owner

Étape 2 : EXTRACTION
    ├─ Export des données au format standard (Parquet, CSV)
    ├─ Génération du fichier de métadonnées d'archivage
    └─ Vérification d'intégrité (hash MD5/SHA-256)

Étape 3 : TRANSFERT VERS ARCHIVES
    ├─ Chiffrement du package d'archive
    ├─ Transfert vers le système d'archivage
    ├─ Vérification de la copie reçue
    └─ Journalisation de l'opération

Étape 4 : MISE À JOUR DES RÉFÉRENCES
    ├─ Mise à jour du catalogue de données (statut : Archivé)
    ├─ Mise à jour du registre des traitements
    └─ Notification aux utilisateurs concernés

Étape 5 : SUPPRESSION DE PRODUCTION
    ├─ Suppression des données du système de production
    ├─ Vérification de la suppression
    └─ Journalisation de la suppression

Étape 6 : VÉRIFICATION FINALE
    ├─ Vérification que les archives sont accessibles
    ├─ Test de restauration sur un échantillon
    └─ Clôture et archivage du dossier d'opération
```

### 3.3 Format et stockage des archives

| Critère | Standard retenu |
|---------|----------------|
| Format des archives | Parquet (données structurées), PDF/A (documents) |
| Compression | Gzip ou Snappy |
| Chiffrement | AES-256 (données CONFIDENTIEL et SECRET) |
| Stockage | Serveur d'archives dédié + copie hors site |
| Indexation | Catalogue de données (section archives) |
| Accessibilité | Sur demande validée, délai de restauration ≤ 48h |

---

## 4. Procédure de destruction

### 4.1 Conditions de destruction

La destruction des données est déclenchée lorsque :
- La durée totale de conservation (active + archivage) est atteinte
- Une demande d'effacement RGPD-like est reçue et approuvée
- Un ordre de destruction est émis par une autorité compétente

### 4.2 Méthodes de destruction certifiée

| Support | Méthode | Certification |
|---------|---------|--------------|
| Bases de données | Écrasement multi-passes (DoD 5220.22-M) + DROP TABLE | Log système |
| Fichiers sur disque dur | Écrasement 3 passes minimum | Log système |
| Disques physiques | Déchiquetage physique ou démagnétisation | Certificat prestataire |
| Bandes magnétiques | Démagnétisation + destruction physique | Certificat prestataire |
| Documents papier | Déchiquetage + collecte sécurisée | Bordereau de destruction |
| Clés USB / supports amovibles | Destruction physique | Log + certificat |

### 4.3 Certificat de destruction

Chaque opération de destruction doit être documentée avec :

```
CERTIFICAT DE DESTRUCTION DE DONNÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date de destruction    : 2026-06-01
Entité détruite        : t_client_inactif_pre2020
Volume détruit         : 12 450 enregistrements | 8,3 MB
Méthode utilisée       : Écrasement multi-passes + DELETE SQL
Responsable exécution  : Data Custodian (Prénom NOM)
Validé par Data Owner  : Directeur Commercial (Prénom NOM)
Validé par Data Steward: Responsable CRM (Prénom NOM)

Raison de la destruction : Échéance de conservation atteinte
                           (clients inactifs depuis 2015, 10 ans)

Hash des données avant destruction : SHA-256: a3f7b9c2...
Vérification post-destruction : Aucun résidu trouvé (requêtes tests)

Signature Data Owner    : _____________________ Date: ________
Signature Data Custodian: _____________________ Date: ________
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 5. Cas particuliers

### 5.1 Contentieux et litiges

Toute donnée faisant l'objet d'un contentieux en cours est soumise à une **suspension de destruction** (legal hold) jusqu'à la résolution définitive du litige, quelle que soit l'échéance de conservation normale.

**Procédure :**
1. Notification du service juridique au CDO dès l'ouverture d'un contentieux
2. Pose d'un drapeau "legal hold" sur les données concernées dans le catalogue
3. Revue mensuelle des legal holds actifs
4. Levée du legal hold par le service juridique après résolution

### 5.2 Données faisant l'objet d'un droit d'accès ou d'opposition

Si une personne exerce ses droits (accès, rectification, opposition) sur des données en cours d'archivage ou proches de la destruction, le processus est suspendu jusqu'à traitement complet de la demande.

### 5.3 Demandes de droit à l'effacement

Le droit à l'effacement (ou "droit à l'oubli") est traité selon les conditions légales :

| Situation | Traitement |
|-----------|-----------|
| Données non nécessaires à la finalité | Effacement sous 30 jours |
| Données nécessaires à une obligation légale | Refus motivé + délai légal |
| Données en cours de contentieux | Suspension + information de la personne |
| Données anonymisées | Non concernées (ne sont plus des données personnelles) |

---

## 6. Planification et suivi

### 6.1 Calendrier des opérations d'archivage

| Fréquence | Opération |
|-----------|-----------|
| Quotidienne | Archivage automatique des logs anciens |
| Mensuelle | Archivage des données clients/fournisseurs arrivant à échéance |
| Trimestrielle | Revue et archivage des données RH |
| Annuelle | Audit complet de la conformité des durées de conservation |
| À l'échéance | Destruction certifiée des archives arrivant en fin de vie |

### 6.2 Responsabilités

| Action | Responsable | Approbateur |
|--------|-------------|-------------|
| Identifier données à archiver | Data Steward | Data Owner |
| Exécuter l'archivage technique | Data Custodian | Data Steward |
| Valider les destructions | Data Owner | CDO |
| Exécuter les destructions | Data Custodian | Data Owner |
| Auditer les rétentions | CDO / Auditeur | Direction |

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
*Base légale : Loi n° 29-2019 Congo, OHADA Acte Uniforme comptable, Code du travail Congo*
