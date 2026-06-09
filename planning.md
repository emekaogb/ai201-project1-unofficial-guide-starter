# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
The domain is computer science students navigating lower-level and upper-level courses at the University of Maryland.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit (r/UMD) Wiki Guide for UMD CS Students | Unofficial guide for compsci students going through all the requirements and steps | https://www.reddit.com/r/UMD/comments/cj7oq4/wiki_project_a_guide_to_computer_science/ |
| 2 | Schedule of Classes - CMSC1XX | 100-level CS courses | https://app.testudo.umd.edu/soc/search?courseId=CMSC1&sectionId=&termId=202608&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on |
| 3 | Schedule of Classes - CMSC2XX| 200-level CS courses| https://app.testudo.umd.edu/soc/search?courseId=CMSC2&sectionId=&termId=202608&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on |
| 4 | Schedule of Classes - CMSC3XX | 300-level CS courses | https://app.testudo.umd.edu/soc/search?courseId=CMSC3&sectionId=&termId=202608&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on |
| 5 | Schedule of Classes - CMSC4XX | 400-level CS courses | https://app.testudo.umd.edu/soc/search?courseId=CMSC4&sectionId=&termId=202608&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on |
| 6 | CMSC131 Course Reviews from PlanetTerp | Self-explanatory | https://planetterp.com/course/CMSC131/reviews |
| 7 | CMSC132 Course Reviews from PlanetTerp | Self-explanatory | https://planetterp.com/course/CMSC132/reviews |
| 8 | CMSC216 Course Reviews from PlanetTerp | Self-explanatory | https://planetterp.com/course/CMSC216/reviews |
| 9 | CMSC250 Course Reviews from PlanetTerp | Self-explanatory | https://planetterp.com/course/CMSC250/reviews |
| 10 | CMSC330 Course Reviews from PlanetTerp | Self-explanatory | https://planetterp.com/course/CMSC330/reviews |
| 11 | CMSC351 Course Reviews from PlanetTerp | Self-explanatory | https://planetterp.com/course/CMSC351/reviews |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
500 characters.
**Overlap:**
100 characters.
**Reasoning:**
Semantic meaning spans multiple sentences in the case of reddit posts and course reviews. Maybe recursive chunking can be implemented given that the documents have specific headings and such. 
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
sentence-transformers --> all-MiniLM-L6-v2
**Top-k:**
Top 5 chunks will be retrieved.
**Production tradeoff reflection:**
The top 5 chunks should provide enough context but may miss some minute details that could be useful. 
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What is the first course I must take as a CS student at UMD? | CMSC131 |
| 2 | What courses will help me with technical interviews? | CMSC132, CMSC351, CMSC451, etc. |
| 3 | What upper level course can I take if I'm interested in networking and cloud computing? | CMSC417, STIC courses like CMSC398P |
| 4 | Who are the best professors to take for CS courses in general? | Varied answers. |
| 5 | What are the easiest 400-level classes to take? | Varied answers. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. For course reviews, some chunks may be mixing two reviews together or even more. For course descriptions, the same risk is present. 

2. Review length and course description length are inconsistent, so implementing a fixed chunking strategy may prove difficult.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I'll give Claude my chunking strategy section and ask it to implement chunk_text() with my specified chunk size and overlap.
**Milestone 4 — Embedding and retrieval:**
I'll give Claude my embedding model and top-k and ask it to implement embed_and_store(). 
**Milestone 5 — Generation and interface:**
I'll specify how the prompt given to the LLM should be structured with both the grounding context and the user query and ask Clause to implement the generate() function, along with the UI to resemble a chatbot system. 