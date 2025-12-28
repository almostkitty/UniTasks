"""
Сервис категоризации новостей.
Распределяет новости по категориям (спорт, политика, технологии и т.д.)
на основе ключевых слов.
"""
import json
from flask import Flask, jsonify, request, Response
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

app = Flask(__name__)

CATEGORY_KEYWORDS = {
    'sport': {'спорт', 'футбол', 'хоккей', 'матч', 'игра', 'sport', 'football', 'match', 'game'},
    'politics': {'политика', 'правительство', 'президент', 'выборы', 'politics', 'government', 'president', 'election'},
    'technology': {'технология', 'компьютер', 'интернет', 'технологии', 'technology', 'computer', 'internet', 'tech'},
    'economics': {'экономика', 'финансы', 'деньги', 'банк', 'economics', 'finance', 'money', 'bank'},
    'science': {'наука', 'исследование', 'ученый', 'science', 'research', 'scientist'},
    'culture': {'культура', 'искусство', 'кино', 'музыка', 'culture', 'art', 'movie', 'music'}
}


def categorize_news(news_item: Dict[str, Any]) -> str:
    """
    Определяет категорию новости на основе ключевых слов.
    
    Args:
        news_item: Словарь с информацией о новости
        
    Returns:
        Название категории или 'other' если категория не определена
    """
    text = f"{news_item.get('title', '')} {news_item.get('description', '')}"
    text_lower = text.lower()
    
    # Подсчитываем совпадения по категориям
    category_scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            category_scores[category] = score
    
    # Возвращаем категорию с наибольшим количеством совпадений
    return max(category_scores, key=category_scores.get) if category_scores else 'other'


def categorize_single_news(news_item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Категоризирует одну новость.
    
    Args:
        news_item: Словарь с информацией о новости
        
    Returns:
        Новость с добавленным полем 'category'
    """
    news_item['category'] = categorize_news(news_item)
    return news_item


def categorize_news_parallel(news_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Категоризирует несколько новостей параллельно.
    Использует threading вместо multiprocessing для совместимости с serverless.
    
    Args:
        news_items: Список новостей для категоризации
        
    Returns:
        Список новостей с добавленным полем 'category'
    """
    max_workers = min(4, len(news_items))
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(categorize_single_news, item): item for item in news_items}
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
        'service': 'Categorizer Service',
        'description': 'Сервис категоризации новостей',
        'endpoints': {
            'GET /': 'Информация о сервисе',
            'GET /health': 'Проверка здоровья сервиса',
            'POST /categorize': 'Категоризация новостей (требует поле "news" в JSON)'
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


@app.route('/categorize', methods=['POST'])
def categorize():
    """
    Эндпоинт для категоризации новостей.
    
    Принимает JSON с полем 'news' - список новостей.
    Возвращает список новостей с добавленным полем 'category'.
    """
    data = request.get_json()
    if not data or 'news' not in data:
        return jsonify({'error': 'Необходимо поле "news" со списком новостей'}), 400
    
    news_items = data['news']
    if not isinstance(news_items, list) or len(news_items) == 0:
        return jsonify({'error': 'Поле "news" должно быть непустым списком'}), 400
    
    # Многопроцессность для параллельной категоризации
    categorized_news = categorize_news_parallel(news_items)
    return jsonify({'news': categorized_news, 'count': len(categorized_news)}), 200


if __name__ == '__main__':
    # Для локальной разработки используем Flask dev server
    # В production используется gunicorn (см. Dockerfile)
    import os
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=False)
