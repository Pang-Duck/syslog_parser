import socket
import json
import time

def send_json_over_udp(json_data, host, port):
    # UDP 소켓 생성
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            # JSON 데이터 전송
            udp_socket.sendto(json_data.encode(), (host, port))
            print("JSON data sended.")
            time.sleep(1)  # 1초 간격으로 전송
    finally:
        udp_socket.close()

if __name__ == "__main__":
    # 전송할 JSON 파일 읽기
    with open("./test_waf.json", "r") as file:
        json_data = file.read()

    # UDP 통신 설정
    host = "localhost"  # 대상 호스트
    port = 8514        # 대상 포트

    # JSON 데이터 전송
    send_json_over_udp(json_data, host, port)