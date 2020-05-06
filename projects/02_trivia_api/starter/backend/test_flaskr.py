import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:grape@localhost:5432/trivia"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["categories"]), 6)

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_fail_get_paginated_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data["message"], "Not Found")

    def test_post_question(self):
        res = self.client().post('/questions', json={
            "question": "Who are you?",
            "answer": "The chosen one.",
            "category": 1,
            "difficulty": 2
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        question = Question.query.filter(
            Question.id == data['created']).one_or_none()
        self.assertNotEqual(question, None)

    def test_fail_post_question(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    # def test_delete_question(self):
    #     res = self.client().delete('/questions/4')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['deleted'], 4)
    #     question = Question.query.filter(
    #         Question.id == 4).one_or_none()
    #     self.assertEqual(question, None)

    def test_fail_delete_question(self):
        res = self.client().delete('/questions/450')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_search(self):
        res = self.client().post('/questions/search', json={
            "search_term": "cassius",
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 1)

    def test_search_pages(self):
        res = self.client().post('/questions/search?page=2', json={
            "search_term": "the",
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 11)
        self.assertEqual(len(data['questions']), 1)

    def test_fail_search(self):
        res = self.client().post('/questions/search?page=3', json={

        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_get_categories_questions(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], 4)
        self.assertEqual(len(data['questions']), 4)

    def test_fail_get_categories_questions(self):
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_quizzes(self):
        res = self.client().post('/quizzes', json={
            "quiz_category": "3",
            "previous_questions": [13, 15]
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIs(data['question']['id'], 14)

    def test_fail_get_quizzes(self):
        res = self.client().post('/quizzes', json={

        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
