import os
import json

import spaces
import torch
import gradio as gr
from sentence_transformers import SentenceTransformer


MODEL_NAME = "dhruv-ai-05/HireMind-AI-Model"
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN secret is not configured.")


model = SentenceTransformer(
    MODEL_NAME,
    token=HF_TOKEN,
)


@spaces.GPU
def predict(resume_text: str, job_description: str) -> float:
    resume_text = resume_text.strip()
    job_description = job_description.strip()

    if not resume_text:
        raise gr.Error("Resume text cannot be empty.")

    if not job_description:
        raise gr.Error("Job description cannot be empty.")

    try:
        embeddings = model.encode(
            [
                resume_text[:5000],
                job_description[:5000],
            ],
            convert_to_tensor=True,
            normalize_embeddings=True,
        )

        similarity = torch.dot(embeddings[0], embeddings[1])
        similarity = torch.clamp(similarity, 0.0, 1.0)

        return float(similarity.item())

    except Exception as e:
        print(f"Prediction error: {e}")
        raise gr.Error("Failed to calculate semantic similarity.")


@spaces.GPU
def predict_batch(pairs):
    """
    Calculate semantic similarity for multiple text pairs
    in a single Hugging Face request.

    Expected input:
    [
        {
            "text_a": "...",
            "text_b": "..."
        },
        ...
    ]

    Returns:
    [
        {
            "index": 0,
            "similarity": 0.82
        },
        ...
    ]
    """

    if isinstance(pairs, str):
        try:
            pairs = json.loads(pairs)
        except json.JSONDecodeError:
            raise gr.Error("Invalid batch input.")

    if not isinstance(pairs, list):
        raise gr.Error("Batch input must be a list.")

    if not pairs:
        return []

    try:
        texts_a = []
        texts_b = []

        for pair in pairs:
            if not isinstance(pair, dict):
                raise gr.Error("Each batch item must be an object.")

            text_a = str(pair.get("text_a", "")).strip()
            text_b = str(pair.get("text_b", "")).strip()

            if not text_a or not text_b:
                raise gr.Error("Batch text values cannot be empty.")

            texts_a.append(text_a[:5000])
            texts_b.append(text_b[:5000])

        all_texts = texts_a + texts_b

        embeddings = model.encode(
            all_texts,
            convert_to_tensor=True,
            normalize_embeddings=True,
            batch_size=32,
        )

        count = len(pairs)

        embeddings_a = embeddings[:count]
        embeddings_b = embeddings[count:]

        similarities = torch.sum(
            embeddings_a * embeddings_b,
            dim=1,
        )

        similarities = torch.clamp(
            similarities,
            0.0,
            1.0,
        )

        return [
            {
                "index": index,
                "similarity": float(similarity.item()),
            }
            for index, similarity in enumerate(similarities)
        ]

    except gr.Error:
        raise

    except Exception as e:
        print(f"Batch prediction error: {e}")
        raise gr.Error("Failed to calculate batch semantic similarity.")


with gr.Blocks() as demo:

    gr.Markdown(
        "# HireMind AI - Semantic Similarity"
    )

    gr.Markdown(
        "Fine-tuned Sentence Transformer for ATS "
        "resume and job-description matching."
    )

    with gr.Tab("Single Similarity"):

        resume_input = gr.Textbox(
            label="Resume Text",
            placeholder="Paste the resume text here...",
            lines=12,
        )

        jd_input = gr.Textbox(
            label="Job Description",
            placeholder="Paste the job description here...",
            lines=12,
        )

        single_output = gr.Number(
            label="Semantic Similarity"
        )

        single_button = gr.Button(
            "Calculate Similarity"
        )

        single_button.click(
            fn=predict,
            inputs=[
                resume_input,
                jd_input,
            ],
            outputs=single_output,
            api_name="predict",
        )

    with gr.Tab("Batch Similarity"):

        batch_input = gr.JSON(
            label="Text Pairs",
            value=[
                {
                    "text_a": "Python machine learning engineer",
                    "text_b": "Python, machine learning and deep learning developer",
                }
            ],
        )

        batch_output = gr.JSON(
            label="Similarities"
        )

        batch_button = gr.Button(
            "Calculate Batch Similarity"
        )

        batch_button.click(
            fn=predict_batch,
            inputs=batch_input,
            outputs=batch_output,
            api_name="predict_batch",
        )


if __name__ == "__main__":
    demo.launch()