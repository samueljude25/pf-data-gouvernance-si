"""
Calcul du score qualité global d'un dataset selon les 6 dimensions.

Score global = Σ (score_dimension × poids_dimension)
Dimensions : complétude (25%), exactitude (25%), cohérence (20%),
             actualité (15%), unicité (10%), validité (5%)

Usage :
    python scoring.py --input data/samples/dataset_brut.csv --entite client
    python scoring.py --input data/samples/dataset_brut.csv --entite client --json

Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000
"""

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration des poids et seuils
# ---------------------------------------------------------------------------

POIDS = {
    "completude": 0.25,
    "exactitude": 0.25,
    "coherence": 0.20,
    "actualite": 0.15,
    "unicite": 0.10,
    "validite": 0.05,
}

SEUILS = {
    "excellent": 95,
    "bon": 85,
    "acceptable": 70,
    "insuffisant": 0,
}

VALEURS_VIDES = {"", "null", "none", "n/a", "na", "nd", "inconnu"}

# Configuration par entité
CONFIG_ENTITE = {
    "client": {
        "champs_obligatoires": ["nom", "prenom", "telephone", "departement", "type_client"],
        "champs_cles_unicite": ["telephone"],
        "champ_date_maj": "date_creation",  # à défaut de date_maj
        "delai_fraicheur_jours": 365,
        "regles_coherence": [],
        "regles_validite": [
            {"champ": "telephone", "type": "format", "pattern": r"^(\+242)?0?[456]\d{7}$"},
            {"champ": "email", "type": "format", "pattern": r"^[^@]+@[^@]+\.[^@]+$", "obligatoire": False},
            {"champ": "type_client", "type": "liste",
             "valeurs": ["Particulier", "Entreprise", "Administration", "ONG"]},
            {"champ": "departement", "type": "liste",
             "valeurs": ["Brazzaville", "Pointe-Noire", "Bouenza", "Cuvette",
                         "Cuvette-Ouest", "Kouilou", "Lékoumou", "Likouala",
                         "Niari", "Plateaux", "Pool", "Sangha"]},
        ],
    },
    "transaction": {
        "champs_obligatoires": ["id_transaction", "montant", "devise", "date_transaction", "type_transaction", "statut"],
        "champs_cles_unicite": ["id_transaction"],
        "champ_date_maj": "date_transaction",
        "delai_fraicheur_jours": 90,
        "regles_coherence": [
            {"description": "Montant positif", "champ": "montant", "type": "positif"},
        ],
        "regles_validite": [
            {"champ": "devise", "type": "liste", "valeurs": ["XAF", "EUR", "USD", "GBP"]},
            {"champ": "type_transaction", "type": "liste",
             "valeurs": ["VENTE", "REMBOURSEMENT", "PAIEMENT", "TRANSFERT", "DEPOT", "RETRAIT", "FRAIS"]},
            {"champ": "statut", "type": "liste",
             "valeurs": ["EN_ATTENTE", "VALIDEE", "REJETEE", "ANNULEE", "EN_COURS"]},
        ],
    },
    "produit": {
        "champs_obligatoires": ["id_produit", "libelle", "categorie", "prix_unitaire", "unite_mesure"],
        "champs_cles_unicite": ["id_produit"],
        "champ_date_maj": "date_creation",
        "delai_fraicheur_jours": 730,
        "regles_coherence": [],
        "regles_validite": [
            {"champ": "categorie", "type": "liste",
             "valeurs": ["Alimentaire", "Santé", "Électronique", "Textile",
                         "BTP", "Services", "Agriculture", "Transport", "Éducation", "Énergie"]},
        ],
    },
}


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def est_vide(valeur) -> bool:
    return valeur is None or str(valeur).strip().lower() in VALEURS_VIDES


def parser_date(valeur: str) -> date | None:
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d %H:%M:%S"]
    for fmt in formats:
        try:
            return datetime.strptime(str(valeur).strip(), fmt).date()
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Calcul des 6 dimensions
# ---------------------------------------------------------------------------

