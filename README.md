# 🎫 End-to-End LLMOps: Intelligent Support Triage

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg?logo=docker)](https://www.docker.com/)
[![Gemini 2.5 Flash](https://img.shields.io/badge/AI-Google_Gemini_2.5_Flash-orange.svg)](https://deepmind.google/technologies/gemini/)

An enterprise-grade, microservices-based AI support automation platform that intelligently classifies customer support tickets, detects urgency levels, generates AI-powered draft responses, and provides real-time operational observability.

Built with a strong emphasis on **LLMOps**, **Site Reliability Engineering (SRE)**, and **cloud-native distributed systems**, this project demonstrates production-grade backend engineering, automated CI/CD, resilient database handling, and real-time telemetry monitoring.

<img width="1918" height="907" alt="image" src="https://github.com/user-attachments/assets/360cce54-58bf-4bb5-8830-341b9cd20e54" />

---

<img width="1910" height="911" alt="image" src="https://github.com/user-attachments/assets/36ccf585-e5c6-4c1e-977a-5a44c15a5fce" />


---

# 🚀 Key Features

### 🧠 AI-Powered Ticket Classification
- Uses **Google Gemini 2.5 Flash** for intelligent support ticket triage
- Automatically identifies:
  - Ticket category
  - Urgency level
  - Confidence score
  - AI-generated draft response
- Enforces deterministic structured outputs using advanced prompt engineering and strict JSON parsing

---

### 🏗️ Distributed Microservices Architecture
- Fully decoupled:
  - Streamlit Frontend
  - FastAPI Backend
  - AI Inference Layer
  - Monitoring Stack
- Services communicate securely through Docker container networking

---

### 🛡️ Fault-Tolerant Database Design
- Primary cloud persistence using **MongoDB Atlas**
- Automatic fallback to **SQLite** during cloud/database outages
- Prevents customer ticket loss during downtime

---

### 📈 Real-Time Monitoring & Observability
- Integrated **Prometheus** for application telemetry collection
- Visualized live metrics through **Grafana dashboards**
- Tracks:
  - API latency
  - HTTP request throughput
  - Traffic spikes
  - System performance metrics

---

### ⚡ Intelligent Priority Detection
- Automatically detects high-priority customer issues using LLM-based urgency classification
- Prioritizes critical tickets for faster response handling
- Generates structured AI summaries for efficient support workflows

---

### ⚙️ DevOps & CI/CD Automation
- Dockerized infrastructure for reproducible deployments
- Automated testing using **GitHub Actions**
- Zero-downtime cloud deployments via **Render**

---

# 🏗️ System Architecture

The application is designed as a production-ready distributed system with independent infrastructure layers.

```text
┌──────────────────────┐
│  Streamlit Frontend  │
└──────────┬───────────┘
           │ HTTP
           ▼
┌──────────────────────┐
│   FastAPI Backend    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Gemini 2.5 Flash API │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ MongoDB Atlas (DB)   │
└──────────┬───────────┘
           │ Fallback
           ▼
┌──────────────────────┐
│ SQLite Local Storage │
└──────────────────────┘
```

---

# 🛠️ Technology Stack

| Component | Technologies Used |
| :--- | :--- |
| **Backend API** | Python, FastAPI, Pydantic, Uvicorn |
| **Frontend UI** | Streamlit, Plotly |
| **Artificial Intelligence** | Google Gemini 2.5 Flash (`google-generativeai`) |
| **Databases** | MongoDB Atlas, SQLite3 |
| **DevOps & Orchestration** | Docker, Docker Compose |
| **CI/CD Pipeline** | GitHub Actions, Render |
| **Monitoring & Observability** | Prometheus, Grafana |
| **Testing** | PyTest |

---

# 📁 Project Structure

```text
ticket-classifier-devops/
├── .github/workflows/
│   └── ci_cd.yml
├── dashboard/
│   └── app.py
├── src/
│   ├── api.py
│   ├── storage.py
│   ├── llm_engine.py
│   └── tests/
├── prometheus/
│   └── prometheus.yml
├── grafana/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

# 💻 Local Execution & Testing

This project is fully containerized using Docker.

## Prerequisites

- Docker Desktop
- Gemini API Key
- MongoDB Atlas URI

---

## Step 1: Clone Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

## Step 2: Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_google_api_key
MONGODB_URI=your_mongodb_connection_string
```

---

## Step 3: Launch the Infrastructure

```bash
docker-compose up --build
```

This launches:
- FastAPI Backend
- Streamlit Dashboard
- Prometheus
- Grafana

---

# 🌐 Access the Services

| Service | URL |
| :--- | :--- |
| Streamlit Frontend | http://localhost:8501 |
| FastAPI Swagger Docs | http://localhost:8000/docs |
| Prometheus Targets | http://localhost:9090 |
| Grafana Dashboard | http://localhost:3000 |

### Default Grafana Credentials

```text
Username: admin
Password: admin
```

---

# 📈 Observability & Monitoring

Prometheus continuously scrapes FastAPI metrics while Grafana visualizes telemetry in real time.

### Example PromQL Query

```promql
rate(http_requests_total[1m])
```

Metrics available:
- Request rate
- API latency
- Error rates
- Traffic spikes
- System throughput

---

# 🔄 CI/CD Pipeline Workflow

The repository includes a fully automated CI/CD workflow.

## Continuous Integration (CI)

Triggered automatically on:
- Push to `main`
- Pull requests

GitHub Actions:
- Installs dependencies
- Runs PyTest suites
- Validates API schemas
- Prevents broken deployments

---

## Continuous Deployment (CD)

After successful CI validation:
- Render automatically pulls the latest build
- Deploys updated containers
- Ensures zero-downtime production updates

---

# 🧪 Example AI Output

```json
{
  "category": "Technical Issue",
  "urgency": "High",
  "confidence_score": 0.96,
  "draft_response": "We are actively investigating your issue and will resolve it as quickly as possible."
}
```

---

# 📊 Engineering Highlights

- Enterprise-Grade LLMOps Pipeline
- Distributed Microservices Architecture
- Fault-Tolerant Cloud-Native Design
- Automated CI/CD Deployment
- Real-Time Monitoring & Telemetry
- AI-Driven Customer Support Automation
- Production-Ready DevOps Workflow
- Intelligent AI-Based Ticket Prioritization

---

# 🚀 Future Improvements

- Kubernetes deployment
- Kafka/RabbitMQ event streaming
- Role-based authentication
- Multi-tenant SaaS architecture
- RAG-based ticket enrichment
- Vector database integration
- Horizontal autoscaling

---




# 🌟 Why This Project Stands Out

Most AI projects simply connect a frontend directly to an LLM API.

This project demonstrates how real-world AI systems are engineered in production environments with:
- Resilience
- Observability
- Automation
- Scalability
- Reliability
- Cloud-native infrastructure

It showcases practical expertise in:
- LLMOps
- Backend Engineering
- DevOps
- Distributed Systems
- SRE Principles
- Production Monitoring
