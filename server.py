# ============================================================================
# Johann Gawron (xgawro00@stud.fit.vutbr.cz)
# 08.03.2020
# Solution: IPK project 1, simple server-client HTTP resolver for domain names
# ============================================================================

import socket
import socketserver
import traceback
import sys

# request handler for server
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        # debug messages to server console
        #print("{}:{} wrote:".format(self.client_address[0], self.client_address[1]))
        #print(self.data.decode())
        #print("----------------------")

        # decoding data from binary
        request = self.data.decode()
        request = request.replace("\r", "")
        # splitting the data by lines
        splitReq = request.split("\n")

        header_f = True

        headers = []
        arrBody = []
        #buffer for responses
        buffer = []
        try:
            for row in splitReq:
                if row == "":
                    header_f = False
                elif header_f:
                    headers.append(row)
                else:
                    arrBody.append(row)

            status_OK = False

            version = headers[0].split(" ")[2].encode()
            #
            if "POST" in headers[0]:
                for tmp in arrBody:
                    if tmp.count(":") < 1:
                        continue
                    tmp2 = tmp.split(":")[1].replace(" ", "")
                    if tmp2 == "A":
                        name = tmp.split(":")[0].replace(" ", "")
                        hostaddr = socket.gethostbyname(name)
                        # skipping wrong inputs
                        if name == hostaddr:
                            continue
                        tmp = tmp.replace(" ", "")

                        status_OK = True

                        buffer.append(tmp + "={}\n".format(hostaddr))

                    elif tmp2 == "PTR":
                        ip = tmp.split(":")[0].replace(" ", "")
                        hostname = socket.gethostbyaddr(ip)
                        # skipping wrong inputs
                        check = ip.replace(".", "").isnumeric()
                        if not check:
                            continue

                        tmp = tmp.replace(" ", "")


                        status_OK = True

                        buffer.append(tmp + "={}\n".format(hostname[0]))

                    else:
                        print("INFO: client has given invalid request: " + tmp)

                if not status_OK:
                    self.request.sendall(version + " 400 Bad Request.\n".encode())
                else:
                    # if all went ok returns 200 OK and whole buffer
                    self.request.sendall(version + " 200 OK.%\r\n\r\n".encode())
                    for tmp in buffer:
                        self.request.sendall(tmp.encode())

            elif "GET" in headers[0]:

                #print(headers[0])
                tmp = headers[0]
                for i in range(1):
                    if "type=A" in tmp:
                        # distillation of important info
                        name = tmp.split("name=")[1]
                        tmp2 = name.split("&type=")
                        url = tmp2[0].strip("\ ,")
                        typ = tmp2[1].split(" ")

                        hostaddr = socket.gethostbyname(url)
                        # returning on wrong inputs
                        if url == hostaddr:
                            continue

                        payload = url + ":" + typ[0] + "=" + hostaddr + "\n"

                        status_OK = True

                        buffer.append(payload)


                    elif "type=PTR" in tmp:
                        # distillation of important info
                        name = tmp.split("name=")[1]
                        tmp2 = name.split("&type=")
                        ip = tmp2[0].strip("\/, ")
                        typ = tmp2[1].split(" ")
                        # returning on wrong inputs

                        check = ip.replace(".","").isnumeric()

                        if not check:
                            continue

                        hostname = socket.gethostbyaddr(ip)

                        payload = ip + ":" + typ[0] + "=" + hostname[0] + "\n"

                        status_OK = True

                        buffer.append(payload)

                    else:
                        self.request.sendall(version + " 400 Bad Request.\n".encode())
                if not status_OK:
                    self.request.sendall(version + " 400 Bad Request.\n".encode())
                else:
                    # if all went ok returns 200 OK and whole buffer
                    self.request.sendall(version + " 200 OK\r\n\r\n".encode())
                    for tmp in buffer:
                        self.request.sendall(tmp.encode())
            else:
                self.request.sendall(version + " 405 Method Not Allowed.\n".encode())

        except:
            self.request.sendall(version + " 500 Internal Server Error.\n".encode())
            traceback.print_exc()


if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", int(sys.argv[1])

        # create the server, binding to localhost on port 9999
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

        try:
            server.serve_forever()
        except:
            pass
    except:
        print("wrong parameters -> server.py PORT")
        pass