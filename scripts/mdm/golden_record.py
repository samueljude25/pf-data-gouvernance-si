"""
Construction du Golden Record — Master Data Management.

Fusionne plusieurs enregistrements représentant la même entité
en un seul enregistrement de référence (golden record).

Règles de survivorship appliquées :
- Valeur la plus récente pour les champs de contact
- Source la plus fiable pour les champs d'identité
- Valeur la plus complète pour les champs optionnels

Usage :
    python golden_record.py --input data/samples/dataset_brut.csv
    python golden_record.py --input data/samples/dataset_brut.csv --output golden_records.csv
    python golden_record.py --input data/samples/dataset_brut.csv --cluster-file clusters.csv

Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000
"""

import argparse
import csv
import hashlib
import re
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Priorité des sources (ordre décroissant de fiabilité)
# ---------------------------------------------------------------------------

PRIORITE_SOURCES = {
    "CRM": 1,
    "ERP": 2,
    "AGENCE": 3,
    "LEGACY": 4,
    "INCONNU": 5,
}

# ---------------------------------------------------------------------------
# Règles de survivorship par champ
# ---------------------------------------------------------------------------

REGLES_SURVIVORSHIP = {
    # Champ : règle de sélection de la "meilleure" valeur
    "nom":         "source_prioritaire",   # Source CRM > ERP > autres
    "prenom":      "source_prioritaire",
    "type_client": "consensus",            # Valeur majoritaire
    "telephone":   "plus_recent",          # Valeur la plus récemment mise à jour
    "email":       "plus_recent",
    "adresse":     "plus_recent",
    "quartier":    "plus_recent",
    "ville":       "source_prioritaire",
    "departement": "source_prioritaire",
    "pays":        "valeur_constante",     # Valeur constante (Congo par défaut)
    "statut":      "source_prioritaire",
}


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def normaliser_telephone(tel: str) -> str:
    """Normalise un numéro de téléphone au format standard (+242XXXXXXXXX)."""
    tel = re.sub(r"[^\d+]", "", str(tel))
    tel = re.sub(r"^(\+242|00242)", "", tel)
    if tel.startswith("0") and len(tel) == 9:
        tel = tel[1:]
    if len(tel) == 8:
        return f"+242{tel}"
    return tel


def est_vide(valeur: str) -> bool:
    vides = {"", "null", "none", "n/a", "na", "nd", "inconnu"}
    return str(valeur).strip().lower() in vides


def parser_date(valeur: str):
    """Parse une date depuis différents formats."""
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d %H:%M:%S"]
    for fmt in formats:
        try:
            return datetime.strptime(str(valeur).strip(), fmt)
        except ValueError:
            continue
    return None


def generer_id_maitre(valeur_cle: str) -> str:
    """Génère un identifiant MDM unique basé sur la valeur clé normalisée."""
    hash_val = hashlib.md5(valeur_cle.encode()).hexdigest()[:6].upper()
    return f"MDM-{hash_val}"


# ---------------------------------------------------------------------------
# Sélection de la meilleure valeur selon la règle de survivorship
# ---------------------------------------------------------------------------

def valeur_par_regle(
    valeurs: list[dict],  # [{"valeur": ..., "source": ..., "date_maj": ...}]
    regle: str,
    champ: str,
) -> str:
    """Applique la règle de survivorship et retourne la meilleure valeur."""
    valeurs_non_vides = [v for v in valeurs if not est_vide(v.get("valeur", ""))]

    if not valeurs_non_vides:
        return ""

    if regle == "source_prioritaire":
        # Trier par priorité de source (plus petit score = plus prioritaire)
        valeurs_triees = sorted(
            valeurs_non_vides,
            key=lambda v: PRIORITE_SOURCES.get(v.get("source", "INCONNU").upper(), 99),
        )
        return str(valeurs_triees[0]["valeur"]).strip()

    if regle == "plus_recent":
        # Valeur associée à la date de mise à jour la plus récente
        valeurs_avec_date = []
        for v in valeurs_non_vides:
            d = parser_date(str(v.get("date_maj", "")))
            valeurs_avec_date.append((d, v["valeur"]))

        valeurs_avec_date_valide = [(d, val) for d, val in valeurs_avec_date if d is not None]

        if valeurs_avec_date_valide:
            return str(sorted(valeurs_avec_date_valide, key=lambda x: x[0], reverse=True)[0][1]).strip()
        return str(valeurs_non_vides[0]["valeur"]).strip()

    if regle == "consensus":
        # Valeur la plus fréquente
        compteur = Counter(str(v["valeur"]).strip() for v in valeurs_non_vides)
        return compteur.most_common(1)[0][0]

    if regle == "valeur_constante":
        # Retourner la valeur du premier enregistrement
        return str(valeurs_non_vides[0]["valeur"]).strip()

    # Par défaut : première valeur non vide
    return str(valeurs_non_vides[0]["valeur"]).strip()


