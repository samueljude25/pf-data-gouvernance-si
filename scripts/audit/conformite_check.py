"""
Vérification de conformité d'un dataset aux règles RGPD-like.

Contrôle la présence de données personnelles, leur classification,
les durées de conservation, et le respect des principes de minimisation.

Usage :
    python conformite_check.py --input data/samples/dataset_brut.csv
    python conformite_check.py --input data/samples/dataset_brut.csv --rapport rapport_conformite.md

Cadre de Gouvernance des Données
Référence : Loi n° 29-2019 Congo, AUPC OHADA, RGPD (UE 2016/679)
"""

import argparse
import csv
import re
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Détecteurs de données personnelles
# ---------------------------------------------------------------------------

DETECTEURS_DONNEES_PERSONNELLES = [
    {
        "id": "DP-001",
        "nom": "Numéro de téléphone",
        "categorie": "ordinaire",
        "pattern": r"(\+242|00242|0?[456]\d{7})",
        "noms_champs_suspects": ["telephone", "tel", "phone", "mobile", "portable"],
        "risque": "Moyen",
    },
    {
        "id": "DP-002",
        "nom": "Adresse email",
        "categorie": "ordinaire",
        "pattern": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",
        "noms_champs_suspects": ["email", "mail", "courriel", "e_mail"],
        "risque": "Moyen",
    },
    {
        "id": "DP-003",
        "nom": "Date de naissance",
        "categorie": "ordinaire",
        "pattern": None,
        "noms_champs_suspects": ["date_naissance", "ddn", "naissance", "birth_date", "date_de_naissance"],
        "risque": "Moyen",
    },
    {
        "id": "DP-004",
        "nom": "Numéro d'identification nationale (NNI)",
        "categorie": "ordinaire",
        "pattern": r"\b\d{9,13}\b",
        "noms_champs_suspects": ["nni", "cni", "id_national", "numero_id", "identifiant_national"],
        "risque": "Élevé",
    },
    {
        "id": "DP-005",
        "nom": "Nom et prénom",
        "categorie": "ordinaire",
        "pattern": None,
        "noms_champs_suspects": ["nom", "prenom", "name", "firstname", "lastname", "full_name", "nom_complet"],
        "risque": "Faible",
    },
    {
        "id": "DP-006",
        "nom": "Adresse postale",
        "categorie": "ordinaire",
        "pattern": None,
        "noms_champs_suspects": ["adresse", "address", "rue", "ville", "quartier", "localite"],
        "risque": "Faible",
    },
    {
        "id": "DP-007",
        "nom": "Données de santé",
        "categorie": "sensible",
        "pattern": None,
        "noms_champs_suspects": [
            "diagnostic", "pathologie", "maladie", "traitement", "medicament",
            "ordonnance", "sante", "health", "medical", "patient", "symptome",
        ],
        "risque": "Très élevé",
    },
    {
        "id": "DP-008",
        "nom": "Données salariales",
        "categorie": "sensible",
        "pattern": None,
        "noms_champs_suspects": ["salaire", "remuneration", "prime", "indemnite", "paie", "revenus", "revenu"],
        "risque": "Élevé",
    },
    {
        "id": "DP-009",
        "nom": "Données biométriques",
        "categorie": "sensible",
        "pattern": None,
        "noms_champs_suspects": [
            "empreinte", "biometrie", "iris", "visage", "face", "fingerprint", "biometric",
        ],
        "risque": "Très élevé",
    },
    {
        "id": "DP-010",
        "nom": "Opinion politique ou syndicale",
        "categorie": "sensible",
        "pattern": None,
        "noms_champs_suspects": ["parti", "syndicat", "opinion_politique", "affiliation"],
        "risque": "Très élevé",
    },
]

# Champs pouvant indiquer une donnée personnelle (détection générique)
MOTS_CLES_PERSO = [
    "nom", "prenom", "name", "email", "mail", "telephone", "tel", "phone",
    "adresse", "address", "naissance", "birth", "age", "genre", "sexe",
    "nni", "cni", "passeport", "identifiant", "contact",
]

CHAMPS_SENSIBLES = [
    "salaire", "sante", "medical", "diagnostic", "diagnostic", "religion",
    "opinion", "syndicat", "biometrie", "empreinte", "condamnation", "jugement",
]

# Durées de conservation recommandées
DUREES_CONSERVATION = {
    "clients": {"active": "5 ans après fin de relation", "archivage": "10 ans"},
    "rh": {"active": "Durée contrat + 2 ans", "archivage": "28 ans (retraite)"},
    "financier": {"active": "10 ans", "archivage": "10 ans"},
    "sante": {"active": "20 ans", "archivage": "10 ans"},
    "audit": {"active": "2 ans", "archivage": "5 ans"},
}


