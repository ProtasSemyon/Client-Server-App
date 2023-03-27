import socket

class ServerConfig:
  def __init__(self, 
               host = "127.0.0.1",
               port = 8080,
               listen = 4, 
               pack_size = 1024,
               charset = "utf-8"):
    self.host = host
    self.port = port
    self.listen = listen
    self.pack_size = pack_size
    self.charset = charset
    
class Server:
  def __init__(self, config: ServerConfig):
    self.config = config
  
  def start(self):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.config.host, self.config.port))
    self.sock.listen(self.config.listen)
    print("Server listening on " + self.config.host + ":" + str(self.config.port))
    
    try:
      while True:
        connection, addr = self.sock.accept()
        self.handle_connection(connection)
        connection.shutdown(socket.SHUT_WR)
        print("Connection closed")
    except KeyboardInterrupt:
      self.sock.close()
      print("Server shutdown")
    
  def handle_connection(self, connection):
    data = connection.recv(self.config.pack_size).decode(self.config.charset)
    print(data)
    connection.send(data.encode(self.config.charset))
    
if __name__ == "__main__":
  server = Server(ServerConfig())
  server.start()
    