# Finding local transcription tools before installing anything

Check all of these and report what exists:

```bash
for c in whisper whisper-cli whisper-cpp mlx_whisper faster-whisper whisperx ffmpeg ffprobe lms; do
  printf "%s: " $c; command -v $c || echo none; done
ls /Applications | grep -iE "whisper|lm studio|macwhisper|superwhisper|handy|aiko"
ls ~/.cache/whisper ~/.cache/huggingface/hub 2>/dev/null        # openai-whisper .pt, HF repos (mlx / gguf)
ls ~/.lmstudio/models/* 2>/dev/null; ~/.lmstudio/bin/lms ls      # LM Studio models (incl. ASR like Qwen3-ASR)
ls ~/Library/Application\ Support | grep -iE "whisper|handy"     # app-bundled models
pip3 list 2>/dev/null | grep -iE "whisper|mlx|ctranslate|torch"; pipx list 2>/dev/null; brew list | grep -i whisper
```

Notes from this machine (Mac Studio M4 Max, 64 GB):
- **openai-whisper 20250625** via Homebrew Python plus `large-v3-turbo.pt`: works on CPU at ~6–11x real time per track with 8 threads. Running two tracks in parallel is fine.
- `device="mps"` fails with word timestamps: `Cannot convert a MPS Tensor to float64`.
- Handy's HF cache has `whisper-large-v3-turbo-gguf` (Q8), Parakeet and Cohere-transcribe GGUFs. They're usable with whisper.cpp-style runtimes, but there's no CLI installed for them.
- LM Studio has `Qwen3-ASR-1.7B-GGUF`: an ASR model, but no word timestamps through the chat API.
- If speed matters: `pip install mlx-whisper` (Metal) with `mlx-community/whisper-large-v3-turbo`. Downloading a model is fine; never upload audio.
