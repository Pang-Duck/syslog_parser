import socket
import logging
import json
import uuid

UDP_IP = "0.0.0.0"
UDP_PORT = 8516
BUFFER_SIZE = 65535
# TARGET_IP = {"172.19.191.61", "172.19.191.62", "172.19.191.63", "172.19.191.64"}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

logging.basicConfig(
    filename="udp_packets.log",
    level=logging.INFO,
    format="%(message)s",
)

while True:
    try:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        packet_data = data.decode("utf-8")

        # syslog의 첫번째 필드
        info_start_index = packet_data.find("unit_hostname=")
        if info_start_index == -1:
            logging.warning(f"unit_hostname not found in packet: {packet_data}")
            continue  # 패킷 무시

        info_string = packet_data[info_start_index:]
        info_list = [item.split("=", 1) for item in info_string.split(",")]

        info_dict = {}
        for item in info_list:
            try:
                key, value = item
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

        # UUID를 사용하여 파일명 생성
        unique_filename = f"udp_packet_{uuid.uuid4()}.log"

        with open(unique_filename, "a") as f:
            f.write(json_data + "\n")

        logging.info(json_data)

    except Exception as e:
        logging.error(f"Error processing packet: {e}")
        pass


# while True:
#    data, addr = sock.recvfrom(BUFFER_SIZE)
#
#    # 특정 IP 주소에서 들어온 패킷만 처리
#    if addr[0] in TARGET_IP:
#        packet_data = data.decode("utf-8")
#        info_start_index = packet_data.find("unit_hostname=")
#        info_end_index = packet_data.find(",response=")
#        info_string = packet_data[info_start_index:info_end_index]
#
#        info_list = [item.split("=") for item in info_string.split(",")]
#        info_dict = {item[0]: item[1] for item in info_list}
#        json_data = json.dumps(info_dict, indent=2)
#
#        logging.info(json_data)
