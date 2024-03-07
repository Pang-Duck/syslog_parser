import socket
import json
import threading
import clickhouse_connect
import random
import os

class SyslogParser(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.output_directory = "/data/dti_waf/syslog_files"

        # DBserver connect
    def __get_client(self,host='211.115.206.6', database='default') -> object : 
        client = clickhouse_connect.get_client(host=self.host,database=self.database)
        return client
    

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((self.host, self.port))
            print(f"Syslog server listening on {self.host}:{self.port}")

            while True:
                data, _ = server_socket.recvfrom(1024 * 1024 * 100) # 버퍼사이즈 지정
                syslog_message = data.decode('utf-8')
                try:
                    # syslog 메시지를 JSON으로 파싱 및 파일명 생성
                    json_data = json.loads(syslog_message)
                    filename = f"syslog_{random.randint(1,1000)}.json"
                   
                    # JSON 파일 저장
                    self.save_to_json(json_data, filename)

                except json.JSONDecodeError as e:
                    print(f"Failed to parse syslog message: {e}")


    def save_to_json(self, json_data, filename):

        filepath = os.path.join(self.output_directory, filename)
        
        # 파일 형태로 JSON 데이터 저장
        with open(filepath, 'w') as f:
            json.dumps(json_data, f)
            f.write('\n')

if __name__ == "__main__":
    receiver = SyslogParser("0.0.0.0", 8514)
    receiver.start()
    receiver.join()  # 이 부분은 데몬 스레드를 메인 스레드와 동기화하는 목적

