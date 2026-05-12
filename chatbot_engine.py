import json
import re
from dataclasses import dataclass
from pathlib import Path


try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:  # pragma: no cover - tested by running without sklearn manually.
    TfidfVectorizer = None
    cosine_similarity = None


@dataclass
class TopicMatch:
    topic: dict | None
    score: float
    method: str


class ChatbotKnowledgeBase:
    def __init__(self, topics, suggested_prompts, disclaimer):
        self.topics = topics
        self.suggested_prompts = suggested_prompts
        self.disclaimer = disclaimer
        self.matching_mode = "keyword"
        self._vectorizer = None
        self._topic_matrix = None
        self._build_vector_index()

    @classmethod
    def from_json(cls, path):
        with Path(path).open("r", encoding="utf-8") as data_file:
            data = json.load(data_file)

        return cls(
            topics=data["topics"],
            suggested_prompts=data["suggested_prompts"],
            disclaimer=data["disclaimer"],
        )

    def _build_vector_index(self):
        if TfidfVectorizer is None:
            return

        corpus = [self._topic_document(topic) for topic in self.topics]
        self._vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            stop_words="english",
        )
        self._topic_matrix = self._vectorizer.fit_transform(corpus)
        self.matching_mode = "tfidf+keyword"

    def _topic_document(self, topic):
        return " ".join(
            [
                topic["title"],
                " ".join(topic["keywords"]),
                topic["answer"],
                " ".join(topic["steps"]),
                " ".join(topic.get("examples", [])),
            ]
        )

    def _normalize(self, text):
        return re.sub(r"\s+", " ", text.strip().lower())

    def _keyword_score(self, message, topic):
        normalized = self._normalize(message)
        words = set(re.findall(r"[a-zA-Z]+", normalized))
        score = 0.0

        for keyword in topic["keywords"]:
            keyword = keyword.lower()

            if " " in keyword and keyword in normalized:
                score += 3.0
            elif keyword in words:
                score += 2.0
            elif len(keyword) > 5 and any(word.startswith(keyword[:6]) for word in words):
                score += 1.0

        return score

    def _tfidf_scores(self, message):
        if self._vectorizer is None or self._topic_matrix is None:
            return [0.0 for _ in self.topics]

        query_vector = self._vectorizer.transform([message])
        return cosine_similarity(query_vector, self._topic_matrix).flatten().tolist()

    def find_topic(self, message):
        cleaned = self._normalize(message)
        if not cleaned:
            return TopicMatch(None, 0.0, self.matching_mode)

        vector_scores = self._tfidf_scores(cleaned)
        best_topic = None
        best_score = 0.0

        for index, topic in enumerate(self.topics):
            keyword_score = self._keyword_score(cleaned, topic)
            vector_score = vector_scores[index] * 8
            combined_score = keyword_score + vector_score

            if combined_score > best_score:
                best_topic = topic
                best_score = combined_score

        return TopicMatch(best_topic, best_score, self.matching_mode)

    def answer(self, message):
        if not self._normalize(message):
            return "Please type a question so I can help."

        match = self.find_topic(message)
        if match.topic and match.score >= 1.0:
            return self._format_topic_response(match.topic)

        topic_names = ", ".join(topic["title"].lower() for topic in self.topics[:6])
        return (
            "I can help with workplace harassment questions in Pakistan, including complaint "
            "steps, relevant law, evidence, penalties, and safety options. Try asking about "
            f"{topic_names}.\n\n{self.disclaimer}"
        )

    def _format_topic_response(self, topic):
        steps = "\n".join(f"- {step}" for step in topic["steps"])
        sources = ""

        if topic.get("sources"):
            source_names = ", ".join(source["name"] for source in topic["sources"])
            sources = f"\n\nReference context: {source_names}"

        return f"{topic['answer']}\n\nUseful next steps:\n{steps}{sources}\n\n{self.disclaimer}"

    def context_for_prompt(self, message, limit=3):
        vector_scores = self._tfidf_scores(message)
        ranked_topics = sorted(
            enumerate(self.topics),
            key=lambda item: self._keyword_score(message, item[1]) + vector_scores[item[0]] * 8,
            reverse=True,
        )

        context_blocks = []
        for _, topic in ranked_topics[:limit]:
            context_blocks.append(
                f"{topic['title']}: {topic['answer']} Steps: {' '.join(topic['steps'])}"
            )

        return "\n\n".join(context_blocks)

    def topic_summaries(self):
        return [
            {
                "id": topic["id"],
                "title": topic["title"],
                "keywords": topic["keywords"],
                "examples": topic.get("examples", []),
            }
            for topic in self.topics
        ]
