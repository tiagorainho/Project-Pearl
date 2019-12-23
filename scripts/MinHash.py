import sys, os
import random
import numpy as np
from scripts import Hash

class MinHash:
    def __init__(self, permutations = 100, threshHold = 0.4):
        self.size = 0
        self.largePrimeNumber = 10007
        self.defaultInsertValue = self.largePrimeNumber
        self.shinglesLength = 3
        self.threshHold = threshHold
        self.permutations = permutations
        self.A = Hash.getRandomValues(self.permutations, self.largePrimeNumber-1)
        self.B = Hash.getRandomValuesDifferentFromArray(self.A, self.largePrimeNumber-1)
        self.signatures = [[0]*self.permutations for i in range(1)]

    #def getCommand(self, text):
        

    def getSimilarity(self, id1, id2):
        return self.getSimilaritySignatures(self.signatures[id1], self.signatures[id2])

    def getSimilaritySignatures(self, sig1, sig2):
        count = 0
        for i in range(self.permutations):
            if sig1[i] == sig2[i]:
                count += 1
        return count/self.permutations

    def updateSignatures(self, content):
        prevSize = self.size
        auxSignatures = np.lib.pad(self.signatures, ((0, len(content)),(0, 0)), 'constant', constant_values=(self.defaultInsertValue))
        if prevSize == 0:
            auxSignatures = np.delete(auxSignatures, (0), axis=0)
        return auxSignatures

    def getShingles(self, content):
        shingles = []
        for i in range(len(content) - self.shinglesLength+1):
            shingles.append(content[i:i+self.shinglesLength])
        return shingles

    def getSignature(self, content):
        shingles = self.getShingles(content)
        signature = [self.defaultInsertValue]*self.permutations
        for i in range(self.permutations-1):
            minor = self.defaultInsertValue
            for shinglesAux in shingles:
                hashValue = Hash.hashFunction(shinglesAux)
                sig = (self.A[i] * hashValue + self.B[i]) % self.defaultInsertValue
                if sig < signature[i]:
                    signature[i] = sig
        return signature

    def add(self, content):
        prevSize = self.size
        self.signatures = self.updateSignatures(content)
        self.size += len(content)
        for i in range(len(content)):
            self.signatures[i+prevSize] = self.getSignature(content[i])

    def printSignatures(self):
        for row in self.signatures:
            print(row)

    
    