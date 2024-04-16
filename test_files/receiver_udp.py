import socket
import json
import threading
import random
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
                data, _ = server_socket.recvfrom(65535)  # 버퍼사이즈 지정
                syslog_message = data.decode("utf-8")
                try:
                    # syslog 메시지를 JSON으로 파싱 및 파일명 생성
                    json_data = json.loads(syslog_message)
                    filename = "syslog.json"

                    # JSON 파일 저장
                    self.save_to_json(json_data, filename)

                except json.JSONDecodeError as e:
                    print(f"Failed to parse syslog message: {e}")

    def save_to_json(self, json_data, filename):
        filepath = os.path.join(self.output_directory, filename)

        if os.path.exists(f"{filepath}"):
            # 파일이 이미 존재하면 기존 파일에 이어서 로그를 추가
            with open(filepath, "a") as f:
                json_string = json.dumps(json_data)
                f.write(f"{json_string}\n")
        else:
            # 파일이 존재하지 않으면 새 파일에 로그를 작성
            with open(filepath, "w") as f:
                json_string = json.dumps(json_data)
                f.write(f"{json_string}\n")

    # with open(filepath, 'w') as f:
    #     json_string = json.dumps(json_data)
    #     f.write(f'{json_string}\n')


if __name__ == "__main__":
    receiver = SyslogParser("0.0.0.0", 8514)
    receiver.start()
    receiver.join()  # 이 부분은 데몬 스레드를 메인 스레드와 동기화하는 목적
