"""Transcribe one mic track locally with openai-whisper (word timestamps).

usage: transcribe.py <in.wav> <out.json> [threads] [model] [names...]

CPU is used on purpose: openai-whisper's word timestamps crash on Apple's MPS backend (no float64).
large-v3-turbo runs ~6-11x real time on an M4 Max with 8 threads; run both mics in parallel.
"""
import json, sys, time
import torch, whisper

src, dst = sys.argv[1], sys.argv[2]
threads = int(sys.argv[3]) if len(sys.argv) > 3 else 8
model = sys.argv[4] if len(sys.argv) > 4 else "large-v3-turbo"
names = sys.argv[5:]
torch.set_num_threads(threads)
m = whisper.load_model(model, device="cpu")
t = time.time()
r = m.transcribe(src, language="en", word_timestamps=True, condition_on_previous_text=False, fp16=False,
                 initial_prompt=f"A working session between {' and '.join(names)}." if names else None, verbose=False)
json.dump(r, open(dst, "w"))
print(f"{src}: {len(r['segments'])} segments in {time.time() - t:.0f}s")
