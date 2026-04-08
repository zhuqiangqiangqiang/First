# Moquan IoT 能力实现

已实现你要的五项能力：

0. 创建 API Key (`create_api_key`)
1. 灯光控制 (`control_light`)
2. 环境信息读取 (`read_environment_info`)
3. 水肥控制 (`control_water_fertilizer`)
4. 水肥信息读取 (`read_water_fertilizer_info`)

## 文件说明

- `moquan_client.py`: API 客户端实现。
- `example_usage.py`: 五项能力的示例调用。

## 快速使用

```bash
python3 example_usage.py
```

你需要把 `example_usage.py` 里的 `YOUR_ADMIN_OR_APP_TOKEN` 替换成实际 token。

## 接口路径可配置

默认路径如下：

- `/api/v1/apikey/create`
- `/api/v1/light/control`
- `/api/v1/environment/read`
- `/api/v1/water-fertilizer/control`
- `/api/v1/water-fertilizer/read`

若你在平台文档中的路径不同，可以在初始化时传入 `EndpointConfig` 覆盖。

```python
from moquan_client import MoquanClient, EndpointConfig

client = MoquanClient(
    base_url="https://developers.moquan.live:9090",
    token="YOUR_TOKEN",
    endpoint_config=EndpointConfig(
        apikey_create="/your/apikey/create/path",
        light_control="/your/light/path",
        environment_read="/your/environment/path",
        water_fertilizer_control="/your/wf/control/path",
        water_fertilizer_read="/your/wf/read/path",
    ),
)
```
