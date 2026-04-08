from moquan_client import MoquanClient


def main() -> None:
    client = MoquanClient(
        base_url="https://developers.moquan.live:9090",
        token="YOUR_ADMIN_OR_APP_TOKEN",
    )

    # 0) API Key 管理
    created_key = client.create_api_key(
        name="greenhouse-automation",
        permissions=[
            "apikey:read",
            "light:write",
            "light:read",
            "environment:write",
            "environment:read",
            "water-fertilizer:write",
            "water-fertilizer:read",
        ],
        expires_at="2026-12-31T23:59:59Z",
    )
    print("create_api_key =>", created_key)
    print("list_api_keys =>", client.list_api_keys(page=1, page_size=10))

    # 1) 灯光控制 + 状态读取
    print("control_light =>", client.control_light(device_id="light-001", power=True, brightness=80))
    print("read_light_info =>", client.read_light_info(device_id="light-001"))

    # 2) 环境控制 + 传感器/控制信息读取
    print(
        "control_environment =>",
        client.control_environment(
            device_id="env-001",
            mode="auto",
            target_temperature=24.5,
            target_humidity=60.0,
            target_co2=800,
            fan_on=True,
            heater_on=False,
            humidifier_on=False,
            dehumidifier_on=True,
        ),
    )
    print("read_environment_info =>", client.read_environment_info(device_id="env-001"))
    print(
        "read_environment_control_info =>",
        client.read_environment_control_info(device_id="env-001"),
    )

    # 3) 水肥控制 + 信息读取
    print(
        "control_water_fertilizer =>",
        client.control_water_fertilizer(
            device_id="wf-001",
            irrigation_on=True,
            fertilizer_ratio=0.12,
            duration_seconds=300,
        ),
    )
    print(
        "read_water_fertilizer_info =>",
        client.read_water_fertilizer_info(device_id="wf-001"),
    )

    # 4) 吊销 API Key（按需执行）
    # print("revoke_api_key =>", client.revoke_api_key(api_key_id="YOUR_API_KEY_ID"))


if __name__ == "__main__":
    main()
