import socket
from utils.headers import *
from utils.http import *

class ClientConfig:
  def __init__(self,
               server_host = "127.0.0.1",
               server_port = 8080,
               pack_size = 1024,
               charset = "utf_8"):
    self.server_host = server_host
    self.server_port = server_port
    self.pack_size = pack_size
    self.charset = charset
    
class Client:
  def __init__(self, config: ClientConfig):
    self.config = config
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
  def connect(self):
    self.socket.connect((self.config.server_host, self.config.server_port))
    
  def send_request(self, method, uri, data): 
    headers = HttpHeaders(default_client_headers)
    if len(uri) == 0:
      uri = '/'
    if uri[0] != '/':
      uri = '/' + uri
    self.connect()
    self.socket.send(bytes(HttpRequest(headers, method, uri, data)))
    
    self.socket.shutdown(socket.SHUT_WR)    
    recv_data = b""
    while True:
      data = self.socket.recv(self.config.pack_size)
      if not data: break
      recv_data += data
    print(recv_data.decode('utf-8'))  
  def close(self):
    self.socket.close()
    
if __name__ == "__main__":
  while True:
    cl = Client(ClientConfig())
    mess = input("Send a message to the server: ")
    cl.send_request('POST', mess, b"clown information")
  
  