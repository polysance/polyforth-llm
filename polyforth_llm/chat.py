from __future__ import annotations

from polyforth_llm.config import load_settings
from polyforth_llm.llm import LLMClient
from polyforth_llm.retriever import Retriever


def _build_prompt(question: str, contexts: list[tuple[int, str]]) -> str:
    context_block = "\n\n".join([f"[p{page}] {text}" for page, text in contexts])
    return (
        "Answer the question using the context below.\n"
        "Rules:\n"
        "1) Prefer context facts over prior knowledge.\n"
        "2) If context is insufficient, explicitly say what is missing.\n"
        "3) Cite supporting statements with [pX] page tags.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question:\n{question}\n"
    )


def run_chat() -> None:
    settings = load_settings()
    retriever = Retriever(settings)
    llm = LLMClient(settings)

    print("polyforth-llm chat ready. Type 'exit' to quit.")
    while True:
        question = input("\n> ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break

        chunks = retriever.search(question)
        contexts = [(c.page, c.text) for c in chunks]
        prompt = _build_prompt(question, contexts)

        answer = llm.complete(prompt)
        print("\n" + answer)