# ---------------------------------------------------------------------------
# Analyse de conformité
# ---------------------------------------------------------------------------

def detecter_donnees_personnelles_champs(entetes: list[str]) -> list[dict]:
    """Détecte les données personnelles probables à partir des noms de champs."""
    detectees = []

    for entete in entetes:
        entete_norm = entete.lower().strip()

        for detecteur in DETECTEURS_DONNEES_PERSONNELLES:
            for nom_suspect in detecteur["noms_champs_suspects"]:
                if nom_suspect in entete_norm or entete_norm in nom_suspect:
                    detectees.append({
                        "champ": entete,
                        "detecteur_id": detecteur["id"],
                        "type_donnee": detecteur["nom"],
                        "categorie": detecteur["categorie"],
                        "risque": detecteur["risque"],
                        "methode_detection": "nom_de_champ",
                    })
                    break

    return detectees


def detecter_donnees_personnelles_contenu(
    lignes: list[dict],
    echantillon_max: int = 50,
) -> list[dict]:
    """Détecte les données personnelles par analyse du contenu (pattern matching)."""
    detectees = []
    echantillon = lignes[:echantillon_max]

    for detecteur in DETECTEURS_DONNEES_PERSONNELLES:
        if not detecteur["pattern"]:
            continue

        for entete in (echantillon[0].keys() if echantillon else []):
            nb_correspondances = 0
            for ligne in echantillon:
                valeur = str(ligne.get(entete, ""))
                if re.search(detecteur["pattern"], valeur):
                    nb_correspondances += 1

            taux = nb_correspondances / len(echantillon) if echantillon else 0
            if taux > 0.3:  # Plus de 30% des valeurs correspondent
                detectees.append({
                    "champ": entete,
                    "detecteur_id": detecteur["id"],
                    "type_donnee": detecteur["nom"],
                    "categorie": detecteur["categorie"],
                    "risque": detecteur["risque"],
                    "methode_detection": "pattern_contenu",
                    "taux_correspondance": f"{taux*100:.0f}%",
                })

    return detectees


def verifier_minimisation(entetes: list[str], donnees_perso: list[dict]) -> list[dict]:
    """Vérifie le principe de minimisation des données."""
    violations = []

    # Vérifier les champs potentiellement excessifs
    champs_potentiellement_excessifs = []
    for entete in entetes:
        entete_lower = entete.lower()
        # Champs très détaillés rarement nécessaires
        suspects = ["ip_address", "localisation_gps", "geolocation", "device_id",
                    "cookies", "historique_navigation", "password", "mot_de_passe"]
        for s in suspects:
            if s in entete_lower:
                champs_potentiellement_excessifs.append(entete)

    if champs_potentiellement_excessifs:
        violations.append({
            "type": "Champs potentiellement excessifs",
            "description": "Des champs peuvent violer le principe de minimisation",
            "champs": champs_potentiellement_excessifs,
            "recommendation": "Évaluer la nécessité de ces champs pour la finalité déclarée",
        })

    # Données sensibles sans justification évidente
    donnees_sensibles = [d for d in donnees_perso if d["categorie"] == "sensible"]
    if donnees_sensibles:
        violations.append({
            "type": "Données sensibles détectées",
            "description": "Des données de catégorie spéciale nécessitent une justification légale renforcée",
            "donnees": [d["type_donnee"] for d in donnees_sensibles],
            "recommendation": "Vérifier la base légale (consentement explicite, obligation légale) et réaliser une AIPD",
        })

    return violations


def verifier_structures_conformite(entetes: list[str]) -> dict:
    """Vérifie la présence de structures suggérant une bonne conformité."""
    checklist = {
        "champ_date_creation": False,
        "champ_date_maj": False,
        "champ_consentement": False,
        "champ_statut": False,
        "champ_source": False,
        "champ_classification": False,
    }

    entetes_lower = [e.lower() for e in entetes]

    if any("date_creation" in e or "created_at" in e or "date_saisie" in e for e in entetes_lower):
        checklist["champ_date_creation"] = True
    if any("date_maj" in e or "updated_at" in e or "date_modification" in e for e in entetes_lower):
        checklist["champ_date_maj"] = True
    if any("consentement" in e or "consent" in e or "opt_in" in e or "acceptation" in e for e in entetes_lower):
        checklist["champ_consentement"] = True
    if any("statut" in e or "status" in e or "actif" in e for e in entetes_lower):
        checklist["champ_statut"] = True
    if any("source" in e or "origine" in e or "canal" in e for e in entetes_lower):
        checklist["champ_source"] = True
    if any("classification" in e or "sensibilite" in e or "niveau" in e for e in entetes_lower):
        checklist["champ_classification"] = True

    return checklist


