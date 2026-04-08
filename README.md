# Moquan IoT 客户端（按文档可覆盖路径）

你反馈“接口地址不对”后，这版做了两件事：

1. **每个接口支持多候选路径自动尝试**（`/xxx`、`/api/xxx`、`/api/v1/xxx`）。
2. **支持用 `EndpointConfig` 强制覆盖**，把你文档中的真实路径放第一位。

> 强烈建议：以官方文档为准，把真实路径写入 `EndpointConfig`，避免猜测路径。

## 安全说明

- 不要把 token 硬编码进代码仓库。
- 示例改成从环境变量读取：`MOQUAN_TOKEN`。

## 设备接口（已补齐）

- 设备列表：`list_devices`
- 设备详情：`get_device_detail`

## 示例运行

```bash
export MOQUAN_TOKEN='你的token'
python3 example_usage.py
```

## 按文档覆盖路径示例

```python
from moquan_client import EndpointConfig, MoquanClient

client = MoquanClient(
    base_url="https://developers.moquan.live:9090",
    token="YOUR_TOKEN",
    endpoint_config=EndpointConfig(
        # 文档真实地址放第一位
        device_list=["/open/device/list"],
        device_detail=["/open/device/detail"],
        light_control=["/open/light/control"],
        environment_control=["/open/environment/control"],
        water_fertilizer_control=["/open/water-fertilizer/control"],
    ),
)
```
