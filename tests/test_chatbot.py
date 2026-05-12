import unittest

from app import app, get_response, knowledge_base
from chatbot_engine import ChatbotKnowledgeBase


class ChatbotProjectTests(unittest.TestCase):
    def test_dataset_loads_expected_topics(self):
        kb = ChatbotKnowledgeBase.from_json("data/legal_knowledge.json")

        self.assertGreaterEqual(len(kb.topics), 20)
        self.assertIn("What is workplace harassment?", kb.suggested_prompts)

    def test_intern_question_matches_worker_coverage(self):
        reply = get_response("Can an intern complain about workplace harassment?")

        self.assertIn("intern", reply.lower())
        self.assertIn("general legal information", reply.lower())

    def test_whatsapp_question_matches_online_evidence(self):
        reply = get_response("Can WhatsApp messages be evidence?")

        self.assertTrue("online" in reply.lower() or "screenshots" in reply.lower())
        self.assertIn("messages", reply.lower())

    def test_retaliation_question_matches_pressure_topic(self):
        reply = get_response("I am being threatened after reporting harassment")

        self.assertIn("threat", reply.lower())
        self.assertTrue("retaliation" in reply.lower() or "pressure" in reply.lower())

    def test_topics_endpoint_returns_dataset_summary(self):
        client = app.test_client()
        response = client.get("/topics")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(knowledge_base.topics))
        self.assertTrue({"id", "title", "keywords", "examples"}.issubset(response.json[0]))

    def test_chat_endpoint_returns_reply(self):
        client = app.test_client()
        response = client.post("/chat", json={"message": "How do I file a complaint?"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("reply", response.json)
        self.assertIn("complaint", response.json["reply"].lower())


if __name__ == "__main__":
    unittest.main()
