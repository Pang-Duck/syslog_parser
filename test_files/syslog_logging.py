import socket
import json
import threading
import os
import re


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
                    # 사용자 정의 파싱 로직을 통해 필요한 필드 추출
                    parsed_data = self.parse_syslog_message(syslog_message)
                    filename = "syslog.json"
                    self.save_to_json(parsed_data, filename)
                except Exception as e:
                    print(f"Failed to parse syslog message: {e}")

    def parse_syslog_message(self, syslog_message):
        parsed_data = {}

        # unit_hostname
        match = re.search(r'unit_hostname="(.*?)"', syslog_message)
        if match:
            parsed_data["unit_hostname"] = match.group(1)

        # management_ip_address
        match = re.search(r'management_ip address="(.*?)"', syslog_message)
        if match:
            parsed_data["management_ip_address"] = match.group(1)

        # management_ip_address_2
        match = re.search(r'management_ip_adress_2="(.*?)"', syslog_message)
        if match:
            parsed_data["management_ip_address_2"] = match.group(1)

        # http_class_name
        match = re.search(r'http_class_name="(.*?)"', syslog_message)
        if match:
            parsed_data["http_class_name"] = match.group(1)

        # web_application_name
        match = re.search(r'web_application_name="(.*?)"', syslog_message)
        if match:
            parsed_data["web_application_name"] = match.group(1)

        # policy_name
        match = re.search(r'policy_name="(.*?)"', syslog_message)
        if match:
            parsed_data["policy_name"] = match.group(1)

        # policy_apply_date
        match = re.search(r'policy_apply_date="(.*?)"', syslog_message)
        if match:
            parsed_data["policy_apply_date"] = match.group(1)

        # violations
        match = re.search(r'violations="(.*?)"', syslog_message)
        if match:
            parsed_data["violations"] = match.group(1)

        # support_id
        match = re.search(r'support_id="(.*?)"', syslog_message)
        if match:
            parsed_data["support_id"] = match.group(1)

        # request_status
        match = re.search(r'request_status="(.*?)"', syslog_message)
        if match:
            parsed_data["request_status"] = match.group(1)

        # response_code
        match = re.search(r'response_code="(.*?)"', syslog_message)
        if match:
            parsed_data["response_code"] = match.group(1)

        # ip_client
        match = re.search(r'ip_client="(.*?)"', syslog_message)
        if match:
            parsed_data["ip_client"] = match.group(1)

        # route_domain
        match = re.search(r'route_domain="(.*?)"', syslog_message)
        if match:
            parsed_data["route_domain"] = match.group(1)

        # method
        match = re.search(r'method="(.*?)"', syslog_message)
        if match:
            parsed_data["method"] = match.group(1)

        # protocol
        match = re.search(r'protocol="(.*?)"', syslog_message)
        if match:
            parsed_data["protocol"] = match.group(1)

        # x_forwarded_for_header_value
        match = re.search(r'x_forwarded_for_header_value="(.*?)"', syslog_message)
        if match:
            parsed_data["x_forwarded_for_header_value"] = match.group(1)

        # sig_ids
        match = re.search(r'sig_ids="(.*?)"', syslog_message)
        if match:
            parsed_data["sig_ids"] = match.group(1)

        # sig_names
        match = re.search(r'sig_names="(.*?)"', syslog_message)
        if match:
            parsed_data["sig_names"] = match.group(1)

        # date_time
        match = re.search(r'date_time="(.*?)"', syslog_message)
        if match:
            parsed_data["date_time"] = match.group(1)

        # severity
        match = re.search(r'severity="(.*?)"', syslog_message)
        if match:
            parsed_data["severity"] = match.group(1)

        # attack_type
        match = re.search(r'attack_type="(.*?)"', syslog_message)
        if match:
            parsed_data["attack_type"] = match.group(1)

        # geo_location
        match = re.search(r'geo_location="(.*?)"', syslog_message)
        if match:
            parsed_data["geo_location"] = match.group(1)

        # ip_address_intelligence
        match = re.search(r'ip_address_intelligence="(.*?)"', syslog_message)
        if match:
            parsed_data["ip_address_intelligence"] = match.group(1)

        # username
        match = re.search(r'username="(.*?)"', syslog_message)
        if match:
            parsed_data["username"] = match.group(1)

        # session_id
        match = re.search(r'session_id="(.*?)"', syslog_message)
        if match:
            parsed_data["session_id"] = match.group(1)

        # src_port
        match = re.search(r'src_port="(.*?)"', syslog_message)
        if match:
            parsed_data["src_port"] = match.group(1)

        # dest_port
        match = re.search(r'dest_port="(.*?)"', syslog_message)
        if match:
            parsed_data["dest_port"] = match.group(1)

        # dest_ip
        match = re.search(r'dest_ip="(.*?)"', syslog_message)
        if match:
            parsed_data["dest_ip"] = match.group(1)

        # sub_violations
        match = re.search(r'sub_violations="(.*?)"', syslog_message)
        if match:
            parsed_data["sub_violations"] = match.group(1)

        # virus_name
        match = re.search(r'virus_name="(.*?)"', syslog_message)
        if match:
            parsed_data["virus_name"] = match.group(1)

        # violation_rating
        match = re.search(r'violation_rating="(.*?)"', syslog_message)
        if match:
            parsed_data["violation_rating"] = match.group(1)

        # websocket_direction
        match = re.search(r'websocket_direction="(.*?)"', syslog_message)
        if match:
            parsed_data["websocket_direction"] = match.group(1)

        # websocket_message_type
        match = re.search(r'websocket_message_type="(.*?)"', syslog_message)
        if match:
            parsed_data["websocket_message_type"] = match.group(1)

        # device_id
        match = re.search(r'device_id="(.*?)"', syslog_message)
        if match:
            parsed_data["device_id"] = match.group(1)

        # staged_sig_ids
        match = re.search(r'staged_sig_ids="(.*?)"', syslog_message)
        if match:
            parsed_data["staged_sig_ids"] = match.group(1)

        # staged_sig_names
        match = re.search(r'staged_sig_names="(.*?)"', syslog_message)
        if match:
            parsed_data["staged_sig_names"] = match.group(1)

    def save_to_json(self, json_data, filename):
        filepath = os.path.join(self.output_directory, filename)

        with open(filepath, "a") as f:
            json_string = json.dumps(json_data, indent=2)
            f.write(f"{json_string}\n")


if __name__ == "__main__":
    receiver = SyslogParser("0.0.0.0", 8514)
    receiver.start()
    receiver.join()
