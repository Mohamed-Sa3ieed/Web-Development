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
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'Joker2016', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Add dummy question for insertion
        self.new_question = {
            'question': 'what is the current year?',
            'answer': 2020,
            'difficulty': 1,
            'category': 4
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'], 6)
        self.assertTrue(data['categories'])

    def test_paginate_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertIsNone(data['currentCategory'])
        self.assertTrue(data['total_questions'])

    def test_404_send_invalid_questions_pagination(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_422_delete_does_not_exist_question(self):
        res = self.client().delete('/questions/100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_405_question_creation_not_allowed(self):
        res = self.client().post('questions/1000', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 405)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_get_category_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']), 0)
        self.assertTrue(data['total_questions'], 0)
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['currentCategory'], {'1':'Science'})

    def test_404_if_category_does_not_exists(self):
        res = self.client().get('/categories/100/1questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['message'], 'Not Found')

    def test_get_quiz_next_question(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['question'], None)

    def test_405_quiz_begin_not_allowed(self):
        res = self.client().post('/quizzes/1', json={
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['message'], 'Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
