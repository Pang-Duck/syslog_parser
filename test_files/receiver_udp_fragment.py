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
        self.buffer_size = 65535  # 버퍼 사이즈 지정

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((self.host, self.port))
            print(f"Syslog server listening on {self.host}:{self.port}")

            while True:
                data, _ = server_socket.recvfrom(self.buffer_size)
                self.process_data(data)

    def process_data(self, data):
        try:
            # 조각화된 데이터 조합
            if hasattr(self, "fragmented_data"):
                self.fragmented_data += data
            else:
                self.fragmented_data = data

            syslog_message = self.fragmented_data.decode("utf-8")
            json_data = json.loads(syslog_message)

            filename = f"syslog_{random.randint(1,1000)}.json"
            self.save_to_json(json_data, filename)

            # 조합된 데이터 초기화
            self.fragmented_data = b""
        except json.JSONDecodeError as e:
            print(f"Failed to parse syslog message: {e}")

    def save_to_json(self, json_data, filename):
        filepath = os.path.join(self.output_directory, filename)

        if os.path.exists(filepath):
            with open(filepath, "a") as f:
                json_string = json.dumps(json_data)
                f.write(f"{json_string}\n")
        else:

            with open(filepath, "w") as f:
                json_string = json.dumps(json_data)
                f.write(f"{json_string}\n")


if __name__ == "__main__":
    receiver = SyslogParser("0.0.0.0", 8514)
    receiver.start()
    receiver.join()
