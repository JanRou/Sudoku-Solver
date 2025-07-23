import math

class BaseCell:
    def __init__(self, dim, row, col, group):
        self.number = 0 # 0 means not solved, 1 - n means solved
        self.dimension = dim # 4=2x2, 9=3x3, 16=4x4, 25=5x5 ...
        self.row=row # row and column are 0 based
        self.column=col
        self.newNumber = 0 # new number when changed
        self.newCandidates = [] # new candidates when changed
        self.candidates = []
        for col in range(1, 1+self.dimension):
            self.candidates.append(col)
        self.group = group
        self.changed = False # ?
        self.isInitial = False # is true, when the number is given for the puzzle
        self.isMarked = False # True when the cell is marked like belonging to a pair

    @property
    def Dimension(self):
        return self.dimension

    @property
    def Row(self):
        return self.row

    @property
    def Column(self):
        return self.column

    @property
    def Group(self):
        return self.group
    
    @property
    def Number(self):
        return self.number

    @Number.setter
    def Number(self, n): # It doesn't work for inherited class calling base class property?
        self.SetNumber(n)

    def SetNumber(self, n, isInitial=False):
        # Assigning to Number means the cell is marked changed and newNumber holds the solution for the cell
        if 0 < n and n <= self.dimension:
            if isInitial:
                # Initital number is used, when the sudoku is cleared for retry
                self.isInitial = isInitial
                self.number = n
            else:
                self.newNumber = n
                # clear list of candidates and set the only one
                self.candidates.clear()
                self.newCandidates.clear()
                self.changed = True
        else:
            raise ValueError            

    @property
    def NewNumber(self):
        result = 0
        if self.changed:
            result = self.newNumber
        return result

    @property
    def Solved(self):
        return self.number != 0

    @property
    def IsInitial(self):
        return self.isInitial

    @property
    def Changed(self):
        return self.changed
    
    @property
    def IsMarked(self):
        return self.isMarked

    def Mark(self):
        self.isMarked = True

    def DoChange(self):
        # Sets the solution, when newNumber holds a solution and clears list of candidates
        # Clears temporary variables newNumber and newCandidates and changed flag
        self.isMarked = False
        if not self.Solved and self.changed:
            if self.newNumber != 0:
                self.number = self.newNumber
                self.candidates.clear()
            # Refactor: Can I avoid the copy and clear lists of candidates and newCandidates?
            if self.newCandidates != []:
                self.candidates.clear()
                self.candidates = self.newCandidates.copy()
            self.newCandidates.clear()
            self.newNumber = 0
            self.changed = False

    def SetSingleCandidateToNewNumber(self):
        if len(self.candidates) == 1:
            # only one candidate left, set cell newNumber and flag changed
            if self.candidates[0] != 0:
                self.newNumber = self.candidates[0]
                self.changed = True
            else:
                raise ValueError

    @property
    def Candidates(self):
        result = []
        if not self.Solved:            
            result = self.candidates
        return result

    @property
    def NewCandidates(self):
        return self.newCandidates

    def Remove(self, candidateToRemove):
        if 0 < candidateToRemove and candidateToRemove <= self.dimension:
            if not self.Solved:
                if (not self.changed) or self.newCandidates == []:
                    self.newCandidates = self.candidates.copy() # copy so new candidates are a new list object
                if candidateToRemove in self.newCandidates:
                    self.changed = True
                    self.newCandidates.remove(candidateToRemove)
        else:
            raise ValueError
        
    def AppendSingleCandidates(self, singleCandidates):
        # Append new single candidates in the cell to the list of single candidates
        # Don't append when already solved.
        if not self.Solved:
            # Find unique singleCandidates from candidates, when cell isn't changed,
            # otherwise use newCandidates, because another FindSingles algorithm
            # may have changed the candidates to a single candidate.
            candidates = self.candidates
            if self.changed:
                candidates = self.newCandidates
            for candidate in candidates:
                if not candidate in singleCandidates:
                    singleCandidates.append(candidate)
        return singleCandidates
    
    def CountAndSetFirstCellForSingleCandidate(self, singleCandidate, count, firstCell):
        # Jump over solved cells.
        candidates = self.candidates
        if self.changed:
            candidates = self.newCandidates
        if (not self.Solved) and singleCandidate in candidates:
            count += 1
            if count==1:
                firstCell = self  # return this as first just in case it's the only one
        return (count, firstCell)
    


    


