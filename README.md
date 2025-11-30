# 🌍 KM-Agent FP Multi-Secteurs (MVP)

![Status](https://img.shields.io/badge/Status-MVP%20Complete-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![LangChain](https://img.shields.io/badge/LangChain-0.1-orange)
![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-purple)

**KM-Agent** est un agent IA conversationnel, modulaire et multi-secteurs conçu pour fournir une assistance technique, un diagnostic et une formation professionnelle en Afrique.

Ce MVP cible initialement quatre secteurs prioritaires : **Énergie Solaire**, **Mécanique**, **AgriTech** et **Construction**.

---

## 🚀 Fonctionnalités Clés

### 🧠 1. Intelligence Multi-Secteurs
- **Routage Intelligent** : Analyse la requête utilisateur pour identifier le secteur (Solaire, Mécanique, etc.) et activer les outils appropriés.
- **Architecture Modulaire** : Facilement extensible à de nouveaux secteurs (Santé, Éducation) sans modifier le cœur de l'agent.

### 📚 2. RAG (Retrieval-Augmented Generation)
- **Base de Connaissances Locale** : Utilise ChromaDB pour stocker et récupérer des manuels techniques, normes de sécurité et guides de maintenance.
- **Réponses Contextuelles** : L'IA répond en se basant *uniquement* sur les documents vérifiés, réduisant les hallucinations.

### 💬 3. Mémoire Conversationnelle
- **Suivi de Contexte** : L'agent se souvient des échanges précédents (via `session_id`) pour une conversation fluide et naturelle.

### 📸 4. Capacités Multimodales
- **Analyse d'Images** : Les utilisateurs peuvent envoyer des photos (panneaux solaires, pièces moteur) pour un diagnostic visuel instantané par Gemini Pro Vision.

### 🌍 5. Support Multilingue
- **Adaptabilité** : Conçu pour comprendre et répondre dans la langue de l'utilisateur (Français, Anglais, et structure prête pour les langues locales).

---

## 🛠️ Architecture Technique

- **Backend** : FastAPI (Python)
- **Orchestration** : LangChain
- **LLM** : Google Gemini 1.5 Flash (via `langchain-google-genai`)
- **Vector DB** : ChromaDB (Local)
- **Simulation** : Moteur de scénarios JSON pour la formation.

---

## 📦 Installation & Démarrage

### Pré-requis
- Python 3.10+
- Une clé API Google AI Studio

### 1. Cloner le projet
```bash
git clone https://github.com/AIGeniusDeveloper/km_agent.git
cd km_agent
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration
Créez un fichier `.env` à la racine :
```env
GOOGLE_API_KEY=votre_clé_api_ici
```

### 4. Ingérer les données (RAG)
Chargez les manuels techniques dans la base vectorielle :
```bash
python -m app.rag.ingest
```

### 5. Lancer le serveur
```bash
python main.py
```
L'API sera accessible sur `http://localhost:8000`.

---

## 🔌 Utilisation de l'API

Documentation Swagger complète disponible sur : `http://localhost:8000/docs`

### Endpoint Principal : `/chat`

**Requête (JSON) :**
```json
{
  "query": "Mon panneau solaire ne charge pas, voici une photo.",
  "session_id": "user_123",
  "image_base64": "<chaine_base64_de_l_image>"
}
```

**Réponse :**
```json
{
  "response": "D'après l'image, le panneau semble couvert de poussière...",
  "sector": "solar",
  "confidence": 1.0,
  "context": [...]
}
```

---

## 🗺️ Roadmap

- [x] **Phase 1** : Architecture Core & Routage (Fait)
- [x] **Phase 2** : RAG Solaire & Mécanique (Fait)
- [x] **Phase 3** : Simulateur de Tâches (Fait)
- [x] **Phase 4** : Mémoire & Multimodal (Fait)
- [ ] **Phase 5** : Support AgriTech & BTP
- [ ] **Phase 6** : Interface Vocale (ASR/TTS)
- [ ] **Phase 7** : Déploiement Cloud

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou une Pull Request pour discuter des changements majeurs.

---

**Développé avec ❤️ pour l'autonomisation technique en Afrique.**
