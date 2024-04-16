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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)  # 연결 수신 대기

            print(f"Syslog server listening on {self.host}:{self.port}")

            while True:

                connection, _ = server_socket.accept()
                print("Client connected.")

                try:

                    data = connection.recv(65535)
                    syslog_message = data.decode("utf-8")

                    json_data = json.loads(syslog_message)
                    filename = f"syslog_{random.randint(1,1000)}.json"

                    self.save_to_json(json_data, filename)

                except json.JSONDecodeError as e:
                    print(f"Failed to parse syslog message: {e}")

                finally:
                    # 클라이언트 연결 종료
                    connection.close()
                    print("Client disconnected.")

    def save_to_json(self, json_data, filename):
        filepath = os.path.join(self.output_directory, filename)

        if os.path.exists(filepath):

            with open(filepath, "a") as f:
                json.dump(json_data, f, indent=4)
                f.write("\n")
        else:

            with open(filepath, "w") as f:
                json.dump(json_data, f, indent=4)
                f.write("\n")


if __name__ == "__main__":
    receiver = SyslogParser("0.0.0.0", 8514)
    receiver.start()
    receiver.join()