def score_completude(lignes: list[dict], champs_obligatoires: list[str]) -> tuple[float, dict]:
    """Dimension 1 : Complétude des champs obligatoires."""
    if not lignes or not champs_obligatoires:
        return 100.0, {}

    total_cellules = len(lignes) * len(champs_obligatoires)
    renseignees = 0
    detail = {}

    for champ in champs_obligatoires:
        nb_renseignes = sum(1 for l in lignes if not est_vide(l.get(champ, "")))
        taux = nb_renseignes / len(lignes) * 100
        detail[champ] = round(taux, 2)
        renseignees += nb_renseignes

    score = renseignees / total_cellules * 100
    return round(score, 2), detail


def score_exactitude(lignes: list[dict], config: dict) -> tuple[float, dict]:
    """
    Dimension 2 : Exactitude par règles de plausibilité.
    Sans source de vérité externe, utilise des règles de vraisemblance :
    - Valeurs numériques dans des plages raisonnables
    - Dates cohérentes (pas dans le futur)
    - Formats typiquement corrects
    """
    if not lignes:
        return 100.0, {}

    controles = 0
    conformes = 0
    detail = {}

    # Plausibilité des montants (si champ montant présent)
    if any("montant" in l for l in lignes):
        for l in lignes:
            val = l.get("montant", "")
            if not est_vide(val):
                controles += 1
                try:
                    nb = float(str(val).replace(",", ".").replace(" ", ""))
                    # Plausibilité : montant entre 1 et 100M FCFA
                    if 0 < nb <= 100_000_000:
                        conformes += 1
                except ValueError:
                    pass
        if controles > 0:
            detail["montant_plausible"] = round(conformes / controles * 100, 2)

    # Plausibilité dates de naissance (si présent)
    if any("date_naissance" in l for l in lignes):
        nb_ok = 0
        nb_total = 0
        for l in lignes:
            val = l.get("date_naissance", "")
            if not est_vide(val):
                nb_total += 1
                d = parser_date(str(val))
                if d:
                    age = (date.today() - d).days // 365
                    if 0 <= age <= 110:
                        nb_ok += 1
        if nb_total > 0:
            controles += nb_total
            conformes += nb_ok
            detail["age_plausible"] = round(nb_ok / nb_total * 100, 2)

    # Si aucun contrôle spécifique applicable, estimation basée sur l'absence d'anomalies flagrantes
    if controles == 0:
        # Estimation conservative : 85% par défaut si aucun contrôle
        return 85.0, {"note": "Exactitude estimée — aucun contrôle de plausibilité applicable"}

    score = conformes / controles * 100
    return round(score, 2), detail


def score_coherence(lignes: list[dict], regles_coherence: list[dict]) -> tuple[float, dict]:
    """Dimension 3 : Cohérence des données."""
    if not lignes or not regles_coherence:
        # Sans règles de cohérence spécifiques, score de référence élevé
        return 99.0, {"note": "Pas de règles de cohérence intra-enregistrement définies"}

    total = len(lignes) * len(regles_coherence)
    violations = 0
    detail = {}

    for regle in regles_coherence:
        nb_viol = 0
        for l in lignes:
            if regle["type"] == "positif":
                val = l.get(regle["champ"], "")
                if not est_vide(val):
                    try:
                        if float(str(val).replace(",", ".")) <= 0:
                            nb_viol += 1
                    except ValueError:
                        nb_viol += 1
        detail[regle["description"]] = nb_viol
        violations += nb_viol

    score = (total - violations) / total * 100
    return round(score, 2), detail


def score_actualite(lignes: list[dict], champ_date: str, delai_jours: int) -> tuple[float, dict]:
    """Dimension 4 : Actualité des données."""
    if not lignes or not champ_date:
        return 80.0, {"note": "Champ de date de mise à jour non disponible"}

    date_limite = date.today() - timedelta(days=delai_jours)
    nb_actuels = 0
    nb_avec_date = 0
    nb_format_invalide = 0

    for l in lignes:
        val = l.get(champ_date, "")
        if not est_vide(val):
            d = parser_date(str(val))
            if d:
                nb_avec_date += 1
                if d >= date_limite:
                    nb_actuels += 1
            else:
                nb_format_invalide += 1

    if nb_avec_date == 0:
        return 50.0, {"note": "Aucune date valide trouvée", "nb_format_invalide": nb_format_invalide}

    score = nb_actuels / nb_avec_date * 100
    return round(score, 2), {
        "delai_fraicheur_jours": delai_jours,
        "date_limite": str(date_limite),
        "nb_avec_date": nb_avec_date,
        "nb_actuels": nb_actuels,
        "nb_format_invalide": nb_format_invalide,
    }


