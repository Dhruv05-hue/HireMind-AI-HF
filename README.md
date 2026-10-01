# 🚀 HireMind AI — Hugging Face Integrated ATS Resume Analyzer

> An AI-powered Applicant Tracking System (ATS) that analyzes resumes, validates technical skills against project/experience evidence, compares resumes with job descriptions, and generates a comprehensive ATS score — while offloading heavy semantic ML inference to a private Hugging Face service.

---

## ✨ Overview

**HireMind AI** is a full-stack AI-powered resume analysis system designed to evaluate resumes using a combination of:

- 🧠 **spaCy NLP** for local resume parsing and text analysis
- 🔎 **Deterministic keyword and skill matching**
- 🤖 **Fine-tuned Sentence Transformer** for semantic similarity
- ☁️ **Hugging Face Spaces** for remote ML inference
- ⚡ **Batch semantic similarity** to reduce repeated network requests
- 📊 **Multi-component ATS scoring**
- 🎯 **Job Description matching**
- 🛡️ **Privacy/location detection**
- 📝 **Actionable resume feedback**
- 📄 **Resume file processing**

The main architectural goal of this version is to keep the FastAPI backend lightweight by moving the heavy Sentence Transformer model out of the backend runtime.

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │   Streamlit Frontend  │
                         │                      │
                         │ Resume Upload        │
                         │ Job Description      │
                         │ Results Dashboard    │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │   FastAPI Backend    │
                         │                      │
                         │ Resume Processing    │
                         │ spaCy NLP             │
                         │ Keyword Matching      │
                         │ ATS Scoring           │
                         │ PDF/DOCX Processing   │
                         └──────────┬───────────┘
                                    │
                                    │ Gradio Client
                                    ▼
                  ┌──────────────────────────────────┐
                  │   Hugging Face ML Service       │
                  │                                  │
                  │  Private Sentence Transformer   │
                  │  Fine-tuned MPNet Model         │
                  │  Single Similarity API           │
                  │  Batch Similarity API            │
                  └───────────────┬──────────────────┘
                                  │
                                  ▼
                       ┌────────────────────┐
                       │ Private HF Model   │
                       │ HireMind-AI-Model  │
                       │                    │
                       │ all-mpnet-base-v2  │
                       │ Fine-tuned for ATS │
                       └────────────────────┘
```

### Why this architecture?

The fine-tuned Sentence Transformer is relatively large compared with the lightweight FastAPI application. Instead of loading it directly inside the API server, semantic inference is delegated to Hugging Face.

This allows the backend to focus on:

- Resume parsing
- NLP processing
- deterministic matching
- scoring
- API orchestration

while Hugging Face handles:

- embedding generation
- semantic similarity
- GPU-backed inference

---

## 🧠 AI / ML Pipeline

The analysis pipeline follows this flow:

```text
Resume
  │
  ▼
File Extraction
  │
  ▼
Resume Parsing
  │
  ├── Experience
  ├── Education
  ├── Skills
  ├── Projects
  ├── Summary
  └── Keywords
  │
  ▼
Deterministic Analysis
  │
  ├── Keyword matching
  ├── Skill matching
  ├── Formatting analysis
  ├── Grammar analysis
  └── Privacy/location detection
  │
  ▼
Semantic Fallback
  │
  └── Hugging Face ML Service
          │
          └── Fine-tuned MPNet
  │
  ▼
JD Comparison
  │
  ├── Keyword overlap
  └── Semantic similarity
  │
  ▼
ATS Score
  │
  ├── Formatting
  ├── Keywords
  ├── Content
  ├── Skill validation
  └── ATS compatibility
  │
  ▼
Final Report
```

---

# 🤖 Machine Learning Model

The project uses a fine-tuned Sentence Transformer based on:

```text
all-mpnet-base-v2
```

The model was fine-tuned using resume/job-description semantic data with a cosine-similarity objective.

### Model characteristics

| Property | Value |
|---|---|
| Base Model | `all-mpnet-base-v2` |
| Embedding Dimension | 768 |
| Training Objective | Cosine Similarity |
| Fine-tuning Framework | Sentence Transformers |
| Deployment | Hugging Face |
| Model Visibility | Private |
| Inference | Hugging Face Space |

### Hugging Face Model

urlHireMind-AI-Modelhttps://huggingface.co/dhruv-ai-05/HireMind-AI-Model

The model repository is private and requires authentication through the Hugging Face Space secret.

---

# ☁️ Hugging Face ML Service

The semantic similarity model is exposed through a Gradio-based Hugging Face Space.

### Space

urlHireMind-AI-ML-Servicehttps://huggingface.co/spaces/dhruv-ai-05/HireMind-AI-ML-Service

The service exposes two inference operations:

### 1. Single Similarity

```text
/predict
```

Accepts:

```text
text_a
text_b
```

and returns:

```text
similarity
```

Example:

```text
Python machine learning engineer
        ↕
