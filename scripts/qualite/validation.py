"""
Validation des règles de qualité sur un dataset CSV.

Applique les règles définies dans config/regles_validation.yaml
et retourne les violations détectées.

Usage :
    python validation.py --input data/samples/dataset_brut.csv --entite client
    python validation.py --input data/samples/dataset_brut.csv --entite transaction --output violations.csv

Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000
"""

import argparse
import csv
import re
import sys
from datetime import date, datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Règles de validation intégrées (version simplifiée sans dépendance YAML)
# Ces règles reflètent le contenu de config/regles_validation.yaml
# ---------------------------------------------------------------------------

REGLES_PAR_ENTITE = {
    "client": [
        {
            "id": "CLI-001",
            "champ": "id_client",
            "type": "format",
            "pattern": r"^CLI-\d{6}$",
            "description": "Identifiant client au format CLI-XXXXXX",
            "severite": "critique",
        },
        {
            "id": "CLI-002",
            "champ": "nom",
            "type": "non_vide",
            "description": "Le nom ne peut pas être vide",
            "severite": "critique",
        },
        {
            "id": "CLI-004",
            "champ": "prenom",
            "type": "non_vide",
            "description": "Le prénom ne peut pas être vide",
            "severite": "critique",
        },
        {
            "id": "CLI-005",
            "champ": "date_naissance",
            "type": "date_passee",
            "description": "La date de naissance doit être dans le passé",
            "severite": "critique",
            "obligatoire": False,
        },
        {
            "id": "CLI-006",
            "champ": "date_naissance",
            "type": "age_minimum",
            "age_min": 18,
            "description": "Le client doit avoir au moins 18 ans",
            "severite": "avertissement",
            "obligatoire": False,
        },
        {
            "id": "CLI-007",
            "champ": "date_naissance",
            "type": "age_maximum",
            "age_max": 120,
            "description": "L'âge ne peut pas dépasser 120 ans",
            "severite": "critique",
            "obligatoire": False,
        },
        {
            "id": "CLI-008",
            "champ": "telephone",
            "type": "format",
            "pattern": r"^(\+242)?0?[456]\d{7}$",
            "description": "Numéro de téléphone Congo : 0[456]XXXXXXX ou +242[456]XXXXXXX",
            "severite": "important",
        },
        {
            "id": "CLI-009",
            "champ": "telephone",
            "type": "non_vide",
            "description": "Le téléphone ne peut pas être vide",
            "severite": "important",
        },
        {
            "id": "CLI-010",
            "champ": "email",
            "type": "format",
            "pattern": r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$",
            "description": "Format email invalide",
            "severite": "important",
            "obligatoire": False,
        },
        {
            "id": "CLI-011",
            "champ": "departement",
            "type": "liste_valeurs",
            "valeurs": [
                "Brazzaville", "Pointe-Noire", "Bouenza", "Cuvette",
                "Cuvette-Ouest", "Kouilou", "Lékoumou", "Likouala",
                "Niari", "Plateaux", "Pool", "Sangha",
            ],
            "description": "Département doit appartenir aux 12 départements du Congo",
            "severite": "important",
        },
        {
            "id": "CLI-012",
            "champ": "type_client",
            "type": "liste_valeurs",
            "valeurs": ["Particulier", "Entreprise", "Administration", "ONG"],
            "description": "Type client invalide",
            "severite": "important",
        },
    ],
    "transaction": [
        {
            "id": "TXN-001",
            "champ": "id_transaction",
            "type": "format",
            "pattern": r"^TXN-\d{4}-\d{8}$",
            "description": "Identifiant transaction au format TXN-AAAA-NNNNNNNN",
            "severite": "critique",
        },
        {
            "id": "TXN-003",
            "champ": "montant",
            "type": "valeur_positive",
            "description": "Le montant doit être positif",
            "severite": "critique",
        },
        {
            "id": "TXN-006",
            "champ": "devise",
            "type": "liste_valeurs",
            "valeurs": ["XAF", "EUR", "USD", "GBP"],
            "description": "Devise non reconnue",
            "severite": "critique",
        },
        {
            "id": "TXN-007",
            "champ": "date_transaction",
            "type": "date_passee",
            "description": "La date de transaction doit être dans le passé",
            "severite": "critique",
        },
        {
            "id": "TXN-009",
            "champ": "type_transaction",
            "type": "liste_valeurs",
            "valeurs": ["VENTE", "REMBOURSEMENT", "PAIEMENT", "TRANSFERT", "DEPOT", "RETRAIT", "FRAIS"],
            "description": "Type de transaction invalide",
            "severite": "critique",
        },
        {
            "id": "TXN-010",
            "champ": "statut",
            "type": "liste_valeurs",
            "valeurs": ["EN_ATTENTE", "VALIDEE", "REJETEE", "ANNULEE", "EN_COURS"],
            "description": "Statut de transaction invalide",
            "severite": "critique",
        },
    ],
    "produit": [
        {
            "id": "PRD-001",
            "champ": "id_produit",
            "type": "format",
            "pattern": r"^PRD-[A-Z]{3}-\d{4}$",
            "description": "Identifiant produit au format PRD-CAT-NNNN",
            "severite": "critique",
        },
        {
            "id": "PRD-002",
            "champ": "libelle",
            "type": "non_vide",
            "description": "Le libellé ne peut pas être vide",
            "severite": "critique",
        },
        {
            "id": "PRD-003",
            "champ": "categorie",
            "type": "liste_valeurs",
            "valeurs": [
                "Alimentaire", "Santé", "Électronique", "Textile",
                "BTP", "Services", "Agriculture", "Transport",
                "Éducation", "Énergie",
            ],
            "description": "Catégorie produit invalide",
            "severite": "important",
        },
        {
            "id": "PRD-004",
            "champ": "prix_unitaire",
            "type": "valeur_positive_ou_zero",
            "description": "Le prix unitaire doit être >= 0",
            "severite": "critique",
        },
    ],
}

