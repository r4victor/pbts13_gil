# A TCP echo server with a given number of dummy CPU-bound threads.
# Measure the effects of CPU-bound threads on I/O-bound threads.
# See how switch_interval affects the performance.
# Run: $ python effect2_server_threads.py number_of_cpu_threads [switch_interval]
# Then run the client: $ python effect2_client.py


from threading import Thread
import socket
import sys


def compute():
    n = 0
    while True:
        n += 1
        n -= 1


def run_server(host='127.0.0.1', port=33333):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client_sock, addr = sock.accept()
        print('Connection from', addr)
        Thread(target=handle_client, args=(client_sock,)).start()


def handle_client(sock):
    while True:
        received_data = sock.recv(4096)
        if not received_data:
            break
        sock.sendall(received_data)

    print('Client disconnected:', sock.getpeername())
    sock.close()


def main():
    cpu_threads_num = int(sys.argv[1])

    if len(sys.argv) >= 3:
        switch_interval = float(sys.argv[2])
        sys.setswitchinterval(switch_interval)

    for _ in range(cpu_threads_num):
        Thread(target=compute).start()
    run_server()


if __name__ == '__main__':
    main()