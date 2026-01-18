"""
Defines two logical LLM-based agents:

- Question-Agent: generates questions using Meta's LLaMA model (via Groq)
- Answer-Agent: generates answers using OpenAI's GPT-OSS-120B model (via Groq)
"""

from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from project root
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path)

# Question-Agent LLM (Meta LLaMA)
question_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
)

# Answer-Agent LLM (OpenAI GPT-OSS)
answer_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
)


def question_agent(context: str, subject: str, difficulty: str) -> str:
    prompt = (
        "You are a question-generation agent.\n"
        f"Subject: {subject}\n"
        f"Difficulty level: {difficulty}\n\n"
        f"{context}\n\n"
        "TASK:\n"
        "Generate ONE clear, unambiguous question related to the subject.\n\n"
        "Constraints:\n"
        "- The output must contain EXACTLY ONE question.\n"
        "- Do NOT combine multiple sub-questions using 'and', 'or', commas, or clauses.\n"
        "- The question must be answerable with a single focused response.\n"
        "- If tempted to ask multiple things, choose the MOST important one.\n"
        "- Do not repeat previous questions.\n\n"
        "Return ONLY the question."
    )

    try:
        response = question_llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        raise RuntimeError("Question generation failed") from e



def answer_agent(question: str, context: str) -> str:
    """Generate a concise and well-structured answer."""
    prompt = (
        "You are an answer-generation agent.\n\n"
        f"Question:\n{question}\n\n"
        f"{context}\n\n"
        "TASK:\n"
        "Provide a concise, accurate, and well-structured answer.\n\n"
        "Constraints:\n"
        "- Use the MINIMUM number of points required for clarity (typically 2–4).\n"
        "- Each point should capture a distinct key idea.\n"
        "- Prefer short bullet points over paragraphs.\n"
        "- Do NOT add background unless strictly necessary.\n"
        "- Use previous context ONLY if it improves correctness.\n"
        "- Limit the answer to 3–5 short sentences OR 2–4 bullet points.\n"
        "- Do not wander into unrelated topics."
    )
    try:
        response = answer_llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        raise RuntimeError("Answer generation failed") from e







