# 컴퓨터정보과 3-A 202044008 박준형
# 클라이언트 프로그램 - 여러 프로그램으로 복사하여 실험 진행함.

import socket
import argparse
import threading

port = 2500     # 접속할 포트

def handle_recv(cli_sock, user):
    while 1:
        try:
            data = cli_sock.recv(1024)
        except:
            print("연결이 종료되었습니다.")
            break
        data = data.decode('utf-8')
        if not user in data:
            print(data)

def handle_send(cli_sock):
    while 1:
        data = input()
        cli_sock.send(data.encode('utf-8'))
        if data == "/종료":
            break
    cli_sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "\nClient Application\n-p port\n-i host\n-s string")
    parser.add_argument('-p', help = "port")
    parser.add_argument('-i', help = "host", required = True)
    parser.add_argument('-u', help = "user", required = True)

    args = parser.parse_args()
    host = args.i
    user = str(args.u)
    try:
        port = int(args.p)
    except:
        pass

    # TCP 타입 소켓 객체를 생성
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 호스트와 포트를 통해 서버 접속
    cli_sock.connect((host, port))


    cli_sock.send(user.encode('utf-8'))

    rcv_thread = threading.Thread(target = handle_recv, args = (cli_sock, user))
    rcv_thread.daemon = True
    rcv_thread.start()

    send_thread = threading.Thread(target = handle_send, args = (cli_sock,))
    send_thread.daemon = True
    send_thread.start()

    send_thread.join()
    rcv_thread.join()
