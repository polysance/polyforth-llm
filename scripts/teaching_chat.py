#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from polyforth_llm.teaching import run_teaching_chat


if __name__ == "__main__":
    run_teaching_chat()
