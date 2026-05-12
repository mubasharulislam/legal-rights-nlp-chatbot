# Error Analysis

## Overview

The current chatbot uses TF-IDF and keyword matching, so most errors are retrieval errors. An incorrect response usually means that the wrong topic was ranked highest, the correct topic did not pass the relevance threshold, or the query was outside the supported domain.

## Lexical Mismatch

TF-IDF depends on surface-level word overlap. If a user describes a concept using wording that is absent from the topic document, the correct topic may receive a low score.

Example:

```text
My supervisor is making my job difficult after I spoke up.
```

This may imply retaliation, but the query does not explicitly use terms such as `retaliation`, `threat`, `pressure`, `complaint`, or `after reporting`. Sparse retrieval may therefore rank a related but incorrect topic.

## Ambiguous Queries

Some questions are underspecified:

```text
What can I do now?
Can I report him?
```

These queries may refer to complaint filing, evidence preservation, worker eligibility, ombudsperson routes, emotional support, or immediate safety. The current system selects one best topic and does not ask clarifying questions.

## Domain-Specific Vocabulary

Workplace harassment law includes formal terms such as:

- `ombudsperson`
- `inquiry committee`
- `competent authority`
- `retaliation`
- `victimisation`
- `workplace scope`

Users may instead write informal phrases such as:

- `HR`
- `boss`
- `office people`
- `company ignored me`
- `revenge`
- `pressure`

The manually curated keyword lists help bridge this gap, but coverage is incomplete and must be expanded through evaluation.

## Semantic Limitations

The system does not model entailment, causality, temporal order, negation, or speaker intent. It may struggle to distinguish between:

- "I was threatened before filing a complaint" and "I was threatened after filing a complaint"
- "Can WhatsApp messages be evidence?" and "Someone deleted WhatsApp messages"
- "My employer ignored my complaint" and "I ignored my employer's complaint process"
- "I am afraid of false accusations" and "Someone made a false accusation against me"

These distinctions matter in legal-information contexts, but sparse vector methods mainly compare token overlap.

## Retrieval Error Types

Expected error categories include:

- **False positive:** a topic is retrieved because of shared vocabulary but is not actually relevant.
- **False negative:** the correct topic exists but does not share enough terms with the query.
- **Near miss:** the correct topic is ranked second or third but only the top topic is returned.
- **Keyword over-triggering:** one strong keyword dominates the score despite broader query context.
- **Long-query dilution:** important signals are weakened by unrelated narrative detail.
- **Language mismatch:** Roman Urdu, Urdu, or code-switched queries do not match the English corpus well.

## Limitations of Sparse Vector Methods

TF-IDF is interpretable and efficient, but it has known limitations:

- it represents text as weighted terms rather than structured meaning
- it does not recognize synonyms unless they appear in the corpus
- it is sensitive to spelling variation and morphology
- it does not handle Urdu, Roman Urdu, or code-switching without extra preprocessing
- it may overweight rare terms that are not central to user intent
- it cannot reliably capture negation, sequence, or legal conditions

## Evaluation Recommendations

A stronger evaluation setup should include:

- top-k ranked topics for each query
- expected topic labels
- multiple valid labels for ambiguous queries
- out-of-scope labels
- score distributions for successful and failed retrievals
- failure categories such as lexical mismatch, ambiguity, language mismatch, and missing coverage

Qualitative examples are available in `reports/evaluation_examples.md`.
