import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class ReceiverAgent(Agent):

    class InitBehav(OneShotBehaviour):
        def on_available(self, jid, stanza):
            print("[{}] Agent {} is available.".format(
                self.agent.name, jid.split("@")[0]))

        def on_subscribed(self, jid):
            print("[{}] Agent {} has accepted the subscription.".format(
                self.agent.name, jid.split("@")[0]))
            print("[{}] Contacts List: {}".format(
                self.agent.name, self.agent.presence.get_contacts()))

        def on_subscribe(self, jid):
            print("[{}] Agent {} asked for subscription. Let's aprove it.".format(
                self.agent.name, jid.split("@")[0]))
            self.presence.approve(jid)
            self.presence.subscribe(jid)

        async def run(self):
            print("init beha")
            self.presence.set_available()
            self.presence.on_subscribe = self.on_subscribe
            self.presence.on_subscribed = self.on_subscribed
            self.presence.on_available = self.on_available

    class RecvBehav(CyclicBehaviour):

        async def on_start(parameter_list):
            print("RecvBehav running")

        async def run(self):

            # wait for a message for 10 seconds
            msg = await self.receive(timeout=10)
            try:
                if msg:
                    if msg.body == "Archivo":
                        print("Message received with content: {}".format(msg.body))
                        print("From: {}".format(msg.sender))
                    elif msg.body == "Tipo":
                        print("Message received with content: {}".format(msg.body))
                        print("From: {}".format(msg.sender))
                    elif msg.body == "Cpu":
                        print("Message received with content: {}".format(msg.body))
                        print("From: {}".format(msg.sender))
                else:
                    sleep(2)
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
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            receiveragent.stop()
            break
    print("Agents finished")
