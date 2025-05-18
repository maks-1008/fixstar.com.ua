"""
Middleware для обработки медиа-файлов
"""
import os
import posixpath
import mimetypes
import logging
import traceback
from urllib.parse import unquote

from django.conf import settings
from django.http import Http404, FileResponse

# Настройка логирования
logger = logging.getLogger("app.middleware")

class MediaFileMiddleware:
    """
    Middleware для обслуживания медиа-файлов в режиме промышленной эксплуатации.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.media_prefix = settings.MEDIA_URL
        self.media_root = settings.MEDIA_ROOT
        logger.info(f"MediaFileMiddleware инициализирован с MEDIA_URL={self.media_prefix}, MEDIA_ROOT={self.media_root}")
        
    def __call__(self, request):
        """
        Обрабатываем запрос.
        """
        try:
            path = request.path
            logger.debug(f"MediaFileMiddleware обрабатывает запрос: {path}")
            
            # Обработка запроса к favicon.ico напрямую
            if path == '/favicon.ico':
                favicon_path = os.path.join(settings.STATIC_ROOT, 'favicon.ico')
                if os.path.exists(favicon_path):
                    logger.debug(f"Обрабатываем favicon.ico из {favicon_path}")
                    return FileResponse(open(favicon_path, 'rb'), content_type='image/x-icon')
                    
            # Пытаемся обработать медиа-файл
            if not settings.DEBUG and path.startswith(self.media_prefix):
                logger.debug(f"Запрос к медиа-файлу: {path}")
                try:
                    response = self.process_media_request(request)
                    if response:
                        logger.debug(f"Медиа-файл обработан успешно: {path}")
                        return response
                    else:
                        logger.debug(f"Медиа-файл не найден: {path}")
                except Exception as e:
                    # В случае ошибки продолжаем выполнение стандартной цепочки middleware
                    logger.error(f"Ошибка при обработке медиа-файла {path}: {e}", exc_info=True)
                    
            # Если это не медиа-файл или произошла ошибка, продолжаем обработку запроса
            logger.debug(f"Передаем запрос дальше: {path}")
            return self.get_response(request)
        except Exception as e:
            logger.error(f"Критическая ошибка в MediaFileMiddleware: {e}")
            logger.error(traceback.format_exc())
            return self.get_response(request)
        
    def process_media_request(self, request):
        """
        Проверяем, является ли запрос запросом к медиа-файлу.
        Если да, то обслуживаем файл напрямую.
        """
        # Путь относительно MEDIA_URL
        path = request.path[len(self.media_prefix):]
        path = posixpath.normpath(unquote(path)).lstrip('/')
        
        # Полный путь к файлу
        full_path = os.path.join(self.media_root, path)
        logger.debug(f"Проверка пути к файлу: {full_path}")
        
        # Проверяем существование файла
        if os.path.exists(full_path) and os.path.isfile(full_path):
            logger.debug(f"Файл найден: {full_path}")
            return self.serve_file(request, full_path)
        
        # Если файл не существует, возвращаем None, чтобы продолжить обработку запроса
        logger.debug(f"Файл не найден: {full_path}")
        return None
        
    def serve_file(self, request, file_path):
        """
        Обслуживает файл напрямую с использованием FileResponse.
        """
        try:
            # Определяем content type
            content_type, encoding = mimetypes.guess_type(file_path)
            
            # Если content type не определен, используем application/octet-stream
            if content_type is None:
                content_type = 'application/octet-stream'
                
            logger.debug(f"Обслуживаем файл {file_path} с content_type={content_type}")
            
            # Создаем FileResponse с правильным content type
            response = FileResponse(open(file_path, 'rb'), content_type=content_type)
            
            # Устанавливаем заголовок Content-Encoding если необходимо
            if encoding:
                response['Content-Encoding'] = encoding
                
            return response
        except Exception as e:
            # В случае ошибки (например, если файл нельзя открыть) логируем и возвращаем None
            logger.error(f"Ошибка при обслуживании файла {file_path}: {e}", exc_info=True)
            return None 