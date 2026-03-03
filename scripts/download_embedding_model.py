#!/usr/bin/env python3
from pathlib import Path

from sentence_transformers import SentenceTransformer


def main() -> None:
    model_id = "sentence-transformers/all-MiniLM-L6-v2"
    target = Path("models/all-MiniLM-L6-v2")
    target.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {model_id} to {target} ...")
    model = SentenceTransformer(model_id)
    model.save(str(target))
    print("Done.")


if __name__ == "__main__":
    main()
