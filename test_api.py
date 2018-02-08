from api import app, api, Chat, Chats
from unittest import TestCase
from model import connect_to_db, db, Message, example_data

class FlaskTestsApi(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        example_data()

    def tearDown(self):

        db.session.close()
        db.drop_all()

    def test_post_adds_event_to_db_and_returns_401_status_with_correct_json(self):

        inputs = {
            'username': 'whitney',
            'text': 'event posted!',
            'timeout': '30'
        }

        post_result = self.client.post('/chat', data=inputs)

        self.assertIn('id', post_result.data)
        self.assertIn('5', post_result.data)
        self.assertEqual(201, post_result.status_code)

        get_result = self.client.get('/chat/5')
        self.assertIn('event posted!', get_result.data)

    def test_post_adds_event_successfully_without_timeout_input(self):

        inputs = {
            'username': 'whitney',
            'text': 'test timeout'
        }

        post_result = self.client.post('/chat', data=inputs)
        self.assertEqual(201, post_result.status_code)

        get_result = self.client.get('/chat/5')


    def test_invalid_post_with_missing_inputs_returns_400(self):

        inputs = {
            'text': 'missing username'
        }

        result = self.client.post('/chat', data=inputs)
        self.assertEqual(400, result.status_code)

    def test_invalid_post_with_invalid_timeout_returns_400(self):

        inputs = {
            'username': 'whitney',
            'text': 'incorrect timeout format',
            'timeout': 'not a number'
        }

        result = self.client.post('/chat', data=inputs)
        self.assertEqual(400, result.status_code)

    def test_get_with_message_id_retrieves_correct_message(self):

        result = self.client.get('/chat/1')

        self.assertIn('username', result.data)
        self.assertIn('Test Message', result.data)

    def test_invalid_get_without_existing_username_returns_404(self):

        result = self.client.get('/chat/6')

        self.assertEqual(404, result.status_code)

    def test_get_with_username_returns_only_unexpired_messages(self):

        result = self.client.get('/chats/whitney')

        self.assertIn('id', result.data)
        self.assertIn('text', result.data)
        self.assertIn('Hello Whitney', result.data)
        self.assertIn('Second message', result.data)
        self.assertNotIn('Expired message', result.data)

    def test_messages_expire_after_get_chats_for_user(self):

        expire_chats = self.client.get('/chats/whitney')
        result = self.client.get('/chats/whitney')

        self.assertNotIn('id', result.data)
        self.assertNotIn('text', result.data)

if __name__ == '__main__':
    import unittest
    unittest.main()
