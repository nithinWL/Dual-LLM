"""
Main application module.

Coordinates FastAPI request handling, session orchestration,
difficulty progression, conversational memory, and JSON output.
"""

from fastapi import FastAPI, HTTPException
from typing import List
from pathlib import Path
from datetime import datetime
import json

from schemas import Request, Response, QApair
from agents import question_agent, answer_agent


app = FastAPI(
    title="Dual-LLM Q&A Session API",
    description="Runs a multi-turn Q&A session using two LLM-based agents",
    version="1.0.0",
)

# Directory to store final JSON outputs
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


@app.post("/run-session", response_model=Response)
async def run_session_endpoint(request: Request) -> Response:
    """Run a multi-turn Q&A session."""
    if request.num_pairs <= 0:
        raise HTTPException(
            status_code=400,
            detail="num_pairs must be greater than 0"
        )

    try:
        pairs = run_session(
            subject=request.subject,
            num_pairs=request.num_pairs
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate Q&A session"
        )

    response = Response(
        subject=request.subject,
        num_pairs=len(pairs),
        pairs=pairs
    )

    # Save final output as JSON file (assignment requirement)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_subject = "".join(c if c.isalnum() else "_" for c in request.subject)
    filename = f"qa_session_{safe_subject}_{timestamp}.json"
    filepath = OUTPUT_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(response.model_dump(), f, indent=2, ensure_ascii=False)

    return response


def difficulty(x: int, num_pairs: int) -> str:
    """Gradually increase difficulty: easy → medium → hard."""
    ratio = x / num_pairs
    if ratio <= 0.33:
        return "easy"
    elif ratio <= 0.66:
        return "medium"
    else:
        return "hard"


def run_session(subject: str, num_pairs: int) -> List[QApair]:
    """Run the question–answer interaction loop."""
    pairs: List[QApair] = []

    for i in range(1, num_pairs + 1):
        level = difficulty(i, num_pairs)

        context_q = context_generate(pairs, if_question=True)
        question = question_agent(context_q, subject, level)

        context_a = context_generate(pairs, if_question=False)
        answer = answer_agent(question, context_a)

        pairs.append(QApair(id=i, question=question, answer=answer))

    return pairs


def context_generate(pairs: List[QApair], if_question: bool) -> str:
    """Generate conversational memory from previous Q/A pairs."""
    lines = []

    for pair in pairs:
        lines.append(f"Q{pair.id}: {pair.question}")
        lines.append(f"A{pair.id}: {pair.answer}")
        lines.append("")

    if if_question:
        lines.append(
            "QUESTION GUIDELINES:\n"
            "Build on prior discussion and avoid repetition.\n"
            "Adjust difficulty as specified."
        )
    else:
        lines.append(
            "ANSWER GUIDELINES:\n"
            "Remain consistent with prior answers and stay concise."
        )

    return "\n".join(lines)





        




