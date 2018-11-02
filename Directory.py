import time
import re
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

import json

TIMEOUT = 100000000

_filesExtension = {
    'image': ['png', 'jpg', 'jpeg', 'tiff', 'tif', 'gif', 'svg'],
    'text': ['txt', 'docx', 'doc', '1st', 'latex', 'md5.txt', 'odt', 'tex'],
    'sound': ['mp3', 'flac', 'm4a', 'm4p', 'm4r', 'mid', 'midi', 'vlc', 'wav', 'wave', 'wma'],
    'video': ['mpg', 'mov', 'wmv', 'rm', '3gp', 'avi', 'hdv', 'mp4', 'mpeg4'],
    'pdf': ['pdf']
}


def cleanSender(sender):
    return str(sender).split("/")[0]


class DirectoryAgent(Agent):
    direc = dict()

    class NewFileBehav(CyclicBehaviour):
        def setDirec(self, Dir):
            self.direc = Dir

        async def run(self):
            msg = await self.receive(timeout=TIMEOUT)
            if msg:
                title = msg.get_metadata("title")
                body = msg.body
                sender = cleanSender(msg.sender)
                print("## REQUEST TO ADD NEW FILE")
                print("title of new file: {}".format(title))
                print("from: {}".format(sender))
                print()

                if(title in self.direc):
                    self.direc[title].append(sender)
                    print("File already exists!")
                    print("Peer added to the list of peers")
                else:
                    self.direc[title] = [sender]
                    print("File added to directory!")

    class AskFileBehav(CyclicBehaviour):
        def setDirec(self, Dir):
            self.direc = Dir

        async def run(self):
            msg = await self.receive(timeout=TIMEOUT)
            if msg:
                title = msg.get_metadata("title")
                sender = cleanSender(msg.sender)

                print("## REQUEST FOR GETTING A FILE")
                print("title of asked file: {}".format(title))
                print("from: {}".format(sender))

                if title in self.direc:
                    listOfPeers = self.direc[title]
                else:
                    listOfPeers = []
                stringList = json.dumps(listOfPeers)

                msg = Message(to=sender)
                msg.set_metadata("job", "listOfPeers")
                msg.set_metadata("title", title)
                msg.set_metadata("list", stringList)
                await self.send(msg)
            print()

    class SearchFilesBehav(CyclicBehaviour):
        def setDirec(self, Dir):
            self.direc = Dir

        def findFilesByNamePart(self, fileNamePart):
            existingFiles = self.direc.keys()
            return [file for file in existingFiles if fileNamePart.lower() in file.lower()]

        async def run(self):
            msg = await self.receive(timeout=TIMEOUT)
            if msg:
                search = msg.get_metadata("search")
                sender = cleanSender(msg.sender)

                print("## REQUEST FOR SEARCHING FOR FILES")
                print(f"Searching files by {search}")
                print(f"from {sender}")

                listOfFiles = self.findFilesByNamePart(search)
                stringList = json.dumps(listOfFiles)

                msg = Message(to=sender)
                msg.set_metadata("job", "listOfFiles")
                msg.set_metadata("search", search)
                msg.set_metadata("files", stringList)
                print(f"Sending {msg}")
                await self.send(msg)
            print()

    def setup(self):
        print("Directory started")
        newFBehav = self.NewFileBehav()
        newFBehav.setDirec(self.direc)
        newFTemp = Template()
        newFTemp.set_metadata("job", "newFile")
        self.add_behaviour(newFBehav, newFTemp)

        askFBehav = self.AskFileBehav()
        askFBehav.setDirec(self.direc)
        askFTemp = Template()
        askFTemp.set_metadata("job", "askFile")
        self.add_behaviour(askFBehav, askFTemp)

        searchFBehav = self.SearchFilesBehav()
        searchFBehav.setDirec(self.direc)
        searchFTemp = Template()
        searchFTemp.set_metadata("job", "searchFiles")
        self.add_behaviour(searchFBehav, searchFTemp)


if __name__ == "__main__":
    directory = DirectoryAgent("13-10665+6@jabber.at", "operativos3")
    directory.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            directory.stop()
            break
    print("Agents finished")
