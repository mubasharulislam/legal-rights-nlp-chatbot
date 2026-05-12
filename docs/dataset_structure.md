# Dataset Structure

## Overview

The chatbot uses a structured JSON knowledge base stored in `data/legal_knowledge.json`. The dataset is designed as a small domain corpus for retrieval-based legal information access.

The dataset contains:

- a global legal-information disclaimer
- suggested prompts for the user interface
- topic entries used as retrievable documents

## Top-Level Schema

```json
{
  "disclaimer": "This is general legal information...",
  "suggested_prompts": [
    "What is workplace harassment?",
    "How do I file a complaint?"
  ],
  "topics": [
    {
      "id": "complaint",
      "title": "How to file a complaint",
      "keywords": [],
      "examples": [],
      "answer": "...",
      "steps": [],
      "sources": []
    }
  ]
}
```

## Field Descriptions

### `disclaimer`

A global disclaimer appended to local retrieval answers. It clarifies that the chatbot provides general legal information and does not replace legal advice or official support services.

### `suggested_prompts`

A list of example questions shown in the browser interface. These prompts also communicate the system's intended scope to users.

### `topics`

The main corpus. Each topic functions as both:

- a retrieval document for matching
- a response template for the selected answer

## Topic Schema

### `id`

A stable machine-readable identifier for the topic.

Example:

```json
"id": "retaliation"
```

### `title`

A human-readable topic name.

Example:

```json
"title": "Retaliation or pressure"
```

The title contributes to the TF-IDF document representation.

### `keywords`

A manually curated list of terms and phrases associated with the topic.

Example:

```json
"keywords": [
  "retaliation",
  "threatened after reporting",
  "pressure",
  "blackmail",
  "victimisation"
]
```

Keywords support both direct keyword scoring and TF-IDF document construction. They operate as a small domain lexicon.

### `examples`

Example user queries that may map to the topic.

Example:

```json
"examples": [
  "I am being threatened after reporting",
  "pressure to withdraw complaint"
]
```

Examples improve retrieval by adding realistic user phrasing to the topic document.

### `answer`

The main response text returned when the topic is selected. This text is intentionally concise and informational.

### `steps`

A list of practical next steps. These are appended to the answer under the "Useful next steps" heading.

### `sources`

Reference context for the topic. Each source includes a name and URL or local reference.

Example:

```json
{
  "name": "Protection against Harassment of Women at the Workplace Act, 2010",
  "url": "https://natlex.ilo.org/..."
}
```

## Dataset as a Retrieval Corpus

During indexing, each topic is converted into a single text document:

```text
title + keywords + answer + steps + examples
```

This design gives the retriever several kinds of lexical evidence:

- formal legal terminology from titles and answers
- user-centered vocabulary from examples
- domain signals from keywords
- procedural vocabulary from steps

## Current Topic Coverage

The dataset covers workplace harassment topics such as:

- definition of workplace harassment
- types of harassment
- who can complain
- workplace scope
- relevant Pakistani law
- employer responsibility
- inquiry committee
- complaint process
- ombudsperson route
- evidence and witnesses
- retaliation
- confidentiality
- penalties and appeals
- online harassment
- immediate safety
- emotional support

## Dataset Limitations

The dataset is manually curated and limited in size. It does not yet include:

- a labeled retrieval benchmark
- Urdu or Roman Urdu examples
- systematic paraphrase coverage
- expert-reviewed coverage for every possible legal scenario
- jurisdiction-specific referral details for all provinces
- metadata for topic difficulty, risk level, or urgency

For a research version, the dataset should be expanded with labeled queries, paraphrases, multilingual examples, and error categories.
