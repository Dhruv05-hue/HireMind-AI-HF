import os
import json
import logging
from typing import Dict

from groq import Groq


logger = logging.getLogger("ats_resume_scorer")


GROQ_MODEL = "openai/gpt-oss-120b"

_client = None


# ============================================================
# GROQ CLIENT
# ============================================================

def _get_client() -> Groq:
    global _client

    if _client is None:

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable not set"
            )

        _client = Groq(
            api_key=api_key
        )

    return _client


# ============================================================
# RESUME PARSER PROMPTS
# ============================================================

RESUME_SYSTEM_PROMPT = (
    "You are a resume parser. "
    "Extract information accurately from the resume. "
    "Do not invent information. "
    "Return ONLY a valid JSON object. "
    "No explanation, no markdown."
)


RESUME_USER_PROMPT = """Extract the following information from this resume and return it as JSON:

{{
  "name": "full name",
  "email": "email address",
  "phone": "phone number",
  "linkedin": "LinkedIn URL if present, otherwise null",
  "github": "GitHub URL if present, otherwise null",

  "professional_summary": "the full text of the Summary, Profile, About Me, Objective, or Professional Summary section at the top of the resume. Copy the ENTIRE paragraph exactly as written. If no such section exists, return an empty string.",

  "skills": [
    "all technical and soft skills explicitly listed or mentioned in the resume"
  ],

  "experience": [
    {{
      "job_title": "",
      "company": "",
      "start_date": "",
      "end_date": "",
      "duration_months": 0,
      "description": ""
    }}
  ],

  "education": [
    {{
      "degree": "",
      "institution": "",
      "year": ""
    }}
  ],

  "certifications": [
    "list of certifications"
  ],

  "projects": [
    {{
      "title": "project name",
      "description": "accurate description of what the project does and how it was built, using only information explicitly present in the resume",
      "technologies": [
        "every specific technology, programming language, framework, library, database, platform, API, ML/AI technique, tool, or technical methodology explicitly mentioned as being used in THIS project"
      ]
    }}
  ],

  "action_verbs": [
    "strong action verbs used in bullet points, such as developed, implemented, designed"
  ],

  "keywords": [
    "important technical terms and ATS-relevant keywords explicitly present in the resume"
  ]
}}

IMPORTANT INSTRUCTIONS:

GENERAL:
- Extract information ONLY from the resume.
- Do NOT invent technologies, skills, tools, frameworks, libraries, databases, or methodologies.
- If something is not explicitly supported by the resume, do not add it.
- Return ONLY valid JSON.
- Do not return markdown.
- Do not return explanations.

SKILLS:
- Extract all technical skills explicitly mentioned anywhere in the resume.
- Include programming languages, frameworks, libraries, databases, cloud platforms, APIs, ML/AI techniques, tools, and relevant technical concepts.
- Include soft skills only if they are explicitly listed as skills.
- Do not infer skills from a project unless the technology or skill is actually mentioned in that project.

PROJECTS:
- Identify every project described in the resume.
- For each project, extract its actual title.
- Write a concise but accurate description based only on the project information in the resume.
- The "technologies" array is extremely important.
- For EACH project, inspect the project's title, description, bullet points, and surrounding project content.
- Extract EVERY specific technology explicitly associated with that project.
- Do NOT limit the technologies list to only the most obvious technologies.
- Include programming languages, frameworks, libraries, databases, APIs, platforms, tools, ML/AI techniques, and technical methodologies when explicitly mentioned.
- If the project says it uses a technology, that technology must appear in the project's "technologies" array.
- Do NOT copy the entire global Skills section into every project.
- A technology should appear in a project only when the resume provides evidence that the project uses it.
- Do NOT add a technology merely because it appears somewhere else in the resume.
- Preserve specific technology names when possible.

Examples:

If a project says:
"Built an image classification application using Python, PyTorch, CNNs and OpenCV."

Return technologies like:
["Python", "PyTorch", "CNN", "OpenCV"]

If a project says:
"Developed a REST API using FastAPI and PostgreSQL and containerized it using Docker."

Return:
["FastAPI", "REST API", "PostgreSQL", "Docker"]

If a project says:
"Created an AI fitness coach using Python, MediaPipe, OpenCV and Streamlit."

Return:
["Python", "MediaPipe", "OpenCV", "Streamlit"]

Do NOT add PyTorch to that project unless PyTorch is actually mentioned in the project content.

TECHNOLOGY NORMALIZATION:
Use canonical names where appropriate:

- "CNNs" -> "CNN"
- "REST APIs" -> "REST API"
- "RESTful APIs" -> "REST API"
- "NodeJS" -> "Node.js"
- "Node.js development" -> "Node.js"
- "Python programming" -> "Python"
- "Postgres" -> "PostgreSQL"
- "sklearn" -> "scikit-learn"
- "Open CV" -> "OpenCV"
- "Natural Language Processing" -> "NLP"
- "Machine Learning" -> "Machine Learning"
- "Deep Learning" -> "Deep Learning"

Do not create a technology that is not supported by the resume.

EXPERIENCE:
- Extract job title, company, dates, duration, and description.
- Preserve the meaning of the original experience.
- Calculate duration_months from the provided dates when possible.
- If end_date is "Present" or "Current", calculate duration using the current date.
- If dates are unavailable or cannot be reliably calculated, use 0.

ACTION VERBS:
- Extract strong action verbs that actually occur in the resume.
- Prefer verbs from project and experience bullet points.

KEYWORDS:
- Extract important ATS-relevant technical terms explicitly present in the resume.
- Include programming languages, frameworks, libraries, tools, databases, APIs, platforms, ML/AI techniques, and technical concepts.
- Do not fill keywords with generic words such as:
  "experience", "candidate", "job", "role", "team", "company", "work", "responsibility", or "development".

Return ONLY valid JSON.

Resume Text:
{raw_text}
"""


