# Architecture Diagram

This diagram shows the main query-to-response pipeline for the retrieval-based NLP legal chatbot.

```mermaid
flowchart LR
    user["User Query"]
    normalize["Query Normalization"]
    retrieve["TF-IDF + Keyword Retrieval"]
    rank["Topic Ranking"]
    format["Response Formatter"]
    api["Flask API"]
    frontend["Frontend Interface"]

    user --> normalize
    normalize --> retrieve
    retrieve --> rank
    rank --> format
    format --> api
    api --> frontend

    subgraph kb["Structured Legal Knowledge Base"]
        topics["Topic Documents"]
        keywords["Keywords + Examples"]
        answers["Answers + Next Steps"]
    end

    topics --> retrieve
    keywords --> retrieve
    answers --> format

    classDef primary fill:#0f766e,color:#ffffff,stroke:#0b5f59,stroke-width:1px;
    classDef process fill:#ffffff,color:#172033,stroke:#cbd5e1,stroke-width:1px;
    classDef data fill:#f8fafc,color:#334155,stroke:#cbd5e1,stroke-width:1px;

    class user,frontend primary;
    class normalize,retrieve,rank,format,api process;
    class topics,keywords,answers data;
```

## Pipeline Summary

1. **User Query:** the user enters a natural-language workplace harassment question.
2. **Query Normalization:** text is lowercased, stripped, and whitespace-normalized.
3. **TF-IDF + Keyword Retrieval:** the query is compared against topic documents using sparse vector similarity and domain keyword scoring.
4. **Topic Ranking:** topics are ranked by combined retrieval score.
5. **Response Formatter:** the selected topic is converted into an answer with practical next steps, source context, and disclaimer.
6. **Flask API:** the response is returned through the `/chat` JSON endpoint.
7. **Frontend Interface:** the browser chat UI displays the response.
