access_control_allow_origin  = "Access-Control-Allow-Origin"
access_control_allow_methods = "Access-Control-Allow-Methods"
content_type                 = "Content-Type"
host                         = "Host"
accept                       = "Accept"
accept_encoding              = "Accept-Encoding"
user_agent                   = "User-Agent"

default_server_headers = {
  access_control_allow_origin   : "http://localhost:8080"
  #access_control_allow_methods  : "GET, POST, OPTIONS",
  #content_type                  : "text/html"
}

default_client_headers = {
  host            : "127.0.0.1:8080",
  user_agent      : "CLOWN",
  accept          : "text/plain",
  accept_encoding : "utf-8"
}


