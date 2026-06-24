"""
Détection et résolution des doublons par similarité.

Utilise le matching exact et l'algorithme de Jaro-Winkler (similarité fuzzy)
pour détecter les doublons même avec des variations d'orthographe.

Usage :
    python deduplication.py --input data/samples/dataset_brut.csv
    python deduplication.py --input data/samples/referentiel_clients.csv --seuil 0.85
    python deduplication.py --input data/samples/dataset_brut.csv --output clusters.csv

Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000
"""

import argparse
import csv
import re
import unicodedata
from pathlib import Path


# ---------------------------------------------------------------------------
# Normalisation des chaînes
# ---------------------------------------------------------------------------

def normaliser(valeur: str) -> str:
    """Normalise une chaîne : minuscules, sans accents, sans espaces superflus."""
    if not valeur:
        return ""
    # Supprimer les accents
    valeur = unicodedata.normalize("NFD", str(valeur))
    valeur = "".join(c for c in valeur if unicodedata.category(c) != "Mn")
    # Minuscules
    valeur = valeur.lower()
    # Supprimer caractères non alphanumériques (sauf espaces)
    valeur = re.sub(r"[^a-z0-9\s]", " ", valeur)
    # Normaliser les espaces
    valeur = " ".join(valeur.split())
    return valeur


def normaliser_telephone(tel: str) -> str:
    """Normalise un numéro de téléphone congolais."""
    tel = re.sub(r"[^\d+]", "", str(tel))
    # Supprimer le préfixe international +242 ou 00242
    tel = re.sub(r"^(\+242|00242)", "", tel)
    # Supprimer le 0 initial si présent (pour numéro local)
    if tel.startswith("0") and len(tel) == 9:
        tel = tel[1:]
    return tel


# ---------------------------------------------------------------------------
# Algorithme de similarité Jaro-Winkler
# ---------------------------------------------------------------------------

