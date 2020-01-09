import os
import unittest
from unittest import TestCase
from server import app 
import responses
import json

class RoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_api(self):
        response = self.app.get('/API', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    @responses.activate
    def test_twit_500(self):
        responses.add(responses.GET,
            'https://takehome.io/twitter',
            json={'key': 'value'},
            status=500
        )
        response = self.app.get('/API', follow_redirects = True)
        self.assertEqual(json.dumps(response.json), '{"response_code": 500, "twitter_error": "{\\"key\\": \\"value\\"}"}')

    @responses.activate
    def test_fb_500(self):
        responses.add(responses.GET,
            'https://takehome.io/twitter',
            json={'key': 'value'},
            status=200
        )
        responses.add(responses.GET,
            'https://takehome.io/facebook',
            json={'key': 'value'},
            status=500
        )
        response = self.app.get('/API', follow_redirects = True)
        self.assertEqual(json.dumps(response.json), '{"facebook_error": "{\\"key\\": \\"value\\"}", "response_code": 500}')

    @responses.activate
    def test_insta_500(self):
        responses.add(responses.GET,
            'https://takehome.io/twitter',
            json={'key': 'value'},
            status=200
        )
        responses.add(responses.GET,
            'https://takehome.io/facebook',
            json={'key': 'value'},
            status=200
        )
        responses.add(responses.GET,
            'https://takehome.io/instagram',
            json={'key': 'value'},
            status=500
        )
        response = self.app.get('/API', follow_redirects = True)
        self.assertEqual(json.dumps(response.json), '{"instagram_error": "{\\"key\\": \\"value\\"}", "response_code": 500}')       
    
    @responses.activate
    def test_200(self):
        responses.add(responses.GET,
            'https://takehome.io/twitter',
            json={'key': 'value'},
            status=200
        )
        responses.add(responses.GET,
            'https://takehome.io/facebook',
            json={'key': 'value'},
            status=200
        )
        responses.add(responses.GET,
            'https://takehome.io/instagram',
            json={'key': 'value'},
            status=200
        )
        response = self.app.get('/API', follow_redirects = True)
        self.assertEqual(json.dumps(response.json), '{"twitter_body": {"key": "value"}, "instagram_body": {"key": "value"}, "facebook_body": {"key": "value"}}')

if __name__ == "__main__":
    unittest.main()    
