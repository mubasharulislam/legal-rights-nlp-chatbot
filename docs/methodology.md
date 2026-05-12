# Methodology

## Research Framing

The Legal Rights Chatbot is a domain-specific information retrieval system for workplace harassment legal information in Pakistan. It is designed as a Computational Linguistics / NLP portfolio project rather than a general conversational AI product.

The central research question is how a small, curated legal knowledge base can support natural-language access when users may not know formal legal terminology. Instead of generating unconstrained legal answers, the system retrieves structured, human-written topic entries and formats them into concise informational responses.

## Corpus Design

The knowledge base is stored in `data/legal_knowledge.json`. Each topic is treated as a retrievable document containing:

- topic title
- manually selected keywords
- example user queries
- answer text
- recommended next steps
- source metadata

At indexing time, the retrievable document representation is created by concatenating the topic title, keywords, answer, steps, and examples. This combines formal legal language with likely user phrasing.

## Retrieval Pipeline

The retrieval pipeline follows this sequence:

```text
User query
  -> normalization
  -> TF-IDF vectorization
  -> cosine similarity against topic documents
  -> keyword scoring
  -> hybrid ranking
  -> threshold decision
  -> formatted response or fallback response
```

Query normalization lowercases text, strips whitespace, and collapses repeated spaces. The current system does not perform stemming, lemmatization, spelling correction, named entity recognition, or language identification.

## TF-IDF Representation

When `scikit-learn` is installed, the system builds a TF-IDF index using:

- lowercasing
- English stop-word removal
- unigram and bigram features

The user query is transformed into the same vector space as the topic corpus. Cosine similarity is then used to estimate query-document relevance.

## Keyword Scoring

The TF-IDF score is combined with a manually curated keyword score:

- multi-word keyword phrase match: `+3.0`
- exact single-word match: `+2.0`
- prefix-style match for longer keywords: `+1.0`

This symbolic component improves matching for legally important vocabulary such as `intern`, `ombudsperson`, `retaliation`, `evidence`, and `WhatsApp messages`.

The final ranking score is:

```text
combined_score = keyword_score + (tfidf_cosine_similarity * 8)
```

## Information Retrieval Terminology

The project can be described using standard IR terminology:

- **Corpus:** the structured topic set in the JSON knowledge base.
- **Document:** one topic representation formed from title, keywords, examples, answer, and steps.
- **Query:** the user's natural-language message.
- **Index:** the TF-IDF topic matrix.
- **Ranking function:** combined TF-IDF and keyword score.
- **Relevance threshold:** minimum score required before returning a topic answer.
- **Fallback response:** controlled response used when no topic is retrieved confidently.

## Linguistic Challenges

The domain presents several NLP challenges:

- users may describe harassment indirectly or emotionally
- legal concepts have multiple surface forms, such as `complaint`, `report`, `case`, and `application`
- employment categories vary, including interns, freelancers, trainees, students, and domestic workers
- evidence may be described through platform-specific terms such as WhatsApp, screenshots, emails, and call logs
- sensitive queries may involve fear, retaliation, blackmail, confidentiality, or immediate safety

The current system is lexical rather than deeply semantic, so curated keywords and examples are central to its linguistic coverage.

## Query Ambiguity

Some user queries can map to multiple topics. For example:

```text
Can I report him?
```

This could refer to eligibility, complaint procedure, workplace scope, evidence, or safety. The current system returns a single best topic. A research-oriented extension could expose top-k candidates or ask clarification questions when several topics score similarly.

## Evaluation Approach

The current tests are functional and example-based. They check dataset loading, selected retrieval cases, and API behavior. A fuller NLP evaluation would require:

- labeled query-to-topic examples
- top-1 accuracy
- top-k recall
- mean reciprocal rank
- separate out-of-scope test cases
- qualitative error analysis by linguistic category
