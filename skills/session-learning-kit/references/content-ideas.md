# Content Ideas: Turning Coaching Sessions into Learning Material

Ways to repurpose a recorded 1:1 session (transcript + audio) into content that reinforces the client's learning, at little or no cost.

## Toolbox

### Local / open-source (cost: $0, private)
| Model | Where | Use |
|---|---|---|
| Qwen3.6-35B-A3B (GGUF) | LM Studio | Main writer: summaries, quizzes, podcast scripts; fits a full ~2.5 h transcript (~35k tokens) |
| Gemma 4 26B-A4B (GGUF) | Hugging Face cache | Second opinion / different writing voice |
| Whisper large-v3-turbo, Parakeet, Qwen3-ASR | local | Transcribing future sessions |
| Kokoro-82M | local (pip `kokoro`) | Text-to-speech for podcasts; small, fast on Apple Silicon |

### Credits / paid
- **Venice.ai:** private inference (no data retention), image generation, TTS, larger open models.
- **v0:** generating websites and UI.
- **Frontier (Claude, GPT, Gemini):** a final polish pass only. A full transcript is ~35k tokens, so a pass costs cents.
- **Google NotebookLM:** free, polished two-host Audio Overviews, but content goes to Google.

## Ideas, ranked by learning value

1. **Session playbook / study guide.** Chapters with timestamps, key concepts in plain language, a glossary, open questions, homework. *Local Qwen.*
2. **Flashcards + quiz.** 30–50 Anki cards plus a short quiz where every answer links to the moment it was discussed ("you asked this at 00:42:10"). Retrieval practice is the strongest way to reinforce learning. *Local Qwen → Anki CSV.*
3. **Two-voice recap podcast.** A 10–15 min NotebookLM-style episode recapping the key ideas as a conversation.
   - Open-source: Qwen script + Kokoro voices (free).
   - Venice: TTS + models on credits.
   - Frontier: NotebookLM Audio Overview (free, cloud).
4. **Interactive learning site.** A v0-built client portal: chapters, quizzes, glossary, and "hear the original" buttons that play the real audio at a timestamp (the SRT makes this easy). Reusable template per client.
5. **"Ask your session" chatbot.** Transcript loaded into LM Studio's chat with document attachments, so the client can ask "what did Pat say about open-source models?" Local, free, private.
6. **Visual cheat sheet.** A one-page diagram (e.g. frontier vs open-source, when to use which), with illustrations from Venice image models.
7. **Spaced follow-ups.** 3–4 short emails over two weeks, each recapping one idea and asking one question. *Local Qwen.*
8. **Content for the coaching business** (with client permission). Quotable clips, a LinkedIn/blog post on "what clients ask about AI," anonymized FAQs.

## Recommended split
- **~90% local open-source** for drafts, quizzes, scripts and summaries: free and private.
- **Venice** for images, TTS and larger open models when needed.
- **v0** for the website only.
- **Frontier** for an optional final polish.

## Privacy
Client sessions stay private with local models. Get the client's OK before sending session content to cloud services or publishing anything.

## Folder convention
```
atxworkshop/
  content-ideas/            ← this file
  content/
    <client-or-project>/    e.g. acme-labs
      study-guide/
      flashcards/
      podcast/
```
