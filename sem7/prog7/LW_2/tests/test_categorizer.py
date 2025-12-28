"""
Тесты для сервиса категоризации.
"""
import unittest
from services.categorizer.app import app, categorize_news, categorize_single_news, categorize_news_parallel


class TestCategorizer(unittest.TestCase):
    """Тесты для сервиса категоризации"""
    
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
    
    def test_categorize_missing_news(self):
        """Тест категоризации без поля news"""
        response = self.client.post('/categorize', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_categorize_empty_news(self):
        """Тест категоризации с пустым списком новостей"""
        response = self.client.post('/categorize', json={'news': []})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_categorize_sport(self):
        """Тест категоризации спортивных новостей"""
        news_item = {'title': 'Футбольный матч', 'description': 'Игра команды'}
        result = categorize_news(news_item)
        self.assertEqual(result, 'sport')
    
    def test_categorize_politics(self):
        """Тест категоризации политических новостей"""
        news_item = {'title': 'Политика', 'description': 'Президент выборы'}
        result = categorize_news(news_item)
        self.assertEqual(result, 'politics')
    
    def test_categorize_technology(self):
        """Тест категоризации технологических новостей"""
        news_item = {'title': 'Технология', 'description': 'Компьютер интернет'}
        result = categorize_news(news_item)
        self.assertEqual(result, 'technology')
    
    def test_categorize_other(self):
        """Тест категоризации новостей без категории"""
        news_item = {'title': 'Разное', 'description': 'Обычная новость'}
        result = categorize_news(news_item)
        self.assertEqual(result, 'other')
    
    def test_categorize_single_news(self):
        """Тест категоризации одной новости"""
        news_item = {'title': 'Футбол', 'description': 'Матч'}
        result = categorize_single_news(news_item)
        self.assertIn('category', result)
        self.assertEqual(result['category'], 'sport')
    
    def test_categorize_news_parallel(self):
        """Тест параллельной категоризации новостей"""
        news_items = [
            {'title': 'Футбол', 'description': 'Матч'},
            {'title': 'Политика', 'description': 'Выборы'}
        ]
        result = categorize_news_parallel(news_items)
        self.assertEqual(len(result), 2)
        self.assertIn('category', result[0])
        self.assertIn('category', result[1])


if __name__ == '__main__':
    unittest.main()

