from api import Events, app, api
from unittest import TestCase
from model import connect_to_db, db, Message

# 200 GET, PUT, POST 
# 201 POST
# 204 DELETE
# 304 not modified/redirect
# 400 bad request. server could not understand client
# 401 unauthorized client
# 403 forbidden
# 404 not cfound
# 500 internal server error
# 503 service unavailable. server is down or undergoing maintenance

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

    def test_post_adds_event_with_event_type(self):

        inputs = {
            'event_type': 'TESTTEST'
        }

        result = self.client.post('/api/events', data=inputs)

        self.assertIn('TESTTEST', result.data)

    def test_get_of_nonexistent_event_returns_404(self):

        result = self.client.get('/api/events/5')

        self.assertEqual(404, result.status_code)

    def test_get_with_id_retrieves_correct_event(self):

        result = self.client.get('/api/events/1')

        self.assertIn('fire', result.data)

    def test_get_retrieves_all_events(self):

        result = self.client.get('/api/events')

        self.assertIn('fire', result.data)
        self.assertIn('storm', result.data)


if __name__ == '__main__':
    import unittest
    unittest.main()
