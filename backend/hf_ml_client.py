from functools import lru_cache
from typing import List, Tuple

from gradio_client import Client


HF_SPACE = "dhruv-ai-05/HireMind-AI-ML-Service"


@lru_cache(maxsize=1)
def get_hf_client() -> Client:
    return Client(HF_SPACE)


def calculate_semantic_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Calculate semantic similarity for a single pair of texts.
    """

    if not isinstance(text_a, str) or not text_a.strip():
        return 0.0

    if not isinstance(text_b, str) or not text_b.strip():
        return 0.0

    client = get_hf_client()

    result = client.predict(
        resume_text=text_a[:5000],
        job_description=text_b[:5000],
        api_name="/predict",
    )

    return float(result)


def calculate_batch_semantic_similarity(
    pairs: List[Tuple[str, str]],
) -> List[float]:
    """
    Calculate semantic similarity for multiple text pairs
    using a single Hugging Face request.

    Args:
        pairs:
            List of (text_a, text_b) tuples.

    Returns:
        List of similarity scores in the same order as pairs.
    """

    if not pairs:
        return []

    valid_pairs = []

    for text_a, text_b in pairs:
        if (
            isinstance(text_a, str)
            and text_a.strip()
            and isinstance(text_b, str)
            and text_b.strip()
        ):
            valid_pairs.append(
                {
                    "text_a": text_a[:5000],
                    "text_b": text_b[:5000],
                }
            )
        else:
            valid_pairs.append(
                {
                    "text_a": "",
                    "text_b": "",
                }
            )

    request_pairs = [
        pair
        for pair in valid_pairs
        if pair["text_a"] and pair["text_b"]
    ]

    if not request_pairs:
        return [0.0] * len(pairs)

    client = get_hf_client()

    result = client.predict(
        pairs=request_pairs,
        api_name="/predict_batch",
    )

    result_by_index = {
        int(item["index"]): float(item["similarity"])
        for item in result
    }

    similarities = []

    request_index = 0

    for pair in valid_pairs:
        if not pair["text_a"] or not pair["text_b"]:
            similarities.append(0.0)
            continue

        similarities.append(
            result_by_index.get(request_index, 0.0)
        )

        request_index += 1

    return similarities