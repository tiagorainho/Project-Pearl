from scripts import MinHash
import json

class voiceAnalyser:
    def __init__(self, commandsFile):
        self.minHash = MinHash.MinHash(100)
        with open(commandsFile) as f:
            self.commands = json.load(f)["commands"]
        
        if len(self.commands) == 0 or self.commands == None:
            print("No commands in use")
        self.initiateMinHash()

    def initiateMinHash(self):
        lst = []
        for command in self.commands:
            lst.append(command["command"].lower())
            for variant in command["equivalent"]:
                lst.append(variant.lower())
        self.minHash.add(lst)

    def getMostSimilar(self, content):
        if len(content) == 0:
            return ""
        bigger = 0
        signature = self.minHash.getSignature(content.lower())
        prediction = ""
        for i in range(self.minHash.size):
            counter = 0
            for command in self.commands:
                auxSimilarity = self.minHash.getSimilaritySignatures(signature, self.minHash.signatures[counter])
                if auxSimilarity > bigger:
                    bigger = auxSimilarity
                    prediction = command["command"]
                counter += 1
                for variant in command["equivalent"]:
                    if auxSimilarity > bigger:
                        bigger = auxSimilarity
                        prediction = command["command"]
                    counter += 1
        return prediction