def score_unicite(lignes: list[dict], champs_cles: list[str]) -> tuple[float, dict]:
    """Dimension 5 : Unicité des enregistrements sur les champs clés."""
    if not lignes:
        return 100.0, {}

    nb_total = len(lignes)
    valeurs_cles = []
    for l in lignes:
        cle = tuple(str(l.get(c, "")).strip().lower() for c in champs_cles)
        valeurs_cles.append(cle)

    nb_distincts = len(set(valeurs_cles))
    nb_doublons = nb_total - nb_distincts

    score = nb_distincts / nb_total * 100
    return round(score, 2), {
        "champs_cles": champs_cles,
        "nb_total": nb_total,
        "nb_distincts": nb_distincts,
        "nb_doublons": nb_doublons,
        "pct_doublons": round(nb_doublons / nb_total * 100, 2),
    }


def score_validite(lignes: list[dict], regles_validite: list[dict]) -> tuple[float, dict]:
    """Dimension 6 : Validité des formats et valeurs."""
    if not lignes or not regles_validite:
        return 95.0, {"note": "Règles de validité non définies pour ce profil"}

    total_controles = 0
    conformes = 0
    detail = {}

    for regle in regles_validite:
        champ = regle["champ"]
        obligatoire = regle.get("obligatoire", True)
        nb_ok = 0
        nb_controles = 0

        for l in lignes:
            val = str(l.get(champ, "")).strip()
            if est_vide(val):
                if not obligatoire:
                    continue
                # Valeur vide obligatoire = non conforme
                nb_controles += 1
                continue

            nb_controles += 1
            type_regle = regle["type"]

            if type_regle == "format":
                if re.match(regle["pattern"], val.replace(" ", "")):
                    nb_ok += 1
            elif type_regle == "liste":
                if val in regle["valeurs"]:
                    nb_ok += 1

        if nb_controles > 0:
            taux = nb_ok / nb_controles * 100
            detail[f"{champ}_{regle['type']}"] = round(taux, 2)
            total_controles += nb_controles
            conformes += nb_ok

    if total_controles == 0:
        return 95.0, {"note": "Aucun contrôle applicable sur les données présentes"}

    score = conformes / total_controles * 100
    return round(score, 2), detail


# ---------------------------------------------------------------------------
# Score global et interprétation
# ---------------------------------------------------------------------------

def niveau_qualite(score: float) -> str:
    if score >= SEUILS["excellent"]:
        return "EXCELLENT"
    if score >= SEUILS["bon"]:
        return "BON"
    if score >= SEUILS["acceptable"]:
        return "ACCEPTABLE"
    return "INSUFFISANT"