# ---------------------------------------------------------------------------
# Construction du golden record
# ---------------------------------------------------------------------------

def construire_golden_record(
    groupe: list[dict],
    cle_groupage: str = "telephone",
) -> dict:
    """
    Construit le golden record à partir d'un groupe d'enregistrements doublons.

    Args:
        groupe: liste d'enregistrements représentant la même entité
        cle_groupage: champ utilisé comme clé d'identification

    Returns:
        dict: Le golden record construit
    """
    if not groupe:
        return {}

    if len(groupe) == 1:
        # Pas de fusion nécessaire
        r = groupe[0].copy()
        r["_sources"] = r.get("source", "INCONNU")
        r["_nb_sources"] = 1
        r["_id_maitre"] = generer_id_maitre(str(r.get(cle_groupage, "")))
        r["_score_confiance"] = 70.0
        r["_date_creation_maitre"] = datetime.now().strftime("%Y-%m-%d")
        return r

    # Construire les vecteurs de valeurs par champ
    tous_champs = set()
    for r in groupe:
        tous_champs.update(r.keys())

    golden = {}

    for champ in tous_champs:
        if champ.startswith("_"):
            continue

        regle = REGLES_SURVIVORSHIP.get(champ, "source_prioritaire")
        valeurs = [
            {
                "valeur": r.get(champ, ""),
                "source": r.get("source", "INCONNU"),
                "date_maj": r.get("date_creation", ""),
            }
            for r in groupe
        ]
        golden[champ] = valeur_par_regle(valeurs, regle, champ)

    # Normaliser le téléphone dans le golden record
    if "telephone" in golden:
        tel_norm = normaliser_telephone(golden["telephone"])
        if tel_norm:
            golden["telephone"] = tel_norm

    # Métadonnées MDM
    valeur_cle = golden.get(cle_groupage, "")
    golden["_id_maitre"] = generer_id_maitre(str(valeur_cle))
    golden["_sources"] = "|".join(set(r.get("source", "INCONNU") for r in groupe))
    golden["_nb_sources"] = len(groupe)
    golden["_date_creation_maitre"] = datetime.now().strftime("%Y-%m-%d")

    # Calcul du score de confiance MDM
    golden["_score_confiance"] = calculer_score_confiance(groupe, golden)

    return golden