VALEURS_VIDES = {"", "null", "none", "n/a", "na", "nd"}


def est_vide(valeur: str) -> bool:
    return valeur is None or str(valeur).strip().lower() in VALEURS_VIDES


def parser_date(valeur: str) -> date | None:
    """Tente de parser une date depuis plusieurs formats courants."""
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]
    valeur = valeur.strip()
    for fmt in formats:
        try:
            return datetime.strptime(valeur, fmt).date()
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Moteur de validation
# ---------------------------------------------------------------------------

def valider_regle(ligne: dict, regle: dict, numero_ligne: int) -> dict | None:
    """
    Applique une règle à un enregistrement.
    Retourne un dict de violation ou None si conforme.
    """
    champ = regle["champ"]
    valeur_brute = ligne.get(champ, "")
    valeur = str(valeur_brute).strip() if valeur_brute is not None else ""
    type_regle = regle["type"]
    obligatoire = regle.get("obligatoire", True)

    # Si vide et non obligatoire → pas de violation
    if est_vide(valeur) and not obligatoire:
        return None

    # Si vide et obligatoire → violation de complétude (sauf pour certaines règles)
    if est_vide(valeur) and obligatoire and type_regle not in ("non_vide",):
        return {
            "numero_ligne": numero_ligne,
            "regle_id": regle["id"],
            "champ": champ,
            "valeur": repr(valeur_brute),
            "description": f"Champ obligatoire manquant : {champ}",
            "severite": regle["severite"],
            "type_violation": "completude",
        }

    # --- Règle : non_vide ---
    if type_regle == "non_vide":
        if est_vide(valeur):
            return {
                "numero_ligne": numero_ligne,
                "regle_id": regle["id"],
                "champ": champ,
                "valeur": repr(valeur_brute),
                "description": regle["description"],
                "severite": regle["severite"],
                "type_violation": "completude",
            }
        return None

    # --- Règle : format (regex) ---
    if type_regle == "format":
        valeur_test = valeur.replace(" ", "")
        if not re.match(regle["pattern"], valeur_test):
            return {
                "numero_ligne": numero_ligne,
                "regle_id": regle["id"],
                "champ": champ,
                "valeur": repr(valeur),
                "description": regle["description"],
                "severite": regle["severite"],
                "type_violation": "validite",
            }
        return None

    # --- Règle : liste_valeurs ---
    if type_regle == "liste_valeurs":
        if valeur not in regle["valeurs"]:
            return {
                "numero_ligne": numero_ligne,
                "regle_id": regle["id"],
                "champ": champ,
                "valeur": repr(valeur),
                "description": f"{regle['description']} — valeur : '{valeur}'",
                "severite": regle["severite"],
                "type_violation": "validite",
            }
        return None

    # --- Règle : valeur_positive ---
    if type_regle == "valeur_positive":
        try:
            nb = float(valeur.replace(",", ".").replace(" ", ""))
            if nb <= 0:
                return {
                    "numero_ligne": numero_ligne,
                    "regle_id": regle["id"],
                    "champ": champ,
                    "valeur": valeur,
                    "description": regle["description"],
                    "severite": regle["severite"],
                    "type_violation": "validite",
                }
        except ValueError:
            return {
                "numero_ligne": numero_ligne,
                "regle_id": regle["id"],
                "champ": champ,
                "valeur": repr(valeur),
                "description": f"Valeur non numérique pour {champ}",
                "severite": regle["severite"],
                "type_violation": "validite",
            }
        return None

    # --- Règle : valeur_positive_ou_zero ---
    if type_regle == "valeur_positive_ou_zero":
        try:
            nb = float(valeur.replace(",", ".").replace(" ", ""))
            if nb < 0:
                return {
                    "numero_ligne": numero_ligne,
                    "regle_id": regle["id"],
                    "champ": champ,
                    "valeur": valeur,
                    "description": regle["description"],
                    "severite": regle["severite"],
                    "type_violation": "validite",
                }
        except ValueError:
            return {
                "numero_ligne": numero_ligne,
                "regle_id": regle["id"],
                "champ": champ,
                "valeur": repr(valeur),
                "description": f"Valeur non numérique pour {champ}",
                "severite": regle["severite"],
                "type_violation": "validite",
            }
        return None

    # --- Règle : date_passee ---
    if type_regle == "date_passee":
        d = parser_date(valeur)
        if d is None:
            return {
                "numero_ligne": numero_ligne,
                "regle_id": regle["id"],
                "champ": champ,
                "valeur": repr(valeur),
                "description": f"Format de date invalide pour {champ}",
                "severite": regle["severite"],
                "type_violation": "validite",
            }
        if d > date.today():
            return {
                "numero_ligne": numero_ligne,
                "regle_id": regle["id"],
                "champ": champ,
                "valeur": valeur,
                "description": regle["description"],
                "severite": regle["severite"],
                "type_violation": "validite",
            }
        return None

    # --- Règle : age_minimum ---
    if type_regle == "age_minimum":
        d = parser_date(valeur)
        if d:
            age = (date.today() - d).days // 365
            if age < regle["age_min"]:
                return {
                    "numero_ligne": numero_ligne,
                    "regle_id": regle["id"],
                    "champ": champ,
                    "valeur": valeur,
                    "description": f"{regle['description']} (âge calculé : {age} ans)",
                    "severite": regle["severite"],
                    "type_violation": "validite",
                }
        return None

    # --- Règle : age_maximum ---
    if type_regle == "age_maximum":
        d = parser_date(valeur)
        if d:
            age = (date.today() - d).days // 365
            if age > regle["age_max"]:
                return {
                    "numero_ligne": numero_ligne,
                    "regle_id": regle["id"],
                    "champ": champ,
                    "valeur": valeur,
                    "description": f"{regle['description']} (âge calculé : {age} ans)",
                    "severite": regle["severite"],
                    "type_violation": "validite",
                }
        return None

    return None


