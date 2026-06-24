# Politique d'Accès aux Données

**Version :** 1.0
**Date :** 2026-06-01
**Référentiel :** ISO 27001, Loi n° 29-2019 Congo

---

## 1. Principes fondamentaux

### 1.1 Moindre privilège
Chaque utilisateur dispose uniquement des accès strictement nécessaires à l'exercice de ses fonctions. Tout accès supplémentaire doit être justifié et approuvé.

### 1.2 Besoin d'en connaître
L'accès à une donnée est accordé uniquement si l'utilisateur a un besoin professionnel légitime et identifié d'accéder à cette donnée.

### 1.3 Séparation des fonctions
Les fonctions incompatibles (saisie, validation, administration) sont exercées par des personnes différentes pour éviter les fraudes et erreurs non détectées.

### 1.4 Révocabilité immédiate
Tout accès peut être révoqué immédiatement en cas de départ, changement de poste, incident de sécurité ou non-respect des règles.

---

## 2. Matrice d'accès par rôle et niveau de classification

### Légende
- **L** : Lecture seule
- **E** : Écriture (création, modification)
- **S** : Suppression
- **A** : Administration (gestion des droits)
- **-** : Aucun accès
- **LM** : Lecture masquée (données pseudonymisées)

### Matrice principale

| Profil | PUBLIC | INTERNE | CONFIDENTIEL | SECRET |
|--------|--------|---------|--------------|--------|
| CDO | L, E | L, E | L, E | L (lecture seule) |
| Data Owner (son domaine) | L, E, S | L, E, S | L, E, S | L |
| Data Owner (autre domaine) | L | L | - | - |
| Data Steward (son domaine) | L, E | L, E | L, E | - |
| Data Steward (autre domaine) | L | L | - | - |
| Data Custodian | L | L, A | L (technique) | L (technique, logs) |
| Data Engineer | L, E | L, E | L, E (traitement) | - |
| Data Analyst | L | L | LM | - |
| Responsable de service | L | L | L (son domaine) | - |
| Agent standard | L | L | - | - |
| Prestataire externe | L | - | - | - |
| Auditeur interne | L | L | L (audit seulement) | - |
| Auditeur externe | L | L | LM | - |
| Direction Générale | L | L | L | L |
| DPO | L | L | L | L (consultation) |

---

## 3. Matrice d'accès par domaine et fonction

### Domaine : Données Clients

| Fonction | Coordonnées | Historique transactions | Données personnelles | Scoring/Profil |
|----------|-------------|------------------------|---------------------|----------------|
| Commercial terrain | L, E | L | L | L |
| Responsable commercial | L, E | L | L, E | L, E |
| Service client | L, E | L | L | - |
| Marketing | LM | LM | - | L |
| Finance | - | L | - | - |
| RH | - | - | - | - |
| IT/Support | L (technique) | - | - | - |

### Domaine : Données Financières

| Fonction | Transactions | Salaires | Budgets | Bilans |
|----------|-------------|----------|---------|--------|
| DAF / Directeur Financier | L, E, S | L, E | L, E, S | L, E |
| Contrôleur de gestion | L, E | L | L, E | L |
| Comptable | L, E | - | L | L |
| Direction Générale | L | L | L | L |
| Auditeur | L | L | L | L |
| Commercial | - | - | L (partiel) | - |
| Agent standard | - | - | - | - |

### Domaine : Données RH

| Fonction | Effectifs | Salaires | Évaluations | Données médicales |
|----------|-----------|----------|-------------|-------------------|
| DRH | L, E | L, E | L, E | L |
| Responsable RH | L, E | L (son équipe) | L, E (son équipe) | - |
| Manager direct | L | - | L, E (son équipe) | - |
| Paie | - | L, E | - | - |
| Agent concerné | L (ses propres données) | L (son bulletin) | L (ses propres) | L (ses propres) |
| Médecin du travail | - | - | - | L, E |
| Auditeur | L | L | - | - |

---

## 4. Procédures de gestion des accès

### 4.1 Demande d'accès

**Processus standard (niveaux PUBLIC et INTERNE) :**
1. L'agent soumet une demande via le système de ticketing SI
2. Validation automatique pour les accès standard de son profil métier
3. Notification par email de l'ouverture des droits

**Processus renforcé (niveau CONFIDENTIEL) :**
1. L'agent soumet une demande motivée (justification métier)
2. Validation par le manager direct
3. Approbation du Data Owner du domaine concerné
4. Mise en oeuvre technique par le Data Custodian
5. Durée de validité maximale : 1 an, renouvelable sur justification

**Processus exceptionnel (niveau SECRET) :**
1. L'agent soumet une demande formelle écrite
2. Validation par le manager + Directeur de département
3. Approbation du Data Owner + CDO
4. Co-signature de la Direction Générale
5. Mise en oeuvre technique avec traçabilité renforcée
6. Durée de validité limitée à la durée de la mission (max 6 mois)

### 4.2 Délais de traitement

