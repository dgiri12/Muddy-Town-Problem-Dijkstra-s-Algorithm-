class DField:
    def __init__(self, house, shortest, prevHouse):
        self.house = house
        self.shortest = shortest
        self.prevHouse = prevHouse

    def printValues(self):
        # if encountered null value, print info
        if self.house == "Z" or  self.prevHouse == "Z":
            print(str(self.house) + "\t" + str(self.shortest) + "\t" +
                    str(self.prevHouse)+ "\t 'Z' means Null")
        else:
            print(str(self.house) + "\t" + str(self.shortest) + "\t" +
                    str(self.prevHouse))

#1 iterates a list and generates a list of unique houses that were in that list
def getHouseList(_stringList):
    houseList = []
    for i in _stringList:
        line = i.split(",")
        try:
            if line[1] not in houseList:
                if line[1] != "Z": houseList.append(line[1]) # 'Z' means null
            if line[2] not in houseList:
                if line[2] != "Z": houseList.append(line[2])
        except IndexError: # this means this line is just name of town
            continue
    return houseList

# initialize the dTable
def dTableInit(_houseList):
    dTable = []
    for i in _houseList:
        temp = DField(i,-1,"Z") 
        # '-1' means infinity and 'Z' means null-string
        dTable.append(temp)
    return dTable

# finds the vertex with the shortest distance in the dTable, but also not present in _visitedList
# it will return '-1' if everything in the list has been visited
def findVertexShortestDistance(_dTable, _visitedList):
    minimum = -1
    foundIndex = -1
    for idx, i in enumerate(_dTable):
        if i.house in _visitedList: # skip if already visited
            continue
        if minimum == -1:
            minimum = i.shortest
            foundIndex = idx
            continue
        if i.shortest == -1: # inf cannot be min, so goto next
            continue
        if i.shortest < minimum:
            minimum = i.shortest
            foundIndex = idx
    return foundIndex # this is the index of vertex in dTable with shortest distance

def findInTable(_dTable, _houseToFind): # finds the given housename (string) in the dTable and 
    # returns its index or '-1' if not found
    found = False
    for index, i in enumerate(_dTable):
        if i.house == _houseToFind:
            found = True
            return index
    if found == False: return -1

def removeTownName(_stringList):
    newList = []
    firstLine = True
    for i in _stringList:
        if firstLine == True:
            firstLine = False
            continue
        newList.append(i)
    return newList

def townProcessor(stringList):
    print("Processing town and generating dTable")
    stringList = removeTownName(stringList)
    houseList = getHouseList(stringList) # initialize a houselist into that variable
    dTable = dTableInit(houseList) # initialize a dTable into that variable

    visitedList = [] # list of houses that have been visited

    # set the distance from start vertex to start vertex as 0
    dTable[0].shortest = 0
    # the shortest distance of all other vertices have already been
    # set to inf == -1
    

    while True:
        currentVertexIndex = findVertexShortestDistance(dTable,visitedList)
        # ^ also checks visitedList, if all visited then returns '-1'
        currentVertex = dTable[currentVertexIndex].house
        currentVertexShortest = dTable[currentVertexIndex].shortest

        # terminate loop if visitedList is full
        if currentVertexIndex == -1: break

        neighboursPosition = [] # line position in the stringList
        neighbours = [] # list of the actual neighbours (strings)
        neighboursDistanceValue = [] # corresponding list of the neighbour's distance values

        # find the unvisited neighbours of this vertex and store in list
        for index, i in enumerate(stringList):
            line = i.split(",")
            if line[1] == currentVertex:
                if line[2] in visitedList: continue
                neighbours.append(line[2])
                neighboursPosition.append(index)
                neighboursDistanceValue.append(int(line[0]))
            # now for the reverse order, find neighbours
            if line[2] == currentVertex:
                if line[1] in visitedList: continue
                neighbours.append(line[1])
                neighboursPosition.append(index)
                neighboursDistanceValue.append(int(line[0]))
            # as long as connections in stringList are not repeated as
            # in "6,A,B" and "6,B,A", there will be no duplicate
            # neighbours

        # if the calculatedDistance is shorter than the neighbour's distance, update values
        # in dTable for those neighbours
        for index, i in enumerate(neighbours):
            calculatedDistance = currentVertexShortest + neighboursDistanceValue[index]
            # -1 means infinity, so just put that as the new distance value and skip loop
            if dTable[findInTable(dTable,i)].shortest == -1:
                dTable[findInTable(dTable,i)].shortest = calculatedDistance
                # also update the prevHouse value for the neighbours entries in the dTable
                dTable[findInTable(dTable,i)].prevHouse = currentVertex
                continue
            if calculatedDistance < dTable[findInTable(dTable,i)].shortest:
                dTable[findInTable(dTable,i)].shortest = calculatedDistance
                # also update the prevHouse value for the neighbours entries in the dTable
                dTable[findInTable(dTable,i)].prevHouse = currentVertex
                continue

        # now add the current vertex to the list of visited vertices
        visitedList.append(currentVertex)

    return dTable 

def townProcessor_test():
    string1 = [
            "Willow",
            "6,A,B",
            "1,A,D",
            "2,D,B",
            "1,D,E",
            "2,E,B",
            "5,E,C",
            "5,C,B"]

    dTable = townProcessor(string1)

    correctDtable = []
    f1 = DField("A", 0, "Z")
    f2 = DField("B", 3, "D")
    f3 = DField("D", 1, "A")
    f4 = DField("E", 2, "D")
    f5 = DField("C", 7, "E")
    correctDtable.append(f1)
    correctDtable.append(f2)
    correctDtable.append(f3)
    correctDtable.append(f4)
    correctDtable.append(f5)

    testPassed = True

    # check values between correct dTable and created dTable
    if len(dTable) != len(correctDtable): testPassed = False
    for index, i in enumerate(dTable):
        if i.house != correctDtable[index].house:
            testPassed = False
        if i.shortest != correctDtable[index].shortest:
            testPassed = False
        if i.prevHouse != correctDtable[index].prevHouse:
            testPassed = False
    return testPassed

def printDTable(dTable):
    print("House\tShortest Distance From Start Point\tParent")
    for i in dTable:
        i.printValues()


