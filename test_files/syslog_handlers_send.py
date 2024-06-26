import json
import socket
import time
import logging
import logging.handlers

# 로그 레벨 및 포맷 설정
logger = logging.getLogger()

logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s")

# SyslogHandler 설정
syslog_handler = SysLogHandler(
    address=("123.123.123.123", 8516), socktype=socket.SOCK_DGRAM
)
syslog_handler.setLevel(logging.INFO)
syslog_handler.setFormatter(formatter)


# FileHandler 설정
# file_handler = logging.FileHandler('/data/waf/syslog_files/test5.log',mode ="w")
# file_handler.setLevel(logging.info)
# file_handler.setFormatter(formatter)

# Logger에 SyslogHandler 추가
logger.addHandler(syslog_handler)
# logger.addHnadler(file_handler)

# 로그 메시지 출력
logger.info(
    'J5_WAF_DR_1.test.com ASM:unit_hostname="J5_WAF_DR_1.test.com",management_ip address="172.73.191.241",management_ip_adress_2="N/A",http_class_name="/Comon/20191212_dr_test_pollcy",web_application_name="/Comon/20191212_dr_test_policy",policy_name="/Comon/20191212_dr_test_policy",policy_apply_date="2024-1-31 19:25:56",violations="N/A",support_id="17385031276654459874",request_status="passed",response_code="200",ip_client="59.7.254.200",route_domain="0",method="POST",protocol="HTTP",query_string="",x_forwarded_for_header_value="N/A",sig_ids="N/A",sig_names="N/A",date_time="2024-02-02 14:12:50",severity="Informational",attack_type="N/A",geo_location="KR",ip_address_intelligence="N/A",username="N/A",session_id="22ad7acirfc0323b",src_port="60866",dest_port="80",dest_ip="192.168.178,136",sub_violations="N/A",virus_name="N/A",violatlon_rating="1",websocket_direction="N/A",websocket_message_type="N/A",device_id="N/A",staged_sig_ids="200005007",staged_sig_names="LDAP injection attempt (CN in Distinguished Name)",threat_campaign_names="N/A",staged_threat_campaign_names="N/A",blocking_exception_reason="N/A",captcha_result="not_received",microservice="N/A",tap_event_id="N/A",tap_vid="N/A",vs_name="/Common/vs_dr sof_80",sig_cves="N/A",staged_sig_cves="N/A",uri="/transkeyServlet",fragment="",request="POST /transkeyServlet HTTP/1.1\r\nHost:tstrib3.shinnan.comtrinconnection:keep alivelrincontent-Lengtn:672\rinsec-ch-ua:12 2Not A(Brands22:v-X2299x22.X22Google Chramax22:v-X2212122,%2Chcomiu271v-%22121x22\r\nsac-ch-ua-platform:X22windowsk22\r\nsec-ch-ua-nobile:70\r\nuser-Agent:Moziila/5.0 (Hindows NT 10.win64:x4)ApplewebKit/537.36 (KHTML.like Gucko)chrom/121,0.0.0 Safori/537,30\rkncontent-type:applicaticn/x-mw-Torm-urlencoded:charset-UTF-BrAnAccept/rnorigin:ht tps://tstrib3.test.com\r\nsec-Fotch-Site:same-origin\r\nses-Fetch-Hode cors\r\nsec-Fatch-Dest:erpty\r\nReferer:https://tstrib3.test.cow/Indox jspirinAccept Encodingi geip,de flato,br\r\nAccept-Language:ko-KR,ko:q-B.9.n-0B,eniq-a.7\r\nCookie:USER PLATFORM-Win32,Systen languago-kg_D-092J01cB-5ca8-Jc9c-3842-83dabacb194d-170623358513d:PCTn-7CA 0439220,810-6417184346013,1786487165:-8n-09231Zp18-C31,1,1705340528.10,117868485424.8.=g393KTT3D57S-151.1170034852810.11796R54200,0:-85585cH65651,1,175248573 10.1.1706848542.0.0.0:SESSIONID-M321cVSHLnc71senaTUkSOQepCtQHQ2hrvNteozAUj3NKSano55v9qulG1ZYr cmizG9tYNlut 3/pY7437ThcHBFNI-GA12 439402034.1706233577:SELFCTED_CERT IAFO- (27duvlceTds22:22HARD_DISK22,22devicnSub22:%222222ck22:X22id-cignkoras2TstcAcout JDAccrediteucAcok70signkorea2Cc0KR88n-00x31)lastAccss-17 06850224492;14 etrunnc110;aLL4117605458-1-1i-5a2 TOMVEWC95-6s1,2.1706858771.26,0,1706059077763.0.0 inirtropmset5e3imK-yky-e4ba2878uro9dr615s5e95953173528373a9ac58675 -9f4013Dt8r846t3b886b32de:50aa09272t69n488edc771c4b74c5f8383edac644742ec941792c2343a931381fb1c1255f9d4h3a1r556rf2 caodsbtodf4t3258e34397b5d131a565d94613447a1b14202490ea817 6b60f31fea18d6760535 afbc38a97C96d9424959e97e4566b99ed05947f56(58398t9c8991aitd4dia3csba5c28z46a/147a4e921eab16b7t925a16704eds09gfot13a5258c16:0:455cr7A3rf9963afe5t11c4026 9bf24546f091r29cc79/edsar2dc370a22c66cde58e82a8c47ds4aacbdc76d75de9foBf4fcaaf27cc7afroe5ade42transkeyuuid-37083a2cc00c7b2fc550060808-71651069887a7e/bfo5c668271esersuseCert-tru e&rode-commonBTK-requestToken-1535463269origIn=0",response="Response lo2ging disabled"'
)
