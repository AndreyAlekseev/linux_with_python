import socket
from config import HOST, PORT, BUFFER_SIZE

my_socket = socket.socket()
print(f'Your port: {PORT}')
my_socket.bind((HOST, PORT))
my_socket.listen()
connection, address = my_socket.accept()
print(f'Browser address: {address}')
data = connection.recv(BUFFER_SIZE).decode("utf-8").strip()
request_headers: dict = {}
headers = data.split(sep="\r\n")
server_response: str = f"HTTP/1.1 200 OK"
result = None
for i, header in enumerate(headers):
    if i == 0:
        continue
    header_key = header.split(sep=":")[0].strip()
    header_value = header.split(sep=":")[1].strip()
    request_headers[header_key] = header_value
    result = '; '.join(f'{key.capitalize()}: {value}' for key, value in request_headers.items())

connection.send(
    f"{server_response}\r\n\r\n<h1>Received headers:</h1>\r\n\r\n<div>{result}</div>".encode("utf-8"))
