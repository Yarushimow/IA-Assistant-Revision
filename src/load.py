"""Étape 1 : charger les fiches et les découper en passages (chunks)."""
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "fiches"

def load_fiches(data_dir: Path = DATA_DIR) -> list[dict]:
    """Renvoie une liste de {"source": nom_du_fichier, "text": contenu}."""
    fiches = []                                  # 1. la liste qu'on va remplir

    for fichier in data_dir.glob("*.md"):        # 2. pour chaque fichier .md du dossier
        contenu = fichier.read_text(encoding="utf-8")  # 3. lire le texte du fichier
        fiche = {"source": fichier.name, "text": contenu}     # 4. ranger nom + texte dans un dictionnaire
        fiches.append(fiche)                        # 5. ajouter ce dictionnaire à la liste

    return fiches                                   # 6. renvoyer la liste complète


def chunk_fiche(fiche: dict, max_chars: int = 800) -> list[dict]:
    """Découpe une fiche en passages, un par section (titre Markdown)."""
    passages = []
    section = "Introduction"     # titre de la section en cours
    lignes = []                  # lignes de la section en cours
    dans_code = False            # E. au départ, est-on dans un bloc de code ?

    for ligne in fiche["text"].splitlines():
        if ligne.startswith("```"):
            dans_code = not dans_code                    # F. basculer True <-> False

        if ligne.startswith("#") and not dans_code:      # G. un titre, seulement hors d'un bloc de code
            texte = "\n".join(lignes).strip()           # recoller la section précédente
            if len(texte) >= 50:                        # ignorer les sections presque vides
                passages.append({"source": fiche["source"], "section": section, "text": texte})
            section = ligne.lstrip("#").strip()         # le nouveau titre, sans les #
            lignes = []                                 # on repart de zéro
        else:
            lignes.append(ligne)                        # une ligne normale : on la garde

    # traiter la dernière section (aucun titre ne la suit)
    texte = "\n".join(lignes).strip()
    if len(texte) >= 50:
        passages.append({"source": fiche["source"], "section": section, "text": texte})

    return passages


if __name__ == "__main__":
    fiches = load_fiches()
    print(f"{len(fiches)} fiches chargées")
    chunks = [c for f in fiches for c in chunk_fiche(f)]
    print(f"{len(chunks)} passages")
    print(chunks[0])

