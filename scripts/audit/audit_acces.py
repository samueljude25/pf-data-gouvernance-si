"""
Simulation et analyse des logs d'audit des accès aux données.

Génère des logs d'accès simulés et produit des rapports d'audit
pour la conformité et la détection d'anomalies.

Usage :
    python audit_acces.py --generer --nb-logs 500 --output logs_acces.csv
    python audit_acces.py --analyser --input logs_acces.csv
    python audit_acces.py --generer --analyser --nb-logs 200

Cadre de Gouvernance des Données — DAMA-DMBOK / ISO 8000
Conformité : Loi n° 29-2019 Congo, RGPD-like
"""

import argparse
import csv
import random
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path


# ---------------------------------------------------------------------------
# Données de référence pour la simulation
# ---------------------------------------------------------------------------

UTILISATEURS = [
    {"id": "USR001", "nom": "MOUYABI Jean", "role": "Data Analyst", "departement": "Commercial"},
    {"id": "USR002", "nom": "NGUESSO Marie", "role": "Data Steward", "departement": "Gouvernance"},
    {"id": "USR003", "nom": "BAKALA Pierre", "role": "Responsable RH", "departement": "RH"},
    {"id": "USR004", "nom": "LOEMBA Claire", "role": "Directeur Financier", "departement": "Finance"},
    {"id": "USR005", "nom": "MAKOUMBOU Henri", "role": "Data Engineer", "departement": "DSI"},
    {"id": "USR006", "nom": "NZABA Sophie", "role": "Commercial terrain", "departement": "Commercial"},
    {"id": "USR007", "nom": "KIMBEMBE David", "role": "Administrateur BDD", "departement": "DSI"},
    {"id": "USR008", "nom": "TATY Françoise", "role": "Comptable", "departement": "Finance"},
    {"id": "USR009", "nom": "MASSAMBA Robert", "role": "Data Owner", "departement": "Commercial"},
    {"id": "USR010", "nom": "NKOUKA Théodore", "role": "Prestataire externe", "departement": "EXTERNE"},
]

RESSOURCES = [
    {"nom": "t_client_maitre", "classification": "CONFIDENTIEL", "domaine": "Commercial"},
    {"nom": "t_transaction", "classification": "CONFIDENTIEL", "domaine": "Finance"},
    {"nom": "t_employe", "classification": "CONFIDENTIEL", "domaine": "RH"},
    {"nom": "t_salaire", "classification": "CONFIDENTIEL", "domaine": "Finance"},
    {"nom": "ref_produit", "classification": "INTERNE", "domaine": "Commercial"},
    {"nom": "ref_geographie", "classification": "PUBLIC", "domaine": "Referentiel"},
    {"nom": "rapport_ca_mensuel", "classification": "INTERNE", "domaine": "Finance"},
    {"nom": "t_patient", "classification": "CONFIDENTIEL", "domaine": "Santé"},
    {"nom": "dossier_disciplinaire", "classification": "CONFIDENTIEL", "domaine": "RH"},
    {"nom": "cles_chiffrement", "classification": "SECRET", "domaine": "Sécurité"},
]

ACTIONS = ["SELECT", "INSERT", "UPDATE", "DELETE", "EXPORT", "PRINT", "SHARE"]
RESULTATS = ["SUCCES", "ECHEC_DROITS", "ECHEC_TECHNIQUE", "SUCCES_ALERTE"]
IP_INTERNES = [f"192.168.1.{i}" for i in range(1, 50)]
IP_EXTERNES = [f"41.203.{random.randint(1,254)}.{random.randint(1,254)}" for _ in range(10)]


# ---------------------------------------------------------------------------
# Génération de logs simulés
# ---------------------------------------------------------------------------

