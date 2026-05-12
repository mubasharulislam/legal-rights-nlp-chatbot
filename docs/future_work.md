# Future Work

## Research Trajectory

The current system is a transparent English-language TF-IDF retrieval prototype. A natural next research direction is to move toward multilingual and low-resource NLP for Pakistani legal-information access, where users may ask questions in English, Urdu, Roman Urdu, or code-switched English-Urdu.

## Roman Urdu NLP

Roman Urdu is important because many users write Urdu in Latin script in informal digital communication. It introduces challenges not handled by the current English retrieval pipeline:

- non-standard spelling
- inconsistent tokenization
- English legal terms embedded in Roman Urdu syntax
- informal expressions for harassment, pressure, fear, shame, and authority
- lack of large labeled datasets for this specific domain

Future work could add Roman Urdu query examples, build a domain lexicon, and use character n-grams or fuzzy matching to reduce spelling sensitivity.

## Multilingual Retrieval

The knowledge base could be expanded into a multilingual retrieval corpus with English, Urdu script, and Roman Urdu variants of each topic. Each topic could include multilingual examples and keywords that contribute directly to retrieval.

Potential retrieval settings include:

- English query to English topic
- Urdu query to Urdu topic
- Roman Urdu query to Roman Urdu topic
- code-switched query to multilingual topic representation
- cross-lingual query to English legal-information response

This would allow retrieval evaluation by language and script rather than assuming English performance transfers to multilingual users.

## Code-Switching Detection

A more advanced system could detect whether a query is English, Urdu, Roman Urdu, or code-switched. This would help choose the appropriate preprocessing and retrieval strategy.

Possible routing:

- English queries use the current TF-IDF pipeline.
- Roman Urdu queries use character n-gram retrieval.
- Urdu-script queries use Urdu normalization and tokenization.
- Mixed queries use multilingual embeddings or hybrid sparse-dense retrieval.

Code-switching detection would also improve error analysis by separating retrieval failures from language identification failures.

## Semantic Embeddings

The current sparse vector method depends on lexical overlap. Future work could compare TF-IDF against dense semantic sentence embeddings that represent queries and topics in a shared vector space.

This may improve retrieval for indirect paraphrases such as:

```text
My supervisor is making my job difficult after I spoke up.
```

which may imply retaliation even without explicit keywords.

Suggested experiments:

- compare TF-IDF with sentence-transformer embeddings
- evaluate multilingual embeddings for English, Urdu, and Roman Urdu
- test hybrid sparse-dense retrieval
- measure performance on ambiguous and indirect queries
- inspect whether semantic retrieval increases false positives in legal contexts

## Transformer-Based Retrieval

Transformer-based retrieval could be explored in two stages:

1. A bi-encoder model embeds queries and topic documents for efficient nearest-neighbor retrieval.
2. A cross-encoder reranker scores top-k query-topic pairs more carefully.

Possible architecture:

```text
User query
  -> sparse TF-IDF retrieval
  -> dense multilingual embedding retrieval
  -> top-k candidate merge
  -> transformer reranking
  -> confidence-aware answer or clarification question
```

This would preserve the interpretability of sparse retrieval while testing whether transformer models improve recall, paraphrase handling, and multilingual matching.

## Low-Resource Language Processing

Urdu and Roman Urdu legal-information retrieval are low-resource settings, especially for sensitive domains such as workplace harassment. Future work should focus on dataset construction as much as model design.

Important next steps:

- create a labeled multilingual query set
- collect paraphrases from English, Urdu, Roman Urdu, and code-switched usage
- document spelling variants and culturally specific expressions
- evaluate retrieval separately by language and script
- report top-1 accuracy, top-k recall, MRR, and error categories
- design privacy-preserving annotation guidelines
- consult legal and language experts before deployment

The long-term goal is a multilingual legal-information retrieval system that handles low-resource, code-switched, and informal user language while remaining transparent, bounded, and safe for a sensitive social-impact domain.
