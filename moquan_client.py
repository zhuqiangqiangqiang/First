"""Moquan IoT API client.

说明：
- 你反馈“文档地址不对”后，本实现改为“多候选路径 + 可覆盖路径”模式：
  每个能力会按候选路径依次尝试，或者优先使用你传入的 endpoint 覆盖。
- 建议仍以官方文档为准，通过 EndpointConfig 显式覆盖路径。
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any
from urllib import error, parse, request


class MoquanAPIError(RuntimeError):
    """Raised when the Moquan API returns an error."""


@dataclass
class EndpointConfig:
    """Endpoint paths for Moquan API.

    每个字段是“候选路径列表”，客户端会从前到后尝试。
    如果你确认文档路径，请把正确路径放在列表第一位。
    """

    apikey_create: list[str] = field(
        default_factory=lambda: ["/apikey/create", "/api/apikey/create", "/api/v1/apikey/create"]
    )
    apikey_list: list[str] = field(
        default_factory=lambda: ["/apikey/list", "/api/apikey/list", "/api/v1/apikey/list"]
    )
    apikey_revoke: list[str] = field(
        default_factory=lambda: ["/apikey/revoke", "/api/apikey/revoke", "/api/v1/apikey/revoke"]
    )

    device_list: list[str] = field(
        default_factory=lambda: ["/device/list", "/api/device/list", "/api/v1/device/list"]
    )
    device_detail: list[str] = field(
        default_factory=lambda: ["/device/detail", "/api/device/detail", "/api/v1/device/detail"]
    )

    light_control: list[str] = field(
        default_factory=lambda: ["/light/control", "/api/light/control", "/api/v1/light/control"]
    )
    light_read: list[str] = field(
        default_factory=lambda: ["/light/read", "/api/light/read", "/api/v1/light/read"]
    )

    environment_control: list[str] = field(
        default_factory=lambda: [
            "/environment/control",
            "/api/environment/control",
            "/api/v1/environment/control",
        ]
    )
    environment_read: list[str] = field(
        default_factory=lambda: ["/environment/read", "/api/environment/read", "/api/v1/environment/read"]
    )
    environment_control_read: list[str] = field(
        default_factory=lambda: [
            "/environment/control/read",
            "/api/environment/control/read",
            "/api/v1/environment/control/read",
        ]
    )

    water_fertilizer_control: list[str] = field(
        default_factory=lambda: [
            "/water-fertilizer/control",
            "/api/water-fertilizer/control",
            "/api/v1/water-fertilizer/control",
        ]
    )
    water_fertilizer_read: list[str] = field(
        default_factory=lambda: [
            "/water-fertilizer/read",
            "/api/water-fertilizer/read",
            "/api/v1/water-fertilizer/read",
        ]
    )


class MoquanClient:
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

    def create_api_key(self, *, name: str, permissions: list[str] | None = None, expires_at: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": name}
        if permissions is not None:
            payload["permissions"] = permissions
        if expires_at is not None:
            payload["expiresAt"] = expires_at
        return self._request_any("POST", self.endpoint_config.apikey_create, payload=payload)

    def list_api_keys(self, *, page: int = 1, page_size: int = 20) -> dict[str, Any]:
        return self._request_any("GET", self.endpoint_config.apikey_list, query={"page": page, "pageSize": page_size})

    def revoke_api_key(self, *, api_key_id: str) -> dict[str, Any]:
        return self._request_any("POST", self.endpoint_config.apikey_revoke, payload={"apiKeyId": api_key_id})

    def list_devices(self, *, page: int = 1, page_size: int = 50, device_type: str | None = None, keyword: str | None = None) -> dict[str, Any]:
        query: dict[str, Any] = {"page": page, "pageSize": page_size}
        if device_type:
            query["deviceType"] = device_type
        if keyword:
            query["keyword"] = keyword
        return self._request_any("GET", self.endpoint_config.device_list, query=query)

    def get_device_detail(self, *, device_id: str) -> dict[str, Any]:
        return self._request_any("GET", self.endpoint_config.device_detail, query={"deviceId": device_id})

    def control_light(self, *, device_id: str, power: bool, brightness: int | None = None, color_temp: int | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"deviceId": device_id, "power": "on" if power else "off"}
        if brightness is not None:
            payload["brightness"] = brightness
        if color_temp is not None:
            payload["colorTemp"] = color_temp
        return self._request_any("POST", self.endpoint_config.light_control, payload=payload)

    def read_light_info(self, *, device_id: str) -> dict[str, Any]:
        return self._request_any("GET", self.endpoint_config.light_read, query={"deviceId": device_id})

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
        return self._request_any("POST", self.endpoint_config.environment_control, payload=payload)

    def read_environment_info(self, *, device_id: str) -> dict[str, Any]:
        return self._request_any("GET", self.endpoint_config.environment_read, query={"deviceId": device_id})

    def read_environment_control_info(self, *, device_id: str) -> dict[str, Any]:
        return self._request_any("GET", self.endpoint_config.environment_control_read, query={"deviceId": device_id})

    def control_water_fertilizer(self, *, device_id: str, irrigation_on: bool, fertilizer_ratio: float | None = None, duration_seconds: int | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"deviceId": device_id, "irrigation": "on" if irrigation_on else "off"}
        if fertilizer_ratio is not None:
            payload["fertilizerRatio"] = fertilizer_ratio
        if duration_seconds is not None:
            payload["durationSeconds"] = duration_seconds
        return self._request_any("POST", self.endpoint_config.water_fertilizer_control, payload=payload)

    def read_water_fertilizer_info(self, *, device_id: str) -> dict[str, Any]:
        return self._request_any("GET", self.endpoint_config.water_fertilizer_read, query={"deviceId": device_id})

    def _request_any(
        self,
        method: str,
        paths: list[str],
        payload: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        for path in paths:
            try:
                return self._request_once(method=method, path=path, payload=payload, query=query)
            except MoquanAPIError as exc:
                last_error = exc
                continue
        raise MoquanAPIError(f"All endpoint candidates failed for {method} {paths}: {last_error}")

    def _request_once(
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
            raise MoquanAPIError(f"HTTP {exc.code} {url}: {body or exc.reason}") from exc
        except error.URLError as exc:
            raise MoquanAPIError(f"Network error {url}: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise MoquanAPIError(f"Invalid JSON response from {url}") from exc
