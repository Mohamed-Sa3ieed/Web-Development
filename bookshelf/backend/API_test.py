import os
import unittest
import json

from flaskr import create_app
from models import setup_db, Book


class bookself_books(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'bookshelf_test'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'Joker2016', '127.0.0.1:5432', self.database_name)
        self.headers = {'Content-Type': 'application/json'}
        setup_db(self.app, self.database_path)

        """define a new book for testing"""
        self.newBook = {
            'title': 'Anansi Boys',
            'author': 'Neil Gaiman',
            'rating': 5
        }

    def tearDown(self):
        """Here we define the needed functionality after each test case"""
        pass

    def test_paginated_books(self):
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/books?page=1000')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_get_book_search_with_result(self):
        res = self.client().post('/books', json={'search': 'Novel'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertEqual(len(data['books']), 1)

    def test_get_book_search_without_result(self):
        res = self.client().post('/books', json={'search': 'applejacks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_books'], 0)
        self.assertEqual(len(data['books']), 0)

    def test_update_book_rating(self):
        res = self.client().patch(
            '/books/22', json={'rating': 1}, content_type="application/json")
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 22).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['rating'], 1)

    def test_400_for_failed_update(self):
        res = self.client().patch('/books/1')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    def test_delete_book(self):
        res = self.client().delete('/books/1')
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
        self.assertEqual(book, None)

    def test_422_if_book_does_not_exist(self):
        res = self.client().delete('/books/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_book(self):
        res = self.client().post('/books', json=self.newBook)
        data = res.get_json()

        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'], True)
        self.assertTrue(len(data['books']))

    def test_405_if_book_creation_not_allowed(self):
        res = self.client().post('/books/45', json=self.newBook)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')


if __name__ == "__main__":
    unittest.main()