# ============================================================
# GROQ REQUEST
# ============================================================

def _call_groq(
    client: Groq,
    system_prompt: str,
    user_prompt: str,
) -> str:

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.0,
        max_tokens=4096,
    )

    return response.choices[0].message.content.strip()


# ============================================================
# JSON PARSER
# ============================================================

def _try_parse_json(
    text: str,
) -> dict | None:

    cleaned = text.strip()

    # Remove markdown code fences if present.
    if cleaned.startswith("```"):

        first_newline = (
            cleaned.index("\n")
            if "\n" in cleaned
            else len(cleaned)
        )

        cleaned = cleaned[
            first_newline + 1:
        ]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)

        if isinstance(result, dict):
            return result

        return None

    except json.JSONDecodeError:
        return None


# ============================================================
# RESUME PARSER
# ============================================================

def parse_resume(
    raw_text: str,
) -> Dict:

    client = _get_client()

    prompt = RESUME_USER_PROMPT.format(
        raw_text=raw_text
    )

    # --------------------------------------------------------
    # First attempt
    # --------------------------------------------------------

    raw_response = _call_groq(
        client,
        RESUME_SYSTEM_PROMPT,
        prompt,
    )

    result = _try_parse_json(
        raw_response
    )

    # IMPORTANT:
    # The original code had this condition reversed.
    if result is not None:
        return _validate_resume_result(
            result
        )

    # --------------------------------------------------------
    # Retry
    # --------------------------------------------------------

    logger.warning(
        "Groq resume parse: first attempt returned invalid JSON, retrying..."
    )

    strict_prompt = (
        "Your previous response was not valid JSON. "
        "Return ONLY the raw JSON object, "
        "with no markdown, no explanation, "
        "and no code fences.\n\n"
        + prompt
    )

    raw_response = _call_groq(
        client,
        RESUME_SYSTEM_PROMPT,
        strict_prompt,
    )

    result = _try_parse_json(
        raw_response
    )

    if result is not None:
        return _validate_resume_result(
            result
        )

    raise ValueError(
        "Groq returned an unparseable response "
        "after retry. Raw response:\n"
        + raw_response[:500]
    )


# ============================================================
# JD PARSER
# ============================================================

JD_SYSTEM_PROMPT = (
    "You are a job description parser. "
    "Extract information accurately from the job description. "
    "Return ONLY a valid JSON object. "
    "No explanation, no markdown."
)


JD_USER_PROMPT = """Extract the following from this job description and return as JSON:

{{
  "job_title": "",
  "required_skills": [
    "list of specific technical skills explicitly required"
  ],
  "preferred_skills": [
    "list of specific technical skills explicitly preferred"
  ],
  "experience_required": "",
  "education_required": "",
  "key_responsibilities": [
    "list of responsibilities"
  ],
  "keywords": [
    "list of specific ATS-relevant technical skills and technologies"
  ]
}}

Important instructions:

- required_skills: Include ONLY specific skills, technologies, programming languages,
  frameworks, libraries, tools, platforms, databases, ML/AI techniques, cloud technologies,
  APIs, or technical methodologies explicitly required by the job description.

- preferred_skills: Include ONLY specific technical skills, technologies, frameworks,
  libraries, tools, platforms, databases, or technical methodologies explicitly described
  as preferred, bonus, or nice-to-have.

- keywords: Include ONLY specific ATS-relevant technical terms that represent a skill,
  technology, tool, framework, programming language, database, platform, API, ML/AI technique,
  or technical domain.

- Do NOT include generic words or phrases such as:
  "experience", "candidate", "job", "role", "position", "team", "company",
  "responsibilities", "work", "development", "knowledge", "ability",
  "strong communication", "problem solving", "an AI/ML engineer",
  or similar generic phrases.

- Do NOT combine multiple independent skills into one keyword.

For example:
"Python, PyTorch, and TensorFlow"

must become:

["Python", "PyTorch", "TensorFlow"]

- Prefer canonical skill names:

"CNNs" -> "CNN"
"REST APIs" -> "REST API"
"Node.js development" -> "Node.js"
"Python programming" -> "Python"

- Do not create skills that are merely implied.
- Extract only terms actually present in the job description.

- "computer vision applications" should be represented as "Computer Vision".
- "machine learning models" should be represented as "Machine Learning".
- "deep learning models" should be represented as "Deep Learning".

- Return ONLY valid JSON.
- No markdown.
- No explanation.

Job Description Text:
{raw_text}
"""


