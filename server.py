
import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

# Handle TCP clients
def handle_tcp_client(conn, address):
    print("TCP Client Connected:", address)

    try:
        while True:
            data = conn.recv(1024)

            if not data:
                break

            message = data.decode()
            print("TCP Message:", message)

            reply = "ACK: " + message
            conn.sendall(reply.encode())

    finally:
        conn.close()
        print("TCP Client Disconnected:", address)


# TCP Server
def run_tcp_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen()

    print("TCP Server Listening...")

    while True:
        conn, address = server.accept()

        thread = threading.Thread(
            target=handle_tcp_client,
            args=(conn, address)
        )

        thread.start()


# UDP Server
def run_udp_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    server.bind((HOST, PORT))

    print("UDP Server Listening...")

    while True:
        data, address = server.recvfrom(1024)

        message = data.decode()
        print("UDP Message:", message)

        reply = "RECEIVED: " + message

        server.sendto(reply.encode(), address)


# Start both servers
threading.Thread(
    target=run_tcp_server,
    daemon=True
).start()

run_udp_server()
