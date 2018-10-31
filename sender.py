import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from spade.behaviour import FSMBehaviour, State

STATE_ONE = "STATE_ONE"


class SenderAgent(Agent):

 
    class Behav2(CyclicBehaviour):
        async def run(self):
            

            print("InformBehav running")
            msg = Message(to="13-10665@jabber.at")     # Instcdantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            # msg.body = "Hello World"                    # Set the message content

            msg.body = input("send: ")

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            # self.agent.stop()


    def setup(self):
        print("SenderAgent started")
        c=self.Behav2()
        self.add_behaviour(c)

       


if __name__ == "__main__":
    n = int(input("agent:"))
    if n==1:
        jid, pwd = "avero@jabber.at", "020994dejesus"
    else:
        jid, pwd = "amandi@jabber.at", "020994dejesus"
    # senderagent = SenderAgent("avero@jwchat.org", "020994")

    senderagent = SenderAgent(jid, pwd)
    senderagent.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            break
    print("Agents finished")