def generer_log(
    date_debut: datetime,
    date_fin: datetime,
    inclure_anomalies: bool = True,
) -> dict:
    """Génère un événement de log d'accès aléatoire."""
    utilisateur = random.choice(UTILISATEURS)
    ressource = random.choice(RESSOURCES)

    # Définir les actions probables selon le rôle
    actions_role = {
        "Data Analyst": ["SELECT", "EXPORT"],
        "Data Steward": ["SELECT", "UPDATE", "INSERT"],
        "Responsable RH": ["SELECT", "UPDATE"],
        "Directeur Financier": ["SELECT"],
        "Data Engineer": ["SELECT", "INSERT", "UPDATE", "DELETE"],
        "Commercial terrain": ["SELECT"],
        "Administrateur BDD": ["SELECT", "INSERT", "UPDATE", "DELETE"],
        "Comptable": ["SELECT", "INSERT"],
        "Data Owner": ["SELECT", "UPDATE"],
        "Prestataire externe": ["SELECT"],
    }
    actions_possibles = actions_role.get(utilisateur["role"], ["SELECT"])

    # Pondérer SELECT très fortement
    action = random.choices(
        ACTIONS,
        weights=[50, 10, 15, 5, 12, 5, 3],
        k=1
    )[0]

    # Résultat : généralement succès, parfois échec
    if utilisateur["role"] == "Prestataire externe" and ressource["classification"] in ("CONFIDENTIEL", "SECRET"):
        resultat = random.choice(["ECHEC_DROITS", "ECHEC_DROITS", "ECHEC_TECHNIQUE"])
    else:
        resultat = random.choices(
            RESULTATS,
            weights=[85, 8, 5, 2],
            k=1
        )[0]

    # Date aléatoire dans la plage
    delta = date_fin - date_debut
    date_acces = date_debut + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

    # Heure de bureau (8h-18h) ou hors horaires (anomalie potentielle)
    est_heure_bureau = 8 <= date_acces.hour < 18

    # IP : interne ou externe
    est_ip_externe = utilisateur["departement"] == "EXTERNE" or random.random() < 0.05
    ip = random.choice(IP_EXTERNES if est_ip_externe else IP_INTERNES)

    # Nombre de lignes accédées
    if action == "SELECT":
        nb_lignes = random.choices([1, 10, 100, 1000, 10000], weights=[30, 30, 20, 15, 5])[0]
    elif action in ("INSERT", "UPDATE"):
        nb_lignes = random.choices([1, 5, 20], weights=[60, 30, 10])[0]
    else:
        nb_lignes = random.choice([1, 5, 10])

    # Durée de la session (secondes)
    duree = random.randint(1, 3600) if action == "SELECT" else random.randint(1, 60)

    log = {
        "date_acces": date_acces.strftime("%Y-%m-%d %H:%M:%S"),
        "id_utilisateur": utilisateur["id"],
        "nom_utilisateur": utilisateur["nom"],
        "role": utilisateur["role"],
        "departement": utilisateur["departement"],
        "ressource": ressource["nom"],
        "classification_ressource": ressource["classification"],
        "domaine_ressource": ressource["domaine"],
        "action": action,
        "resultat": resultat,
        "nb_lignes_accedees": nb_lignes,
        "duree_secondes": duree,
        "ip_source": ip,
        "est_ip_externe": str(est_ip_externe).upper(),
        "est_heure_bureau": str(est_heure_bureau).upper(),
        "session_id": f"SES-{random.randint(100000, 999999)}",
    }

    # Injection d'anomalies intentionnelles
    if inclure_anomalies and random.random() < 0.03:
        anomalie = random.choice([
            "acces_hors_horaires_ressource_confidentielle",
            "volume_export_anormal",
            "acces_secret_non_autorise",
            "echec_acces_repete",
        ])

        if anomalie == "acces_hors_horaires_ressource_confidentielle":
            log["date_acces"] = date_acces.replace(hour=2, minute=random.randint(0, 59)).strftime("%Y-%m-%d %H:%M:%S")
            log["classification_ressource"] = "CONFIDENTIEL"
            log["est_heure_bureau"] = "FALSE"
            log["_anomalie"] = anomalie
        elif anomalie == "volume_export_anormal":
            log["action"] = "EXPORT"
            log["nb_lignes_accedees"] = random.randint(50000, 200000)
            log["_anomalie"] = anomalie
        elif anomalie == "acces_secret_non_autorise":
            log["ressource"] = "cles_chiffrement"
            log["classification_ressource"] = "SECRET"
            log["resultat"] = "ECHEC_DROITS"
            log["_anomalie"] = anomalie
        elif anomalie == "echec_acces_repete":
            log["resultat"] = "ECHEC_DROITS"
            log["_anomalie"] = anomalie

    return log


