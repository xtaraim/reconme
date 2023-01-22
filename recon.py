import socket
import requests
from bs4 import BeautifulSoup

# target website
target_url = "https://www.example.com"

# check if the website is live
try:
    requests.get(target_url)
    print("Website is live.")
except requests.exceptions.RequestException as e:
    print("Website is down.")
    exit()

# resolve the IP address of the target website
ip_address = socket.gethostbyname(target_url)
print("IP address:", ip_address)

# check open ports
open_ports = []
for port in range(1, 65535):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((ip_address, port))
    if result == 0:
        open_ports.append(port)
    sock.close()

if open_ports:
    print("Open ports:", open_ports)
else:
    print("No open ports found.")

# check for internal IPs
internal_ips = []
r = requests.get(target_url)
soup = BeautifulSoup(r.content, 'html.parser')
for link in soup.find_all('a'):
    url = link.get('href')
    if url.startswith("http"):
        ip = socket.gethostbyname(url.split("/")[2])
        if ip == ip_address:
