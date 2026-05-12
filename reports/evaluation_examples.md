# Evaluation Examples

## Overview

This document presents realistic qualitative evaluation examples for the Legal Rights Chatbot. The goal is to show how the current TF-IDF plus keyword retrieval system behaves across successful, failed, and ambiguous user queries.

These examples are not a formal benchmark. They are diagnostic cases for understanding retrieval behavior, lexical matching, ambiguity, and the limits of sparse vector methods in a sensitive legal-information domain.

Current retrieval method:

```text
TF-IDF cosine similarity + keyword scoring
```

The system retrieves one best-matching topic when the combined score is at least `1.0`. If the score is below that threshold, it returns a fallback response describing the chatbot's supported scope.

## Successful Retrievals

### Example 1: Worker Coverage

User query:

```text
Can an intern complain about workplace harassment?
```

Retrieved topic:

```text
Who can complain
```

Observed score:

```text
7.885
```

Retrieved response excerpt:

```text
The 2022 amendment broadened important definitions. The law is not limited only to one narrow type of worker.
```

Explanation:

The query contains strong lexical overlap with topic keywords such as `intern`, `intern complain`, and `complain`. The match is successful because both the user query and the topic document contain explicit worker-status vocabulary.

Retrieval behavior:

- high keyword match
- useful TF-IDF overlap
- correct topic selected
- response directly addresses the user's eligibility question

### Example 2: Online Evidence

User query:

```text
Can WhatsApp messages be evidence?
```

Retrieved topic:

```text
Online harassment connected to work
```

Observed score:

```text
8.827
```

Retrieved response excerpt:

```text
Online messages, calls, emails, social-media contact, or image-based threats can matter if they are connected to work, study, training, employment, or power over you.
```

Explanation:

The query is retrieved successfully because the knowledge base contains platform-specific keywords such as `whatsapp`, `whatsapp messages`, and `whatsapp evidence`. The topic also includes online communication terms in the answer and steps.

Retrieval behavior:

- strong platform-specific keyword match
- strong bigram overlap on `WhatsApp messages`
- relevant practical response about preserving screenshots and message context

Note:

This query could also reasonably map to the broader `Evidence and documentation` topic. The current system returns only one topic, so it selects the highest-scoring online-harassment topic rather than showing both relevant candidates.

### Example 3: Retaliation

User query:

```text
I am being threatened after reporting harassment
```

Retrieved topic:

```text
Retaliation or pressure
```

Observed score:

```text
10.921
```

Retrieved response excerpt:

```text
Pressure, threats, forced resignation, unfair transfer, salary action, or punishment because you complained can be very serious.
```

Explanation:

This is a strong retrieval case because the query contains the phrase `threatened after reporting`, which is close to the topic's manually curated keyword phrases. The topic is also semantically appropriate because the user describes harm after reporting.

Retrieval behavior:

- strong phrase-level keyword evidence
- correct legal/practical category
- high score relative to other topics

### Example 4: Complaint Filing

User query:

```text
How do I file a complaint?
```

Retrieved topic:

```text
How to file a complaint
```

Observed score:

```text
8.415
```

Retrieved response excerpt:

```text
A complaint can usually be made to your organization's inquiry committee or to the relevant ombudsperson.
```

Explanation:

The query directly matches key topic vocabulary: `file`, `complaint`, and `complain`. This is an expected success case for sparse retrieval because the user wording closely matches the topic title, keywords, and examples.

Retrieval behavior:

- high title and keyword overlap
- low ambiguity
- clear procedural answer

## Ambiguous Queries

### Example 5: Broad Help-Seeking Query

User query:

```text
What can I do now?
```

Retrieved topic:

```text
None
```

Observed score:

```text
0.000
```

System response type:

```text
Fallback response
```

Explanation:

This query is too general for the current lexical retrieval system. It does not contain domain-specific words such as `complaint`, `evidence`, `harassment`, `threat`, or `safety`. A human reader would need context from previous turns, but the system currently treats each query independently.

Retrieval behavior:

- no strong lexical overlap
- no topic passes threshold
- fallback response is appropriate

Research implication:

This case suggests the need for dialogue context, clarification questions, or a default triage flow. A stronger system might ask:

```text
Are you asking about filing a complaint, collecting evidence, immediate safety, or emotional support?
```

### Example 6: Underspecified Reporting Query

User query:

```text
Can I report him?
```

Retrieved topic:

```text
How to file a complaint
```

Observed score:

```text
3.554
```

Retrieved response excerpt:

```text
A complaint can usually be made to your organization's inquiry committee or to the relevant ombudsperson.
```

Explanation:

