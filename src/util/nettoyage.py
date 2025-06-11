import re


def nettoyer(text):
    # 1. Supprimer les tabulations et espaces superflus à gauche/droite
    lines = text.splitlines()
    cleaned_lines = [line.strip() for line in lines]

    # 2. Supprimer les lignes vides
    non_empty_lines = [line for line in cleaned_lines if line]

    # 3. Rejoindre les lignes avec un saut de ligne propre
    final_text = "\n".join(non_empty_lines)

    return final_text