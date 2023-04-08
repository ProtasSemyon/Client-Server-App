from builtins import bytes # type: ignore
import os 
import socket
from utils.headers import *
from utils.http import *
import click
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ServerConfig:
  def __init__(self, 
               host = "127.0.0.1",
               port = 8080,
               pack_size = 1024,
               log_file = 'log.txt',
               charset = "utf-8",
               root = "server/"):
    self.host = host
    self.port = port
    self.pack_size = pack_size
    self.charset = charset
    self.root = root
    self.log_file = log_file
    
class Server:
  def __init__(self, config: ServerConfig):
    self.config = config
    self.methods = ['GET', 'POST', 'OPTIONS']
    
    handler = logging.FileHandler(self.config.log_file)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    handler_console = logging.StreamHandler()
    handler_console.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.addHandler(handler_console)
    
  def methods_to_str(self):
    result = ""
    for method in self.methods:
      result += method + ", "
    result = result[:-2]
    return result
  
  def start(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.config.host, self.config.port))
    self.sock.listen(0)
    logger.info("Server listening on " + self.config.host + ":" + str(self.config.port))
    
    try:
      while True:
        connection, addr = self.sock.accept()
        self.handle_connection(connection)
        connection.shutdown(socket.SHUT_WR)
        logger.info("Connection " + addr[0] + ":" + str(addr[1]) + " closed")
    except KeyboardInterrupt:
      self.sock.shutdown(socket.SHUT_WR)
      self.sock.close()
      logger.info("Server shutdown")
          
  def handle_connection(self, connection: socket.socket):
    request = connection.recv(self.config.pack_size)
    
    first_str, headers, body = parse_headers(request)
    
    method = first_str[0]
    
    first_str_log = b" ".join(first_str)
    
    code = SUCCESS
    
    match method:
      case b'GET':
        code = self.send_get(connection, first_str[1], headers)
      case b'OPTIONS':
        code = self.send_options(connection)
      case b'POST':
        code = self.send_post(connection, first_str[1], headers, body)
      case _:
        code = self.send_bad_request(connection, headers)
    logger.info((first_str_log + b" " + str(code).encode('utf-8')).decode('utf-8'))
    
  def send_bad_request(self, connection, headers):
    if headers[user_agent.encode('utf-8')][0] == b'CLOWN':
      new_headers = HttpHeaders(default_server_headers)
      new_headers.add_header(access_control_allow_methods, self.methods_to_str())
      connection.send(bytes(HttpResponse(new_headers, b'Bad request', status=BAD_REQUEST))) # type: ignore
    else:
      self.send_get(connection, '/400.html', {})
    return BAD_REQUEST
      
  def send_post(self, connection, uri, headers, data):
    if uri == b'/':
      return self.send_bad_request(connection, headers)
    if type(uri) == bytes:
      uri = uri.decode('utf-8')
    filename = (self.config.root + uri[1:]).encode('utf8')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
      f.write(data)
      f.close()
    return self.send_ok(connection, headers)
  
  def detect_type_of_file(self, filename):
    extension = os.path.splitext(filename)[1]
    if type(extension) is bytes:
      extension = extension.decode('utf-8')
    
    match extension:
      case '.html':
        return 'text/html'
      case '.json':
        return 'application/json'
      case '.png':
        return 'image/png'
      case '.jpg':
        return 'image/jpeg'
      case '.jpeg':
        return 'image/jpeg'
      case '.css':
        return 'text/css'
      case '.js':
        return 'text/javascript'
      case '.svg':
        return 'image/svg+xml'
      case '.gif':
        return 'image/gif'
      case _:
        return 'text/plain'
  
  def send_get(self, connection, uri, headers):
    if uri == b'/':
      return self.send_ok(connection, headers)
    if type(uri) == bytes:
      uri = uri.decode('utf-8')
    filename = (self.config.root + uri[1:]).encode('utf8')
       
    try:
      with open(filename, 'rb') as file:
        new_headers = HttpHeaders(default_server_headers)
        file_ext = self.detect_type_of_file(filename)
        new_headers.add_header(content_type, file_ext)
        connection.send(bytes(HttpResponse(new_headers)))
        connection.sendfile(file)
    except FileNotFoundError:
      return self.send_not_found(connection, headers)
      
  def send_options(self, connection):
    headers = HttpHeaders(default_server_headers)
    headers.add_header(access_control_allow_methods, self.methods_to_str())
    connection.send(bytes(HttpResponse(headers)))
    return SUCCESS
  
  def send_ok(self, connection, headers):
    if headers[user_agent.encode('utf-8')][0] == b'CLOWN':
      new_headers = HttpHeaders(default_server_headers)
      connection.send(bytes(HttpResponse(new_headers)))
    else:
      self.send_get(connection, '/200.html', {})
    return SUCCESS
      
  def send_not_found(self, connection, headers):
    if headers[user_agent.encode('utf-8')][0] == b'CLOWN':
      headers = HttpHeaders(default_server_headers)
      connection.send(bytes(HttpResponse(headers, status=NOT_FOUND)))
    else:
      self.send_get(connection, '/404.html', {})
    return NOT_FOUND

@click.command()
@click.option('-h', '--host', default='localhost', help='Server host. Default: localhost')
@click.option('-p', '--port', default=8080, help='Server port. Default: 8080')
@click.option('-l', '--log_file', default = 'server.log', help='Log file name. Default: log.txt')
def server_run(host, port, log_file):
  server = Server(ServerConfig(host=host, port=port, log_file=log_file))
  server.start()
    
if __name__ == "__main__":
  server_run()   