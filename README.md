# projet_tp_security
ona fait une outille pour controle une machine client
ona 2 fichier:
server.py et client.py
ona utilse les socket pour faire la connection entre le administrateur et le client
ona utiliser le python 3
comment fonction les 2 programme:
1)- server.py:
ona cree une class qui s'appelle Server()
donc on  cree une instance de cette class :
local_ip = ip
port_de_communication = port
server = Server(ip,port_de_communication)
server.start()

2)- client.py:
ona cree class qui s'appelle Backdoor_final()
donc on  cree une instance de cette class :
ip_de_serveur = ip
port_de_communication = port
backdoor = Backdoor_final(ip_de_server,port_de_communication)
backdoor.run()



