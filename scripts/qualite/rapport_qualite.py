"""
Génération d'un rapport qualité complet en Markdown.

Orchestre les scripts profiling.py, validation.py et scoring.py
pour produire un rapport professionnel complet.

Usage :
    python rapport_qualite.py --input data/samples/dataset_brut.csv --entite client
    python rapport_qualite.py --input data/samples/dataset_brut.csv --entite client --output rapport.md

Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

# Import des modules du cadre de gouvernance
sys.path.insert(0, str(Path(__file__).parent))
from profiling import profiler_dataset
from scoring import calculer_score_global, CONFIG_ENTITE
from validation import valider_dataset, REGLES_PAR_ENTITE


EMOJIS_NIVEAU = {
    "EXCELLENT": "Excellent",
    "BON": "Bon",
    "ACCEPTABLE": "Acceptable",
    "INSUFFISANT": "Insuffisant",
}

COULEUR_NIVEAU = {
    "EXCELLENT": ">= 95",
    "BON": ">= 85",
    "ACCEPTABLE": ">= 70",
    "INSUFFISANT": "< 70",
}


def lire_csv(chemin: str) -> list[dict]:
    with open(chemin, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def generer_rapport_complet(chemin: str, entite: str) -> str:
    """Génère un rapport qualité Markdown complet."""
    lignes = lire_csv(chemin)
    nb_lignes = len(lignes)

    # Calculs
    print("  [1/3] Profiling du dataset...")
    profil = profiler_dataset(chemin)

    print("  [2/3] Calcul du score qualité...")
    resultat_score = calculer_score_global(lignes, entite)

    print("  [3/3] Validation des règles métier...")
    violations = valider_dataset(lignes, entite)

    # Construction du rapport
    now = datetime.now()
    rapport = []

    # -----------------------------------------------------------------------
    # En-tête
    # -----------------------------------------------------------------------
    rapport.extend([
        f"# Rapport Qualité des Données",
        f"",
        f"**Entité analysée :** {entite.upper()}  ",
        f"**Fichier source :** `{chemin}`  ",
        f"**Date du rapport :** {now.strftime('%Y-%m-%d à %H:%M:%S')}  ",
        f"**Référentiel :** DAMA-DMBOK / ISO 8000  ",
        f"**Cadre :** Gouvernance des Données — Afrique centrale",
        f"",
        f"---",
        f"",
    ])

    # -----------------------------------------------------------------------
    # Synthèse exécutive
    # -----------------------------------------------------------------------
    score = resultat_score["score_global"]
    niveau = resultat_score["niveau"]
    nb_viol_critiques = sum(1 for v in violations if v["severite"] == "critique")
    nb_viol_importantes = sum(1 for v in violations if v["severite"] == "important")
    nb_viol_avertissements = sum(1 for v in violations if v["severite"] == "avertissement")

    rapport.extend([
        f"## 1. Synthèse Exécutive",
        f"",
        f"| Indicateur | Valeur | Statut |",
        f"|-----------|--------|--------|",
        f"| **Score qualité global** | **{score:.1f} / 100** | **{EMOJIS_NIVEAU[niveau]}** |",
        f"| Enregistrements analysés | {nb_lignes:,} | — |",
        f"| Violations critiques | {nb_viol_critiques} | {'OK' if nb_viol_critiques == 0 else 'ACTION REQUISE'} |",
        f"| Violations importantes | {nb_viol_importantes} | {'OK' if nb_viol_importantes == 0 else 'AVERTISSEMENT'} |",
        f"| Avertissements | {nb_viol_avertissements} | — |",
        f"| Doublons exacts | {profil['nb_doublons_exacts']} | {'OK' if profil['nb_doublons_exacts'] == 0 else 'A CORRIGER'} |",
        f"",
    ])

    # Conclusion exécutive
    if score >= 95:
        conclusion = (
            f"Les données de l'entité **{entite}** présentent un niveau de qualité **excellent** ({score:.1f}/100). "
            f"Elles sont certifiées prêtes pour tous les usages critiques, y compris les rapports réglementaires et les décisions stratégiques."
        )
    elif score >= 85:
        conclusion = (
            f"Les données de l'entité **{entite}** présentent un niveau de qualité **bon** ({score:.1f}/100). "
            f"Des améliorations ciblées sont recommandées sur les dimensions les moins performantes. "
            f"L'usage pour les rapports décisionnels est autorisé avec les réserves mentionnées."
        )
    elif score >= 70:
        conclusion = (
            f"Les données de l'entité **{entite}** présentent un niveau de qualité **acceptable** ({score:.1f}/100) "
            f"mais nécessitent un plan d'action qualité. Les usages critiques sont **limités** jusqu'à correction. "
            f"Voir les recommandations en section 5."
        )
    else:
        conclusion = (
            f"**ALERTE** : Les données de l'entité **{entite}** présentent un niveau de qualité **insuffisant** ({score:.1f}/100). "
            f"Les usages critiques sont **suspendus** jusqu'à correction complète. "
            f"Une action correctrice urgente est requise — voir section 5."
        )

    rapport.extend([
        f"**Conclusion :** {conclusion}",
        f"",
        f"---",
        f"",
    ])

    # -----------------------------------------------------------------------
    # Score par dimension
    # -----------------------------------------------------------------------
    rapport.extend([
        f"## 2. Score par Dimension de Qualité",
        f"",
        f"| Dimension | Score | Poids | Contribution | Niveau |",
        f"|-----------|-------|-------|--------------|--------|",
    ])

    for dim, data in resultat_score["dimensions"].items():
        contribution = data["score"] * data["poids"]
        niv_dim = "Excellent" if data["score"] >= 95 else ("Bon" if data["score"] >= 85 else ("Acceptable" if data["score"] >= 70 else "Insuffisant"))
        rapport.append(
            f"| {dim.capitalize()} | {data['score']:.1f}% | {data['poids']*100:.0f}% | {contribution:.1f} | {niv_dim} |"
        )

    rapport.extend([
        f"| **Score global** | | **100%** | **{score:.1f}** | **{EMOJIS_NIVEAU[niveau]}** |",
        f"",
        f"### Détails par dimension",
        f"",
    ])

    descriptions_dimensions = {
        "completude": "Taux de renseignement des champs obligatoires",
        "exactitude": "Correspondance des données avec la réalité (plausibilité)",
        "coherence": "Absence de contradictions intra et inter-enregistrements",
        "actualite": "Fraîcheur des données par rapport au délai de mise à jour requis",
        "unicite": "Absence de doublons sur les champs clés d'identification",
        "validite": "Conformité aux formats, listes de valeurs et contraintes définies",
    }

    for dim, data in resultat_score["dimensions"].items():
        rapport.extend([
            f"#### {dim.capitalize()}",
            f"",
            f"*{descriptions_dimensions[dim]}*",
            f"",
            f"**Score :** {data['score']:.1f}%",
            f"",
        ])
        if data["detail"] and not isinstance(data["detail"], dict) or (isinstance(data["detail"], dict) and data["detail"]):
            if isinstance(data["detail"], dict):
                for k, v in data["detail"].items():
                    if k != "note":
                        rapport.append(f"- `{k}` : {v}")
                if "note" in data["detail"]:
                    rapport.append(f"- *Note : {data['detail']['note']}*")
        rapport.append(f"")

    rapport.extend([
        f"---",
        f"",
    ])

    # -----------------------------------------------------------------------
    # Profil du dataset
    # -----------------------------------------------------------------------
    rapport.extend([
        f"## 3. Profil du Dataset",
        f"",
        f"| Attribut | Valeur |",
        f"|---------|--------|",
        f"| Nombre de lignes | {profil['nb_lignes']:,} |",
        f"| Nombre de colonnes | {profil['nb_colonnes']} |",
        f"| Doublons exacts | {profil['nb_doublons_exacts']} |",
        f"| Taux d'unicité lignes | {profil['taux_unicite_lignes_pct']}% |",
        f"| Complétude globale (tous champs) | {profil['taux_completude_global_pct']}% |",
        f"",
        f"### Profil des colonnes",
        f"",
        f"| Colonne | Type | Complétude | Distincts | Top valeur |",
        f"|---------|------|------------|-----------|------------|",
    ])

    for nom, col in profil["colonnes"].items():
        top = col["top_valeurs"][0][0] if col["top_valeurs"] else "—"
        if len(str(top)) > 20:
            top = str(top)[:20] + "..."
        rapport.append(
            f"| `{nom}` | {col['type_detecte']} | {col['taux_completude_pct']}% | {col['nb_distincts']} | `{top}` |"
        )

    rapport.extend([
        f"",
        f"---",
        f"",
    ])

    # -----------------------------------------------------------------------
    # Violations détectées
    # -----------------------------------------------------------------------
    rapport.extend([
        f"## 4. Violations Détectées",
        f"",
        f"**Total violations : {len(violations)}** "
        f"({nb_viol_critiques} critiques, {nb_viol_importantes} importantes, {nb_viol_avertissements} avertissements)",
        f"",
    ])

    if not violations:
        rapport.append(f"Aucune violation détectée. Le dataset respecte toutes les règles de qualité définies.")
    else:
        # Par sévérité
        for sev in ["critique", "important", "avertissement"]:
            viol_sev = [v for v in violations if v["severite"] == sev]
            if not viol_sev:
                continue

            rapport.extend([
                f"### Violations {sev.capitalize()} ({len(viol_sev)})",
                f"",
                f"| Règle | Champ | Occurrences | Description |",
                f"|-------|-------|-------------|-------------|",
            ])

            # Regrouper par règle
            par_regle = {}
            for v in viol_sev:
                cle = (v["regle_id"], v["champ"], v["description"])
                par_regle[cle] = par_regle.get(cle, 0) + 1

            for (rid, champ, desc), cnt in sorted(par_regle.items(), key=lambda x: -x[1]):
                desc_court = desc[:60] + "..." if len(desc) > 60 else desc
                rapport.append(f"| `{rid}` | `{champ}` | {cnt} | {desc_court} |")

            rapport.append(f"")

        # Exemples détaillés
        rapport.extend([
            f"### Exemples de violations (10 premières)",
            f"",
            f"| Ligne | Règle | Champ | Valeur | Sévérité |",
            f"|-------|-------|-------|--------|----------|",
        ])
        for v in violations[:10]:
            valeur_court = str(v["valeur"])[:30]
            rapport.append(
                f"| {v['numero_ligne']} | `{v['regle_id']}` | `{v['champ']}` | `{valeur_court}` | {v['severite']} |"
            )

    rapport.extend([
        f"",
        f"---",
        f"",
    ])

    # -----------------------------------------------------------------------
    # Recommandations
    # -----------------------------------------------------------------------
    rapport.extend([
        f"## 5. Recommandations",
        f"",
        f"### 5.1 Actions prioritaires",
        f"",
    ])

    actions = []

    if nb_viol_critiques > 0:
        actions.append(
            f"1. **URGENT — Corriger les {nb_viol_critiques} violations critiques** "
            f"avant tout usage des données en production. "
            f"Ces violations compromettent l'intégrité fondamentale du dataset."
        )

    if profil["nb_doublons_exacts"] > 0:
        actions.append(
            f"2. **Déduplication** — {profil['nb_doublons_exacts']} doublons exacts détectés. "
            f"Exécuter `deduplication.py` pour une analyse approfondie et la construction du golden record."
        )

    # Dimensions faibles
    for dim, data in resultat_score["dimensions"].items():
        if data["score"] < 70:
            actions.append(
                f"3. **Dimension {dim}** ({data['score']:.1f}%) — Niveau insuffisant. "
                f"Action corrective immédiate requise."
            )
        elif data["score"] < 85:
            actions.append(
                f"4. **Dimension {dim}** ({data['score']:.1f}%) — Amélioration recommandée pour atteindre l'objectif de 85%."
            )

    # Champs avec faible complétude
    for nom, col in profil["colonnes"].items():
        if col["taux_completude_pct"] < 80:
            actions.append(
                f"5. **Complétude `{nom}`** ({col['taux_completude_pct']}%) — "
                f"Mettre en place une validation obligatoire à la saisie."
            )

    if not actions:
        actions.append("Aucune action prioritaire. Maintenir le niveau actuel et surveiller les indicateurs mensuellement.")

    for action in actions:
        rapport.append(action)
        rapport.append("")

    rapport.extend([
        f"### 5.2 Plan d'action qualité",
        f"",
        f"| Action | Responsable | Délai | Priorité |",
        f"|--------|-------------|-------|----------|",
    ])

    if nb_viol_critiques > 0:
        rapport.append(f"| Correction des violations critiques | Data Steward + Data Engineer | 48h | Urgente |")
    if profil["nb_doublons_exacts"] > 0:
        rapport.append(f"| Campagne de déduplication | Data Engineer MDM | 1 semaine | Haute |")

    for dim, data in resultat_score["dimensions"].items():
        if data["score"] < 85:
            rapport.append(f"| Amélioration dimension {dim} | Data Steward | 1 mois | Moyenne |")

    rapport.extend([
        f"",
        f"### 5.3 Surveillance continue",
        f"",
        f"- Recalculer le score qualité **mensuellement** avec ce script",
        f"- Configurer des **alertes automatiques** si le score descend sous 80/100",
        f"- Intégrer ces contrôles dans les **pipelines ETL** (voir `validation.py`)",
        f"- Publier le score qualité dans le **catalogue de données**",
        f"",
        f"---",
        f"",
        f"## 6. Informations Techniques",
        f"",
        f"| Paramètre | Valeur |",
        f"|-----------|--------|",
        f"| Script | rapport_qualite.py |",
        f"| Version référentiel | DAMA-DMBOK v2, ISO 8000 |",
        f"| Poids complétude | 25% |",
        f"| Poids exactitude | 25% |",
        f"| Poids cohérence | 20% |",
        f"| Poids actualité | 15% |",
        f"| Poids unicité | 10% |",
        f"| Poids validité | 5% |",
        f"",
        f"---",
        f"",
        f"*Rapport généré automatiquement par le Cadre de Gouvernance des Données*  ",
        f"*Organisation : [Nom de l'Organisation] — Brazzaville, Congo*",
    ])

    return "\n".join(rapport)


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Génération d'un rapport qualité complet en Markdown")
    parser.add_argument("--input", "-i", required=True, help="Chemin du fichier CSV à analyser")
    parser.add_argument("--entite", "-e", required=True,
                        choices=list(CONFIG_ENTITE.keys()),
                        help=f"Entité : {list(CONFIG_ENTITE.keys())}")
    parser.add_argument("--output", "-o", help="Chemin du rapport de sortie .md")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Erreur : fichier introuvable : {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Génération du rapport qualité pour : {args.input} (entité : {args.entite})")
    print("Étapes :")

    rapport = generer_rapport_complet(args.input, args.entite)

    if args.output:
        Path(args.output).write_text(rapport, encoding="utf-8")
        print(f"\nRapport sauvegardé : {args.output}")
    else:
        print(rapport)

    print(f"\nRapport qualité généré avec succès.")


if __name__ == "__main__":
    main()
