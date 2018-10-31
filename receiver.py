import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

class ReceiverAgent(Agent):

    class RecvBehav(CyclicBehaviour):
        async def on_start(parameter_list):
            print("RecvBehav running")

        
        async def run(self):
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            try:
                if msg:
                    if msg.body=="Archivo":
                        print("Message received with content: {}".format(msg.body))
                        print("From: {}".format(msg.sender))
                    elif msg.body=="Tipo":
                        print("Message received with content: {}".format(msg.body))
                        print("From: {}".format(msg.sender))
                    elif msg.body=="Cpu":
                        print("Message received with content: {}".format(msg.body))
                        print("From: {}".format(msg.sender))
                    else:
                        print("It's not a option")
                else:
                    pass
            except:
                pass
            # stop agent from behaviour
            # self.agent.stop()

    def setup(self):
        print("Directory started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)


if __name__ == "__main__":
    receiveragent = ReceiverAgent("13-10665@jabber.at", "operativos3")
    receiveragent.start()
    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break
    print("Agents finished")
