# Retrieval Evaluation Examples

This document provides realistic evaluation examples for the legal NLP chatbot's retrieval behavior. The examples are designed for qualitative analysis rather than formal benchmark reporting.

Each case includes:

- user query
- expected topic
- retrieved topic
- success or failure explanation

The examples focus on lexical mismatch, ambiguity, legal terminology variation, and paraphrase handling.

## Evaluation Cases

| Case | User Query | Expected Topic | Retrieved Topic | Outcome |
| --- | --- | --- | --- | --- |
| 1 | What counts as workplace harassment? | What workplace harassment means | What workplace harassment means | Success |
| 2 | Can a trainee complain if she is harassed at work? | Who can complain | Who can complain | Success |
| 3 | My company is ignoring my complaint | Employer responsibilities | Employer responsibilities | Success |
| 4 | Where do I submit a harassment application? | How to file a complaint | How to file a complaint | Success |
| 5 | Can WhatsApp screenshots help prove harassment? | Evidence and documentation / Online harassment connected to work | Online harassment connected to work | Partial success |
| 6 | What if no one believes me? | Fear of not being believed | Fear of not being believed | Success |
| 7 | Can I report him? | Ambiguous: complaint process, eligibility, workplace scope | How to file a complaint | Partial success |
| 8 | What should I do now? | Ambiguous: safety, complaint, evidence, support | Fallback response | Partial success |
| 9 | My supervisor is making my job difficult after I spoke up | Retaliation or pressure | Types of harassment | Failure |
| 10 | He keeps contacting me after office hours on Instagram | Online harassment connected to work / workplace scope | Online harassment connected to work | Success |
| 11 | Who investigates the case inside the office? | Inquiry committee | Inquiry committee | Success |
| 12 | Can the harasser be fired? | Possible penalties | Possible penalties | Success |
| 13 | I want to challenge the decision | Appeals and next steps after decision | Appeals and next steps after decision | Success |
| 14 | My boss is taking revenge after my report | Retaliation or pressure | Retaliation or pressure | Success |
| 15 | I need a sample letter for HR | What to write in a complaint | What to write in a complaint | Success |

## Detailed Analysis

### 1. Direct Lexical Match

User query:

```text
What counts as workplace harassment?
```

Expected topic:

```text
What workplace harassment means
```

Retrieved topic:

```text
What workplace harassment means
```

Explanation:

This is a successful retrieval because the query contains direct lexical overlap with the topic title, examples, and keywords. Terms such as `workplace`, `harassment`, and `counts` are represented in the knowledge base through the topic title and example query `what counts as harassment`.

Retrieval behavior:

- strong keyword overlap
- strong topic-title similarity
- low ambiguity

### 2. Legal Coverage Variation

User query:

```text
Can a trainee complain if she is harassed at work?
```

Expected topic:

```text
Who can complain
```

Retrieved topic:

```text
Who can complain
```

Explanation:

This query uses worker-status vocabulary. The topic includes related terms such as `trainee`, `intern`, `employee`, `contract`, `freelancer`, and `student`. The system succeeds because the legal category is explicitly represented in the manually curated keyword list.

Retrieval behavior:

- domain keyword match
- clear legal-information intent
- successful handling of employment-status variation

### 3. Legal Terminology Variation

User query:

```text
Where do I submit a harassment application?
```

Expected topic:

```text
How to file a complaint
```

Retrieved topic:

```text
How to file a complaint
```

Explanation:

The user says `application` rather than `complaint`. This is a successful legal terminology variation case because the complaint topic includes keywords such as `complaint`, `complain`, `report`, `file`, `submit`, `application`, and `case`.

Retrieval behavior:

- successful synonym coverage through manual keywords
- good mapping from informal/legal-administrative vocabulary to the complaint topic

### 4. Platform-Specific Evidence Query

User query:

```text
Can WhatsApp screenshots help prove harassment?
```

Expected topic:

```text
Evidence and documentation / Online harassment connected to work
```

Retrieved topic:

```text
Online harassment connected to work
```

Explanation:

This is a partial success. The retrieved topic is relevant because it discusses online messages and work-connected digital harassment. However, the query also asks about proof and screenshots, which could map to `Evidence and documentation`.

Retrieval behavior:

- strong match on `WhatsApp`
- strong match on online communication vocabulary
- one-topic retrieval hides another valid topic

Improvement:

Return top-k topics or merge evidence guidance when both online communication and proof-related terms are present.

### 5. Ambiguous Reporting Query

