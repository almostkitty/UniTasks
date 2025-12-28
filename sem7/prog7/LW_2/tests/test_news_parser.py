"""
Тесты для сервиса парсинга новостей.
"""
import unittest
from services.news_parser.app import app, parse_single_feed, parse_feeds_parallel


class TestNewsParser(unittest.TestCase):
    """Тесты для сервиса парсинга новостей"""
    
    def setUp(self):
        """Настройка тестового клиента"""
        self.client = app.test_client()
        self.app = app
    
    def test_health_endpoint(self):
        """Тест эндпоинта /health"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
    
    def test_parse_missing_feeds(self):
        """Тест парсинга без поля feeds"""
        response = self.client.post('/parse', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_parse_empty_feeds(self):
        """Тест парсинга с пустым списком feeds"""
        response = self.client.post('/parse', json={'feeds': []})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_parse_invalid_url(self):
        """Тест парсинга с некорректным URL"""
        response = self.client.post('/parse', json={'feeds': ['invalid-url']})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_parse_single_feed_invalid(self):
        """Тест парсинга одного невалидного фида"""
        result = parse_single_feed('http://invalid-url-that-does-not-exist.com/rss')
        self.assertEqual(result, [])
    
    def test_parse_feeds_parallel_empty(self):
        """Тест параллельного парсинга пустого списка"""
        result = parse_feeds_parallel([])
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()

