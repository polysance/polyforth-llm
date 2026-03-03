from __future__ import annotations

from dataclasses import dataclass

from polyforth_llm.config import load_settings
from polyforth_llm.llm import LLMClient
from polyforth_llm.retriever import RetrievedChunk, Retriever


TEACHING_SYSTEM_PROMPT = (
    "You are a polyForth teaching assistant. Teach clearly and incrementally. "
    "Use only retrieved context when possible. Always cite supporting facts "
    "with [source] tags. If context is missing, explicitly say what is missing."
)


@dataclass
class TeachingState:
    mode: str = "explain"


def _render_context(chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return "(no context found)"
    return "\n\n".join([f"[{c.source}] ({c.heading}) {c.text}" for c in chunks])


def _explain_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    return (
        "Teaching mode: explain.\n"
        "Give a direct explanation, a small example, and one short practice task.\n\n"
        f"Context:\n{_render_context(chunks)}\n\n"
        f"Student question:\n{question}\n"
    )


def _socratic_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    return (
        "Teaching mode: socratic.\n"
        "Do not give the full answer immediately. Ask 1-2 focused questions first, "
        "then provide a concise guided explanation. Include citations.\n\n"
        f"Context:\n{_render_context(chunks)}\n\n"
        f"Student question:\n{question}\n"
    )


def _quiz_prompt(topic: str, chunks: list[RetrievedChunk], count: int) -> str:
    return (
        "Teaching mode: quiz.\n"
        f"Generate {count} short questions on the topic, then provide an answer key.\n"
        "Format:\n"
        "1) Questions section\n"
        "2) Answer key section\n"
        "Cite sources in answer key with [source].\n\n"
        f"Context:\n{_render_context(chunks)}\n\n"
        f"Topic:\n{topic}\n"
    )


def _help_text() -> str:
    return (
        "Commands:\n"
        "  /mode explain|socratic|quiz\n"
        "  /lesson <topic>\n"
        "  /quiz <topic> [count]\n"
        "  /help\n"
        "  exit\n"
    )


def run_teaching_chat() -> None:
    settings = load_settings()
    retriever = Retriever(settings)
    llm = LLMClient(settings)
    state = TeachingState()

    print("polyforth-llm teaching chat ready.")
    print(_help_text())

    while True:
        raw = input("\n[tutor] > ").strip()
        if not raw:
            continue
        if raw.lower() in {"exit", "quit"}:
            break
        if raw == "/help":
            print(_help_text())
            continue
        if raw.startswith("/mode "):
            mode = raw.split(maxsplit=1)[1].strip().lower()
            if mode not in {"explain", "socratic", "quiz"}:
                print("Invalid mode. Use: explain, socratic, quiz.")
                continue
            state.mode = mode
            print(f"Mode set to: {state.mode}")
            continue
        if raw.startswith("/quiz "):
            payload = raw.split(maxsplit=1)[1].strip()
            parts = payload.rsplit(" ", 1)
            topic = payload
            count = 5
            if len(parts) == 2 and parts[1].isdigit():
                topic = parts[0].strip()
                count = int(parts[1])
            chunks = retriever.search(topic, top_k=max(settings.top_k, 8))
            prompt = _quiz_prompt(topic, chunks, count)
            answer = llm.complete(
                prompt, system_prompt=TEACHING_SYSTEM_PROMPT, temperature=0.3
            )
            print("\n" + answer)
            continue
        if raw.startswith("/lesson "):
            question = raw.split(maxsplit=1)[1].strip()
        else:
            question = raw

        chunks = retriever.search(question)
        if state.mode == "socratic":
            prompt = _socratic_prompt(question, chunks)
            temp = 0.4
        elif state.mode == "quiz":
            prompt = _quiz_prompt(question, chunks, 5)
            temp = 0.3
        else:
            prompt = _explain_prompt(question, chunks)
            temp = 0.2

        answer = llm.complete(
            prompt,
            system_prompt=TEACHING_SYSTEM_PROMPT,
            temperature=temp,
        )
        print("\n" + answer)
