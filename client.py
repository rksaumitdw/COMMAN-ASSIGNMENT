
import socket
import time

client_id = input("Enter Client ID: ")

server_ip = input(
    "Enter Server IP [127.0.0.1]: "
).strip() or "127.0.0.1"

port = int(input("Enter Port Number [5000]: ") or 5000)

protocol = input(
    "Select Protocol (TCP/UDP): "
).upper()

message = input("Enter Message: ")

if protocol == "TCP":

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        client.connect((server_ip, port))

        print("Connection Status: Connected")

        start = time.perf_counter()

        client.sendall(
            (client_id + ": " + message).encode()
        )

        reply = client.recv(1024).decode()

        end = time.perf_counter()

        print("Message Received:", reply)
        print("Acknowledgment: Received")

        print(
            "Transmission Time:",
            round((end - start) * 1000, 3),
            "ms"
        )

    except OSError as error:
        print("Connection Error:", error)

    finally:
        client.close()


elif protocol == "UDP":

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    client.settimeout(3)

    try:
        start = time.perf_counter()

        client.sendto(
            (client_id + ": " + message).encode(),
            (server_ip, port)
        )

        print("Connection Status: Connectionless")

        reply, address = client.recvfrom(1024)

        end = time.perf_counter()

        print("Message Received:", reply.decode())
        print("Acknowledgment: Reply Received")

        print(
            "Transmission Time:",
            round((end - start) * 1000, 3),
            "ms"
        )

    except socket.timeout:
        print("No response received.")

    finally:
        client.close()

else:
    print("Invalid Protocol!")