def jaro(s1: str, s2: str) -> float:
    """Calcule la similarité de Jaro entre deux chaînes."""
    if s1 == s2:
        return 1.0
    if not s1 or not s2:
        return 0.0

    len1, len2 = len(s1), len(s2)
    match_dist = max(len1, len2) // 2 - 1
    match_dist = max(0, match_dist)

    s1_matches = [False] * len1
    s2_matches = [False] * len2
    matches = 0
    transpositions = 0

    for i in range(len1):
        start = max(0, i - match_dist)
        end = min(i + match_dist + 1, len2)
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    jaro_sim = (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3
    return jaro_sim


def jaro_winkler(s1: str, s2: str, p: float = 0.1) -> float:
    """Calcule la similarité de Jaro-Winkler (favorise les préfixes communs)."""
    j = jaro(s1, s2)
    prefix = 0
    for i in range(min(4, len(s1), len(s2))):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break
    return j + prefix * p * (1 - j)


def similarite(s1: str, s2: str) -> float:
    """Calcule la similarité normalisée entre deux chaînes."""
    s1_norm = normaliser(s1)
    s2_norm = normaliser(s2)
    if not s1_norm and not s2_norm:
        return 1.0
    if not s1_norm or not s2_norm:
        return 0.0
    return jaro_winkler(s1_norm, s2_norm)


# ---------------------------------------------------------------------------
# Clés de blocage (blocking keys)
# Pour réduire le nombre de comparaisons O(n²)
# ---------------------------------------------------------------------------

def cle_blocage_client(enregistrement: dict) -> str:
    """
    Génère une clé de blocage pour regrouper les candidats doublons.
    Réduit les comparaisons en ne comparant que les enregistrements
    ayant la même clé de blocage.
    """
    nom = normaliser(enregistrement.get("nom", ""))
    prenom = normaliser(enregistrement.get("prenom", ""))
    tel = normaliser_telephone(enregistrement.get("telephone", ""))

    # Clé 1 : premières lettres du nom
    cle_nom = nom[:3] if len(nom) >= 3 else nom

    # Clé 2 : premières lettres du prénom
    cle_prenom = prenom[:2] if len(prenom) >= 2 else prenom

    # Clé 3 : 4 derniers chiffres du téléphone
    cle_tel = tel[-4:] if len(tel) >= 4 else tel

    return f"{cle_nom}_{cle_prenom}" if cle_nom or cle_prenom else f"tel_{cle_tel}"


# ---------------------------------------------------------------------------
# Calcul du score de similarité entre deux enregistrements
# ---------------------------------------------------------------------------

def score_paire(rec1: dict, rec2: dict) -> dict:
    """
    Calcule un score de similarité global entre deux enregistrements clients.
    Retourne le score et le détail par attribut.
    """
    scores = {}
    poids = {}

    # Nom (poids 35%)
    nom1 = normaliser(rec1.get("nom", ""))
    nom2 = normaliser(rec2.get("nom", ""))
    if nom1 and nom2:
        scores["nom"] = jaro_winkler(nom1, nom2)
        poids["nom"] = 0.35

    # Prénom (poids 25%)
    prenom1 = normaliser(rec1.get("prenom", ""))
    prenom2 = normaliser(rec2.get("prenom", ""))
    if prenom1 and prenom2:
        scores["prenom"] = jaro_winkler(prenom1, prenom2)
        poids["prenom"] = 0.25

    # Téléphone (poids 30%) — comparaison normalisée
    tel1 = normaliser_telephone(rec1.get("telephone", ""))
    tel2 = normaliser_telephone(rec2.get("telephone", ""))
    if tel1 and tel2:
        scores["telephone"] = 1.0 if tel1 == tel2 else jaro_winkler(tel1, tel2)
        poids["telephone"] = 0.30

    # Email (poids 10%) — comparaison exacte après normalisation
    email1 = str(rec1.get("email", "")).strip().lower()
    email2 = str(rec2.get("email", "")).strip().lower()
    if email1 and email2 and "@" in email1 and "@" in email2:
        scores["email"] = 1.0 if email1 == email2 else 0.0
        poids["email"] = 0.10

    if not scores:
        return {"score_global": 0.0, "detail": {}}

    total_poids = sum(poids.values())
    score_global = sum(scores[k] * poids[k] for k in scores) / total_poids

    return {
        "score_global": round(score_global, 4),
        "detail": {k: round(v, 4) for k, v in scores.items()},
    }


# ---------------------------------------------------------------------------
# Algorithme de déduplication
# ---------------------------------------------------------------------------

def detecter_doublons(lignes: list[dict], seuil: float = 0.85) -> list[dict]:
    """
    Détecte les paires de doublons potentiels.

    Args:
        lignes: liste d'enregistrements (dicts)
        seuil: seuil de similarité minimum pour considérer deux enregistrements comme doublons

    Returns:
        Liste de paires de doublons avec scores
    """
    paires_doublons = []

    # 1. Doublons exacts (sur champs clés)
    print("  Détection des doublons exacts...")
    par_telephone = {}
    for i, l in enumerate(lignes):
        tel = normaliser_telephone(l.get("telephone", ""))
        if tel and len(tel) >= 7:
            if tel not in par_telephone:
                par_telephone[tel] = []
            par_telephone[tel].append(i)

    for tel, indices in par_telephone.items():
        if len(indices) > 1:
            for j in range(len(indices)):
                for k in range(j + 1, len(indices)):
                    i1, i2 = indices[j], indices[k]
                    paires_doublons.append({
                        "index_1": i1,
                        "index_2": i2,
                        "type": "exact_telephone",
                        "score_global": 1.0,
                        "valeur_commune": tel,
                        "nom_1": lignes[i1].get("nom", ""),
                        "nom_2": lignes[i2].get("nom", ""),
                        "prenom_1": lignes[i1].get("prenom", ""),
                        "prenom_2": lignes[i2].get("prenom", ""),
                        "telephone_1": lignes[i1].get("telephone", ""),
                        "telephone_2": lignes[i2].get("telephone", ""),
                        "action_recommandee": "fusion",
                    })

    # 2. Doublons par similarité (fuzzy matching avec blocage)
    print(f"  Détection fuzzy (seuil={seuil}) avec blocking par nom...")

    # Indexer par clé de blocage
    blocs = {}
    for i, l in enumerate(lignes):
        cle = cle_blocage_client(l)
        if cle not in blocs:
            blocs[cle] = []
        blocs[cle].append(i)

    indices_deja_apparies = {(p["index_1"], p["index_2"]) for p in paires_doublons}
    comparaisons = 0

    for cle, indices in blocs.items():
        if len(indices) < 2:
            continue
        for j in range(len(indices)):
            for k in range(j + 1, len(indices)):
                i1, i2 = indices[j], indices[k]
                if (i1, i2) in indices_deja_apparies or (i2, i1) in indices_deja_apparies:
                    continue

                comparaisons += 1
                resultat = score_paire(lignes[i1], lignes[i2])
                score = resultat["score_global"]

                if score >= seuil:
                    paires_doublons.append({
                        "index_1": i1,
                        "index_2": i2,
                        "type": "fuzzy",
                        "score_global": score,
                        "detail": resultat["detail"],
                        "nom_1": lignes[i1].get("nom", ""),
                        "nom_2": lignes[i2].get("nom", ""),
                        "prenom_1": lignes[i1].get("prenom", ""),
                        "prenom_2": lignes[i2].get("prenom", ""),
                        "telephone_1": lignes[i1].get("telephone", ""),
                        "telephone_2": lignes[i2].get("telephone", ""),
                        "action_recommandee": "revision_manuelle" if score < 0.92 else "fusion",
                    })
                    indices_deja_apparies.add((i1, i2))

    print(f"  Comparaisons effectuées : {comparaisons}")
    return sorted(paires_doublons, key=lambda x: -x["score_global"])


def construire_clusters(paires: list[dict], nb_total: int) -> dict:
    """
    Regroupe les paires en clusters d'enregistrements liés.
    Utilise un algorithme Union-Find simplifié.
    """
    parent = list(range(nb_total))

    def trouver(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def unir(x, y):
        rx, ry = trouver(x), trouver(y)
        if rx != ry:
            parent[ry] = rx

    for paire in paires:
        if paire.get("action_recommandee") == "fusion":
            unir(paire["index_1"], paire["index_2"])

    clusters = {}
    for i in range(nb_total):
        racine = trouver(i)
        if racine not in clusters:
            clusters[racine] = []
        clusters[racine].append(i)

    return {k: v for k, v in clusters.items() if len(v) > 1}


# ---------------------------------------------------------------------------
# Rapport et export
# ---------------------------------------------------------------------------

def afficher_resume(paires: list[dict], clusters: dict, nb_lignes: int):
    """Affiche un résumé en console."""
    print(f"\n{'='*60}")
    print(f"RÉSULTATS DÉDUPLICATION")
    print(f"{'='*60}")
    print(f"Enregistrements analysés : {nb_lignes}")
    print(f"Paires de doublons       : {len(paires)}")
    print(f"  - Doublons exacts      : {sum(1 for p in paires if p['type'] == 'exact_telephone')}")
    print(f"  - Doublons fuzzy       : {sum(1 for p in paires if p['type'] == 'fuzzy')}")
    print(f"  - Action 'fusion'      : {sum(1 for p in paires if p.get('action_recommandee') == 'fusion')}")
    print(f"  - Révision manuelle    : {sum(1 for p in paires if p.get('action_recommandee') == 'revision_manuelle')}")
    print(f"Clusters de doublons     : {len(clusters)}")
    print(f"Enregistrements concernés: {sum(len(v) for v in clusters.values())}")
    print(f"{'='*60}")

    if paires:
        print(f"\nTop 5 paires de doublons :")
        for paire in paires[:5]:
            print(f"  Score {paire['score_global']:.3f} | "
                  f"{paire['nom_1']} {paire['prenom_1']} (tel:{paire['telephone_1']}) "
                  f"<-> {paire['nom_2']} {paire['prenom_2']} (tel:{paire['telephone_2']}) "
                  f"[{paire['type']}]")


def exporter_paires(paires: list[dict], chemin: str):
    """Exporte les paires de doublons en CSV."""
    if not paires:
        print("Aucun doublon à exporter.")
        return

    entetes = ["index_1", "index_2", "type", "score_global", "action_recommandee",
               "nom_1", "prenom_1", "telephone_1",
               "nom_2", "prenom_2", "telephone_2"]

    with open(chemin, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=entetes, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(paires)
    print(f"Paires exportées : {chemin} ({len(paires)} paires)")


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Détection des doublons par similarité")
    parser.add_argument("--input", "-i", required=True, help="Chemin du fichier CSV")
    parser.add_argument("--seuil", "-s", type=float, default=0.85,
                        help="Seuil de similarité Jaro-Winkler (0.0 à 1.0, défaut : 0.85)")
    parser.add_argument("--output", "-o", help="Fichier CSV de sortie pour les paires de doublons")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Erreur : fichier introuvable : {args.input}")
        return

    with open(args.input, encoding="utf-8", newline="") as f:
        lignes = list(csv.DictReader(f))

    print(f"Déduplication de {len(lignes)} enregistrements (seuil={args.seuil})...")
    paires = detecter_doublons(lignes, seuil=args.seuil)
    clusters = construire_clusters(paires, len(lignes))
    afficher_resume(paires, clusters, len(lignes))

    if args.output:
        exporter_paires(paires, args.output)


if __name__ == "__main__":
    main()
