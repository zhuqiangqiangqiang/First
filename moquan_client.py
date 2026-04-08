"""Moquan IoT API client.

该客户端封装了常用控制和数据读取能力：
1. API Key 管理（创建 / 查询 / 吊销）
2. 设备查询（设备列表 / 设备详情）
3. 灯光控制与状态读取
4. 环境控制与环境信息读取
5. 水肥控制与信息读取

说明：
- 由于运行环境可能无法直接访问目标地址，接口路径允许按实际文档覆盖。
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib import error, parse, request


class MoquanAPIError(RuntimeError):
    """Raised when the Moquan API returns an error."""


@dataclass
class EndpointConfig:
    """Endpoint paths for Moquan API."""

    apikey_create: str = "/api/v1/apikey/create"
    apikey_list: str = "/api/v1/apikey/list"
    apikey_revoke: str = "/api/v1/apikey/revoke"

    device_list: str = "/api/v1/device/list"
    device_detail: str = "/api/v1/device/detail"

    light_control: str = "/api/v1/light/control"
    light_read: str = "/api/v1/light/read"

    environment_control: str = "/api/v1/environment/control"
    environment_read: str = "/api/v1/environment/read"
    environment_control_read: str = "/api/v1/environment/control/read"

    water_fertilizer_control: str = "/api/v1/water-fertilizer/control"
    water_fertilizer_read: str = "/api/v1/water-fertilizer/read"


class MoquanClient:
    """Simple HTTP client for Moquan developer API."""

    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 15.0,
        endpoint_config: EndpointConfig | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.endpoint_config = endpoint_config or EndpointConfig()

    # -------------------------------
    # API KEY
    # -------------------------------
    def create_api_key(
        self,
        *,
        name: str,
        permissions: list[str] | None = None,
        expires_at: str | None = None,
    ) -> dict[str, Any]:
        """创建新的 API Key。expires_at 建议 ISO8601，例如 2026-12-31T23:59:59Z。"""
        payload: dict[str, Any] = {"name": name}
        if permissions is not None:
            payload["permissions"] = permissions
        if expires_at is not None:
            payload["expiresAt"] = expires_at
        return self._request("POST", self.endpoint_config.apikey_create, payload)

    def list_api_keys(self, *, page: int = 1, page_size: int = 20) -> dict[str, Any]:
        """读取 API Key 列表。"""
        return self._request(
            "GET",
            self.endpoint_config.apikey_list,
            query={"page": page, "pageSize": page_size},
        )

    def revoke_api_key(self, *, api_key_id: str) -> dict[str, Any]:
        """吊销 API Key。"""
        return self._request(
            "POST",
            self.endpoint_config.apikey_revoke,
            payload={"apiKeyId": api_key_id},
        )

    # -------------------------------
    # DEVICES
    # -------------------------------
    def list_devices(
        self,
        *,
        page: int = 1,
        page_size: int = 50,
        device_type: str | None = None,
        keyword: str | None = None,
    ) -> dict[str, Any]:
        """获取设备列表，可按设备类型与关键字筛选。"""
        query: dict[str, Any] = {"page": page, "pageSize": page_size}
        if device_type is not None:
            query["deviceType"] = device_type
        if keyword is not None:
            query["keyword"] = keyword
        return self._request("GET", self.endpoint_config.device_list, query=query)

    def get_device_detail(self, *, device_id: str) -> dict[str, Any]:
        """获取单个设备详情。"""
        return self._request(
            "GET",
            self.endpoint_config.device_detail,
            query={"deviceId": device_id},
        )

    # -------------------------------
    # LIGHT
    # -------------------------------
    def control_light(
        self,
        *,
        device_id: str,
        power: bool,
        brightness: int | None = None,
        color_temp: int | None = None,
    ) -> dict[str, Any]:
        """控制灯光开关和可选亮度/色温。"""
        payload: dict[str, Any] = {
            "deviceId": device_id,
            "power": "on" if power else "off",
        }
        if brightness is not None:
            payload["brightness"] = brightness
        if color_temp is not None:
            payload["colorTemp"] = color_temp
        return self._request("POST", self.endpoint_config.light_control, payload)

    def read_light_info(self, *, device_id: str) -> dict[str, Any]:
        """读取灯光状态与参数。"""
        return self._request(
            "GET",
            self.endpoint_config.light_read,
            query={"deviceId": device_id},
        )

    # -------------------------------
    # ENVIRONMENT
    # -------------------------------
    def control_environment(
        self,
        *,
        device_id: str,
        mode: str | None = None,
        target_temperature: float | None = None,
        target_humidity: float | None = None,
        target_co2: int | None = None,
        fan_on: bool | None = None,
        heater_on: bool | None = None,
        humidifier_on: bool | None = None,
        dehumidifier_on: bool | None = None,
    ) -> dict[str, Any]:
        """环境控制：支持模式、目标值和执行器开关。"""
        payload: dict[str, Any] = {"deviceId": device_id}
        if mode is not None:
            payload["mode"] = mode
        if target_temperature is not None:
            payload["targetTemperature"] = target_temperature
        if target_humidity is not None:
            payload["targetHumidity"] = target_humidity
        if target_co2 is not None:
            payload["targetCO2"] = target_co2
        if fan_on is not None:
            payload["fan"] = "on" if fan_on else "off"
        if heater_on is not None:
            payload["heater"] = "on" if heater_on else "off"
        if humidifier_on is not None:
            payload["humidifier"] = "on" if humidifier_on else "off"
        if dehumidifier_on is not None:
            payload["dehumidifier"] = "on" if dehumidifier_on else "off"
        return self._request("POST", self.endpoint_config.environment_control, payload)

    def read_environment_info(self, *, device_id: str) -> dict[str, Any]:
        """读取环境传感信息，例如温湿度、光照、CO2 等。"""
        return self._request(
            "GET",
            self.endpoint_config.environment_read,
            query={"deviceId": device_id},
        )

    def read_environment_control_info(self, *, device_id: str) -> dict[str, Any]:
        """读取环境控制配置和当前控制执行状态。"""
        return self._request(
            "GET",
            self.endpoint_config.environment_control_read,
            query={"deviceId": device_id},
        )

    # -------------------------------
    # WATER FERTILIZER
    # -------------------------------
    def control_water_fertilizer(
        self,
        *,
        device_id: str,
        irrigation_on: bool,
        fertilizer_ratio: float | None = None,
        duration_seconds: int | None = None,
    ) -> dict[str, Any]:
        """控制水肥系统状态，并可携带施肥比和执行时长。"""
        payload: dict[str, Any] = {
            "deviceId": device_id,
            "irrigation": "on" if irrigation_on else "off",
        }
        if fertilizer_ratio is not None:
            payload["fertilizerRatio"] = fertilizer_ratio
        if duration_seconds is not None:
            payload["durationSeconds"] = duration_seconds
        return self._request(
            "POST",
            self.endpoint_config.water_fertilizer_control,
            payload,
        )

    def read_water_fertilizer_info(self, *, device_id: str) -> dict[str, Any]:
        """读取水肥系统信息，例如运行状态、流量、电导率等。"""
        return self._request(
            "GET",
            self.endpoint_config.water_fertilizer_read,
            query={"deviceId": device_id},
        )

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{parse.urlencode(query)}"

        data: bytes | None = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        req = request.Request(
            url=url,
            method=method,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {"status": "ok"}
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            raise MoquanAPIError(
                f"HTTP {exc.code} calling {url}: {body or exc.reason}"
            ) from exc
        except error.URLError as exc:
            raise MoquanAPIError(f"Network error calling {url}: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise MoquanAPIError(f"Invalid JSON response from {url}") from exc
