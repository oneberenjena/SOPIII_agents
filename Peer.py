import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

import json

TIMEOUT = 100000000

DirectoryAddress="13-10665+6@jabber.at"

def cleanSender(sender):
    return str(sender).split("/")[0]

class PeerAgent(Agent):
    class PeerBehav(CyclicBehaviour):
        async def run(self):
            print("Options:")
            print("1: Add new file")
            print("2: Ask for file")
            print("3: Search for files")
            option = input("select option: ")
            print()
            if option == "1":
                await self.addFileToDirectory()
            elif option == "2":
                await self.askFileFromDirectory()
            elif option == "3":
                await self.searchFilesInDirectory()
            else:
                print("############### Invalid Option ###############")
                print()


        async def addFileToDirectory(self):
            print("############### Add new file ###############")
            msg = Message(to=DirectoryAddress)
            msg.set_metadata("job", "newFile")
            title = input("title: ")
            msg.set_metadata("title", title)
            await self.send(msg)
            print()

        async def askFileFromDirectory(self):
            print("############### Ask file ###############")
            msg = Message(to=DirectoryAddress)
            msg.set_metadata("job", "askFile")
            title = input("title: ")
            msg.set_metadata("title", title)
            await self.send(msg)

            msg = await self.receive(timeout=TIMEOUT)
            if msg:
                print()
                print("Received list of peers")

                listOfPeers = json.loads(msg.get_metadata("list"))

                print("list:")
                for peer in listOfPeers:
                    print("+ {}".format(peer))
                await self.connectWithPeer(title)
                print("TODO: Get file from peer and inform directory")
            print()

        async def searchFilesInDirectory(self):
            print("############### Search file(s) by name ###############")
            msg = Message(to=DirectoryAddress)
            msg.set_metadata("job", "searchFiles")
            search = input("search by: ")
            msg.set_metadata("search", search)
            await self.send(msg)

            msg = await self.receive(timeout=TIMEOUT)
            if msg:
                print()
                print("Received list of files")

                listOfFiles = json.loads(msg.get_metadata("files"))

                print("Files matching your search:")
                for file in listOfFiles:
                    print(f"+ {file}")

                print()
                # self.askFileFromDirectory()

            print()



        async def connectWithPeer(self,myFile):
            print("############### Conecting with peer with the file ###############")
            name = input("Peer Name: ")
            msg = Message(to=name+"@jabber.at")
            msg.set_metadata("job", "connectFiles")
            msg.set_metadata("title", myFile)
            await self.send(msg)


            msg = await self.receive(timeout=TIMEOUT)
            if msg:
                print()
                print("Recived answer")
                fileAsked = msg.get_metadata("file")
                print("Files:")
                print(fileAsked)
            print()


    class PeerTransf(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=TIMEOUT)
            if msg:
                title = msg.get_metadata("title")
                sender = cleanSender(msg.sender)

                print("## REQUEST FOR GETTING A FILE")
                print("title of asked file: {}".format(title))
                print("from: {}".format(sender))

                sendFile="Send Files"

                msg = Message(to=sender)
                msg.set_metadata("job", "connectFiles")
                msg.set_metadata("title", title)
                msg.set_metadata("file", sendFile)
                await self.send(msg)
            print()




    def setup(self):
        print("PeerAgent started")
        peerBehav = self.PeerBehav()
        peerConnect =self.PeerTransf()

        listOfPeersTemp = Template()
        listOfPeersTemp.set_metadata("job", "listOfPeers")
        # self.add_behaviour(peerBehav, listOfPeersTemp)

        listOfFilesTemp = Template()
        listOfFilesTemp.set_metadata("job", "listOfFiles")

        connectPeerTemp = Template()
        connectPeerTemp.set_metadata("job", "connectFiles")

        self.add_behaviour(peerBehav, listOfPeersTemp | listOfFilesTemp |connectPeerTemp)
        self.add_behaviour(peerConnect, listOfPeersTemp | listOfFilesTemp |connectPeerTemp)


if __name__ == "__main__":
    n = int(input("agent: "))
    jid, pwd = "13-10665+"+str(n)+"@jabber.at", "operativos3"

    peerAgent = PeerAgent(jid, pwd)
    peerAgent.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            peerAgent.stop()
            break
    print("Agents finished")
