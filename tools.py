# modulo para enviar mensagem via telegram
def envia_msg(ip,estado_atual): 
    '''
    envia_msg(ip,estado_atual)
    estado_atual: true,false,reboot
    '''
    #////////////////////controle/////////////////////////////
    if estado_atual == False:
        mensagem = f'o dispositivo {ip} foi desligado'
    elif estado_atual == True:
        mensagem = f'o dispositivo {ip} foi ligado'
    elif estado_atual == 'reboot':
        mensagem = f'o dispositivo {ip} foi reiniciado'
    #/////////////////////////////////////////////////////////
    import telebot
    try:       
        bot = telebot.TeleBot("5851288143:AAFZQUrc_tf9Dk6S-ZKDEKMVwnnMfGvP68Y")#token_bot
        chat_id = 5027001523 #chat do usuario
        bot.send_message(chat_id, mensagem) # envio msg
    except:
        print('erro')
#-----------------------------------------------------------------------------------------------------#
# mover lista de ips 
def antenas(iten):
    '''
   
    '''
    adicionar_inf = dict()
    entrada_ip = ''
    porta = ''
    inf = list()
    lista = open('antenas.txt', 'r') #abre txt em modo leitura
    ips = lista.readlines()#ler linhas do texto
    for ip in ips:
        ip = ip.rstrip('\n').replace(" ", "") #exclui simbolo "\n"
        if ip not in '' and ip[0] not in '#':# ignora linha em branco

            for x in ip:# separa ip da porta 
                if x != ':':
                    entrada_ip = entrada_ip + x 
                else:
                    break
            porta = ip
            porta = porta.replace(entrada_ip,'').replace(':','').replace(' ','')
            adicionar_inf['ip'] = entrada_ip
            adicionar_inf['porta'] = porta
            adicionar_inf['estado_anterior'] = ''    
            adicionar_inf['estado_atual'] = ''
            adicionar_inf['timeout'] = 0  
            adicionar_inf['desligada'] = False
            iten.append(adicionar_inf.copy())
            entrada_ip = porta = ''
    lista.close()
#-----------------------------------------------------------------------------------------------------#
#verificaçao de dispositivos da rede 
def rqst(ip,port):
    if port == '': 
        port = 80
    '''
    rqst(ip)
    ip -> identaçao de dispositivo (geralmete ip)
    que deseja receber um retorno de true ou false 
    para o estado de comunicaçao do dispositivo
    '''
    #from time import sleep
    import socket
    from time import sleep
    exito = 0
    for x in range(2):

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3) # definir um timeout de 10 segundos
            port = int(port)
            sock.connect((ip,port))
            exito = exito + 1
            sock.close()
          
            sleep(0.5)
        except socket.error as e:
            exito = exito - 1
         
    #print(exito)
    if exito >0:
        return True
    else:
        return False
        
#-----------------------------------------------------------------------------------------------------#
# adicionar log
def logadd(dispositivo,ip,status_antena,mudanca):
    '''
    logadd(dispositivo,ip,status_antena,mudanca)

    status_antena: (true,false,reboot)
    '''
    from datetime import datetime
    from datetime import time
    data = datetime.now()
    agora = data.strftime("%A/%d/%B/%y %I:%M:%S")

    add = open("logfile.txt", "a") 
    if status_antena == False:
        status = "dispositivo desligado"
    elif status_antena == True:
        status = "dispositivo ligado"
    elif status_antena == 'reboot':
        status = 'dispositivo reiniciado'

    if mudanca is True:
        add.write(f"\n{dispositivo}: {ip} estado: {status} as {agora}") 
    else:
        add.write(f"\n{dispositivo}: {ip} estado: {status}") 
        
    
    add.close()
#-----------------------------------------------------------------------------------------------------#
def logserver(dispositivo,status,mudanca):
    from datetime import datetime
    from datetime import time
    data = datetime.now()
    agora = data.strftime("%A/%d/%B/%y %I:%M:%S")

    add = open("logfile.txt", "a")
    if mudanca is True:
        add.write(f"\n{dispositivo}: estado: {status} as {agora}") 
    else:
        add.write(f"\n{dispositivo}: estado: {status}")
    add.close()
#-----------------------------------------------------------------------------------------------------#
#TIMEOUT ANTENAS
def timeout(segundos): 
    from datetime import datetime
    add = open("timeout.txt", "a")
    timeoff_inicial = datetime.now().strftime("%S")
    while True:
        timeoff_atual = datetime.now().strftime("%S")
        if timeoff_atual != timeoff_inicial:
            segundos = segundos + 1
            return segundos
            #add.write(f"\ndispositivo:{ip} timeout: {seg}")
            break

#-----------------------------------------------------------------------------------------------------#
def println(*iten):
    import os
    '''esta função mostra mais de um iten, bsta colocar todos o itens
        exemplo:
            v1 = 1
            v2 = 2
                println(v1,v2)
                1
                2  
                    '''
    os.system('cls')
    for x in iten:
        print(x)
#-----------------------------------------------------------------------------------------------------#
    
def rqst2(ip):
    '''
    rqst(ip)
    ip -> identaçao de dispositivo (geralmete ip)
    que deseja receber um retorno de true ou false 
    para o estado de comunicaçao do dispositivo
    '''
    #from time import sleep
    from urllib.request import urlopen
    from time import sleep
    exito = 0
    for x in range(3):
        
        try:
            response = urlopen("http://" + ip, timeout=3)
            exito = exito + 1
            sleep(0.5)
        except:
            exito = exito - 1
         
    #print(exito)
    if exito >=0:
        return True
    else:
        return False
#-----------------------------------------------------------------------------------------------------#
