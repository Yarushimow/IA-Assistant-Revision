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
    section = "Introduction"
    lignes = []
    dans_code = False
    for ligne in fiche["text"].splitlines():
        if ligne.startswith("```"):
            dans_code = not dans_code
        if ligne.startswith("#") and not dans_code:
            texte = "\n".join(lignes).strip()
            if len(texte) >= 50:
                for morceau in decouper_texte(texte, max_chars):
                    passages.append({"source": fiche["source"], "section": section, "text": morceau})
            section = ligne.lstrip("#").strip()
            lignes = []
        else:
            lignes.append(ligne)
    texte = "\n".join(lignes).strip()
    if len(texte) >= 50:
        for morceau in decouper_texte(texte, max_chars):
            passages.append({"source": fiche["source"], "section": section, "text": morceau})
    return passages 

def decouper_texte(texte: str, max_chars: int) -> list[str]:
    """Regroupe les paragraphes en morceaux de max_chars caractères maximum."""
    paragraphes = texte.split("\n\n")          # couper sur les lignes vides
    morceaux = []
    courant = ""                            # la boîte en cours
    for para in paragraphes:
        # +2 pour le "\n\n" qu'on remettra entre les deux
        if courant and len(courant) + len(para) + 2 > max_chars:
            morceaux.append(courant.strip())   # on ferme la boîte
            courant = para                     # nouvelle boîte avec ce paragraphe
        else:
            courant = courant + "\n\n" + para  # on ajoute à la boîte
    if courant.strip():
        morceaux.append(courant.strip())                    # la dernière boîte
    return morceaux


if __name__ == "__main__":
    fiches = load_fiches()
    print(f"{len(fiches)} fiches chargées")
    chunks = [c for f in fiches for c in chunk_fiche(f)]
    print(f"{len(chunks)} passages")
    print(chunks[0])