def calculer_score_conformite(
    donnees_perso: list[dict],
    violations_minimisation: list[dict],
    checklist: dict,
    nb_lignes: int,
) -> tuple[float, str]:
    """Calcule un score de conformité sur 100."""
    score = 100.0

    # Pénalités
    nb_donnees_sensibles = sum(1 for d in donnees_perso if d["categorie"] == "sensible")
    nb_donnees_risque_eleve = sum(1 for d in donnees_perso if d["risque"] in ("Élevé", "Très élevé"))

    # Données sensibles sans preuve de conformité
    if nb_donnees_sensibles > 0 and not checklist["champ_consentement"]:
        score -= 25

    if nb_donnees_risque_eleve > 0 and not checklist["champ_date_creation"]:
        score -= 10

    score -= len(violations_minimisation) * 10

    # Bonus pour bonnes pratiques
    nb_bonnes_pratiques = sum(1 for v in checklist.values() if v)
    score += min(nb_bonnes_pratiques * 3, 15)

    score = max(0, min(100, score))

    if score >= 80:
        niveau = "Satisfaisant"
    elif score >= 60:
        niveau = "Partiellement conforme"
    elif score >= 40:
        niveau = "Non conforme — actions requises"
    else:
        niveau = "Critique — conformité insuffisante"

    return round(score, 1), niveau


# ---------------------------------------------------------------------------
# Génération du rapport de conformité
# ---------------------------------------------------------------------------

