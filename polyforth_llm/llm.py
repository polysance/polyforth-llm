from __future__ import annotations

from openai import OpenAI

from polyforth_llm.config import Settings


class LLMClient:
    def __init__(self, settings: Settings) -> None:
        if not settings.llm_api_key:
            raise ValueError("Missing LLM_API_KEY in environment.")
        self.settings = settings
        self.client = OpenAI(api_key=settings.llm_api_key, base_url=settings.llm_base_url)

    def complete(
        self,
        user_prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        resp = self.client.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {"role": "system", "content": system_prompt or self.settings.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content or ""
