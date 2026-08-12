import aiohttp
import logging
from typing import Optional, Dict, Any, List
from config import settings

logger = logging.getLogger(__name__)

BASE_URL = settings.API_BASE_URL  # Добавьте в .env: API_BASE_URL=https://mlstartupbackend-mentrixlabs.amvera.io


class APIClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = BASE_URL

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        headers = self._headers()
        
        # ---- ОТЛАДОЧНЫЙ ВЫВОД ----
        logger.debug(f"🔍 Request: {method} {url}")
        logger.debug(f"📨 Headers: {headers}")
        logger.debug(f"📦 Data: {data}")
        logger.debug(f"🔗 Params: {params}")
        # ---------------------------
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=data, params=params, headers=self._headers()) as resp:
                if resp.status >= 400:
                    try:
                        error_detail = await resp.json()
                        error_msg = error_detail.get("detail", f"Ошибка {resp.status}")
                    except:
                        error_msg = await resp.text()
                    logger.error(f"API error {resp.status}: {error_msg}")
                    raise Exception(f"API error {resp.status}: {error_msg}")
                return await resp.json()

    async def update_tg_id(self, tg_id: int) -> Dict:
        """Привязать Telegram ID к текущему пользователю (требуется токен)."""
        return await self._request("PUT", "/auth/update_tg_id", data={"tg_id": tg_id})

    # ----- Аутентификация -----
    async def register(self, username: str, email: str, password: str) -> Dict:
        return await self._request("POST", "/auth/register", data={"username": username, "email": email, "password": password})

    async def login(self, username: str, password: str) -> Dict:
        url = f"{self.base_url}/auth/login"
        # Данные для form-urlencoded
        payload = {"username": username, "password": password}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as resp:
                if resp.status >= 400:
                    try:
                        error_detail = await resp.json()
                        error_msg = error_detail.get("detail", f"Ошибка {resp.status}")
                    except:
                        error_msg = await resp.text()
                    logger.error(f"API error {resp.status}: {error_msg}")
                    raise Exception(f"API error {resp.status}: {error_msg}")
                return await resp.json()
        
    async def get_me(self) -> Dict:
        return await self._request("GET", "/auth/me")

    # ----- Товары -----
    async def get_goods(self, page: int = 1, size: int = 20) -> List[Dict]:
        return await self._request("GET", "/goods", params={"page": page, "size": size})

    async def get_goods_by_id(self, goods_id: int) -> Dict:
        return await self._request("GET", f"/goods/{goods_id}")

    async def create_goods(self, url: str) -> Dict:
        return await self._request("POST", "/goods", data={"url": url, "name": url, "description": ""})

    async def delete_goods(self, goods_id: int) -> None:
        await self._request("DELETE", f"/goods/{goods_id}")

    # ----- SEO -----
    async def generate_seo(self, goods_id: int) -> Dict:
        return await self._request("POST", "/seo/generate", data={"goods_id": goods_id})

    async def get_seo_history(self, goods_id: int) -> Dict:
        return await self._request("GET", f"/seo/history/{goods_id}")

    # ----- Инфографика (пока нет эндпоинта, но если есть) -----
    # Если у вас есть эндпоинт /infographics/search, добавьте аналогично.

    # ----- Отчёты -----
    async def generate_report(self, goods_id: int) -> bytes:
        url = f"{self.base_url}/reports/generate/{goods_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._headers()) as resp:
                if resp.status >= 400:
                    error_msg = await resp.text()
                    raise Exception(f"Report error {resp.status}: {error_msg}")
                return await resp.read()  # возвращает PDF как bytes