from moquan_client import MoquanClient


def main() -> None:
    client = MoquanClient(
        base_url="https://developers.moquan.live:9090",
        token="YOUR_ADMIN_OR_APP_TOKEN",
    )

    # 0) 创建 API Key（通常需要管理权限 token）
    print(
        client.create_api_key(
            name="greenhouse-automation",
            permissions=["light:write", "environment:read", "water-fertilizer:write"],
            expires_at="2026-12-31T23:59:59Z",
        )
    )

    # 1) 灯光控制
    print(client.control_light(device_id="light-001", power=True, brightness=80))

    # 2) 环境信息读取
    print(client.read_environment_info(device_id="env-001"))

    # 3) 水肥控制
    print(
        client.control_water_fertilizer(
            device_id="wf-001",
            irrigation_on=True,
            fertilizer_ratio=0.12,
            duration_seconds=300,
        )
    )

    # 4) 水肥信息读取
    print(client.read_water_fertilizer_info(device_id="wf-001"))


if __name__ == "__main__":
    main()