User query:

```text
Can I report him?
```

Expected topic:

```text
Ambiguous: complaint process, eligibility, workplace scope
```

Retrieved topic:

```text
How to file a complaint
```

Explanation:

This is a partial success. The retrieved topic is relevant because `report` is a keyword for complaint filing. However, the query is underspecified. The user may be asking whether they are eligible to complain, where to report, whether the incident counts as workplace harassment, or what evidence is needed.

Retrieval behavior:

- keyword `report` drives the match
- single-label retrieval gives a plausible but incomplete answer
- ambiguity is not resolved through clarification

Improvement:

When a query is short and ambiguous, the chatbot could ask a clarification question or return multiple possible topics.

### 6. Broad Context-Dependent Query

User query:

```text
What should I do now?
```

Expected topic:

```text
Ambiguous: safety, complaint, evidence, support
```

Retrieved topic:

```text
Fallback response
```

Explanation:

This is a reasonable fallback. The query contains no topic-specific vocabulary. A human might infer urgency or distress from context, but the current system does not use conversation history or dialogue state. Since no topic passes the retrieval threshold, the system returns a scope-setting fallback response.

Retrieval behavior:

- low lexical overlap
- no clear topic match
- fallback prevents an arbitrary answer

Improvement:

Add a triage-style clarification response for broad help-seeking queries.

### 7. Lexical Mismatch in Retaliation Query

User query:

```text
My supervisor is making my job difficult after I spoke up
```

Expected topic:

```text
Retaliation or pressure
```

Retrieved topic:

```text
Types of harassment
```

Explanation:

This is a retrieval failure caused by lexical mismatch. The phrase `after I spoke up` implies possible retaliation, but the query does not contain explicit terms such as `retaliation`, `threat`, `pressure`, `complaint`, `reporting`, or `victimisation`. The word `job` overlaps with the harassment-types topic, so the sparse retrieval model selects a related but less appropriate topic.

Retrieval behavior:

- implied meaning is not captured by lexical overlap
- sparse vector method cannot infer retaliation from `after I spoke up`
- returned topic is related to harassment but misses the user's likely concern

Improvement:

Add paraphrases such as `after I spoke up`, `after speaking up`, `made my job difficult`, and `treated me badly after reporting` to the retaliation topic. A semantic embedding model may also improve this case.

### 8. Informal Retaliation Paraphrase

User query:

```text
My boss is taking revenge after my report
```

Expected topic:

```text
Retaliation or pressure
```

Retrieved topic:

```text
Retaliation or pressure
```

Explanation:

This is a successful paraphrase case because the topic includes informal and legal variants such as `revenge`, `after reporting`, `after complaint`, `threat`, `pressure`, and `victimisation`. The query does not use the formal term `retaliation`, but it still shares enough vocabulary with the topic.

Retrieval behavior:

- successful informal vocabulary mapping
- keyword list covers non-technical phrasing
- correct topic selected

### 9. Complaint Drafting Variation

User query:

```text
I need a sample letter for HR
```

Expected topic:

```text
What to write in a complaint
```

Retrieved topic:

```text
What to write in a complaint
```

Explanation:

This is a successful legal-document variation case. The user does not say `complaint draft`, but the topic includes terms such as `write`, `draft`, `format`, `application`, `letter`, `template`, and `sample`.

Retrieval behavior:

- strong keyword coverage
- successful mapping from everyday request to legal-document topic

### 10. Appeal Terminology

User query:

```text
I want to challenge the decision
```

Expected topic:

```text
Appeals and next steps after decision
```

Retrieved topic:

```text
Appeals and next steps after decision
```

Explanation:

This is a successful legal terminology variation case. The user says `challenge` rather than `appeal`, but both terms are included in the appeal topic's vocabulary.

Retrieval behavior:

- synonym-like legal keyword match
- correct mapping to post-decision procedure

## Summary

The retrieval system performs well when the query contains:

- direct legal terms represented in the knowledge base
- manually curated synonym or paraphrase variants
- topic-specific workplace vocabulary
- platform-specific evidence terms such as `WhatsApp` or `screenshots`

The system is weaker when:

- the relevant meaning is implied rather than explicit
- the query is short and underspecified
- multiple topics are valid
- legal intent depends on context from previous turns
- paraphrases are not represented in keywords or examples

These examples suggest that the next evaluation step should use top-k retrieval, ambiguity labels, and a larger paraphrase set for legally important concepts such as retaliation, complaint filing, evidence, and workplace scope.