def generer_logs(
    nb_logs: int,
    date_debut: datetime,
    date_fin: datetime,
) -> list[dict]:
    """Génère nb_logs événements de log simulés."""
    logs = []
    for _ in range(nb_logs):
        logs.append(generer_log(date_debut, date_fin))
    return sorted(logs, key=lambda l: l["date_acces"])


# ---------------------------------------------------------------------------
# Analyse des logs d'audit
# ---------------------------------------------------------------------------

def analyser_logs(logs: list[dict]) -> dict:
    """Analyse complète des logs d'accès et détection d'anomalies."""

    total = len(logs)
    if total == 0:
        return {"erreur": "Aucun log à analyser"}

    # Statistiques globales
    par_action = Counter(l["action"] for l in logs)
    par_resultat = Counter(l["resultat"] for l in logs)
    par_utilisateur = Counter(l["id_utilisateur"] for l in logs)
    par_ressource = Counter(l["ressource"] for l in logs)
    par_classification = Counter(l["classification_ressource"] for l in logs)

    # Anomalies détectées
    anomalies = []

    # 1. Accès hors horaires sur ressources CONFIDENTIEL/SECRET
    hors_horaires_sensibles = [
        l for l in logs
        if l.get("est_heure_bureau", "TRUE") == "FALSE"
        and l["classification_ressource"] in ("CONFIDENTIEL", "SECRET")
        and l["resultat"] == "SUCCES"
    ]
    if hors_horaires_sensibles:
        anomalies.append({
            "type": "Accès hors horaires sur données sensibles",
            "nombre": len(hors_horaires_sensibles),
            "severite": "ELEVEE",
            "exemples": [
                f"{l['nom_utilisateur']} → {l['ressource']} à {l['date_acces']}"
                for l in hors_horaires_sensibles[:3]
            ],
        })

    # 2. Volumes d'export anormaux (> 10 000 lignes)
    exports_massifs = [
        l for l in logs
        if l["action"] == "EXPORT" and int(l.get("nb_lignes_accedees", 0)) > 10000
    ]
    if exports_massifs:
        anomalies.append({
            "type": "Export massif de données",
            "nombre": len(exports_massifs),
            "severite": "ELEVEE",
            "exemples": [
                f"{l['nom_utilisateur']} → {l['nb_lignes_accedees']} lignes depuis {l['ressource']}"
                for l in exports_massifs[:3]
            ],
        })

    # 3. Tentatives répétées d'accès refusé (> 5 pour un même utilisateur)
    echecs_par_user = Counter(
        l["id_utilisateur"] for l in logs if l["resultat"] == "ECHEC_DROITS"
    )
    utilisateurs_echecs_repetes = {u: c for u, c in echecs_par_user.items() if c >= 3}
    if utilisateurs_echecs_repetes:
        anomalies.append({
            "type": "Tentatives répétées d'accès refusé",
            "nombre": len(utilisateurs_echecs_repetes),
            "severite": "MOYENNE",
            "detail": dict(utilisateurs_echecs_repetes),
        })

    # 4. Accès depuis IP externe sur données CONFIDENTIEL
    acces_externe_sensible = [
        l for l in logs
        if l.get("est_ip_externe", "FALSE") == "TRUE"
        and l["classification_ressource"] in ("CONFIDENTIEL", "SECRET")
        and l["resultat"] == "SUCCES"
    ]
    if acces_externe_sensible:
        anomalies.append({
            "type": "Accès distant sur données confidentielles",
            "nombre": len(acces_externe_sensible),
            "severite": "MOYENNE",
            "exemples": [
                f"{l['nom_utilisateur']} ({l['ip_source']}) → {l['ressource']}"
                for l in acces_externe_sensible[:3]
            ],
        })

    # 5. Actions DELETE sur données CONFIDENTIEL
    deletions_sensibles = [
        l for l in logs
        if l["action"] == "DELETE"
        and l["classification_ressource"] in ("CONFIDENTIEL", "SECRET")
    ]
    if deletions_sensibles:
        anomalies.append({
            "type": "Suppressions sur données sensibles",
            "nombre": len(deletions_sensibles),
            "severite": "ELEVEE",
            "exemples": [
                f"{l['nom_utilisateur']} → DELETE sur {l['ressource']}"
                for l in deletions_sensibles[:3]
            ],
        })

    # Métriques de conformité
    nb_succes = par_resultat.get("SUCCES", 0) + par_resultat.get("SUCCES_ALERTE", 0)
    nb_echecs = par_resultat.get("ECHEC_DROITS", 0)
    nb_erreurs_techniques = par_resultat.get("ECHEC_TECHNIQUE", 0)

    return {
        "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "periode": {
            "debut": min(l["date_acces"] for l in logs),
            "fin": max(l["date_acces"] for l in logs),
        },
        "statistiques": {
            "total_evenements": total,
            "nb_succes": nb_succes,
            "nb_echecs_droits": nb_echecs,
            "nb_erreurs_techniques": nb_erreurs_techniques,
            "taux_succes_pct": round(nb_succes / total * 100, 2),
            "par_action": dict(par_action.most_common()),
            "par_classification": dict(par_classification.most_common()),
            "top_utilisateurs": dict(par_utilisateur.most_common(5)),
            "top_ressources": dict(par_ressource.most_common(5)),
        },
        "anomalies": anomalies,
        "nb_anomalies_detectees": len(anomalies),
        "niveau_risque": "ELEVE" if any(a["severite"] == "ELEVEE" for a in anomalies)
                        else ("MOYEN" if anomalies else "FAIBLE"),
    }


