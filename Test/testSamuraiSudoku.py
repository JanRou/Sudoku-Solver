import unittest
import math

from context import normal
from samurai.samuraiSudoku import SamuraiSudoku

if __name__ == '__main__':
    unittest.main()

class TestSamuraiSudoku(unittest.TestCase):

    def testConstructorOk(self):
        # Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)

        # Act
        resultDimension = dut.Dimension
        resultGrid = dut.Grid
        resultSudokus = dut.Sudokus

        # Assert
        #    0 1 2 3 0 1 2 3
        #   -----------------
        # 0 !2.1!3.4|3.4!2.1!
        # 1 !4.3!1.2|1.2!4.3!
        # 2 !3.2! . ! . !1.4!
        # 3 !1.4! . ! . !3.2!
        #   !===!---!---!===!
        # 0 !2.1! . ! . !4.3!
        # 1 !4.3! . ! . !2.1!
        # 2 !3.4!2.1|2.1!3.4!
        # 3 !2.1!4.3|4.3!1.2!
        #   ---------  -----------------------------------------
        self.assertEqual(dimension, resultDimension)
        self.assertEqual(grid, resultGrid)
        self.assertTrue(resultSudokus[0].Sudoku[0][0].Solved)
        self.assertFalse(resultSudokus[0].Sudoku[2][3].Solved)
        self.assertEqual(2, resultSudokus[0].Sudoku[0][0].Number)
        self.assertEqual(1, resultSudokus[0].Sudoku[0][1].Number)
        self.assertFalse(dut.Solved)

    def testSharedCellsAreOk(self):
        # Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)

        # Act
        # Set cell nummber for sudokus not in the middle => middle sudoku is changed
        dut.Set( 0, 2, 2, 4)
        dut.Set( 4, 0, 0, 1)
        # Set cell nummber for sudoku in the middle => not in the middle sudokus changed
        dut.Set( 2, 0, 3, 3)
        dut.Set( 2, 2, 1, 2)
        
        resultSudokus = dut.Sudokus

        # Assert
        self.assertEqual(resultSudokus[0].Sudoku[2][2].Number, resultSudokus[2].Sudoku[0][0].Number)
        self.assertEqual(resultSudokus[4].Sudoku[0][0].Number, resultSudokus[2].Sudoku[2][2].Number)
        self.assertEqual(resultSudokus[2].Sudoku[0][3].Number, resultSudokus[1].Sudoku[2][1].Number)
        self.assertEqual(resultSudokus[2].Sudoku[2][1].Number, resultSudokus[3].Sudoku[0][3].Number)

    def testRemoveCandidatesHookForSharedCells(self):
        #Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)
        # Set upper left cell in the group to 4
        cell00Middle = dut.Sudokus[2].Sudoku[0][0]
        cell00Middle.Number = 4
        cell00Middle.DoChange()

        #Act
        dut.RemoveCandidatesHook(cell00Middle, dut.Sudokus[2])
        dut.DoChange()
        resultUpperLeftSudoku = dut.Sudokus[0].Sudoku

        #Assert
        # Is 4 removed from the shared cells in the lower right group of the upper left sudoku?
        self.assertEqual([1,2,3], resultUpperLeftSudoku[2][3].Candidates)
        self.assertEqual([1,2,3], resultUpperLeftSudoku[3][2].Candidates)
        self.assertEqual([1,2,3], resultUpperLeftSudoku[3][3].Candidates)

    def testFindPossibleCandidates(self):
        #Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)

        #Act
        dut.FindPossibleCandidates()
        result = dut.Sudokus[2].Sudoku

        #Assert
        # Do all the cells of middle sudoku a single candidate?        
        for r in range(dimension):
            for c in range(dimension):
                self.assertTrue(result[r][c].Changed, "r="+str(r)+", c="+str(c))
                self.assertEqual(1, len(result[r][c].NewCandidates))

    def testSetSingles(self):
        #Arrange
        dimension = 4
        grid = 5
        dut = self.create2x2plus1TestSamuraiSudoku( dimension, grid)
        dut.Sudokus[2].Sudoku[0][0].Remove(1)
        dut.Sudokus[2].Sudoku[0][0].Remove(2)
        dut.Sudokus[2].Sudoku[0][1].Remove(2)
        dut.Sudokus[2].Sudoku[0][1].Remove(4)
        dut.Sudokus[2].Sudoku[1][0].Remove(1)
        dut.Sudokus[2].Sudoku[1][0].Remove(4)
        dut.Sudokus[2].Sudoku[2][1].Remove(1)
        dut.Sudokus[2].Sudoku[2][1].Remove(4)
        # Here are the candidates in middle sudoku  removed (it's not a real situation):
        # 0 ... omitted for breverity
        # 2 ... !(3,4).(1,3)    ! ...
        # 3 ... !(2,3).(2,3)! ...
        # ...                 

        #Act
        dut.SetSingles()
        dut.DoChange()
        resultSolved = dut.Sudokus[0].Solved
        resultSudoku = dut.Sudokus[0].Sudoku

        #Assert
        # Here is the resulting sudoku in the middle:
        #    0 1 2 3 0 1 2 3
        #        0 1 2 3
        #   -----------------
        # 0 ... omitted for breverity
        # 2 ... !4.1! ...
        # 3 ... !2.3! ...
        # ... 
        # Is the upper left sudoku solved?
        self.assertTrue(resultSolved)
        self.assertTrue(resultSudoku[2][2].Solved)
        self.assertEqual(resultSudoku[2][2].Number, 4)
        self.assertTrue(resultSudoku[2][3].Solved)
        self.assertEqual(resultSudoku[2][3].Number, 1)

    def create2x2plus1TestSamuraiSudoku(self, dimension, grid):
        #    0 1 2 3 0 1 2 3
        #   -----------------
        # 0 !2.1!3.4H3.4!2.1!
        # 1 !4.3!1.2H1.2!4.3!
        # 2 !3.2! . ! . !1.4!
        # 3 !1.4! . ! . !3.2!
        #   !===!---!---!===!
        # 0 !2.1! . ! . !4.3!
        # 1 !4.3! . ! . !2.1!
        # 2 !3.4!2.1H2.1!3.4!
        # 3 !2.1!4.3H4.3!1.2!
        testSudokus = []
        testSudoku = []
        testSudoku.append([2,1,3,4])
        testSudoku.append([4,3,1,2])
        testSudoku.append([3,2,0,0])
        testSudoku.append([1,4,0,0])
        testSudokus.append(testSudoku)
        testSudoku = []
        testSudoku.append([3,4,2,1])
        testSudoku.append([1,2,4,3])
        testSudoku.append([0,0,1,4])
        testSudoku.append([0,0,3,2])
        testSudokus.append(testSudoku)
        testSudoku = [] # Empty middle [2] sudoku
        testSudokus.append(testSudoku)        
        testSudoku = []
        testSudoku.append([2,1,0,0])
        testSudoku.append([4,3,0,0])
        testSudoku.append([3,4,2,1])
        testSudoku.append([2,1,4,3])
        testSudokus.append(testSudoku)
        testSudoku = []
        testSudoku.append([0,0,4,3])
        testSudoku.append([0,0,2,1])
        testSudoku.append([2,1,3,4])
        testSudoku.append([4,3,1,2])
        testSudokus.append(testSudoku)

        sudoku= SamuraiSudoku( dimension, grid)

        for s in range(grid):
            for row in range(dimension):
                for col in range(dimension):
                    if testSudokus[s] != [] and testSudokus[s][row][col]!=0:
                        sudoku.Set( s, row, col, testSudokus[s][row][col],True)

        sudoku.DoChange()
        return sudoku
