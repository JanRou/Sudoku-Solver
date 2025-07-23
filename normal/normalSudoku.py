from basesudoku.basesudoku import BaseSudoku
from basesudoku.basecell import BaseCell
import math

class NormalSudoku(BaseSudoku):
    def __init__(self, dimension):
        self.state = 0
        super().__init__(dimension, self.createCell, 'Normal')
        self.start=0
        self.findPossibleCandidates = 1
        self.findSingles = 2
        self.findNakedPairsRow = 3
        self.findNakedPairsColumn = 4
        self.findNakedPairsGroup = 5
        self.updateSudoku = 99
        self.done = 100
        self.ConstraintChecked = False
        self.steps = {  self.start:                  'Set single candidate as solution in cells'
                      , self.findPossibleCandidates: 'Find possible candidates'
                      , self.findSingles:            'Find single candidate in row, column and group'
                      , self.findNakedPairsRow:      'Find naked pairs row wise'
                      , self.findNakedPairsColumn:   'Find naked pairs column wise'
                      , self.findNakedPairsGroup:    'Find naked pairs 3x3 square wise'
                      , self.updateSudoku:           'Update sudoku'
                      , self.done:                   'Done, solved'}

    def createCell(self, dim, rw, cl):
        rho = round(math.sqrt(self.dimension))
        group = (rw//rho)*rho + (cl//rho) # upper left square is indexed 0, next to the right 1, and so forth.
        cell = BaseCell( dim, rw, cl, group)
        return cell    
       
    def GetState(self):
        return self.state
    
    def RemoveCandidatesHook( self, cell):
        # Common with JigSaw
        self.RemoveCandidatesInGroupForNumber( cell.Group, cell.Number)

    def FindPossibleCandidates(self):
        # Common with JigSaw
        self.FindPossibleCandidatesBase(self.RemoveCandidatesHook)

    def SetSingles(self):
        self.FindSinglesBase(self.FindSinglesGroup) # uses standard base hook

    def CellInCellsWithPairs( self, row, column, cellsWithPairs):
        # helper function ? Could one use the marks?
        result = False
        for cell in cellsWithPairs:
            result = cell.Row == row and cell.Column == column
            if result:
                break
        return result

    def GetPairsOfCandidateNumbers(self, cellsWithPairs):
        # helper function
        result = []
        for i in range(len(cellsWithPairs)-1):
            for j in range(i+1,len(cellsWithPairs)):
                pair = set(cellsWithPairs[i].Candidates) | set(cellsWithPairs[j].Candidates) # | means union of two pairs
                if len(pair) == 2:
                    # Found a pair of numbers
                    result.append(pair)
                    # Set marks for the pairs for the view
                    cellsWithPairs[i].Mark()
                    cellsWithPairs[j].Mark()
                    break; # there have to be only one naked pair in cellsWithPair (do check it or don't?)
        return result
    
    def RemoveCandiatesForPairsFound(self, cellsWithPairs, pairsOfCandidateNumbers, cell):
        if not (self.CellInCellsWithPairs( cell.Row, cell.Column, cellsWithPairs) or cell.Solved):
            for candiatePairToRemove in pairsOfCandidateNumbers:
                for candiateToRemove in candiatePairToRemove:
                    cell.Remove(candiateToRemove)
    
    def FindNakedPairsRow(self):        
        for row in range(self.dimension):
            # Get all candidate pairs per row
            cellsWithPairs = []
            for column in range(self.dimension):
                if (not self.sudoku[row][column].Solved) and len(self.sudoku[row][column].Candidates) == 2:
                    cellsWithPairs.append(self.sudoku[row][column])
            # TODO FindNakedPairs... skal ikke opdatere sudoku. Det skal UpdateChange. Markørerne for 
            # TODO par fjerner UpdateChange, når den har fjernet kandidater fra øvrige celler.
            # Find pairs of numbers from two cells with the same pair of candidates
            pairsOfCandidateNumbers = self.GetPairsOfCandidateNumbers(cellsWithPairs)
            # remove candidates from all other cells of the row that are in pairsOfCandidateNumbers
            for column in range(self.dimension):
                self.RemoveCandiatesForPairsFound( cellsWithPairs, pairsOfCandidateNumbers, self.sudoku[row][column])

    def FindNakedPairsColumn(self):
        for column in range(self.dimension):
            # Get all candidate pairs per column
            cellsWithPairs = []
            for row in range(self.dimension):
                if (not self.sudoku[row][column].Solved) and len(self.sudoku[row][column].Candidates) == 2:
                    cellsWithPairs.append(self.sudoku[row][column])
            # TODO FindNakedPairs... skal ikke opdatere sudoku. Det skal UpdateChange. Markørerne for 
            # TODO par fjerner UpdateChange, når den har fjernet kandidater fra øvrige celler.
            # Find pairs of numbers from two cells with the same pair of candidates
            pairsOfCandidateNumbers = self.GetPairsOfCandidateNumbers(cellsWithPairs)
            # remove candidates from all other cells of the column that are in pairsOfCandidateNumbers
            for row in range(self.dimension):
                self.RemoveCandiatesForPairsFound( cellsWithPairs, pairsOfCandidateNumbers, self.sudoku[row][column])

    def FindNakedPairsGroup(self):
        for group in range(self.dimension):
            # Get all candidate pairs per group
            cellsWithPairs = []
            for cell in self.groups[group]:
                if (not cell.Solved) and len(cell.Candidates) == 2:
                    cellsWithPairs.append(cell)
            # TODO FindNakedPairs... skal ikke opdatere sudoku. Det skal UpdateChange. Markørerne for 
            # TODO par fjerner UpdateChange, når den har fjernet kandidater fra øvrige celler.
            # Find pairs of numbers from two cells with the same pair of candidates
            pairsOfCandidateNumbers = self.GetPairsOfCandidateNumbers(cellsWithPairs)
            # remove candidates from all other cells of the row that are in pairs
            for cell in self.groups[group]:
                self.RemoveCandiatesForPairsFound( cellsWithPairs, pairsOfCandidateNumbers, cell)

    # def FindNakedPairs(self):
    #     self.FindNakedPairsRow()
    #     self.FindNakedPairsColumn()
    #     self.FindNakedPairsGroup()

    def TakeStep(self):
        # TODO add more rules and more states
        # TODO refactor to state table
        if not self.ConstraintChecked:
            self.ConstraintChecked = self.Check()
            if not self.ConstraintChecked:
                result = 'Sudoku is bad. It has two or more cells with same number'                
        if not self.Solved and self.ConstraintChecked:
            result = self.steps[self.state]
            match self.state:
                case self.start:
                    self.SetSingleCandidatesAsnewNumber()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = self.updateSudoku
                    else:
                        result = result + ", no"
                        self.state = self.findPossibleCandidates
                case self.findPossibleCandidates:
                    self.FindPossibleCandidates()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = self.updateSudoku
                    else:
                        result = result + ", no"
                        self.state = self.findSingles
                case self.findSingles:
                    self.SetSingles()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = self.updateSudoku
                    else:
                        result = result + ", no"
                        self.state = self.findNakedPairsRow
                case self.findNakedPairsRow:
                    self.FindNakedPairsRow()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = self.updateSudoku
                    else:
                        result = result + ", no"
                        self.state = self.findNakedPairsColumn
                case self.findNakedPairsColumn:
                    self.FindNakedPairsColumn()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = self.updateSudoku
                    else:
                        result = result + ", no"
                        self.state = self.findNakedPairsGroup
                case self.findNakedPairsGroup:
                    self.FindNakedPairsGroup()
                    if self.Changed:
                        result = result + ", yes"
                        self.state = self.updateSudoku
                    else:
                        result = result + ", no"
                case self.updateSudoku:
                    self.DoChange()
                    self.state = self.start
                    self.ConstraintChecked = self.Check()
                    if not self.ConstraintChecked:
                        result = result + ' Sudoku is bad, two or more cells have same number'
        else:
            result = self.steps[5]

        return result
   