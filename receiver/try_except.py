info_dict = {}
for item in info_list:
    try:
        key, value = item.split("=")
        info_dict[key] = value.strip('"')
    except ValueError:
        # split("=")에서 값이 예상대로 나오지 않는 경우
        # 이 로그를 남기고 다음 아이템으로 넘어감
        logging.warning(f"Issue parsing item: {item}")

# 필요한 항목이 없는 경우 기본값 설정
required_keys = [
    "unit_hostname",
    "management_ip_address",
    "http_class_name",
    "web_application_name",
    "policy_name",
    "policy_apply_date",
    "request_status",
    "response_code",
    "ip_client",
    "date_time",
    "severity",
    "src_port",
    "dest_port",
    "dest_ip",
    "staged_sig_names",
    "uri",
    "request",
    "response",
]
default_values = {
    "violations": "N/A",
    "support_id": "N/A",
    "method": "N/A",
    "protocol": "N/A",
    "x_forwarded_for_header_value": "N/A",
    "sig_ids": "N/A",
    "sig_names": "N/A",
    "attack_type": "N/A",
    "geo_location": "N/A",
    "ip_address_intelligence": "N/A",
    "username": "N/A",
    "session_id": "N/A",
    "sub_violations": "N/A",
    "virus_name": "N/A",
    "violation_rating": "N/A",
    "websocket_direction": "N/A",
    "websocket_message_type": "N/A",
    "device_id": "N/A",
    "staged_sig_ids": "N/A",
    "threat_campaign_names": "N/A",
    "staged_threat_campaign_names": "N/A",
    "blocking_exception_reason": "N/A",
    "captcha_result": "N/A",
    "microservice": "N/A",
    "tap_event_id": "N/A",
    "tap_vid": "N/A",
    "vs_name": "N/A",
    "sig_cves": "N/A",
    "staged_sig_cves": "N/A",
    "fragment": "N/A",
}

for key in required_keys:
    if key not in info_dict:
        info_dict[key] = default_values.get(key, "N/A")

# 마지막으로 로깅
json_data = json.dumps(info_dict, indent=2)
with open("udp_packet.log", "a") as f:
    f.write(json_data + "\n")
logging.info(json_data)