def valider_dataset(lignes: list[dict], entite: str) -> list[dict]:
    """
    Valide toutes les lignes du dataset pour une entité donnée.
    Retourne la liste de toutes les violations.
    """
    regles = REGLES_PAR_ENTITE.get(entite)
    if not regles:
        raise ValueError(f"Entité inconnue : '{entite}'. Entités disponibles : {list(REGLES_PAR_ENTITE.keys())}")

    violations = []
    for i, ligne in enumerate(lignes, start=2):  # 2 car ligne 1 = entête
        for regle in regles:
            violation = valider_regle(ligne, regle, i)
            if violation:
                violations.append(violation)

    return violations


# ---------------------------------------------------------------------------
# Affichage et export des résultats
# ---------------------------------------------------------------------------

def afficher_resume(violations: list[dict], nb_lignes: int, entite: str):
    """Affiche un résumé console des violations."""
    print(f"\n{'='*60}")
    print(f"RÉSULTAT DE VALIDATION — Entité : {entite.upper()}")
    print(f"{'='*60}")
    print(f"Lignes analysées   : {nb_lignes}")
    print(f"Total violations   : {len(violations)}")

    if not violations:
        print("Aucune violation détectée.")
        return

    # Par sévérité
    par_severite = {}
    for v in violations:
        s = v["severite"]
        par_severite[s] = par_severite.get(s, 0) + 1

    print(f"\nViolations par sévérité :")
    for sev in ["critique", "important", "avertissement"]:
        if sev in par_severite:
            print(f"  {sev:15s} : {par_severite[sev]}")

    # Par règle
    par_regle = {}
    for v in violations:
        rid = v["regle_id"]
        par_regle[rid] = par_regle.get(rid, 0) + 1

    print(f"\nTop règles violées :")
    for rid, cnt in sorted(par_regle.items(), key=lambda x: -x[1])[:10]:
        print(f"  {rid:10s} : {cnt} violations")

    # Exemples
    print(f"\nExemples de violations (5 premières) :")
    for v in violations[:5]:
        print(f"  Ligne {v['numero_ligne']:4d} | {v['regle_id']} | {v['champ']} = {v['valeur']}")
        print(f"           | {v['description']}")


