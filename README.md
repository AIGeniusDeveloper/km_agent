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

### 🧠 1. Intelligence Multi-Secteurs (4 Secteurs)
- **Routage Intelligent** : Analyse la requête utilisateur pour identifier le secteur approprié.
- **Secteurs Supportés** :
  - ⚡ **Énergie Solaire** : Installation, maintenance, diagnostic
  - 🔧 **Mécanique** : Moteurs diesel, maintenance préventive
  - 🌾 **AgriTech** : Analyse des sols, maladies des cultures, fertilisation
  - 🏗️ **ConstructionTech** : Matériaux, fondations, normes de sécurité

### 📚 2. RAG (Retrieval-Augmented Generation)
- **Base de Connaissances** : ChromaDB avec 4 secteurs documentés
- **Réponses Contextuelles** : L'IA répond en se basant *uniquement* sur les documents vérifiés

### 💬 3. Mémoire Conversationnelle
- **Suivi de Contexte** : L'agent se souvient des échanges précédents via `session_id`

### 📸 4. Capacités Multimodales
- **Analyse d'Images** : Diagnostic visuel instantané (panneaux solaires, pièces moteur, cultures, chantiers)

### 🎤 5. Interface Vocale (ASR/TTS)
- **Speech-to-Text** : Transcription audio en texte
- **Text-to-Speech** : Réponses audio synthétisées
- **Voice Chat** : Interaction vocale complète

### 🌍 6. Support Multilingue
- **Adaptabilité** : Répond dans la langue de l'utilisateur (Français, Anglais)

---

## 🏗️ Architecture Modulaire

L'architecture de KM-Agent V2 est conçue pour **faciliter le remplacement** des services tiers sans casser le code :

### Remplacement du LLM (Gemini → Claude/OpenAI/Mistral)
- **Point d'entrée unique** : `app/core/llm_factory.py`
- Modifiez uniquement la factory, tous les composants s'adaptent automatiquement
- Support multi-LLM possible (ex: Gemini pour routing, Claude pour génération)

### Remplacement Voice (Google Cloud → Whisper/ElevenLabs)
- **Abstraction** : `app/api/voice.py`
- Fonctions ASR/TTS isolées, API REST inchangée
- Le frontend reste compatible

### Remplacement Vector DB (ChromaDB → Pinecone/Weaviate)
- **Interface** : `app/rag/retriever.py`
- Méthodes `retrieve()` et `add_documents()` standardisées
- `AgentCore` ne voit aucune différence

**Principe** : Dependency Injection + Abstraction = Flexibilité maximale

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

### V1 (MVP) - ✅ Complete
- [x] Architecture Core & Routage
- [x] RAG Solaire & Mécanique
- [x] Simulateur de Tâches
- [x] Mémoire & Multimodal

### V2 - ✅ Complete
- [x] **Refactoring**: Dependency Injection, Error Handling, Tests (58% coverage)
- [x] **AgriTech Support**: Sols, cultures, maladies
- [x] **ConstructionTech Support**: BTP, matériaux, sécurité
- [x] **Voice Interface**: ASR/TTS endpoints

### V3 - Planned
- [ ] Production Google Cloud Speech integration
- [ ] Redis for session management
- [ ] LangSmith observability
- [ ] Docker deployment
- [ ] CI/CD pipeline

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou une Pull Request pour discuter des changements majeurs.

---

**Développé avec ❤️ pour l'autonomisation technique en Afrique.**
