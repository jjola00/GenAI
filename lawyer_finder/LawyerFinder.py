import csv

class LawyerFinder:
    searchTags = []
    lawyers = []

    def __init__(self, tags):
        self.searchTags = tags

    def GetLawyer(self):
        self.readAllLawyers()

    def getTagsInEntry(self, entry):
        return entry[2].split(',')

    def readAllLawyers(self):
        with open('data/lawyers.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                tagsInEntry = self.getTagsInEntry(line)
                if self.IsTagOverlap(tagsInEntry):
                    self.lawyers = self.lawyers + [line]

    def IsTagOverlap(self, tagsInEntry):
        if self.searchTags in tagsInEntry:
            return True
        return False

finder = LawyerFinder('Capital Markets')
finder.GetLawyer()