def exporter_violations_csv(violations: list[dict], chemin_sortie: str):
    """Exporte les violations dans un fichier CSV."""
    if not violations:
        print(f"Aucune violation à exporter.")
        return

    entetes = ["numero_ligne", "regle_id", "champ", "valeur", "description", "severite", "type_violation"]
    with open(chemin_sortie, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=entetes)
        writer.writeheader()
        writer.writerows(violations)
    print(f"Violations exportées : {chemin_sortie} ({len(violations)} violations)")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Validation des règles de qualité sur un dataset CSV")
    parser.add_argument("--input", "-i", required=True, help="Chemin du fichier CSV à valider")
    parser.add_argument("--entite", "-e", required=True,
                        choices=list(REGLES_PAR_ENTITE.keys()),
                        help=f"Entité à valider : {list(REGLES_PAR_ENTITE.keys())}")
    parser.add_argument("--output", "-o", help="Chemin de sortie pour les violations (CSV)")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Erreur : fichier introuvable : {args.input}", file=sys.stderr)
        sys.exit(1)

    # Lire le CSV
    with open(args.input, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))

    print(f"Validation de {len(lignes)} enregistrements pour l'entité '{args.entite}'...")
    violations = valider_dataset(lignes, args.entite)
    afficher_resume(violations, len(lignes), args.entite)

    if args.output:
        exporter_violations_csv(violations, args.output)

    # Code de sortie : 0 si OK, 1 si violations critiques
    nb_critiques = sum(1 for v in violations if v["severite"] == "critique")
    if nb_critiques > 0:
        print(f"\n{nb_critiques} violations CRITIQUES détectées.")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
