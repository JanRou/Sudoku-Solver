from basesudoku.basesudoku import BaseSudoku
from jigsaw.cell import JigsawCell

class JigsawSudoku(BaseSudoku):
    def __init__(self, d, shape, colours): 
        # d is dimension of sudoku, usually 4, 9, 16, 25 ...
        # shape is d=nxn row and columns with group indexes 0 based, n=sqrt(d), 
        # where 0 is first group at upper left corner and n is last
        self._shape = shape
        self._colours = colours
        self._groups = []  # the soudoku arranged by groups
        for rw in range( 0, d):
            self._groups.append([])        
        super().__init__(d, self.createCell)
        shapeCheck = self.CheckShape(shape) # returns tuple (bool, message)
        if not shapeCheck[0]:
            raise ValueError("Shape check failed: " + shapeCheck[1])
        self.state = 0

    # implements abstract method in base class
    def createCell(self, d, rw, col):
        cell = JigsawCell( d, rw, col, self._shape[rw][col], self._colours)
        self._groups[self._shape[rw][col]].append(cell)
        return cell

    def CheckShape(self, shape): # returns tuple (bool, message)
        # each group index from 0 to dimension-1 must appear dimension times in shape
        groupIndexes = {} # dictionary to hold group indexes and counts as values
        msg = ""
        for r in range( 0, self._dimension):
            for c in range( 0, self._dimension):
                if shape[r][c] in groupIndexes:
                    # found the group, so increment count of group
                    groupIndexes[shape[r][c]] += 1
                else:
                    # not found group index, so add group and set count to 1
                    groupIndexes[shape[r][c]] = 1
        result = True
        for group in range(self._dimension):
            result = result and group in groupIndexes
            if not result: # group index missing
                msg = "Group index " + str(group) + " is not found in shape"
                break
            result = result and groupIndexes[group] == self._dimension
            if not result: # group index count not equal to dimension
                msg = "Count of group " + str(group) + " indexes is not equal to dimension, " + str(self._dimension)
                break
        return (result, msg)
    
    def GetState( self):
        return self.state

    def GetGroup( self, r, c):
        return self._sudoku[r][c].Group

    def RemoveCandidatesInGroupForNumber( self, group, number):
        # remove candidates in group
        for cell in self._groups[group]:
            cell.Remove(number)

    def RemoveCandidatesHook( self, cell):
        self.RemoveCandidatesInGroupForNumber( cell.Group, cell.Number)

    def FindPossibleCandidates(self):
        self.FindPossibleCandidatesBase(self.RemoveCandidatesHook)

    def SetSinglesGroup(self):
        # for debug
        # self.Print()
        for group in range( 0, self._dimension):
            singleCandidates = []
            for cell in self._groups[group]:
                singleCandidates = cell.AppendSingleCandidates(singleCandidates)
            for candidate in singleCandidates:
                count = 0
                firstCell = None
                for cell in self._groups[group]:
                    count, firstCell = cell.CountAndSetFirstCellForSingleCandidate(candidate, count, firstCell)
                if count == 1:
                    # The candidate only appears in one cell for the group.
                    firstCell.Number = candidate

    def SetSingles(self):
        self.FindSinglesBase(self.SetSinglesGroup)
        
    def TakeStep(self):
        self.steps = { 0: 'Find single candidate as solution', 1: 'Find possible candidates'
                , 2: 'Find single candidate in row, column and group', 3: 'Update sudoku'
                , 4: "Done, solved"}
        if not self.Solved:
            result = self.steps[self.state]
            match self.state:
                case 0:
                    self.SetSingleCandidatesAsnewNumber()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = 3
                    else:
                        result = result + ", no"
                        self.state = 1
                case 1:
                    self.FindPossibleCandidates()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = 3
                    else:
                        result = result + ", no"
                        self.state = 2
                case 2:
                    self.SetSingles()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = 3
                    else:
                        result = result + ", no"
                    self.state = 3
                case 3:
                    self.DoChange()
                    self.state = 0
        else:
            result = self.steps[4]

        return result