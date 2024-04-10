import socket
import json
import threading
import os


class SyslogParser(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.output_directory = "/data/waf/syslog_files"

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((self.host, self.port))
            print(f"Syslog server listening on {self.host}:{self.port}")

            while True:
                data, _ = server_socket.recvfrom(65535)
                syslog_message = data.decode("utf-8")
                try:
                    json_data = json.loads(syslog_message)
                    filename = "syslog.json"
                    self.save_to_json(json_data, filename)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse syslog message: {e}")

    def save_to_json(self, json_data, filename):
        filepath = os.path.join(self.output_directory, filename)

        with open(filepath, "a") as f:
            # 필요한 정보만 추출하여 저장
            parsed_data = {
                "unit_hostname": json_data.get("unit_hostname"),
                "management_ip_address": json_data.get("management_ip_address"),
                "management_ip_address_2": json_data.get("management_ip_adress_2"),
                "http_class_name": json_data.get("http_class_name"),
                "web_application_name": json_data.get("web_application_name"),
                "policy_name": json_data.get("policy_name"),
                "policy_apply_date": json_data.get("policy_apply_date"),
                "violations": json_data.get("violations"),
                "support_id": json_data.get("support_id"),
                "request_status": json_data.get("request_status"),
                "response_code": json_data.get("response_code"),
                "ip_client": json_data.get("ip_client"),
                "route_domain": json_data.get("route_domain"),
                "method": json_data.get("method"),
                "protocol": json_data.get("protocol"),
                "query_string": json_data.get("query_string"),
                "x_forwarded_for_header_value": json_data.get(
                    "x_forwarded_for_header_value"
                ),
                "sig_ids": json_data.get("sig_ids"),
                "sig_names": json_data.get("sig_names"),
                "date_time": json_data.get("date_time"),
                "severity": json_data.get("severity"),
                "attack_type": json_data.get("attack_type"),
                "geo_location": json_data.get("geo_location"),
                "ip_address_intelligence": json_data.get("ip_address_intelligence"),
                "username": json_data.get("username"),
                "session_id": json_data.get("session_id"),
                "src_port": json_data.get("src_port"),
                "dest_port": json_data.get("dest_port"),
                "dest_ip": json_data.get("dest_ip"),
                "sub_violations": json_data.get("sub_violations"),
                "virus_name": json_data.get("virus_name"),
                "violation_rating": json_data.get("violatlon_rating"),
                "websocket_direction": json_data.get("websocket_direction"),
                "websocket_message_type": json_data.get("websocket_message_type"),
                "device_id": json_data.get("device_id"),
                "staged_sig_ids": json_data.get("staged_sig_ids"),
                "staged_sig_names": json_data.get("staged_sig_names"),
                "threat_campaign_names": json_data.get("threat_campaign_names"),
                "staged_threat_campaign_names": json_data.get(
                    "staged_threat_campaign_names"
                ),
                "blocking_exception_reason": json_data.get("blocking_exception_reason"),
                "captcha_result": json_data.get("captcha_result"),
                "microservice": json_data.get("microservice"),
                "tap_event_id": json_data.get("tap_event_id"),
                "tap_vid": json_data.get("tap_vid"),
                "vs_name": json_data.get("vs_name"),
                "sig_cves": json_data.get("sig_cves"),
                "staged_sig_cves": json_data.get("staged_sig_cves"),
                "uri": json_data.get("uri"),
                "fragment": json_data.get("fragment"),
                "request": json_data.get("request"),
                "response": json_data.get("response"),
            }
            json_string = json.dumps(parsed_data, indent=2)
            f.write(f"{json_string}\n")


if __name__ == "__main__":
    receiver = SyslogParser("0.0.0.0", 8514)
    receiver.start()
    receiver.join()
