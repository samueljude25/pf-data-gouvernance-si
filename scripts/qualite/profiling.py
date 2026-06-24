"""
Profiling automatique d'un dataset CSV.

Usage :
    python profiling.py --input data/samples/dataset_brut.csv
    python profiling.py --input data/samples/dataset_brut.csv --output rapport_profiling.md

Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000
Contexte : Organisations Afrique centrale / Congo-Brazzaville
"""

import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def lire_csv(chemin: str) -> tuple[list[str], list[dict]]:
    """Lit un fichier CSV et retourne (entetes, lignes)."""
    import csv
    with open(chemin, encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        entetes = lecteur.fieldnames or []
        lignes = list(lecteur)
    return list(entetes), lignes


# ---------------------------------------------------------------------------
# Détection de types
# ---------------------------------------------------------------------------

VALEURS_VIDES = {"", "null", "none", "n/a", "na", "nd", "inconnu", "unknown"}


def est_vide(valeur: str) -> bool:
    return valeur is None or valeur.strip().lower() in VALEURS_VIDES


def detecter_type(valeurs_non_vides: list[str]) -> str:
    """Détecte le type dominant d'une colonne."""
    if not valeurs_non_vides:
        return "vide"

    # Entier
    def est_entier(v):
        try:
            int(v.replace(" ", "").replace(",", ""))
            return True
        except ValueError:
            return False

    # Décimal
    def est_decimal(v):
        try:
            float(v.replace(" ", "").replace(",", "."))
            return True
        except ValueError:
            return False

    # Date (formats courants)
    PATTERNS_DATE = [
        r"^\d{4}-\d{2}-\d{2}$",
        r"^\d{2}/\d{2}/\d{4}$",
        r"^\d{2}-\d{2}-\d{4}$",
    ]

    def est_date(v):
        return any(re.match(p, v.strip()) for p in PATTERNS_DATE)

    echantillon = valeurs_non_vides[:200]
    nb = len(echantillon)

    if sum(1 for v in echantillon if est_entier(v)) / nb >= 0.9:
        return "entier"
    if sum(1 for v in echantillon if est_decimal(v)) / nb >= 0.9:
        return "decimal"
    if sum(1 for v in echantillon if est_date(v)) / nb >= 0.9:
        return "date"
    return "texte"


# ---------------------------------------------------------------------------
# Statistiques numériques
# ---------------------------------------------------------------------------

def stats_numeriques(valeurs: list[float]) -> dict:
    """Calcule les statistiques descriptives d'une série numérique."""
    if not valeurs:
        return {}
    n = len(valeurs)
    valeurs_triees = sorted(valeurs)
    total = sum(valeurs)
    moyenne = total / n
    variance = sum((x - moyenne) ** 2 for x in valeurs) / n
    ecart_type = math.sqrt(variance)

    def percentile(p):
        idx = (p / 100) * (n - 1)
        bas = int(idx)
        haut = min(bas + 1, n - 1)
        return valeurs_triees[bas] + (idx - bas) * (valeurs_triees[haut] - valeurs_triees[bas])

    q1 = percentile(25)
    mediane = percentile(50)
    q3 = percentile(75)
    iqr = q3 - q1
    borne_inf = q1 - 1.5 * iqr
    borne_sup = q3 + 1.5 * iqr
    outliers = [v for v in valeurs if v < borne_inf or v > borne_sup]

    return {
        "min": min(valeurs),
        "max": max(valeurs),
        "moyenne": round(moyenne, 4),
        "mediane": round(mediane, 4),
        "ecart_type": round(ecart_type, 4),
        "q1": round(q1, 4),
        "q3": round(q3, 4),
        "iqr": round(iqr, 4),
        "nb_outliers": len(outliers),
        "pct_outliers": round(len(outliers) / n * 100, 2),
        "exemples_outliers": outliers[:5],
    }


# ---------------------------------------------------------------------------
# Profiling par colonne
# ---------------------------------------------------------------------------

def profiler_colonne(nom: str, valeurs_brutes: list[str]) -> dict:
    """Calcule le profil complet d'une colonne."""
    nb_total = len(valeurs_brutes)
    vides = [v for v in valeurs_brutes if est_vide(v)]
    non_vides = [v.strip() for v in valeurs_brutes if not est_vide(v)]

    nb_vides = len(vides)
    nb_non_vides = len(non_vides)
    taux_completude = round(nb_non_vides / nb_total * 100, 2) if nb_total > 0 else 0

    # Cardinalité
    compteur = Counter(non_vides)
    nb_distincts = len(compteur)
    taux_unicite = round(nb_distincts / nb_non_vides * 100, 2) if nb_non_vides > 0 else 0

    # Top valeurs
    top_valeurs = compteur.most_common(10)

    # Type
    type_detecte = detecter_type(non_vides)

    # Stats numériques
    stats_num = {}
    if type_detecte in ("entier", "decimal") and non_vides:
        try:
            valeurs_num = [float(v.replace(",", ".").replace(" ", "")) for v in non_vides]
            stats_num = stats_numeriques(valeurs_num)
        except ValueError:
            pass

    # Longueur (texte)
    stats_longueur = {}
    if type_detecte == "texte" and non_vides:
        longueurs = [len(v) for v in non_vides]
        stats_longueur = {
            "min": min(longueurs),
            "max": max(longueurs),
            "moyenne": round(sum(longueurs) / len(longueurs), 1),
        }

    # Détection patterns spéciaux
    patterns = {}
    if type_detecte == "texte":
        # Téléphones Congo
        nb_tel = sum(1 for v in non_vides if re.match(r"^(\+242)?0?[456]\d{7}$", v.replace(" ", "")))
        if nb_tel > nb_non_vides * 0.3:
            patterns["telephone_congo"] = f"{nb_tel}/{nb_non_vides} ({round(nb_tel/nb_non_vides*100)}%)"

        # Emails
        nb_email = sum(1 for v in non_vides if re.match(r"^[^@]+@[^@]+\.[^@]+$", v))
        if nb_email > nb_non_vides * 0.3:
            patterns["email"] = f"{nb_email}/{nb_non_vides} ({round(nb_email/nb_non_vides*100)}%)"

    return {
        "nom": nom,
        "type_detecte": type_detecte,
        "nb_total": nb_total,
        "nb_non_vides": nb_non_vides,
        "nb_vides": nb_vides,
        "taux_completude_pct": taux_completude,
        "nb_distincts": nb_distincts,
        "taux_unicite_pct": taux_unicite,
        "top_valeurs": top_valeurs,
        "stats_numeriques": stats_num,
        "stats_longueur": stats_longueur,
        "patterns_detectes": patterns,
    }


# ---------------------------------------------------------------------------
# Profiling global du dataset
# ---------------------------------------------------------------------------

def profiler_dataset(chemin: str) -> dict:
    """Analyse complète d'un fichier CSV."""
    entetes, lignes = lire_csv(chemin)
    nb_lignes = len(lignes)
    nb_colonnes = len(entetes)

    # Déduplication
    lignes_str = [json.dumps(l, sort_keys=True) for l in lignes]
    nb_doublons = nb_lignes - len(set(lignes_str))

    colonnes = {}
    for col in entetes:
        valeurs = [ligne.get(col, "") for ligne in lignes]
        colonnes[col] = profiler_colonne(col, valeurs)

    # Score qualité préliminaire
    taux_completude_global = sum(
        c["taux_completude_pct"] for c in colonnes.values()
    ) / nb_colonnes if nb_colonnes > 0 else 0

    taux_unicite_lignes = round((nb_lignes - nb_doublons) / nb_lignes * 100, 2) if nb_lignes > 0 else 100

    return {
        "fichier": chemin,
        "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nb_lignes": nb_lignes,
        "nb_colonnes": nb_colonnes,
        "nb_doublons_exacts": nb_doublons,
        "taux_unicite_lignes_pct": taux_unicite_lignes,
        "taux_completude_global_pct": round(taux_completude_global, 2),
        "colonnes": colonnes,
    }


# ---------------------------------------------------------------------------
# Génération du rapport Markdown
# ---------------------------------------------------------------------------

def generer_rapport(profil: dict) -> str:
    """Génère un rapport de profiling en Markdown."""
    lines = []
    p = profil

    lines.append(f"# Rapport de Profiling des Données")
    lines.append(f"")
    lines.append(f"**Fichier analysé :** `{p['fichier']}`  ")
    lines.append(f"**Date d'analyse :** {p['date_analyse']}  ")
    lines.append(f"**Outil :** Profiling automatique — Cadre de Gouvernance des Données")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 1. Vue d'ensemble")
    lines.append(f"")
    lines.append(f"| Indicateur | Valeur |")
    lines.append(f"|-----------|--------|")
    lines.append(f"| Nombre de lignes | {p['nb_lignes']:,} |")
    lines.append(f"| Nombre de colonnes | {p['nb_colonnes']} |")
    lines.append(f"| Doublons exacts | {p['nb_doublons_exacts']} |")
    lines.append(f"| Taux d'unicité des lignes | {p['taux_unicite_lignes_pct']}% |")
    lines.append(f"| Complétude globale | {p['taux_completude_global_pct']}% |")
    lines.append(f"")

    # Évaluation rapide
    score_approx = (p['taux_completude_global_pct'] * 0.4
                    + p['taux_unicite_lignes_pct'] * 0.3
                    + 70 * 0.3)  # exactitude et validité non calculables sans règles
    niveau = "Excellent" if score_approx >= 90 else ("Bon" if score_approx >= 80 else ("Acceptable" if score_approx >= 70 else "Insuffisant"))
    lines.append(f"**Score qualité préliminaire (estimation) :** {score_approx:.1f}/100 — {niveau}")
    lines.append(f"")
    lines.append(f"> Score basé uniquement sur complétude et unicité. "
                 f"Utiliser `scoring.py` pour le score complet avec toutes les dimensions.")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 2. Analyse par colonne")
    lines.append(f"")

    for nom, col in p["colonnes"].items():
        statut_completude = "OK" if col["taux_completude_pct"] >= 95 else ("AVERTISSEMENT" if col["taux_completude_pct"] >= 80 else "PROBLEME")
        lines.append(f"### Colonne : `{nom}`")
        lines.append(f"")
        lines.append(f"| Attribut | Valeur |")
        lines.append(f"|---------|--------|")
        lines.append(f"| Type détecté | {col['type_detecte']} |")
        lines.append(f"| Valeurs renseignées | {col['nb_non_vides']}/{col['nb_total']} |")
        lines.append(f"| Taux de complétude | **{col['taux_completude_pct']}%** [{statut_completude}] |")
        lines.append(f"| Valeurs distinctes | {col['nb_distincts']} |")
        lines.append(f"| Taux d'unicité | {col['taux_unicite_pct']}% |")

        if col["stats_numeriques"]:
            sn = col["stats_numeriques"]
            lines.append(f"| Min | {sn['min']} |")
            lines.append(f"| Max | {sn['max']} |")
            lines.append(f"| Moyenne | {sn['moyenne']} |")
            lines.append(f"| Médiane | {sn['mediane']} |")
            lines.append(f"| Écart-type | {sn['ecart_type']} |")
            lines.append(f"| Outliers (IQR) | {sn['nb_outliers']} ({sn['pct_outliers']}%) |")

        if col["stats_longueur"]:
            sl = col["stats_longueur"]
            lines.append(f"| Longueur min | {sl['min']} car. |")
            lines.append(f"| Longueur max | {sl['max']} car. |")
            lines.append(f"| Longueur moy. | {sl['moyenne']} car. |")

        lines.append(f"")

        if col["top_valeurs"]:
            lines.append(f"**Top valeurs :**")
            lines.append(f"")
            lines.append(f"| Valeur | Occurrences |")
            lines.append(f"|--------|-------------|")
            for valeur, cnt in col["top_valeurs"][:5]:
                pct = round(cnt / col["nb_non_vides"] * 100, 1)
                lines.append(f"| `{valeur}` | {cnt} ({pct}%) |")
            lines.append(f"")

        if col["patterns_detectes"]:
            lines.append(f"**Patterns détectés :** {col['patterns_detectes']}")
            lines.append(f"")

        lines.append(f"")

    lines.append(f"---")
    lines.append(f"")
    lines.append(f"## 3. Recommandations")
    lines.append(f"")
    lines.append(f"### Problèmes détectés")
    lines.append(f"")

    problemes = []
    for nom, col in p["colonnes"].items():
        if col["taux_completude_pct"] < 80:
            problemes.append(f"- **Complétude faible** — `{nom}` : {col['taux_completude_pct']}% de valeurs renseignées")
        if col["stats_numeriques"] and col["stats_numeriques"]["pct_outliers"] > 5:
            problemes.append(f"- **Outliers** — `{nom}` : {col['stats_numeriques']['nb_outliers']} valeurs aberrantes ({col['stats_numeriques']['pct_outliers']}%)")

    if p["nb_doublons_exacts"] > 0:
        problemes.append(f"- **Doublons** : {p['nb_doublons_exacts']} lignes dupliquées détectées")

    if problemes:
        for pb in problemes:
            lines.append(pb)
    else:
        lines.append("Aucun problème majeur détecté. Lancer `validation.py` pour les contrôles de règles métier.")

    lines.append(f"")
    lines.append(f"### Prochaines étapes recommandées")
    lines.append(f"")
    lines.append(f"1. Exécuter `validation.py` avec les règles YAML pour les contrôles métier")
    lines.append(f"2. Exécuter `scoring.py` pour le score qualité complet sur les 6 dimensions")
    lines.append(f"3. Exécuter `deduplication.py` pour la détection avancée des doublons")
    lines.append(f"4. Générer le rapport final avec `rapport_qualite.py`")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"*Rapport généré automatiquement — Cadre de Gouvernance des Données*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Profiling automatique d'un dataset CSV"
    )
    parser.add_argument("--input", "-i", required=True, help="Chemin vers le fichier CSV à analyser")
    parser.add_argument("--output", "-o", help="Chemin du rapport de sortie (Markdown)")
    parser.add_argument("--json", action="store_true", help="Afficher aussi le profil complet en JSON")
    args = parser.parse_args()

    chemin = args.input
    if not Path(chemin).exists():
        print(f"Erreur : fichier introuvable : {chemin}", file=sys.stderr)
        sys.exit(1)

    print(f"Analyse de : {chemin} ...")
    profil = profiler_dataset(chemin)

    rapport = generer_rapport(profil)

    if args.output:
        Path(args.output).write_text(rapport, encoding="utf-8")
        print(f"Rapport sauvegardé : {args.output}")
    else:
        print(rapport)

    if args.json:
        print("\n--- PROFIL JSON ---")
        # Sérialiser sans les listes complexes pour la lisibilité
        print(json.dumps({
            k: v for k, v in profil.items() if k != "colonnes"
        }, ensure_ascii=False, indent=2))

    print(f"\nAnalyse terminée : {profil['nb_lignes']} lignes, {profil['nb_colonnes']} colonnes.")
    print(f"Complétude globale : {profil['taux_completude_global_pct']}%")
    print(f"Doublons exacts : {profil['nb_doublons_exacts']}")


if __name__ == "__main__":
    main()
