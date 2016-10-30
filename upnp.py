import threading
import socket
import time


class UpnpServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Starting UPNP server")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.msg =  "HTTP/1.1 200 OK\r\n" + \
                "CACHE-CONTROL: max-age=100\r\n" + \
                "EXT:\r\n" +\
                "LOCATION: http://" + str(self.ip) + ":80/description.xml\r\n" +\
                "SERVER: FreeRTOS/6.0.5, UPnP/1.0, IpBridge/0.1\r\n" +\
                "ST: uuid:0FDD7736-722C-4995-89F2-ABCDEF000000\r\n" +\
                "USN: uuid:0FDD7736-722C-4995-89F2-ABCDEF000000\r\n" +\
                "\r\n";
    def run(self):
        while True:
            self.sock.sendto(self.msg.encode(), ("239.255.255.250", 1901))
            time.sleep(2)
        
        
if __name__ == '__main__':
     th = UpnpServer()
     th.start()
     th.join()