Python, machine learning and deep learning developer

Similarity: ~0.78
```

### 2. Batch Similarity

```text
/predict_batch
```

Accepts multiple text pairs in a single request.

Example:

```json
[
  {
    "text_a": "Python machine learning engineer",
    "text_b": "Python, machine learning and deep learning developer"
  },
  {
    "text_a": "React developer",
    "text_b": "Italian restaurant menu and cooking recipes"
  }
]
```

This approach significantly reduces the number of network requests during skill validation.

---

# ⚡ Batch Semantic Similarity

One of the important optimizations in this project is semantic batching.

### Before

A resume containing many skills could result in:

```text
Skill 1 → HF request
Skill 2 → HF request
Skill 3 → HF request
Skill 4 → HF request
...
Skill N → HF request
```

This introduced unnecessary network latency.

### Now

The backend collects semantic fallback candidates:

```text
Skill 1 ↔ Project
Skill 2 ↔ Project
Skill 3 ↔ Experience
Skill 4 ↔ Project
...
```

and sends them together:

```text
             ┌──────────────────┐
             │ Semantic Pairs    │
             │      Batch        │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Hugging Face     │
             │ ML Service       │
             └────────┬─────────┘
                      │
                      ▼
             Similarity Results
```

This keeps the semantic fallback architecture while reducing repeated client/server communication.

---

# 🎯 ATS Scoring

The final ATS score is composed of five major components:

| Component | Maximum |
|---|---:|
| Formatting | 20 |
| Keywords | 25 |
| Content | 25 |
| Skill Validation | 15 |
| ATS Compatibility | 15 |
| **Total** | **100** |

The scoring pipeline combines deterministic analysis, semantic skill validation, resume quality checks, and job-description matching.

The existing scoring formulas are intentionally preserved while the ML inference layer is moved to Hugging Face.

---

# 🔎 Job Description Matching

When a Job Description is provided, HireMind AI performs:

### Keyword matching

Identifies:

- matched keywords
- missing keywords
- skill gaps

### Semantic matching

The resume and job description are sent to the Hugging Face ML service.

The JD matching calculation combines:

```text
60% Keyword Overlap
+
40% Semantic Similarity
```

This provides both lexical and semantic signals rather than relying exclusively on embeddings.

---

# 🛠️ Technology Stack

## Frontend

- Streamlit

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- spaCy
- RapidFuzz

## AI / ML

- Sentence Transformers
- MPNet
- PyTorch
- Hugging Face Spaces
- Gradio
- Gradio Client

## Resume Processing

- pdfplumber
- PyPDF2
- python-docx
- python-magic

## Other

- Groq
- JWT
- Jinja2
- WeasyPrint
- python-dotenv

---

# 📁 Project Structure

```text
AI_ATS_HF_ML_Service/
│
├── backend/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── services/
│   │   ├── ats_scorer.py
│   │   ├── jd_matcher.py
│   │   ├── resume_analyzer.py
│   │   └── ...
│   │
│   ├── hf_ml_client.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   └── streamlit_app.py
│
├── hf_ml_service/
│   ├── app.py
│   ├── gradio_app.py
│   └── requirements.txt
│
├── models2/
│   └── finetuned-bert/
│
├── jupyter_notebook/
│
├── .env
├── .gitignore
└── README.md
```

---

# 🔐 Environment Variables

The backend uses environment variables for configuration and external services.

Example:

```env
HF_SPACE=dhruv-ai-05/HireMind-AI-ML-Service
```

The Hugging Face Space uses a private secret:

```env
HF_TOKEN=your_huggingface_read_token
```

> ⚠️ Never commit your Hugging Face token or other secrets to GitHub.

For local development, use `.env` and keep it inside `.gitignore`.

---

# 🚀 Local Setup

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AI_ATS_HF_ML_Service
```

---

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3. Install backend dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 4. Start FastAPI

From the project root:

