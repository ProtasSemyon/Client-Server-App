import socket
from utils.headers import *
from utils.http import *

import click
import logging

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
    self.socket.connect((self.config.server_host, self.config.server_port)) # type: ignore
    
  def send_request(self, method, uri, data, show_all): 
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
      
    first_str, head, body = parse_headers(recv_data)
    first_str_log = (b" ".join(first_str)).decode("utf-8")

    if show_all:
      print(recv_data.decode("utf-8"))
    else:
      print(first_str_log)
      
  def close(self):
    self.socket.close()
    
@click.command()
@click.option('-h', '--host', default='localhost', help='Host for connecting')
@click.option('-p', '--port', default=8080, help='Port for connecting')
@click.option('-m', '--method', default='GET', help='HTTP method')
@click.option('-u', '--uri', default='/', help="Unique Resource Identifier")
@click.option('-b', '--body', default="", help="Content for send")
@click.option('-f', '--file', default="", help="File to send")
@click.option('-s', '--show_all', default=False, help="Show all data from HTTP Response")
def client_run(host, port, method, uri, body, file, show_all):
  client = Client(ClientConfig(server_host=host, server_port=port))
  data = body.encode("utf-8")
  if file != "":
    try:
      with open(file, 'rb') as file:
        data = file.read()
    except FileNotFoundError:
      print("bruh")
  
  client.send_request(method, uri, data, show_all)

if __name__ == "__main__":
  client_run()
  
  