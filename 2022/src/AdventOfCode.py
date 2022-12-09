import os
from abc import ABC, abstractmethod

class AdventOfCode:
        _dataLocation = '../data/'
        _inputFileName = 'input'
        def __init__(self,exercise):
            self.exercise = exercise
            self.testData,self.data = self._loadData(exercise)

        def _loadData(self, exercise):
            data = [line for line in open(self._dataLocation + self.inputFileName(exercise)+'.txt','r').readlines()]
            testData = []
            for testFile in self._getTestFiles(exercise):
                testData.append([line for line in open(self._dataLocation+testFile,'r').readlines()])
            return testData,data

        def _getTestFiles(self,exercise):
            files = os.listdir(self._dataLocation)
            return filter(lambda fileName: str(fileName).startswith(self.inputFileName(exercise)+'test'),files)

        def inputFileName(self,exercise):
            exerciseString = ('0' if exercise < 10 else '') + str(exercise)
            return self._inputFileName + exerciseString

        def execute(self,part1,part2):
            print(f'\nRunning exercise {self.exercise}')
            print(f'solution part 1: {part1(self.data)}')
            print(f'solution part 2: {part2(self.data)}\n')

        def executeTest(self,part):
            print(f'\nTesting exercise {self.exercise}')
            for n in range(len(self.testData)):
                print(f'test {n+1}: {part(self.testData[n])}')

        def executeTest(self, part, res):
            print(f'\nTesting exercise {self.exercise}')
            testres = part(self.testData[0])
            if(res != testres):
                raise Exception(f"Test failed: expected: {res} found: {testres}")
            else:
                print(f'Testresult: {testres}')
