import unittest
from app.modules.normalizer import normalize_text
from app.modules.tokenizer import tokenize
from app.modules.document_loader import load_documents
from app.modules.inverted_index import InvertedIndex
from app.modules.wildcard_processor import expand_wildcard
from app.modules.query_processor import QueryProcessor
from app import create_app

class CoreModuleTests(unittest.TestCase):
    def setUp(self):
        self.docs = {
            "one.txt": "Information retrieval uses an inverted index.",
            "two.txt": "The database stores data for searching.",
            "three.txt": "Information systems process data and information."
        }
        self.index = InvertedIndex()
        self.index.build(self.docs)
        self.processor = QueryProcessor(self.index)

    def test_case_folding(self):
        self.assertEqual(normalize_text("Straße"), "strasse")

    def test_tokenizer(self):
        self.assertEqual(tokenize("Hello, WORLD!"), ["hello", "world"])

    def test_inverted_index_positions(self):
        self.assertEqual(self.index.positions("information", "three.txt"), [0, 5])
        self.assertEqual(self.index.term_frequency("information", "three.txt"), 2)

    def test_wildcard_star(self):
        self.assertEqual(expand_wildcard("infor*", self.index.vocabulary), ["information"])

    def test_wildcard_question(self):
        self.assertEqual(expand_wildcard("dat?", {"data", "date", "database"}), ["data", "date"])

    def test_and_query(self):
        results = self.processor.search("information data")
        self.assertEqual([r["document"] for r in results], ["three.txt"])

    def test_or_query(self):
        results = self.processor.search("retrieval OR database")
        self.assertEqual({r["document"] for r in results}, {"one.txt", "two.txt"})

    def test_wildcard_query(self):
        results = self.processor.search("infor*")
        self.assertEqual({r["document"] for r in results}, {"one.txt", "three.txt"})

    def test_reject_mixed_operators(self):
        with self.assertRaises(ValueError):
            self.processor.search("information AND data OR database")

class WebTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"IndexLab", response.data)

    def test_stats_endpoint(self):
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.json["document_count"], 0)

    def test_search_endpoint(self):
        response = self.client.get("/api/search?q=information")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.json["count"], 0)

    def test_empty_query(self):
        response = self.client.get("/api/search?q=")
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
