# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the first course I must take as a CS student at UMD? | CMSC131 | CMSC131 and CMSC132 | Relevant | Partially accurate |
| 2 | What courses will help me with technical interviews? | CMSC351, CMSC451, CMSC389O | CMSC389O | Relevant | Partially accurate |
| 3 | What upper level course can I take if I'm interested in networking and cloud computing? | CMSC417, CMSC398P, etc. | CMSC398P | Relevant | Partially accurate |
| 4 | 	Who are the best professors to take for CS courses in general? | Varied answers. | Nelson Padua-Perez, Mohammed Nayeem Teli, Chau-Wen Tseng, Elias Gonzalez, Fawzi Emad | Relevant | Accurate |
| 5 | What are the easiest 400-level classes to take? | Varied answers. |  Not enough information, but hardest courses are 412 (OS) and 417 (Networks) | Partially relevant | Inaccurate (not enough context given through docs) |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
What are the easiest 400-level classes to take?
**What the system returned:**
I don't have any information on the easiest 400-level classes to take, as the context only mentions that classes like 412 (operating systems) and 417 (networks) are known to be difficult (source: reddit_guide.txt).
**Root cause (tied to a specific pipeline stage):**
Ingesting stage doesn't utilize documents that specify ease of upper-level courses. 
**What you would change to fix it:**
Use documents that rank classes based on difficulty maybe from a reddit post on the r/UMD subreddit made by a student, that has a lot of karma and support.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Helped me understand what specific things I needed to ask Claude to include in its implementation of each stage in the pipeline. 
**One way your implementation diverged from the spec, and why:**
I asked Claude to be mindful of the distances of retrieved chunks. Essentially, if a chunk is more than 0.5 distance away from the query, it doesn't get utilized. This hopefully keeps the response grounded in relevant sources.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
implement get_collection() and embed_and_store(chunks) and retrieve(query, n_results) using chromaDB and sentence transformers all-MiniLM-L6-v2, the details are specified in planning.md and config.py.
- *What it produced:*
The methods in retriver.py.
- *What I changed or overrode:*
I played around with the number of results retrieved to see what would give a more relevant collection of contextual information.

**Instance 2**

- *What I gave the AI:*
implement the generate() function so that the chunks are labeled by file name and include distance scores. Make sure that the system knows not to answer from beyond the retrieved text, say "I don't have any information on this" or something like that. If the distance scores retrieved are too high (maybe more than 0.5?), then they shouldn't be used either.
- *What it produced:*
The methods in generator.py.
- *What I changed or overrode:*
I played around with the threshold to see what gave more accurate responses. 
