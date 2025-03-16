import time
from typing import Optional

import requests
from pydantic import BaseModel, ValidationError

from src.feature.request import schemas
from src.logger import logger
from src.service_url import get_url_emily_database_handler


class RequestHandler:
    def __init__(self, base_url=get_url_emily_database_handler(), headers=None, timeout=10):
        """
        Инициализация класса для работы с запросами.

        :param base_url: Базовый URL для запросов
        :param headers: Заголовки для запросов (по умолчанию None)
        :param timeout: Тайм-аут для запросов (по умолчанию 10 секунд)
        """
        self.base_url = base_url
        self.headers = headers if headers is not None else {}
        self.timeout = timeout

    def __get__(
            self, endpoint: str, path_params: Optional[BaseModel] = None, query_params: Optional = None,
            response_model: Optional = None
    ):
        """
        Выполняет GET-запрос к указанному endpoint.

        :param query_params:
        :param path_params:
        :param response_model:
        :param endpoint: Путь к ресурсу относительно base_url
        :return: Ответ сервера в формате JSON (если есть) или текстовый ответ
        """
        try:
            start_time = time.time()
            if path_params:
                endpoint = endpoint.format(**path_params.model_dump())
            
            url = f"{self.base_url}/{endpoint}"
            logger.debug(
                f"GET запрос: {url} | Параметры: {str(query_params.dict())[:100]}...",
                extra={'tags': {
                    'service': 'http',
                    'action': 'request',
                    'method': 'GET',
                    'endpoint': endpoint,
                    'url': url
                }}
            )
            
            # Преобразуем параметры запроса в словарь
            query_params_dict = query_params.dict() if query_params else None
            response = requests.get(url, headers=self.headers, params=query_params_dict, timeout=self.timeout)
            response.raise_for_status()

            # Обрабатываем ответ с использованием модели
            data = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            logger.debug(f"Ответ - {data}")
            
            logger.info(
                f"Успешный GET ответ: {response.status_code} | Данные: {str(data)[:200]}...",
                extra={'tags': {
                    'service': 'http',
                    'action': 'response',
                    'method': 'GET',
                    'status_code': response.status_code,
                    'data_length': len(str(data)),
                    'duration': time.time() - start_time
                }}
            )
            return response.status_code, (response_model.parse_obj(data) if response_model else data)
        except requests.exceptions.RequestException as error:
            logger.exception(
                "Ошибка GET запроса",
                extra={'tags': {
                    'service': 'http',
                    'action': 'error',
                    'method': 'GET',
                    'error_type': error.__class__.__name__,
                    'status_code': getattr(error.response, 'status_code', None),
                    'endpoint': endpoint
                }}
            )
            return None, None
        except ValidationError as error:
            logger.exception("Произошла ошибка: %s", error)
            return None, None

    def __post__(self, endpoint: str, data: Optional = None, response_model: Optional = None):
        """
            Выполняет POST-запрос к указанному endpoint.

            :param self:
            :param response_model:
            :param endpoint: Путь к ресурсу относительно base_url
            :param data: Данные для отправки в формате form-encoded (по умолчанию None)
            :return: Ответ сервера в формате JSON (если есть) или текстовый ответ
            """
        try:
            start_time = time.time()
            url = f"{self.base_url}/{endpoint}"
            logger.debug(
                f"POST запрос: {url} | Данные: {str(data.model_dump())[:200]}...",
                extra={'tags': {
                    'service': 'http',
                    'action': 'request',
                    'method': 'POST',
                    'endpoint': endpoint,
                    'url': url
                }}
            )
            
            data_dict = data.model_dump() if data else None
            response = requests.post(url, headers=self.headers, json=data_dict, timeout=self.timeout)
            response.raise_for_status()

            data = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            logger.debug(f"Ответ - {data}")
            
            logger.info(
                f"Успешный POST ответ: {response.status_code}",
                extra={'tags': {
                    'service': 'http',
                    'action': 'response',
                    'method': 'POST',
                    'status_code': response.status_code,
                    'data_length': len(str(data)),
                    'duration': time.time() - start_time
                }}
            )
            return response_model.model_validate(data) if response_model else data
        except requests.exceptions.RequestException as error:
            logger.exception(
                "Ошибка POST запроса",
                extra={'tags': {
                    'service': 'http',
                    'action': 'error',
                    'method': 'POST',
                    'error_type': error.__class__.__name__,
                    'status_code': getattr(error.response, 'status_code', None),
                    'endpoint': endpoint
                }}
            )
            return None
        except ValidationError as error:
            logger.exception("Произошла ошибка: %s", error)
            return None

    def __delete__(self, endpoint: str, path_params: Optional[BaseModel] = None, query_params: Optional = None):
        """
        Выполняет DELETE-запрос к указанному endpoint.

        :param endpoint: Путь к ресурсу относительно base_url
        :param path_params: Параметры пути для подстановки в URL
        :param query_params: Параметры запроса
        :return: Ответ сервера в формате JSON (если есть) или текстовый ответ
        """
        try:
            start_time = time.time()
            if path_params:
                endpoint = endpoint.format(**path_params.model_dump())
            
            url = f"{self.base_url}/{endpoint}"
            logger.debug(
                f"DELETE запрос: {url} | Параметры: {str(query_params.dict())[:100]}...",
                extra={'tags': {
                    'service': 'http',
                    'action': 'request',
                    'method': 'DELETE',
                    'endpoint': endpoint,
                    'url': url
                }}
            )
            
            query_params_dict = query_params.dict() if query_params else None
            response = requests.delete(url, headers=self.headers, params=query_params_dict, timeout=self.timeout)
            response.raise_for_status()

            data = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
            logger.debug(f"Ответ - {data}")
            
            logger.warning(
                f"Успешное удаление: {response.status_code}",
                extra={'tags': {
                    'service': 'http',
                    'action': 'response',
                    'method': 'DELETE',
                    'status_code': response.status_code,
                    'data_length': len(str(data)),
                    'duration': time.time() - start_time
                }}
            )
            return data
        except requests.exceptions.RequestException as error:
            logger.exception(
                "Ошибка DELETE запроса",
                extra={'tags': {
                    'service': 'http',
                    'action': 'error',
                    'method': 'DELETE',
                    'error_type': error.__class__.__name__,
                    'status_code': getattr(error.response, 'status_code', None),
                    'endpoint': endpoint
                }}
            )
            return None

    def set_headers(self, headers):
        """
        Устанавливает или обновляет заголовки для запросов.

        :param self:
        :param headers: Словарь с заголовками
        """
        self.headers.update(headers)

    def set_timeout(self, timeout):
        """
        Устанавливает тайм-аут для запросов.

        :param self:
        :param timeout: Тайм-аут в секундах
        """
        self.timeout = timeout

class RequestDataBase(RequestHandler):
    def __create_modified_news__(self, data: schemas.ModifiedPost):
        return self.__post__(endpoint='modified-text/create', data=data)

    def create_modified_news(self, channel: str, id_post: int, text: str):
        data = schemas.ModifiedPost(
            channel=channel,
            id_post=id_post,
            text=text
        )
        return self.__create_modified_news__(data=data)
