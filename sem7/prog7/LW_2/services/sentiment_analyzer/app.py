"""
Сервис анализа тональности новостей.
Определяет эмоциональную окраску текста (позитивная, негативная, нейтральная)
на основе простого алгоритма анализа ключевых слов.
"""
import json
from flask import Flask, jsonify, request, Response
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

app = Flask(__name__)

POSITIVE_WORDS = {
    'хороший', 'отлично', 'успех', 'победа', 'радость', 'счастье',
    'good', 'great', 'success', 'victory', 'joy', 'happy'
}

NEGATIVE_WORDS = {
    'плохой', 'ужасный', 'провал', 'поражение', 'грусть', 'проблема',
    'кризис', 'катастрофа', 'война', 'конфликт', 'страх',
    'bad', 'terrible', 'failure', 'problem', 'crisis', 'war', 'fear'
}


def analyze_sentiment(text: str) -> str:
    """
    Анализирует тональность текста на основе ключевых слов.
    
    Args:
        text: Текст для анализа
        
    Returns:
        'positive', 'negative' или 'neutral'
    """
    if not text:
        return 'neutral'
    text_lower = text.lower()
    # Подсчитываем количество позитивных и негативных слов
    positive_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    negative_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    # Определяем тональность по преобладанию
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    return 'neutral'


def analyze_single_news(news_item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Анализирует тональность одной новости.
    
    Args:
        news_item: Словарь с информацией о новости
        
    Returns:
        Новость с добавленным полем 'sentiment'
    """
    text = f"{news_item.get('title', '')} {news_item.get('description', '')}"
    news_item['sentiment'] = analyze_sentiment(text)
    return news_item


def analyze_news_parallel(news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Анализирует тональность нескольких новостей параллельно.
    Использует threading вместо multiprocessing для совместимости с serverless.
    
    Args:
        news_items: Список новостей для анализа
        
    Returns:
        Список новостей с добавленным полем 'sentiment'
    """
    max_workers = min(4, len(news_items))
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(analyze_single_news, item): item for item in news_items}
        for future in as_completed(future_to_item):
            try:
                results.append(future.result())
            except Exception as e:
                item = future_to_item[future]
                results.append(item)  # Возвращаем оригинальный элемент при ошибке
    return results


@app.route('/', methods=['GET'])
def index():
    """Информация о сервисе и доступных эндпоинтах"""
    data = {
        'service': 'Sentiment Analyzer Service',
        'description': 'Сервис анализа тональности новостей',
        'endpoints': {
            'GET /': 'Информация о сервисе',
            'GET /health': 'Проверка здоровья сервиса',
            'POST /analyze': 'Анализ тональности новостей (требует поле "news" в JSON)'
        }
    }
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype='application/json; charset=utf-8'
    ), 200


@app.route('/health', methods=['GET'])
def health():
    """Проверка здоровья сервиса"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/analyze', methods=['POST'])
def analyze_sentiments():
    """
    Эндпоинт для анализа тональности новостей.
    
    Принимает JSON с полем 'news' - список новостей.
    Возвращает список новостей с добавленным полем 'sentiment'.
    """
    data = request.get_json()
    if not data or 'news' not in data:
        return jsonify({'error': 'Необходимо поле "news" со списком новостей'}), 400
    
    news_items = data['news']
    if not isinstance(news_items, list) or len(news_items) == 0:
        return jsonify({'error': 'Поле "news" должно быть непустым списком'}), 400
    
    # Используем многопроцессность для параллельного анализа
    analyzed_news = analyze_news_parallel(news_items)
    return jsonify({'news': analyzed_news, 'count': len(analyzed_news)}), 200


if __name__ == '__main__':
    # Для локальной разработки используем Flask dev server
    # В production используется gunicorn (см. Dockerfile)
    import os
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=False)
