import unittest
from flask_testing import TestCase
from app import app, load_scores, process_leaderboard, cache

class TestLeaderboardApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['CACHE_TYPE'] = 'null'
        cache.init_app(app)
        return app

    def test_scores_count(self):
        """ Test that only users with at least 3 submissions are included. """
        data = [
            {'name': 'User1', 'submissions': [{'score': 80}, {'score': 90}]},  # Only 2 submissions
            {'name': 'User2', 'submissions': [{'score': 70}, {'score': 60}, {'score': 50}]}  # 3 submissions
        ]
        result = process_leaderboard(data)
        self.assertEqual(len(result), 1)  # Only User2 should be included

    def test_top_24_scores(self):
        """ Test that only the top 24 scores are counted for each user. """
        data = [{'name': 'User1', 'submissions': [{'score': i} for i in range(1, 100)]}]
        result = process_leaderboard(data)
        expected_score = sum(range(76, 100))  # Top 24 scores from 76 to 99
        self.assertEqual(result[0][1], expected_score)

    def test_user_ranking_by_score_sum(self):
        """ Test that users are ranked by the sum of their best submission scores. """
        data = [
            {'name': 'Alice', 'submissions': [{'score': 95}, {'score': 80}, {'score': 75}]},
            {'name': 'Bob', 'submissions': [{'score': 65}, {'score': 60}, {'score': 55}]}
        ]
        result = process_leaderboard(data)
        self.assertEqual(result[0][0], 'Alice')
        self.assertEqual(result[1][0], 'Bob')
        self.assertGreater(result[0][1], result[1][1])  # Alice's score should be higher than Bob's

    def test_api_leaderboard_no_match_found(self):
        """Test the API for no matches found."""
        response = self.client.get('/api/leaderboard?query=Nonexistent&page=1&per_page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)  # Expecting empty results for nonexistent query

if __name__ == '__main__':
    unittest.main()