def calculer_score_global(lignes: list[dict], entite: str) -> dict:
    """Calcule le score qualité global et les scores par dimension."""
    config = CONFIG_ENTITE.get(entite)
    if not config:
        raise ValueError(f"Entité inconnue : {entite}")

    s_completude, det_completude = score_completude(lignes, config["champs_obligatoires"])
    s_exactitude, det_exactitude = score_exactitude(lignes, config)
    s_coherence, det_coherence = score_coherence(lignes, config["regles_coherence"])
    s_actualite, det_actualite = score_actualite(lignes, config["champ_date_maj"], config["delai_fraicheur_jours"])
    s_unicite, det_unicite = score_unicite(lignes, config["champs_cles_unicite"])
    s_validite, det_validite = score_validite(lignes, config["regles_validite"])

    scores = {
        "completude": s_completude,
        "exactitude": s_exactitude,
        "coherence": s_coherence,
        "actualite": s_actualite,
        "unicite": s_unicite,
        "validite": s_validite,
    }

    score_global = sum(scores[dim] * poids for dim, poids in POIDS.items())
    score_global = round(score_global, 2)

    return {
        "entite": entite,
        "nb_enregistrements": len(lignes),
        "date_calcul": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score_global": score_global,
        "niveau": niveau_qualite(score_global),
        "dimensions": {
            "completude": {"score": s_completude, "poids": POIDS["completude"], "detail": det_completude},
            "exactitude": {"score": s_exactitude, "poids": POIDS["exactitude"], "detail": det_exactitude},
            "coherence": {"score": s_coherence, "poids": POIDS["coherence"], "detail": det_coherence},
            "actualite": {"score": s_actualite, "poids": POIDS["actualite"], "detail": det_actualite},
            "unicite": {"score": s_unicite, "poids": POIDS["unicite"], "detail": det_unicite},
            "validite": {"score": s_validite, "poids": POIDS["validite"], "detail": det_validite},
        },
    }


# ---------------------------------------------------------------------------
# Affichage
# ---------------------------------------------------------------------------

def afficher_tableau_bord(resultat: dict):
    """Affiche le tableau de bord qualité en console."""
    r = resultat
    print(f"\n{'='*65}")
    print(f"  SCORE QUALITÉ — Entité : {r['entite'].upper()}")
    print(f"{'='*65}")
    print(f"  Enregistrements analysés : {r['nb_enregistrements']:,}")
    print(f"  Date de calcul           : {r['date_calcul']}")
    print(f"{'='*65}")
    print(f"  SCORE GLOBAL : {r['score_global']:5.1f} / 100  [{r['niveau']}]")
    print(f"{'='*65}")
    print(f"  {'Dimension':<15} {'Score':>8}   {'Poids':>7}   {'Contribution':>12}")
    print(f"  {'-'*50}")

    for dim, data in r["dimensions"].items():
        contribution = data["score"] * data["poids"]
        barre = "█" * int(data["score"] / 10) + "░" * (10 - int(data["score"] / 10))
        print(f"  {dim:<15} {data['score']:>7.1f}%   {data['poids']*100:>6.0f}%   {contribution:>11.1f}")

    print(f"  {'-'*50}")
    print(f"  {'TOTAL':<15} {'':>8}   {'100%':>7}   {r['score_global']:>11.1f}")
    print(f"{'='*65}")

    # Interprétation
    if r["score_global"] >= 95:
        print(f"  Données certifiées — prêtes pour tous usages critiques.")
    elif r["score_global"] >= 85:
        print(f"  Données fiables — amélioration ciblée recommandée.")
    elif r["score_global"] >= 70:
        print(f"  Plan d'action qualité requis — usages critiques limités.")
    else:
        print(f"  ACTION URGENTE — usages critiques suspendus.")
    print(f"{'='*65}\n")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Calcul du score qualité global d'un dataset")
    parser.add_argument("--input", "-i", required=True, help="Chemin du fichier CSV")
    parser.add_argument("--entite", "-e", required=True,
                        choices=list(CONFIG_ENTITE.keys()),
                        help=f"Entité : {list(CONFIG_ENTITE.keys())}")
    parser.add_argument("--json", action="store_true", help="Afficher le résultat en JSON")
    parser.add_argument("--output", "-o", help="Sauvegarder le résultat JSON dans un fichier")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Erreur : fichier introuvable : {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))

    print(f"Calcul du score qualité pour {len(lignes)} enregistrements...")
    resultat = calculer_score_global(lignes, args.entite)
    afficher_tableau_bord(resultat)

    if args.json or args.output:
        json_str = json.dumps(resultat, ensure_ascii=False, indent=2)
        if args.json:
            print(json_str)
        if args.output:
            Path(args.output).write_text(json_str, encoding="utf-8")
            print(f"Résultat JSON sauvegardé : {args.output}")

    # Code de sortie basé sur le niveau
    if niveau_qualite(resultat["score_global"]) == "INSUFFISANT":
        sys.exit(2)
    elif niveau_qualite(resultat["score_global"]) == "ACCEPTABLE":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
