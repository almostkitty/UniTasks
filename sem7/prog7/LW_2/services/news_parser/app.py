"""
Сервис парсинга новостей из RSS-лент.
Использует многопроцессность для параллельной обработки нескольких RSS-источников.
"""
import feedparser
import json
import os
import logging
from flask import Flask, jsonify, request, Response
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_single_feed(feed_url: str) -> List[Dict[str, Any]]:
    """
    Парсит один RSS-фид и возвращает список новостей.
    
    Args:
        feed_url: URL RSS-ленты
        
    Returns:
        Список словарей с информацией о новостях
    """
    try:
        logger.info(f"Парсинг фида: {feed_url}")
        feed = feedparser.parse(feed_url)
        news_items = []
        # Берем все новости из фида (или максимум 20 для производительности)
        for entry in feed.entries[:20]:
            # Получаем описание из разных полей RSS
            description = entry.get('description', '') or entry.get('summary', '') or entry.get('content', [{}])[0].get('value', '')
            news_items.append({
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'description': description,
                'published': entry.get('published', '') or entry.get('updated', ''),
                'source': feed_url
            })
        logger.info(f"Получено {len(news_items)} новостей из {feed_url}")
        return news_items
    except Exception as e:
        logger.error(f"Ошибка при парсинге {feed_url}: {str(e)}", exc_info=True)
        return []


def parse_feeds_parallel(feed_urls: List[str]) -> List[Dict[str, Any]]:
    """
    Парсит несколько RSS-фидов параллельно с использованием threading.
    Threading работает в serverless окружениях, в отличие от multiprocessing.
    
    Args:
        feed_urls: Список URL RSS-лент
        
    Returns:
        Список всех новостей из всех фидов
    """
    # Используем ThreadPoolExecutor для параллельного парсинга
    # Это работает в serverless окружениях, в отличие от multiprocessing
    all_news = []
    max_workers = min(4, len(feed_urls))  # Ограничиваем количество потоков
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(parse_single_feed, url): url for url in feed_urls}
        for future in as_completed(future_to_url):
            try:
                news_list = future.result()
                all_news.extend(news_list)
            except Exception as e:
                url = future_to_url[future]
                logger.error(f"Ошибка при обработке {url}: {str(e)}")
    return all_news


@app.route('/', methods=['GET'])
def index():
    """Информация о сервисе и доступных эндпоинтах"""
    data = {
        'service': 'News Parser Service',
        'description': 'Сервис парсинга новостей из RSS-лент',
        'endpoints': {
            'GET /': 'Информация о сервисе',
            'GET /health': 'Проверка здоровья сервиса',
            'POST /parse': 'Парсинг новостей из RSS-лент (требует поле "feeds" в JSON)'
        },
        'example': {
            'request': {
                'feeds': ['https://lenta.ru/rss', 'https://www.interfax.ru/rss.asp']
            },
            'response': {
                'news': [
                    {
                        'title': 'Заголовок новости',
                        'link': 'https://...',
                        'description': 'Описание...',
                        'published': 'Дата публикации',
                        'source': 'URL RSS-ленты'
                    }
                ],
                'count': 10
            }
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


@app.route('/parse', methods=['POST'])
def parse_news():
    """
    Эндпоинт для парсинга новостей из RSS-лент.
    
    Принимает JSON с полем 'feeds' - список URL RSS-лент.
    Возвращает список новостей в формате JSON.
    """
    try:
        data = request.get_json()
        if not data or 'feeds' not in data:
            return Response(
                json.dumps({'error': 'Необходимо поле "feeds" со списком URL RSS-лент'}, ensure_ascii=False),
                mimetype='application/json; charset=utf-8'
            ), 400
        
        feed_urls = data['feeds']
        if not isinstance(feed_urls, list) or len(feed_urls) == 0:
            return Response(
                json.dumps({'error': 'Поле "feeds" должно быть непустым списком'}, ensure_ascii=False),
                mimetype='application/json; charset=utf-8'
            ), 400
        
        # Валидация URL
        for url in feed_urls:
            if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
                return Response(
                    json.dumps({'error': f'Некорректный URL: {url}'}, ensure_ascii=False),
                    mimetype='application/json; charset=utf-8'
                ), 400
        
        logger.info(f"Начало парсинга {len(feed_urls)} фидов")
        # Используем многопроцессность для параллельного парсинга
        news_items = parse_feeds_parallel(feed_urls)
        logger.info(f"Получено {len(news_items)} новостей всего")
        result = {'news': news_items, 'count': len(news_items)}
        return Response(
            json.dumps(result, ensure_ascii=False, indent=2),
            mimetype='application/json; charset=utf-8'
        ), 200
    except Exception as e:
        logger.error(f"Ошибка в parse_news: {str(e)}", exc_info=True)
        return Response(
            json.dumps({'error': f'Внутренняя ошибка сервера: {str(e)}'}, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        ), 500


if __name__ == '__main__':
    # Для локальной разработки используем Flask dev server
    # В production используется gunicorn (см. Dockerfile)
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)

