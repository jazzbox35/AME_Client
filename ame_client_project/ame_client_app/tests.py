from django.test import TestCase, RequestFactory
from . import views


class DeliberateTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_empty_proposition_list_returns_error(self):
        """Deliberate should return an error when no propositions exist."""
        views.propositions = {"proposition": []}
        request = self.factory.get('/deliberate', {'case': '1'})
        response = views.Deliberate(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "decision": ["ERROR -- Last proposition must be System 2 and Level 1 or Level 2."],
            "judgments": [[]]
        })
