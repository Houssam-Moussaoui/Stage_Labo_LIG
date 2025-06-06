import pickle

# Ton objet Python
data = {"nom": "Moussaoui", "note": 18, "tags": ["AI", "LLM", "RAG"]}

# 🔽 Sauvegarder dans un fichier
with open("mon_fichier.pkl", "wb") as f:
    pickle.dump(data, f)

# 🔼 Recharger plus tard
with open("mon_fichier.pkl", "rb") as f:
    reloaded_data = pickle.load(f)

print(reloaded_data)
# 👉 {'nom': 'Moussaoui', 'note': 18, 'tags': ['AI', 'LLM', 'RAG']}
