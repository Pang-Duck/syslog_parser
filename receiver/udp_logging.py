import socket
import logging
import json


logging.basicConfig(
    filename="udp_packets.log", level=logging.INFO, format="%(asctime)s - %(message)s"
)


UDP_IP = "0.0.0.0"
UDP_PORT = 8516
BUFFER_SIZE = 65535
# TARGET_IP = {"172.19.191.61", "172.19.191.62", "172.19.191.63", "172.19.191.64"}


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    packet_data = data.decode("utf-8")
    info_start_index = packet_data.find("unit_hostname=")
    info_end_index = packet_data.find(",response=")
    info_string = packet_data[info_start_index:info_end_index]
    # 필요한 정보를 JSON 형식으로 변환
    info_list = [item.split("=") for item in info_string.split(",")]
    info_dict = {item[0]: item[1] for item in info_list}
    json_data = json.dumps(info_dict, indent=2)

    logging.info(json_data)


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
