SUCCESS = 200
VERSION = "1.1"

class HttpHeaders:
  def __init__(self):
    self.headers = dict()
    
  def add_header(self, name, value):
    self.headers[name] = value
    
  def __str__(self):
    result = ""
    for name in self.headers.keys():
      result += f"{name}: {self.headers[name]}" + "\r\n"
    return result
    

class HttpResponse:
  def __init__(self, headers, content, status = SUCCESS):
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
  
class HttpRequest:
  def __init__(self, headers, content, method, uri):
    self.headers = headers
    self.content = content
    self.method = method
    self.uri = uri
  
  def __str__(self):
    response = f"{self.method} {self.uri} HTTP/{VERSION}\r\n"
    return response + f"{str(self.headers)}\r\n\r\n{str(self.content)}"