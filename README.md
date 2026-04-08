# Moquan IoT 能力实现

已扩展为“常用控制 + 常用读取”全套方法封装：

## API Key 管理
- 创建 API Key：`create_api_key`
- 查询 API Key 列表：`list_api_keys`
- 吊销 API Key：`revoke_api_key`

## 灯光
- 控制：`control_light`
- 读取：`read_light_info`

## 环境
- 控制：`control_environment`
- 读取传感器数据：`read_environment_info`
- 读取控制配置/状态：`read_environment_control_info`

## 水肥
- 控制：`control_water_fertilizer`
- 读取：`read_water_fertilizer_info`

## 文件说明

- `moquan_client.py`: API 客户端实现。
- `example_usage.py`: 全量能力调用示例。

## 快速使用

```bash
python3 example_usage.py
```

你需要把 `example_usage.py` 里的 `YOUR_ADMIN_OR_APP_TOKEN` 替换成实际 token。

## 默认接口路径

- `/api/v1/apikey/create`
- `/api/v1/apikey/list`
- `/api/v1/apikey/revoke`
- `/api/v1/light/control`
- `/api/v1/light/read`
- `/api/v1/environment/control`
- `/api/v1/environment/read`
- `/api/v1/environment/control/read`
- `/api/v1/water-fertilizer/control`
- `/api/v1/water-fertilizer/read`

## 路径覆盖（按文档适配）

如果你的平台文档接口路径不同，使用 `EndpointConfig` 覆盖：

```python
from moquan_client import MoquanClient, EndpointConfig

client = MoquanClient(
    base_url="https://developers.moquan.live:9090",
    token="YOUR_TOKEN",
    endpoint_config=EndpointConfig(
        environment_control="/your/environment/control/path",
        environment_control_read="/your/environment/control/read/path",
    ),
)
```