# ---------------------------------------------------------------------------
# Rapport d'audit Markdown
# ---------------------------------------------------------------------------

def generer_rapport_audit(analyse: dict) -> str:
    """Génère un rapport d'audit en Markdown."""
    lines = [
        f"# Rapport d'Audit des Accès aux Données",
        f"",
        f"**Date du rapport :** {analyse['date_analyse']}  ",
        f"**Période analysée :** {analyse['periode']['debut']} → {analyse['periode']['fin']}  ",
        f"**Niveau de risque global :** **{analyse['niveau_risque']}**",
        f"",
        f"---",
        f"",
        f"## 1. Synthèse",
        f"",
        f"| Indicateur | Valeur |",
        f"|-----------|--------|",
        f"| Total événements | {analyse['statistiques']['total_evenements']:,} |",
        f"| Taux de succès | {analyse['statistiques']['taux_succes_pct']}% |",
        f"| Accès refusés | {analyse['statistiques']['nb_echecs_droits']} |",
        f"| Erreurs techniques | {analyse['statistiques']['nb_erreurs_techniques']} |",
        f"| Anomalies détectées | **{analyse['nb_anomalies_detectees']}** |",
        f"| Niveau de risque | **{analyse['niveau_risque']}** |",
        f"",
    ]

    if analyse["anomalies"]:
        lines.extend([
            f"## 2. Anomalies Détectées",
            f"",
        ])
        for anomalie in analyse["anomalies"]:
            lines.extend([
                f"### {anomalie['type']} — Sévérité : {anomalie['severite']}",
                f"",
                f"**Nombre d'occurrences :** {anomalie['nombre']}",
                f"",
            ])
            if "exemples" in anomalie:
                lines.append(f"**Exemples :**")
                for ex in anomalie["exemples"]:
                    lines.append(f"- {ex}")
                lines.append(f"")
            if "detail" in anomalie:
                lines.append(f"**Détail :** {anomalie['detail']}")
                lines.append(f"")
    else:
        lines.extend([
            f"## 2. Anomalies",
            f"",
            f"Aucune anomalie significative détectée sur la période analysée.",
            f"",
        ])

    lines.extend([
        f"## 3. Distribution des Accès",
        f"",
        f"### Par action",
        f"",
        f"| Action | Occurrences |",
        f"|--------|-------------|",
    ])
    for action, cnt in analyse["statistiques"]["par_action"].items():
        lines.append(f"| {action} | {cnt} |")

    lines.extend([
        f"",
        f"### Par classification des ressources",
        f"",
        f"| Classification | Accès |",
        f"|---------------|-------|",
    ])
    for classif, cnt in analyse["statistiques"]["par_classification"].items():
        lines.append(f"| {classif} | {cnt} |")

    lines.extend([
        f"",
        f"### Utilisateurs les plus actifs",
        f"",
        f"| Utilisateur | Nombre d'accès |",
        f"|------------|----------------|",
    ])
    for user, cnt in analyse["statistiques"]["top_utilisateurs"].items():
        lines.append(f"| {user} | {cnt} |")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## 4. Recommandations",
        f"",
    ])

    if analyse["niveau_risque"] == "ELEVE":
        lines.extend([
            f"**Actions urgentes requises :**",
            f"",
            f"1. Investiguer immédiatement les anomalies de sévérité ELEVEE",
            f"2. Notifier le Data Owner et le CDO",
            f"3. Suspendre les accès suspects le temps de l'investigation",
            f"4. Documenter l'incident dans le registre des violations",
        ])
    elif analyse["niveau_risque"] == "MOYEN":
        lines.extend([
            f"**Actions recommandées :**",
            f"",
            f"1. Revoir les accès concernés par les anomalies détectées",
            f"2. Renforcer les contrôles sur les ressources sensibles",
            f"3. Sensibiliser les utilisateurs concernés",
        ])
    else:
        lines.extend([
            f"**Situation normale :**",
            f"",
            f"Maintenir la surveillance et recalculer ce rapport mensuellement.",
        ])

    lines.extend([
        f"",
        f"---",
        f"*Rapport généré automatiquement — Cadre de Gouvernance des Données*",
    ])

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Point d'entrée
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Génération et analyse des logs d'audit des accès")
    parser.add_argument("--generer", action="store_true", help="Générer des logs simulés")
    parser.add_argument("--analyser", action="store_true", help="Analyser les logs")
    parser.add_argument("--input", "-i", help="Fichier CSV de logs à analyser")
    parser.add_argument("--output", "-o", help="Fichier CSV de sortie pour les logs générés")
    parser.add_argument("--rapport", "-r", help="Fichier Markdown pour le rapport d'audit")
    parser.add_argument("--nb-logs", "-n", type=int, default=200, help="Nombre de logs à générer (défaut : 200)")
    parser.add_argument("--jours", "-j", type=int, default=30, help="Nombre de jours couverts (défaut : 30)")
    args = parser.parse_args()

    logs = []

    if args.generer:
        date_fin = datetime.now()
        date_debut = date_fin - timedelta(days=args.jours)
        print(f"Génération de {args.nb_logs} logs d'accès simulés...")
        logs = generer_logs(args.nb_logs, date_debut, date_fin)
        print(f"  {len(logs)} logs générés.")

        if args.output:
            tous_champs = set()
            for l in logs:
                tous_champs.update(l.keys())
            champs_sans_meta = [c for c in tous_champs if not c.startswith("_")]
            entetes = sorted(champs_sans_meta)

            with open(args.output, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=entetes, extrasaction="ignore")
                writer.writeheader()
                writer.writerows(logs)
            print(f"  Logs exportés : {args.output}")

    if args.analyser:
        if args.input and not logs:
            if not Path(args.input).exists():
                print(f"Erreur : fichier introuvable : {args.input}")
                return
            with open(args.input, encoding="utf-8", newline="") as f:
                logs = list(csv.DictReader(f))
            print(f"Lecture de {len(logs)} logs depuis {args.input}")

        if not logs:
            print("Erreur : aucun log à analyser. Utilisez --generer ou --input.")
            return

        print(f"Analyse de {len(logs)} événements...")
        analyse = analyser_logs(logs)

        print(f"\n{'='*55}")
        print(f"RAPPORT D'AUDIT — {analyse['niveau_risque']}")
        print(f"{'='*55}")
        print(f"Période : {analyse['periode']['debut']} → {analyse['periode']['fin']}")
        print(f"Événements : {analyse['statistiques']['total_evenements']:,}")
        print(f"Taux succès : {analyse['statistiques']['taux_succes_pct']}%")
        print(f"Anomalies  : {analyse['nb_anomalies_detectees']}")
        print(f"{'='*55}")

        for anomalie in analyse["anomalies"]:
            print(f"\nANOMALIE [{anomalie['severite']}] : {anomalie['type']}")
            print(f"  Occurrences : {anomalie['nombre']}")
            if "exemples" in anomalie:
                for ex in anomalie["exemples"]:
                    print(f"  → {ex}")

        if args.rapport:
            rapport = generer_rapport_audit(analyse)
            Path(args.rapport).write_text(rapport, encoding="utf-8")
            print(f"\nRapport d'audit sauvegardé : {args.rapport}")

    if not args.generer and not args.analyser:
        parser.print_help()


if __name__ == "__main__":
    main()
