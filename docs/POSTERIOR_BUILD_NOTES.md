# Posterior Build Notes

This document captures build-session context, hardware details, and practical operating guidance that would otherwise clutter the main `README.md`.

## Session Logs

For dated, procedural build traces and validation outcomes, see:

1. `evaluation/build-results-2026-03-19.md`

## Host Computer Specs

1. AMD Ryzen 9 5950X Processor
2. ASUS Prime A520M-K Motherboard Socket AM4
3. Corsair Vengeance LPX 64GB (2x32GB) DDR4 3200MHz C16
4. Intenso Internal M.2 SSD SATA III Top, 512 GB, 520 MB/s
5. Debian Linux with KDE Plasma desktop
6. XFX Speedster SWFT105 Radeon RX 6400 Gaming Graphics Card with 4GB GDDR6, AMD RDNA 2 (RX-64XL4SFG2)
7. Corsair 4000D Airflow Tempered Glass Mid-Tower ATX Case
8. be quiet! Pure Power 12 850W Power Supply, 80 Plus Gold Efficiency, ATX 3.1 with full support for PCIe 5.1 GPUs
9. Corsair 240mm AIO Liquid CPU Cooler (AM4 compatible)

## Local Model Profile

### Recommendation for current setup (RX 6400 4GB)

1. Keep retrieval local (FAISS + sentence-transformers).
2. Prefer local inference with compact quantized models for first-round educational exploration.
3. Use hosted fallback only when local quality/latency is insufficient for the teaching target.
4. Prefer moderate context windows for speed/latency.

### Suggested starting model class

1. Local first: compact quantized code-capable instruct model.
2. Hosted fallback: code-capable instruct model via API.

### Not recommended on current setup

1. 30B-class local code models for interactive usage.
2. Expecting 4GB VRAM to run mid/large LLMs effectively.

### Upgrade path

1. Storage first: move to 1TB to 2TB NVMe (model files and cache grow quickly).
2. Then GPU: 24GB VRAM minimum for practical local coding assistants, 48GB+ preferred for larger models and longer contexts.

### Practical deployment split

1. Best quality now: local RAG + hosted LLM API.
2. Best fully local now: local RAG + quantized 7B to 16B model.
