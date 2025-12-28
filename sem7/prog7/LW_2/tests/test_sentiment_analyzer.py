"""
Тесты для сервиса анализа тональности.
"""
import unittest
from services.sentiment_analyzer.app import app, analyze_sentiment, analyze_single_news, analyze_news_parallel


class TestSentimentAnalyzer(unittest.TestCase):
    """Тесты для сервиса анализа тональности"""
    
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
    
    def test_analyze_missing_news(self):
        """Тест анализа без поля news"""
        response = self.client.post('/analyze', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_analyze_empty_news(self):
        """Тест анализа с пустым списком новостей"""
        response = self.client.post('/analyze', json={'news': []})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_analyze_sentiment_positive(self):
        """Тест анализа позитивной тональности"""
        result = analyze_sentiment("Хорошие новости, успех, победа")
        self.assertEqual(result, 'positive')
    
    def test_analyze_sentiment_negative(self):
        """Тест анализа негативной тональности"""
        result = analyze_sentiment("Плохие новости, проблема, кризис")
        self.assertEqual(result, 'negative')
    
    def test_analyze_sentiment_neutral(self):
        """Тест анализа нейтральной тональности"""
        result = analyze_sentiment("Обычные новости")
        self.assertEqual(result, 'neutral')
    
    def test_analyze_single_news(self):
        """Тест анализа одной новости"""
        news_item = {'title': 'Хорошие новости', 'description': 'Успех'}
        result = analyze_single_news(news_item)
        self.assertIn('sentiment', result)
        self.assertEqual(result['sentiment'], 'positive')
    
    def test_analyze_news_parallel(self):
        """Тест параллельного анализа новостей"""
        news_items = [
            {'title': 'Хорошие новости', 'description': 'Успех'},
            {'title': 'Плохие новости', 'description': 'Проблема'}
        ]
        result = analyze_news_parallel(news_items)
        self.assertEqual(len(result), 2)
        self.assertIn('sentiment', result[0])
        self.assertIn('sentiment', result[1])


if __name__ == '__main__':
    unittest.main()

