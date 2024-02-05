import os
import socket
import sys
import threading
projet_name_admin = "\u001b[34mAll-in-One\u001b[0m - \u001b[32mServer\u001b[0m \u001b[37m#\u001b[0m\u001b[34mAdmin\u001b[0m"

if os.name == 'nt': # Only if we are running on Windows
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)


class AdminChatClient:
    def __init__(self, ip, port, credentials):
        self.ip = ip
        self.port = port
        self.credentials = credentials
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.MSize = 2048
        

    def connect_to_server(self):
        try:
            self.client.connect((self.ip, self.port))
            self.client.send(self.credentials.encode())  # Send the credentials as a single string
            self.client_thread()
            
            authentication_result = self.client.recv(self.MSize).decode(errors='ignore')
    
            if authentication_result == "Authentication successful!":
                self.get_host_name_ip()
                print(f"\n{projet_name_admin} [$] Chat started")
                self.client_thread()
            else:
                print(f"\n[!] Authentication failed. Exiting.")
                self.client.close()
                os.abort()
    
        except Exception as e:
            print(f"\n[!] Error connecting to the server: {e}")
            self.client.close()
            

    def get_host_name_ip(self):
        try:
            host_name = socket.gethostname()
            x = socket.gethostbyname(host_name)
            x = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            x.connect(('10.0.0.0', 0))
            host_ip = x.getsockname()[0]
            print("[*] Hostname:", host_name)
            print("[*] IP:", host_ip)
            print("[*] Connected!")

        except Exception as e:
            print(f"\n{projet_name_admin} [!] Unable to get Hostname and IP: {e}")
            

    def handle_sent_msg(self):
        while True:
            try:
                msg_send = input()
                
                if not msg_send:
                    break
                
                else:
                    self.client.send(msg_send.encode())

            except Exception as e:
                print(f"\n{projet_name_admin} [!] Error handling message from server: {e}")
                self.client.close()
                break
            

    def handle_rece_msg(self):
        while True:
            try:
                msg_rece = self.client.recv(self.MSize)
                if not msg_rece:
                    break
                elif msg_rece:
                    decoded_msg = msg_rece.decode(errors='ignore')
                    if decoded_msg.lower() == "exit":
                        self.client.close()
                        sys.exit()
                    else:
                        print(f"\n{decoded_msg}")
                else:
                    self.client.close()
                    break

            except Exception as e:
                print(f"\n{projet_name_admin} [!] Error handling message from server: {e}")
                self.client.close()
                break


    def client_thread(self):
        send = threading.Thread(target=self.handle_sent_msg)
        rece = threading.Thread(target=self.handle_rece_msg)
        send.start()
        rece.start()
        send.join()
        rece.join()
        

if __name__ == "__main__":
    ip = input("[>] Enter IP of server: ")
    port = int(input("[>] Enter port of server: "))
    username = input("[>] Enter username of server: ")
    password = input("[>] Enter password of server: ")

    credentials = f"{username},{password}"

    admin_client = AdminChatClient(ip, port, credentials)
    admin_client.connect_to_server()