| Niveau | Délai standard | Délai urgent |
|--------|---------------|--------------|
| PUBLIC | Automatique | Automatique |
| INTERNE | 2 jours ouvrés | 4 heures |
| CONFIDENTIEL | 5 jours ouvrés | 24 heures |
| SECRET | 10 jours ouvrés | 48 heures (DG) |

### 4.3 Révocation des accès

**Révocation immédiate (< 4 heures) :**
- Départ de l'organisation (démission, fin de contrat, licenciement)
- Suspension disciplinaire
- Incident de sécurité impliquant l'agent
- Signalement de comportement suspect

**Révocation planifiée :**
- Changement de poste : révocation des anciens accès dans les 5 jours ouvrés
- Fin de mission externe : révocation le jour de la fin de mission
- Accès à durée limitée : révocation automatique à l'échéance

### 4.4 Revue des accès

| Fréquence | Portée |
|-----------|--------|
| Mensuelle | Accès niveau SECRET — liste exhaustive |
| Trimestrielle | Accès niveau CONFIDENTIEL |
| Semestrielle | Accès niveau INTERNE |
| Annuelle | Audit complet de tous les accès |

**Lors de la revue :**
- Chaque Data Owner valide les accès à ses données
- Les accès non justifiés ou inactifs depuis plus de 90 jours sont révoqués
- Les anomalies sont escaladées au CDO

---

## 5. Exigences techniques

### 5.1 Authentification

| Classification | Méthode d'authentification |
|---------------|---------------------------|
| PUBLIC | Aucune (accès public) |
| INTERNE | Identifiant + mot de passe fort |
| CONFIDENTIEL | MFA (Multi-Factor Authentication) recommandé |
| SECRET | MFA obligatoire + token physique ou biométrie |

**Politique de mots de passe :**
- Longueur minimale : 12 caractères
- Complexité : majuscules, minuscules, chiffres, caractères spéciaux
- Renouvellement : tous les 90 jours (CONFIDENTIEL/SECRET : 60 jours)
- Historique : les 10 derniers mots de passe ne peuvent être réutilisés
- Verrouillage : après 5 tentatives échouées

### 5.2 Traçabilité

| Action | Niveau de log |
|--------|--------------|
| Connexion réussie | INTERNE+ |
| Tentative de connexion échouée | Tous niveaux |
| Lecture de donnée | CONFIDENTIEL+ |
| Modification de donnée | INTERNE+ |
| Suppression de donnée | Tous niveaux |
| Export / téléchargement | CONFIDENTIEL+ |
| Modification des droits d'accès | Tous niveaux |

**Conservation des logs :**
- Logs d'accès données INTERNE : 1 an
- Logs d'accès données CONFIDENTIEL : 2 ans
- Logs d'accès données SECRET : 5 ans

### 5.3 Chiffrement

| Niveau | En transit | Au repos |
|--------|-----------|---------|
| PUBLIC | TLS 1.2+ recommandé | Non requis |
| INTERNE | TLS 1.2+ obligatoire | Chiffrement disque recommandé |
| CONFIDENTIEL | TLS 1.3 obligatoire | AES-128 minimum |
| SECRET | TLS 1.3 + VPN | AES-256 obligatoire |

---

## 6. Accès des tiers et prestataires

### 6.1 Types d'accès externes autorisés

| Type de tiers | Accès autorisé | Conditions |
|---------------|---------------|-----------|
| Prestataire de développement | INTERNE (env. test uniquement) | Accord de confidentialité, données anonymisées |
| Auditeur externe | CONFIDENTIEL (lecture seule) | Mandat d'audit, NDA, accès temporaire |
| Partenaire commercial | PUBLIC uniquement | Par défaut |
| Partenaire commercial étendu | INTERNE avec approbation | Accord de partenariat |
| Autorités de contrôle | Selon demande légale | Réquisition judiciaire ou administrative |

### 6.2 Conditions pour l'accès externe

1. Signature d'un accord de traitement des données (DPA)
2. Engagement de confidentialité nominatif pour les personnes concernées
3. Accès uniquement via les canaux sécurisés approuvés
4. Interdiction de sous-traiter l'accès sans autorisation préalable
5. Obligation de notification immédiate de tout incident

---

## 7. Sanctions

Le non-respect de la présente politique est passible de :

| Gravité | Exemple | Sanction |
|---------|---------|----------|
| Mineure | Partage interne sans autorisation | Rappel à l'ordre, formation |
| Modérée | Accès à des données hors périmètre | Avertissement formel, révision des accès |
| Grave | Export de données CONFIDENTIEL sans autorisation | Sanctions disciplinaires pouvant aller au licenciement |
| Critique | Fuite ou vente de données SECRET | Sanctions disciplinaires + poursuites judiciaires |

Les violations sont signalées au DRH, au CDO et, si nécessaire, à l'autorité de protection des données et aux instances judiciaires compétentes.

---

*Document produit dans le cadre du Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000*