```bash
python -m uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## 5. Start Streamlit

Open another terminal:

```bash
cd frontend
streamlit run streamlit_app.py
```

The frontend will normally be available at:

```text
http://localhost:8501
```

---

# 🧪 Testing

### Test ATS scorer import

```powershell
python -c "from backend.services.ats_scorer import validate_skills_with_projects; print('ats_scorer import OK')"
```

### Test batch semantic similarity

```powershell
python -c "from backend.hf_ml_client import calculate_batch_semantic_similarity; print(calculate_batch_semantic_similarity([('Python machine learning engineer','Python, machine learning and deep learning developer'),('React developer','Italian restaurant menu and cooking recipes')]))"
```

### Test skill validation

```powershell
python -c "from backend.services.ats_scorer import validate_skills_with_projects; r=validate_skills_with_projects(['Python','Machine Learning','React'],[{'title':'ML Project','description':'Built a machine learning model using Python and scikit-learn','technologies':['Python','scikit-learn']}],[]); print(r)"
```

---

# 🏥 API Health Check

The backend exposes:

```text
GET /api/v1/health
```

Expected response:

```json
{
  "status": "healthy",
  "nlp_loaded": true,
  "ml_service": "huggingface"
}
```

This confirms that:

- the FastAPI application is running
- the local spaCy model is loaded
- semantic ML is configured to use Hugging Face

---

# 🔄 Semantic Similarity Client

The backend communicates with Hugging Face through:

```text
backend/hf_ml_client.py
```

The client provides:

```python
calculate_semantic_similarity()
```

for individual comparisons and:

```python
calculate_batch_semantic_similarity()
```

for multiple comparisons.

The Hugging Face client is cached so repeated calls do not unnecessarily recreate the Gradio client.

---

# 🧩 Design Philosophy

The project deliberately separates **deterministic NLP** from **semantic ML**.

### Deterministic layer

Used for:

- exact skill matching
- normalized matching
- aliases
- plural variants
- keyword matching
- fuzzy matching
- score calculations
- formatting analysis
- privacy detection

### Semantic layer

Used when deterministic matching cannot establish sufficient evidence.

```text
Deterministic Match
       │
       ├── Match found ──────► Accept
       │
       └── No match
              │
              ▼
       Hugging Face Semantic
              │
              ▼
       Similarity Threshold
              │
        ┌─────┴─────┐
        ▼           ▼
      Match       No Match
```

This helps prevent semantic embeddings from unnecessarily creating false-positive skill matches.

---

# 🔒 Privacy & Security

The project follows a few important security principles:

- Hugging Face model repository is private.
- Hugging Face authentication uses a secret token.
- Secrets should never be committed to Git.
- `.env` should remain excluded from version control.
- Resume location information can be detected as a privacy risk.
- The semantic model is isolated from the main backend runtime.

---

# 🌐 Deployment Architecture

A production deployment can use:

```text
                    Internet
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       Streamlit App       FastAPI Backend
                                │
                                │
                                ▼
                     Hugging Face Space
                                │
                                ▼
                      Private HF Model
```

### Suggested responsibilities

**Frontend hosting**

```text
Streamlit
```

**API hosting**

```text
Render / similar Python hosting
```

**ML inference**

```text
Hugging Face Spaces
```

**Model storage**

```text
Private Hugging Face Model Repository
```

---

# 📈 Why Hugging Face Integration?

Running a large transformer directly inside the API server can increase:

- memory consumption
- deployment size
- startup time
- cold-start time
- dependency size

This architecture moves the transformer workload to a dedicated ML service.

The FastAPI backend therefore does not need to install or load:

```text
sentence-transformers
torch
```

for its own semantic inference.

Instead it uses:

```text
gradio_client
```

to communicate with the remote model service.

---

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

- FastAPI backend architecture
- Streamlit application development
- NLP pipelines
- Resume parsing
- ATS scoring
- semantic similarity
- Sentence Transformers
- model fine-tuning
- Hugging Face deployment
- Gradio APIs
- batch inference
- API-to-ML-service architecture
- private model repositories
- environment variables and secrets
- cloud deployment architecture
- performance optimization

---

# 🔮 Future Improvements

Potential future improvements include:

- [ ] Add authentication to the ML API layer
- [ ] Add request caching for repeated semantic comparisons
- [ ] Add batch-size controls
- [ ] Add inference monitoring
- [ ] Add model versioning
- [ ] Add automated ML service health checks
- [ ] Add async inference where appropriate
- [ ] Add more resume/job-description evaluation datasets
- [ ] Improve semantic similarity calibration
- [ ] Add automated deployment pipelines
- [ ] Add comprehensive unit and integration tests

---

# 👨‍💻 Author

**Dhruv Pawar**

AI/ML Developer | Computer Vision & NLP Enthusiast

Focused on building practical AI systems using:

```text
Python
Machine Learning
Deep Learning
Computer Vision
NLP
FastAPI
Streamlit
Hugging Face
```

---

## ⭐ Project Highlights

```text
🧠 Fine-tuned MPNet semantic model
☁️ Hugging Face ML inference
⚡ Batch semantic similarity
🔎 Resume ↔ JD matching
🎯 Skill validation
📊 100-point ATS scoring system
🛡️ Privacy detection
🚀 FastAPI + Streamlit architecture
🔐 Private model deployment
```

---

## 📜 License

Add your preferred license here before publishing the repository publicly.

---

> **HireMind AI** separates application logic from heavyweight ML inference, creating a cleaner architecture where the FastAPI service handles ATS intelligence and Hugging Face handles transformer-based semantic inference.