def generer_rapport_conformite(resultat: dict) -> str:
    """Génère un rapport de conformité RGPD-like en Markdown."""
    lines = [
        f"# Rapport de Conformité — Protection des Données Personnelles",
        f"",
        f"**Date du rapport :** {resultat['date_analyse']}  ",
        f"**Fichier analysé :** `{resultat['fichier']}`  ",
        f"**Référentiel :** Loi n° 29-2019 Congo, AUPC OHADA, RGPD (UE 2016/679)",
        f"",
        f"---",
        f"",
        f"## 1. Score de Conformité",
        f"",
        f"| Indicateur | Valeur |",
        f"|-----------|--------|",
        f"| Score de conformité | **{resultat['score_conformite']}/100** |",
        f"| Niveau | **{resultat['niveau_conformite']}** |",
        f"| Enregistrements analysés | {resultat['nb_lignes']:,} |",
        f"| Données personnelles détectées | {len(resultat['donnees_personnelles_detectees'])} types |",
        f"| Données sensibles | {sum(1 for d in resultat['donnees_personnelles_detectees'] if d['categorie'] == 'sensible')} types |",
        f"",
        f"---",
        f"",
        f"## 2. Données Personnelles Détectées",
        f"",
        f"| Champ | Type de donnée | Catégorie | Risque | Méthode |",
        f"|-------|---------------|-----------|--------|---------|",
    ]

    for dp in resultat["donnees_personnelles_detectees"]:
        lines.append(
            f"| `{dp['champ']}` | {dp['type_donnee']} | {dp['categorie']} | {dp['risque']} | {dp['methode_detection']} |"
        )

    if not resultat["donnees_personnelles_detectees"]:
        lines.append("| — | Aucune donnée personnelle détectée | — | — | — |")

    lines.extend([
        f"",
        f"> **Note :** La détection se base sur les noms de champs et les patterns dans les données. "
        f"Une revue manuelle est recommandée pour confirmer les résultats.",
        f"",
        f"---",
        f"",
        f"## 3. Checklist de Conformité",
        f"",
        f"| Bonne pratique | Présente |",
        f"|---------------|---------|",
    ])

    labels = {
        "champ_date_creation": "Champ de date de création",
        "champ_date_maj": "Champ de date de mise à jour",
        "champ_consentement": "Champ de consentement/opt-in",
        "champ_statut": "Champ de statut d'enregistrement",
        "champ_source": "Champ de source des données",
        "champ_classification": "Champ de classification",
    }

    for cle, label in labels.items():
        present = resultat["checklist_conformite"].get(cle, False)
        statut = "Oui" if present else "Non (manquant)"
        lines.append(f"| {label} | {statut} |")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## 4. Violations et Risques",
        f"",
    ])

    if resultat["violations_minimisation"]:
        for viol in resultat["violations_minimisation"]:
            lines.extend([
                f"### {viol['type']}",
                f"",
                f"**Description :** {viol['description']}",
                f"",
                f"**Recommandation :** {viol['recommendation']}",
                f"",
            ])
    else:
        lines.extend([
            f"Aucune violation de minimisation détectée.",
            f"",
        ])

    lines.extend([
        f"---",
        f"",
        f"## 5. Obligations Réglementaires",
        f"",
        f"En présence de données personnelles, les obligations suivantes s'appliquent :",
        f"",
        f"### Loi n° 29-2019 (Congo-Brazzaville)",
        f"",
        f"- [ ] Le traitement est enregistré auprès de l'ARPCE",
        f"- [ ] La finalité du traitement est définie et documentée",
        f"- [ ] Une base légale est identifiée pour chaque traitement",
        f"- [ ] Les personnes concernées sont informées (notice de confidentialité)",
        f"- [ ] Les droits des personnes peuvent être exercés (accès, rectification, opposition)",
        f"- [ ] Des mesures de sécurité adaptées sont mises en place",
        f"- [ ] Les durées de conservation sont définies et respectées",
        f"",
        f"### Actions à mener si des données sensibles sont présentes",
        f"",
        f"- [ ] Réaliser une Analyse d'Impact sur la Protection des Données (AIPD)",
        f"- [ ] Obtenir un consentement explicite (si applicable)",
        f"- [ ] Renforcer les mesures de sécurité (chiffrement, accès restreints)",
        f"- [ ] Désigner un Délégué à la Protection des Données (DPO)",
        f"",
        f"---",
        f"",
        f"## 6. Durées de Conservation Recommandées",
        f"",
        f"| Domaine | Conservation active | Archivage | Base légale |",
        f"|---------|--------------------|-----------|-|",
        f"| Données clients | 5 ans post-relation | 10 ans | Contrat, légal |",
        f"| Données RH | Contrat + 2 ans | 28 ans | Code du travail |",
        f"| Données financières | 10 ans | 10 ans | OHADA, fiscal |",
        f"| Données de santé | 20 ans | 10 ans | Législation santé |",
        f"| Logs d'audit | 2 ans | 5 ans | Conformité |",
        f"",
        f"---",
        f"*Rapport généré par le Cadre de Gouvernance des Données*  ",
        f"*Contexte : Afrique centrale / Congo-Brazzaville*",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Analyse principale
# ---------------------------------------------------------------------------

def analyser_conformite(chemin: str) -> dict:
    """Analyse complète de la conformité RGPD-like d'un fichier CSV."""
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        entetes = list(lecteur.fieldnames or [])
        lignes = list(lecteur)

    # Détections
    dp_champs = detecter_donnees_personnelles_champs(entetes)
    dp_contenu = detecter_donnees_personnelles_contenu(lignes)

    # Dédupliquer les détections (même champ, même type)
    vus = set()
    donnees_perso = []
    for dp in dp_champs + dp_contenu:
        cle = (dp["champ"], dp["type_donnee"])
        if cle not in vus:
            vus.add(cle)
            donnees_perso.append(dp)

    violations_minimisation = verifier_minimisation(entetes, donnees_perso)
    checklist = verifier_structures_conformite(entetes)
    score, niveau = calculer_score_conformite(donnees_perso, violations_minimisation, checklist, len(lignes))

    return {
        "fichier": chemin,
        "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nb_lignes": len(lignes),
        "nb_colonnes": len(entetes),
        "donnees_personnelles_detectees": donnees_perso,
        "violations_minimisation": violations_minimisation,
        "checklist_conformite": checklist,
        "score_conformite": score,
        "niveau_conformite": niveau,
    }


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Vérification de conformité RGPD-like")
    parser.add_argument("--input", "-i", required=True, help="Fichier CSV à analyser")
    parser.add_argument("--rapport", "-r", help="Rapport Markdown de sortie")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Erreur : fichier introuvable : {args.input}")
        return

    print(f"Analyse de conformité : {args.input} ...")
    resultat = analyser_conformite(args.input)

    print(f"\n{'='*60}")
    print(f"RÉSULTAT CONFORMITÉ RGPD-like")
    print(f"{'='*60}")
    print(f"Score de conformité  : {resultat['score_conformite']}/100")
    print(f"Niveau               : {resultat['niveau_conformite']}")
    print(f"Données personnelles : {len(resultat['donnees_personnelles_detectees'])} types détectés")
    nb_sensibles = sum(1 for d in resultat["donnees_personnelles_detectees"] if d["categorie"] == "sensible")
    if nb_sensibles:
        print(f"  dont sensibles     : {nb_sensibles} (AIPD obligatoire)")
    print(f"{'='*60}")

    if args.rapport:
        rapport = generer_rapport_conformite(resultat)
        Path(args.rapport).write_text(rapport, encoding="utf-8")
        print(f"\nRapport de conformité sauvegardé : {args.rapport}")


if __name__ == "__main__":
    main()
