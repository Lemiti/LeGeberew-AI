# 🌱 Geberena AI (LeGeberew AI)
**AI-Powered Agricultural Advisory & Market Linkage Platform for Ethiopian Farmers**

[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-brightgreen)](https://github.com/your-username/geberena-ai)
[![Framework: FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Framework: React+Vite](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=flat&logo=react)](https://vitejs.dev/)
[![AI: TensorFlow Lite](https://img.shields.io/badge/AI-TensorFlow%20Lite-FF6F00?style=flat&logo=tensorflow)](https://www.tensorflow.org/lite)

---

## 🚀 The Vision
Smallholder farmers form the backbone of Ethiopia's economy but face a "Triple Threat": **Information Gaps**, **Climate Vulnerability**, and **Market Inefficiency**. 

**Geberena AI** is a localized, mobile-first intelligence system that bridges these gaps using computer vision and real-time data to increase crop yield and farmer income.

## ✨ Key Features
*   **🩺 Digital Plant Doctor:** Instant diagnosis of coffee, maize, and potato diseases using a lightweight AI model. Provides expert treatment advice in **Amharic**.
*   **📊 Intelligent Market Connect:** Real-time price transparency across major Ethiopian hubs (Addis Ababa, Adama, Jimma, etc.) to bypass exploitative middlemen.
*   **☁️ Smart Farming Alerts:** Personalized irrigation and planting guidance based on localized weather patterns.
![](https://github.com/Lemiti/LeGeberew-AI/blob/main/imgs/home.jpg)
> *Home page of the app*
## 🧠 Model Performance
Our AI engine utilizes **Transfer Learning** with a **MobileNetV2** architecture, optimized for mobile deployment via TensorFlow Lite.

*   **Accuracy:** Achieved **~94.5% Validation Accuracy**.
*   **Loss:** Successfully converged to **<0.18 Validation Loss** over 10 epochs.
*   **Optimization:** The model is compressed to `.tflite` format for sub-second inference on standard hardware.
![](https://github.com/Lemiti/LeGeberew-AI/blob/main/imgs/training_curve.png)
> *The training curves show a healthy learning rate and high generalization capabilities for Ethiopian crop varieties.*

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React.js (Vite), Tailwind CSS, Lucide-React |
| **Backend** | Python, FastAPI (Asynchronous API) |
| **AI/ML** | TensorFlow, MobileNetV2, Kaggle GPU (Tesla T4) |
| **Database** | SQLite & Structured JSON Knowledge Base |
| **Communication** | RESTful API with Axios |

## 📁 Project Structure
```text
geberena-ai/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── routes/         # Modular API Endpoints (AI, Market, Weather)
│   │   ├── services/       # Core Logic (AI Inference, Data processing)
│   │   └── data/           # Amharic Knowledge Base & Mock Data
│   ├── ml_models/          # Trained .tflite models
│   └── requirements.txt
├── frontend/               # React + Vite Application
│   ├── src/
│   │   ├── api/            # Axios instance configuration
│   │   ├── pages/          # Plant Doctor, Market, Home screens
│   │   └── components/     # Reusable UI elements
│   └── tailwind.config.js  # Mobile-first styling config
└── README.md
```
## ⚙️ Installation & Setup
### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --port 5000 --reload
```
### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
## 🗺️ Roadmap
- [ ] Phase 1: Real-time satellite soil moisture integration.
- [ ] Phase 2: Voice-based advisory (Amharic Text-to-Speech) for low-literacy accessibility.
- [ ] Phase 3: Offline AI inference (On-device TFLite deployment).
---
## Developed with ❤️ for the Ethiopian Agricultural Community.

