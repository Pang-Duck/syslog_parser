import socket
import json
import threading

class SyslogParserTCP(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"WAF Syslog server listening on {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    while True:
                        data = client_socket.recv(4096)
                        if not data:
                            break
                        
                        syslog_message = data.decode('utf-8')
                        try:
                            # syslog 메시지를 JSON으로 파싱
                            json_data = json.loads(syslog_message)
                            
                            # 원하는 대로 처리하는 부분 추가
                            process_waf_log(json_data)
                        except json.JSONDecodeError as e:
                            print(f"Failed to parse syslog message: {e}")

def process_waf_log(json_data):
    # 여기에 WAF syslog 메시지를 처리하는 코드를 추가

    # 예시: AWS WAF syslog에서 필드 추출 및 출력
    timestamp = json_data.get("timestamp")
    webacl_id = json_data.get("webaclId")
    client_ip = json_data.get("httpRequest", {}).get("clientIp")

    print(f"Timestamp: {timestamp}, WebACL ID: {webacl_id}, Client IP: {client_ip}")

if __name__ == "__main__":
    receiver = SyslogParserTCP("0.0.0.0", 8514)
    receiver.start()
    receiver.join()  # 이 부분은 데몬 스레드를 메인 스레드와 동기화하는 목적