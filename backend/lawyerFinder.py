import csv

class LawyerFinder:
    searchTags = []
    lawyers = []

    def __init__(self, tags):
        self.searchTags = tags

    # Returns an array of all the lawyers and their information from our database (data/lawyers.csv).
    def GetLawyers(self):
        self.saveLawyersWithCorrectTags()
        return self.lawyers
    
    # Gets the name of an individual lawyer entry.
    def GetNameOfLawyer(self, lawyer):
        return lawyer[0]
    
    # Gets the lawyers company from their lawyer entry.
    def GetLawyerCompany(self, lawyer):
        return lawyer[2]
    
    # Gets the legal500 link to the lawyer entry.
    def GetLawyerLink(self, lawyer):
        return lawyer[3]

    # Gets all the tags associated with a lawyer.
    def getTagsInEntry(self, entry):
        return entry[2].split(',')

    # Saves lawyers which has the same tags as self.searchTags
    def saveLawyersWithCorrectTags(self):
        with open('data/lawyers.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                tagsInEntry = self.getTagsInEntry(line)
                if self.isTagOverlap(tagsInEntry):
                    self.lawyers = self.lawyers + [line]

    # Checks if the necessary tags are found in a specific lawyer.
    def isTagOverlap(self, tagsInEntry):
        if self.searchTags in tagsInEntry:
            return True
        return False

# Example use case
#finder = LawyerFinder('Capital Markets')
#finder.GetLawyers()
#print(finder.GetNameOfLawyer(finder.lawyers[1]))