The query is ambiguous. It could refer to whether the user is protected, how to file a complaint, whether the workplace has jurisdiction, or what evidence is needed. The system selects the complaint topic because `report` is included as a keyword for complaint filing.

Retrieval behavior:

- relevant but incomplete answer
- single-topic retrieval hides other plausible interpretations
- no clarification question is asked

Research implication:

This is a good candidate for top-k retrieval. The system could show or internally consider:

- `How to file a complaint`
- `Who can complain`
- `Where the law may apply`
- `Evidence and documentation`

## Failed or Partially Failed Retrievals

### Example 7: Retaliation Expressed Indirectly

User query:

```text
My supervisor is making my job difficult after I spoke up
```

Retrieved topic:

```text
Types of harassment
```

Observed score:

```text
3.300
```

Retrieved response excerpt:

```text
Common forms include unwanted sexual comments or jokes, pressure for dates or sexual favors, repeated messages or calls...
```

Expected topic:

```text
Retaliation or pressure
```

Explanation:

This is a realistic retrieval error. The phrase `after I spoke up` implies possible retaliation, but the query does not use explicit terms such as `retaliation`, `threat`, `pressure`, `fired`, `transfer`, or `after complaint`. The word `job` also appears in the harassment-types topic, which may pull the query toward that document.

Retrieval behavior:

- semantically relevant clue is implicit rather than lexical
- sparse vector retrieval cannot infer that `after I spoke up` means reporting or complaining
- wrong but topically adjacent answer is returned

Possible improvement:

Add phrases such as `spoke up`, `after speaking up`, `made my job difficult`, and `treated me badly after reporting` to the retaliation topic examples or keywords.

### Example 8: Out-of-Scope Legal Query

User query:

```text
Do I need a lawyer for divorce?
```

Best internal match:

```text
Fear of not being believed
```

Observed score:

```text
0.441
```

System response type:

```text
Fallback response
```

Explanation:

The system correctly does not return the low-scoring internal match because the score is below the threshold. Although `lawyer` appears in some knowledge-base steps, the query is about divorce, which is outside the chatbot's workplace harassment scope.

Retrieval behavior:

- weak lexical overlap with legal-support language
- below-threshold match
- fallback response prevents an irrelevant legal answer

Research implication:

This is a successful rejection case. It shows why the relevance threshold is important even when some token overlap exists.

### Example 9: Out-of-Scope Non-Employment Query

User query:

```text
My landlord is not returning my deposit
```

Retrieved topic:

```text
None
```

Observed score:

```text
0.000
```

System response type:

```text
Fallback response
```

Explanation:

The query has no meaningful overlap with the workplace harassment corpus. The system returns the fallback response rather than forcing a topic match.

Retrieval behavior:

- no relevant topic terms
- no topic passes threshold
- correct out-of-scope handling

### Example 10: Roman Urdu / Code-Switched Query

User query:

```text
Mera boss mujhe tang kar raha hai
```

Best internal match:

```text
Retaliation or pressure
```

Observed score:

```text
0.669
```

System response type:

```text
Fallback response
```

Explanation:

The query is Roman Urdu. The current system is configured for English lexical matching, so it does not recognize expressions such as `mujhe tang kar raha hai`. The word `boss` may weakly overlap with workplace-related topics, but the score remains below threshold.

Retrieval behavior:

- language mismatch
- no Roman Urdu normalization
- no bilingual lexicon
- fallback response returned

Possible improvement:

Add multilingual support through Roman Urdu examples, bilingual keyword lists, transliteration handling, character n-grams, or multilingual sentence embeddings.

## Summary of Retrieval Behavior

The current retrieval system performs best when:

- the query contains explicit legal or procedural terms
- the query overlaps with manually curated keywords
- the user asks a short, direct question
- platform-specific terms such as `WhatsApp` are present in the dataset

The system is weaker when:

- the user describes the situation indirectly
- the query requires pragmatic inference
- multiple topics are plausible
- the query is long and narrative
- the query uses Roman Urdu, Urdu, or code-switching
- the query is outside the workplace harassment domain but shares generic legal words

## Suggested Evaluation Extensions

Future evaluation should include:

- top-k ranked topics for every query
- expected topic labels
- multiple valid labels for ambiguous queries
- separate labels for out-of-scope queries
- score distributions for successful and failed retrievals
- error categories such as lexical mismatch, ambiguity, language mismatch, and missing knowledge-base coverage

A structured evaluation file could represent each example as:

```json
{
  "query": "Can I report him?",
  "expected_topics": ["complaint", "who_is_protected", "workplace_scope"],
  "retrieved_topic": "complaint",
  "case_type": "ambiguous",
  "notes": "Relevant but underspecified; top-k retrieval would be more informative."
}
```
