import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from spade.behaviour import FSMBehaviour, State
import getpass
STATE_ONE = "STATE_ONE"


class SenderAgent(Agent):



 
    class Behav2(CyclicBehaviour):
        async def on_start(parameter_list):
            print("SenderAgent started")
        
        def internMenu(self):
            print(' Menu de Descargas:')
            print(' 1- Para descargar un archivo ')
            print(' 2- Para descargar algun archivo de tipo especifico ')
            print(' 3- Para hacer requerimiento de CPU')
            print(' 0- Para salir')
            return input(' Ingrese una de las opciones para continuar: ')
 
        async def run(self):
            option = int(self.internMenu())
            msg = Message(to="13-10665@jabber.at")     # Instcdantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            # msg.body = "Hello World"                    # Set the message content
            if option==1:
                msg.body = "Archivo"
                await self.send(msg)
            elif option==2:
                msg.body = "Tipo"
                await self.send(msg)
            elif option==3:
                msg.body = "Cpu"
                await self.send(msg)
            elif option==0:
                self.kill()
            else:
                print("Opcion no disponible, intenta nuevamente")
            # stop agent from behaviour
            # self.agent.stop()

 
    def setup(self):
        c=self.Behav2()
        self.add_behaviour(c)


def menuInit():
    print("\nHola! Bienvenido")
    print("Si ya tienes credenciales en un servidor XMPP , por favor utilizalas para ingresar:")
    #jid = input("Agente JID> ")
    #passwd1 = getpass.getpass()
    #return (jid,passwd1)



if __name__ == "__main__":

    #jid,pwd= menuInit()
    n = int(input("agent:"))
    if n==1:
        jid, pwd = "avero@jabber.at", "020994dejesus"
    else:
        jid, pwd = "amandi@jabber.at", "020994dejesus"
    # senderagent = SenderAgent("avero@jwchat.org", "020994")

    senderagent = SenderAgent(jid, pwd)
    senderagent.start()

    while senderagent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            break
    print("Agents finished")
