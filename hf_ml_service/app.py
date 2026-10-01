import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MODEL_NAME = "dhruv-ai-05/HireMind-AI-Model"


# ---------------------------------------------------------
# FastAPI
# ---------------------------------------------------------

app = FastAPI(
    title="HireMind AI - ML Service",
    description="ML inference service for HireMind AI ATS Resume Analyzer",
    version="1.0.0",
)


# ---------------------------------------------------------
# Load model once when the service starts
# ---------------------------------------------------------

print(f"Loading Sentence Transformer: {MODEL_NAME}")

model = SentenceTransformer(MODEL_NAME)

print("Sentence Transformer loaded successfully.")
print(f"Embedding dimension: {model.get_embedding_dimension()}")


# ---------------------------------------------------------
# Request schema
# ---------------------------------------------------------

class SemanticSimilarityRequest(BaseModel):
    resume_text: str
    job_description: str


# ---------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------

@app.get("/")
async def root():
    return {
        "service": "HireMind AI ML Service",
        "status": "running",
        "model": MODEL_NAME,
        "model_loaded": model is not None,
        "embedding_dimension": model.get_embedding_dimension(),
    }


# ---------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model": MODEL_NAME,
    }


# ---------------------------------------------------------
# Semantic similarity endpoint
# ---------------------------------------------------------

@app.post("/predict")
async def predict(request: SemanticSimilarityRequest):

    resume_text = request.resume_text.strip()
    job_description = request.job_description.strip()

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="resume_text cannot be empty",
        )

    if not job_description:
        raise HTTPException(
            status_code=400,
            detail="job_description cannot be empty",
        )

    try:

        # Keep this consistent with the existing ATS implementation.
        resume_embedding = model.encode(
            resume_text[:5000],
            convert_to_tensor=False,
        )

        jd_embedding = model.encode(
            job_description[:5000],
            convert_to_tensor=False,
        )

        resume_norm = np.linalg.norm(resume_embedding)
        jd_norm = np.linalg.norm(jd_embedding)

        if resume_norm == 0 or jd_norm == 0:
            similarity = 0.0

        else:
            similarity = np.dot(
                resume_embedding,
                jd_embedding,
            ) / (
                resume_norm * jd_norm
            )

        similarity = float(
            np.clip(similarity, 0.0, 1.0)
        )

        return {
            "semantic_similarity": similarity,
        }

    except Exception as e:

        print(f"Prediction error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to calculate semantic similarity",
        )