"""
Unit tests module
"""
from src.database import DatabaseManager

import unittest


class TestDatabase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_name = 'abc'
        self.user_history = {
            'user_id': 1,
            'text': 'abc bbcc',
            'summary': 'abc and ABC',
            'name': 'char' 
        }
        self.db = DatabaseManager(location='local')
        self.users = self.db.users_collection
        self.history = self.db.users_history
    
    def setUp(self):
        self.users.delete_many({})
        self.history.delete_many({})
    
    def tearDown(self):
        self.db.client.close()
    
    def test_add_user(self):
        self.db.add_user(username=self.user_name)

        self.assertEqual(1, self.users.count_documents({}))
        self.assertIsNone(self.db.user_exists('cba'))
        self.assertIsNotNone(self.db.user_exists(self.user_name))

    def test_query_user(self):
        self.db.add_user(username=self.user_name)
        uid = self.db.user_exists(username=self.user_name)
        user_found = self.db.get_user(uid)

        self.assertEqual(user_found['username'], self.user_name)
    
    def test_delete_user(self):
        self.db.add_user(username=self.user_name)
        uid = self.db.user_exists(username=self.user_name)
        self.db.delete_user(uid)

        self.assertEqual(0, self.users.count_documents({}))
    
    def test_add_summary(self):
        summary_id = self.db.add_summarization_history(
            user_id=self.user_history['user_id'],
            text=self.user_history['text'],
            summary=self.user_history['summary'],
            name=self.user_history['name']
        )

        self.assertEqual(1, self.history.count_documents({}))
    
    def test_search_contents(self):
        summary_id = self.db.add_summarization_history(
            user_id=self.user_history['user_id'],
            text=self.user_history['text'],
            summary=self.user_history['summary'],
            name=self.user_history['name']
        )

        true_result = self.db.search_content(string='abc', user_id=self.user_history['user_id'])
        false_result = self.db.search_content(string='def', user_id=self.user_history['user_id'])

        self.assertEqual([], false_result)
        self.assertEqual(self.user_history['name'], true_result[0][1])
        

if __name__ == '__main__':
    unittest.main()
        
    
