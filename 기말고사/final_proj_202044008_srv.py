import socket
import argparse
import threading
import time

svrIP = "127.0.0.1" # IP 주소
port = 2500         # 포트 번호
user_list = {}
notice_flag = 0

def msg_func(msg):
    print(msg)
    for con in user_list.values():
        try:
            con.send(msg.encode('utf-8'))
        except:
            print("연결이 비정상적으로 종료된 소켓이 발견되었습니다.")

def handle_rcv(cli_sock, addr, user):
    msg = "---- %s님이 채팅방에 들어오셨습니다. ----"%user
    msg_func(msg)
    while 1:
        data = cli_sock.recv(1024)
        string = data.decode('utf-8')

        if "/종료" in string:
            msg = "---- %s님이 채팅방에서 나가셨습니다. ----"%user
            # 연결 종료한 사용자 정보 삭제
            del user_list[user]
            msg_func(msg)
            break
        string = "%s : %s"%(user, string)
        msg_func(string)
    cli_sock.close()

def handle_notice(cli_sock, addr, user):
    pass

def accept_func():
    # IPv4 체계, TCP 타입 소켓 객체를 생성
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 포트를 사용 중일 시 오류 해결
    srv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # IP주소와 포트번호를 함께 socket에 바인드.
    # 포트의 범위는 1-65535 사이의 숫자를 사용할 수 있다.
    srv_sock.bind((svrIP, port))

    #서버가 최대 5개의 클라이언트의 접속을 허용한다.
    srv_sock.listen(5)

    while 1:
        try:
            #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            cli_sock, addr = srv_sock.accept()
        except KeyboardInterrupt:
            for user, con in user_list:
                con.close()
            srv_sock.close()
            print("인터럽트 요청이 입력되었습니다.")
            break
        user = cli_sock.recv(1024).decode('utf-8')
        user_list[user] = cli_sock

        # accept()함수로 입력만 받아주고 이후 알고리즘은 핸들러에게 맡김.
        notice_thread = threading.Thread(target=handle_notice, args=(cli_sock, addr, user))
        notice_thread.daemon = True
        notice_thread.start()

        receive_thread = threading.Thread(target=handle_rcv, args=(cli_sock, addr,user))
        receive_thread.daemon = True
        receive_thread.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="\nFinal Project\n-p port\n")
    parser.add_argument('-p', help="port")

    args = parser.parse_args()
    try:
        port = int(args.p)
    except:
        pass
    accept_func()
