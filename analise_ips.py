#===========================================IMPORT============================================#
import os
os.system('cls')
import tools # minha biblioteca
from tools import println
from time import sleep
import requests

#======================================CORPO-DO-CODIGO=======================================#
antenas_lista = list()
tools.antenas(antenas_lista)#exporta para lista {list_ips} ips no arquivo logfile
mudanca = False
internet_ant = ''
tempo_reboot = 25 # tempoi setado para verificar se antena vai reiniciar
while True:
    for ip in antenas_lista:   
#-------------------------------------STATUS_DISPOSITIVOS--------------------------------------#    
        ip['estado_atual'] = tools.rqst(ip['ip'],ip['porta']) # retorna true ou false
        
        #print(ip['estado_atual'])
        if ip['estado_atual'] != ip['estado_anterior']: #identifica mudança de estado "mudanca == False" 
        #modulo para identificar se dispositivo foi desligado ou reiniciado#
            if ip['estado_atual'] == False and ip['desligada'] == False:
                ip['desligada'] = True
                while True:
                    println(antenas_lista[0],antenas_lista[1])
                    timer = tools.timeout(ip['timeout'])   
                    ip['timeout'] = timer
                    if timer >= tempo_reboot:
                        estado = tools.rqst(ip['ip'],ip['porta'])#VIRIFICA SE ANTENA MUDOU STATUS
                        if estado == True:
                            tools.logadd('dispositivo',ip['ip'],'reboot',mudanca)#adiciona log de status da antena  
                            tools.envia_msg(ip['ip'],'reboot')#envia msg telegram se reiniciar
                        else:
                            tools.logadd('dispositivo',ip['ip'],ip['estado_atual'],mudanca)#adiciona log de status da antena  
                            tools.envia_msg(ip['ip'],ip['estado_atual'])#envia msg telegram se desligar
                            ip['timeout'] = 0
                        break
        #modulo para identificar se dispositivo foi ligado da primeira vez ou somente kigado
            elif ip['estado_atual'] == True :  
                if ip['timeout'] == 0 and mudanca == True: 
                    tools.logadd('dispositivo',ip['ip'],ip['estado_atual'],mudanca)#adiciona log de status ligada 
                    tools.envia_msg(ip['ip'],ip['estado_atual'])#envia msg telegram se ligar
                if mudanca == False:
                    tools.logadd('dispositivo',ip['ip'],ip['estado_atual'],mudanca)#adiciona log de status ligada  pela primeira vez
                ip['timeout'] = 0
                ip['desligada'] = False
        ip['estado_anterior'] = ip['estado_atual'] # iguala as variaveis de controle
#--------------------------------checa_comunicaçao_servidor--------------------------------------#
    internet = tools.rqst2('www.google.com')
    if internet != internet_ant and mudanca == True:
        if internet == False:
            tools.logserver('servidor','sem internet',mudanca)  
        else:
            tools.logserver('servidor','internet restabelecida',mudanca)  
    println(antenas_lista[0],antenas_lista[1],internet)
    internet_ant = internet
    mudanca = True


'''
mecher no modulo checa_comunicaçao_servidor e identificar:

sem internet, informa no log.

sem comunicaçao com antenas, unico que reportara por telegram.

sem comunicaçao com roteador, informa no log.
==============================================================
modulo de conexao :
o codigo nao conegue identificar se mais de um equipamento reiniciou  de uma só vez
ele nao notifica no telegram qu o servidor ficou  internet



'''
