 # Requires python3 with futures pip package.
 from concurrent.futures import ThreadPoolExecutor as PoolExecutor
 import http.client
 import socket
 
 def get_it(url):
     try:
         # always set a timeout when you connect to an external server
         #headers = {"access-token": ""}
         connection = http.client.HTTPSConnection(url, timeout=2)
 
         connection.request("GET", "/core", None, headers)
 
         response = connection.getresponse()
         print(response.status, response.reason)
 
         return response.read()
     except socket.timeout:
         # in a real world scenario you would probably do stuff if the
         # socket goes into timeout
         pass
 
 urls = [
     "www.google.com"
 ] * 200
 
 with PoolExecutor(max_workers=4) as executor:
     for _ in executor.map(get_it, urls):
         pass