def calculer_score_confiance(groupe: list[dict], golden: dict) -> float:
    """
    Calcule le score de confiance du golden record (0-100).

    Critères :
    - Nombre de sources concordantes (max 30 pts)
    - Taux de concordance des valeurs entre sources (max 40 pts)
    - Fraîcheur des données (max 20 pts)
    - Complétude du golden record (max 10 pts)
    """
    champs_cles = ["nom", "prenom", "telephone", "email", "departement"]

    # Score sources (30 pts)
    nb_sources = len(groupe)
    score_sources = min(nb_sources / 3 * 30, 30)

    # Score concordance (40 pts)
    concordances = []
    for champ in champs_cles:
        valeurs = [str(r.get(champ, "")).strip() for r in groupe if not est_vide(r.get(champ, ""))]
        if len(valeurs) >= 2:
            valeur_gold = golden.get(champ, "")
            nb_concordants = sum(1 for v in valeurs if v == valeur_gold)
            concordances.append(nb_concordants / len(valeurs))

    score_concordance = (sum(concordances) / len(concordances) * 40) if concordances else 20

    # Score fraîcheur (20 pts) — basé sur la présence de dates de création
    dates_valides = []
    for r in groupe:
        d = parser_date(str(r.get("date_creation", "")))
        if d:
            dates_valides.append(d)

    if dates_valides:
        date_max = max(dates_valides)
        jours = (datetime.now() - date_max).days
        score_fraicheur = max(0, 20 - jours // 180)  # Perd 1 point tous les ~6 mois
    else:
        score_fraicheur = 10

    # Score complétude golden record (10 pts)
    champs_obligatoires = ["nom", "prenom", "telephone", "departement", "type_client"]
    nb_renseignes = sum(1 for c in champs_obligatoires if not est_vide(golden.get(c, "")))
    score_completude = nb_renseignes / len(champs_obligatoires) * 10

    total = score_sources + score_concordance + score_fraicheur + score_completude
    return round(min(total, 100), 1)


# ---------------------------------------------------------------------------
# Processus principal
# ---------------------------------------------------------------------------

def construire_tous_golden_records(
    lignes: list[dict],
    cle_groupage: str = "telephone",
) -> tuple[list[dict], dict]:
    """
    Groupe les enregistrements par clé et construit un golden record par groupe.

    Returns:
        (golden_records, stats)
    """
    # Grouper par clé normalisée
    groupes = {}
    non_groupes = []

    for l in lignes:
        cle_brute = l.get(cle_groupage, "")
        if est_vide(cle_brute):
            non_groupes.append(l)
            continue

        if cle_groupage == "telephone":
            cle_normalisee = normaliser_telephone(cle_brute)
        else:
            cle_normalisee = str(cle_brute).strip().lower()

        if not cle_normalisee:
            non_groupes.append(l)
            continue

        if cle_normalisee not in groupes:
            groupes[cle_normalisee] = []
        groupes[cle_normalisee].append(l)

    # Construire les golden records
    golden_records = []
    nb_fusions = 0

    for cle, groupe in groupes.items():
        gr = construire_golden_record(groupe, cle_groupage)
        golden_records.append(gr)
        if len(groupe) > 1:
            nb_fusions += 1

    # Enregistrements sans clé valide → golden record individuel
    for l in non_groupes:
        gr = construire_golden_record([l], cle_groupage)
        golden_records.append(gr)

    stats = {
        "nb_entrees": len(lignes),
        "nb_golden_records": len(golden_records),
        "nb_fusions": nb_fusions,
        "nb_sans_cle": len(non_groupes),
        "reduction": round((1 - len(golden_records) / len(lignes)) * 100, 1) if lignes else 0,
    }

    return golden_records, stats


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Construction du Golden Record MDM")
    parser.add_argument("--input", "-i", required=True, help="Fichier CSV source")
    parser.add_argument("--output", "-o", help="Fichier CSV de sortie (golden records)")
    parser.add_argument("--cle", "-k", default="telephone",
                        help="Champ utilisé comme clé de groupage (défaut : telephone)")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Erreur : fichier introuvable : {args.input}")
        return

    with open(args.input, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))

    print(f"Construction des golden records pour {len(lignes)} enregistrements...")
    print(f"Clé de groupage : {args.cle}")

    golden_records, stats = construire_tous_golden_records(lignes, cle_groupage=args.cle)

    # Affichage des statistiques
    print(f"\n{'='*55}")
    print(f"RÉSULTATS — GOLDEN RECORDS MDM")
    print(f"{'='*55}")
    print(f"Enregistrements source    : {stats['nb_entrees']:,}")
    print(f"Golden records produits   : {stats['nb_golden_records']:,}")
    print(f"Fusions effectuées        : {stats['nb_fusions']:,}")
    print(f"Sans clé de groupage      : {stats['nb_sans_cle']:,}")
    print(f"Réduction de la base      : {stats['reduction']}%")

    scores = [gr["_score_confiance"] for gr in golden_records if "_score_confiance" in gr]
    if scores:
        print(f"Score confiance moyen     : {sum(scores)/len(scores):.1f}/100")
        print(f"Score confiance min/max   : {min(scores):.1f} / {max(scores):.1f}")
    print(f"{'='*55}")

    if args.output:
        # Déterminer les colonnes (union de tous les champs)
        tous_champs = set()
        for gr in golden_records:
            tous_champs.update(gr.keys())

        # Ordonner : champs métier d'abord, métadonnées MDM ensuite
        champs_meta = [c for c in tous_champs if c.startswith("_")]
        champs_metier = [c for c in tous_champs if not c.startswith("_")]
        entetes = sorted(champs_metier) + sorted(champs_meta)

        with open(args.output, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=entetes, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(golden_records)

        print(f"\nGolden records exportés : {args.output}")
    else:
        # Afficher un aperçu
        print(f"\nAperçu des 5 premiers golden records :")
        for gr in golden_records[:5]:
            print(f"  [{gr.get('_id_maitre', '?')}] "
                  f"{gr.get('nom', '?')} {gr.get('prenom', '?')} "
                  f"— Tel: {gr.get('telephone', '?')} "
                  f"— Sources: {gr.get('_sources', '?')} "
                  f"— Confiance: {gr.get('_score_confiance', '?')}")


if __name__ == "__main__":
    main()
