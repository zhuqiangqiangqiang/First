import os

from moquan_client import EndpointConfig, MoquanClient


def main() -> None:
    token = os.getenv("MOQUAN_TOKEN", "")
    if not token:
        raise RuntimeError("请先设置环境变量 MOQUAN_TOKEN，再运行示例")

    client = MoquanClient(
        base_url="https://developers.moquan.live:9090",
        token=token,
        endpoint_config=EndpointConfig(
            # 把你文档中的“真实地址”放前面，优先命中
            device_list=["/open/device/list", "/device/list", "/api/device/list", "/api/v1/device/list"],
            device_detail=["/open/device/detail", "/device/detail", "/api/device/detail", "/api/v1/device/detail"],
        ),
    )

    print("list_devices =>", client.list_devices(page=1, page_size=20))
    print("get_device_detail =>", client.get_device_detail(device_id="env-001"))


if __name__ == "__main__":
    main()
