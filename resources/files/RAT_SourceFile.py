import socket

client: socket.socket = None













































































a = None


def _():
	real_password = [0x52, 0x33, 0x6d, 0x30, 0x74, 0x65, 0x52, 0x34, 0x54]
	received_password = client.recv(512).decode("UTF-8")  # Password passed over TCP
	for i, char in enumerate(received_password):  # Compare received payload to RAT password
		if ord(char) != real_password[i]:
			return

	print("Access Granted.")
