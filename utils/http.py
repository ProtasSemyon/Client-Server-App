from builtins import bytes # type: ignore


SUCCESS = 200
NOT_FOUND = 404
BAD_REQUEST = 400
ACCEPTED = 202
VERSION = "1.1"


def parse_headers(package: bytes):
  delim1 = b'\r\n\r\n'
  index = package.find(delim1)
  head = package[:index]
  body = package[index + len(delim1):]
  
  delim2 = b'\r\n'
  index = head.find(delim2)
  first_str = head[:index]
  headers = head[index + len(delim2):]
  headers = headers.split(delim2)
  
  headers_dict = dict()
  for header in headers:
    header_data = header.split(b':')
    headers_dict.update({header_data[0]:header_data[1].split(b',')})
    for info in headers_dict[header_data[0]]:
      info = info.split(b';')[0]
  
  return first_str.split(b' '), headers_dict, body
class HttpHeaders:
  def __init__(self, default: dict | None = None):
    if default is None:
      self.headers = dict()
    else :
      self.headers = default
    
  def add_header(self, name, value):
    if self.headers is None:
      self.headers = dict()
    self.headers[name] = value
    
  def __str__(self):
    result = ""
    for name in self.headers.keys():
      result += f"{name}:{self.headers[name]}" + "\r\n"
    return result
    

class HttpResponse:
  def __init__(self, headers, content: bytearray = b'', status = SUCCESS):
    self.headers = headers
    self.content = content
    self.status = status
    
  def __str__(self):
    response = f"HTTP/{VERSION} {str(self.status)} "
    match self.status:
      case SUCCESS:
        response += "OK"
        response += "\r\n"
    return response + f"{str(self.headers)}\r\n{str(self.content)}"
  
  def __bytes__(self):
    response = f"HTTP/{VERSION} {str(self.status)} "
    match self.status:
      case SUCCESS:
        response += "OK"
        response += "\r\n"
    headers = (response + f"{str(self.headers)}\r\n").encode('utf-8')
    return headers + self.content
      
class HttpRequest:
  def __init__(self, headers, method, uri, content: bytearray = b''):
    self.headers = headers
    self.content = content
    self.method = method
    self.uri = uri
  
  def __str__(self):
    request = f"{self.method} {self.uri} HTTP/{VERSION}\r\n"
    return request + f"{str(self.headers)}\r\n{str(self.content)}"
  
  def __bytes__(self) -> bytearray:
    request = f"{self.method} {self.uri} HTTP/{VERSION}\r\n"
    headers = (request + f"{str(self.headers)}\r\n").encode('utf-8')
    return headers + self.content