# ============================================================
# JOB DESCRIPTION PARSER
# ============================================================

def parse_job_description(
    raw_text: str,
) -> Dict:

    client = _get_client()

    prompt = JD_USER_PROMPT.format(
        raw_text=raw_text
    )

    raw_response = _call_groq(
        client,
        JD_SYSTEM_PROMPT,
        prompt,
    )

    result = _try_parse_json(
        raw_response
    )

    if result is not None:
        return _validate_jd_result(
            result
        )

    logger.warning(
        "Groq JD parse: first attempt returned invalid JSON, retrying..."
    )

    strict_prompt = (
        "Your previous response was not valid JSON. "
        "Return ONLY the raw JSON object, "
        "with no markdown, no explanation, "
        "and no code fences.\n\n"
        + prompt
    )

    raw_response = _call_groq(
        client,
        JD_SYSTEM_PROMPT,
        strict_prompt,
    )

    result = _try_parse_json(
        raw_response
    )

    if result is not None:
        return _validate_jd_result(
            result
        )

    raise ValueError(
        "Groq returned an unparseable response "
        "after retry. Raw response:\n"
        + raw_response[:500]
    )


# ============================================================
# VALIDATE JD RESULT
# ============================================================

def _validate_jd_result(
    result: dict,
) -> dict:

    defaults = {
        "job_title": "",
        "required_skills": [],
        "preferred_skills": [],
        "experience_required": "",
        "education_required": "",
        "key_responsibilities": [],
        "keywords": [],
    }

    for key, default in defaults.items():

        if (
            key not in result
            or result[key] is None
        ):
            result[key] = default

        if (
            isinstance(default, list)
            and not isinstance(
                result[key],
                list,
            )
        ):
            result[key] = default

    return result


# ============================================================
# VALIDATE RESUME RESULT
# ============================================================

def _validate_resume_result(
    result: dict,
) -> dict:

    defaults = {
        "name": "",
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "professional_summary": "",
        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],
        "projects": [],
        "action_verbs": [],
        "keywords": [],
    }

    for key, default in defaults.items():

        if (
            key not in result
            or result[key] is None
        ):
            result[key] = default

        if (
            isinstance(default, list)
            and not isinstance(
                result[key],
                list,
            )
        ):
            result[key] = default

    # --------------------------------------------------------
    # Validate experience entries
    # --------------------------------------------------------

    for exp in result.get(
        "experience",
        [],
    ):

        if not isinstance(exp, dict):
            continue

        exp.setdefault(
            "job_title",
            "",
        )

        exp.setdefault(
            "company",
            "",
        )

        exp.setdefault(
            "start_date",
            "",
        )

        exp.setdefault(
            "end_date",
            "",
        )

        exp.setdefault(
            "duration_months",
            0,
        )

        exp.setdefault(
            "description",
            "",
        )

        try:
            exp["duration_months"] = int(
                exp["duration_months"]
            )

        except (
            ValueError,
            TypeError,
        ):
            exp["duration_months"] = 0

    # --------------------------------------------------------
    # Validate project entries
    # --------------------------------------------------------

    for project in result.get(
        "projects",
        [],
    ):

        if not isinstance(
            project,
            dict,
        ):
            continue

        project.setdefault(
            "title",
            "",
        )

        project.setdefault(
            "description",
            "",
        )

        project.setdefault(
            "technologies",
            [],
        )

        # Make sure technologies is always a list.
        if not isinstance(
            project["technologies"],
            list,
        ):
            project["technologies"] = []

        # Remove empty technology values.
        project["technologies"] = [
            str(technology).strip()
            for technology in project[
                "technologies"
            ]
            if technology
            and str(technology).strip()
        ]

    return result