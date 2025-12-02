import unittest
import math

from normal import normal
from normal.normalSudoku import NormalSudoku

if __name__ == '__main__':
    unittest.main()

class TestNormalSudoku(unittest.TestCase):

    def testConstructorOk(self):
                # Arrange
        dimension = 4
        dut = self.create4x4TestSudoku( dimension)

        # Act
        resultDim = dut.Dimension
        resultSudoku = dut.Sudoku

        # Assert
        # 4x4 sudoku constructed
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   ---------  -----------------------------------------
        # 0 ! . !3. !  !(1,2,3,4).(1,2,3,4)!-        .(1,2,3,4)!
        # 1 !4. ! . !  !-        .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4)!(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,4)!-        !(1,2,3,4).(1,2,3,4)!
        #   ---------  -----------------------------------------
        self.assertEqual(dimension, resultDim)
        self.assertFalse(resultSudoku[0][0].Solved)
        self.assertTrue(resultSudoku[1][0].Solved)
        self.assertEqual(4, resultSudoku[1][0].Number)


    def testFindNakedPairsRow(self):
        # Example from https://www.sudokuwiki.org/Naked_Candidates#NP
        # Two pairs in the first rows are marked with curly braces
        #   ------------------- --------------------------------------------------------------------------------
        # 0 !4. . ! . . !9.3.8! !-      .{1,6}  .{1,6}  !(1,2,5).(1,2,5,6,7).(2,5,6,7)!-    .-          .-       !
        # 1 ! .3.2! .9.4!1. . ! !(7,8)  .-      .-      !(5,8)  .-          .-        !-    .(5,6)      .(5,6,7) !
        # 2 ! .9.5!3. . !2.4. ! !(1,7,8).-      .-      !-      .(1,6,7,8)  .{7,6}    !-    .-          .{7,6}   !
        #   !=====!=====!=====! !=======================!=============================!==========================!
        # 3 !3.7. !6. .9! . .4! !-      .-      .(1,8)  !-      .(2,5,8)    .-        !(5,8).(1,2,5,8)  .-       !
        # 4 !5.2.9! . .1!6.7.3! !-      .-      .-      !(4,8)  .(4,8)      .-        !-    .-          .-       !
        # 5 !6. .4!7. .3! .9. ! !-      .(1,8)  .-      !-      .(2,5,8)    .-        !(5,8).-          .(1,2,5) !
        #   !=====!=====!=====! !=======================!=============================!==========================!
        # 6 !9.5.7! . .8!3. . ! !-      .-      .-      !(1,2,4).(1,2,4,6)  .-        !-   .(1,2,6)    .(1,2,6)  !
        # 7 ! . .3!9. . !4. . ! !(1,8)  .(1,6,8).-      !-      .(1,2,5,6,7).(2,5,6,7)!-   .(1,2,5,6,8).(1,2,5,6)!
        # 8 !2.4. ! .3. !7. .9! !-      .-      .(1,6,8)!(1,5)  .-          .(5,6)    !-   .(1,5,6,8)  .-        !
        #   ------------------- ----------------------------------------------------------------------------------
        # The candidates for the first row should be like this after the acting
        #   ------------------- --------------------------------------------------------------------------
        # 0 !4. . ! . . !9.3.8! !-      .{1,6}  .{1,6}  !(2,5).(2,5,7).(2,5,7)!-    .-          .-       !

        # Arrange
        dut = self.create9x9TestSudokuNakedPairRowAndGroup()
        dut.FindPossibleCandidates()
        dut.SetSingleCandidatesAsnewNumber()
        dut.DoChange() # now the sudoku should like above

        # Act
        candidatesrow0col4Before = dut.sudoku[0][4].Candidates
        dut.FindNakedPairsRow()
        candidatesrow0col4After = dut.sudoku[0][4].NewCandidates

        # Assert
        self.assertTrue(1 in candidatesrow0col4Before)
        # Assert that the list of candidates holds 5 candidates before
        self.assertTrue(len(candidatesrow0col4Before) == 5)
        self.assertTrue(6 in candidatesrow0col4Before)
        self.assertFalse(1 in candidatesrow0col4After)
        self.assertFalse(6 in candidatesrow0col4After)
        # Assert that the list of new candidates holds 3 candidates after
        self.assertTrue(len(candidatesrow0col4After) == 3)


    def testFindNakedPairsColumn(self):
        # Example from https://www.sudokuwiki.org/Naked_Candidates#NP
        # Two pairs in fourth colum are marked with curly braces
        #   ------------------- --------------------------------------------------------------------------------
        # 0 ! .8. ! .9. ! .3. ! !(1,4,6,7).-    .(5,6,7)!(1,2,4,5,7).-        .(1,2)  !(2,4,7).-.(2,4)!
        # 1 ! .3. ! . . ! .6.9! !(1,4,7)  .-    .(7,5)  !(1,2,4,5,7).(1,2,7,8).(1,2,8)!(2,4,7).-.-    !
        # 2 !9. .2! .6.6!1.5.8! !-        .(4,7).-      !(4,7)      .-        .-      !-      .-.-    !
        #   !=====!=====!=====! !=======================!=============================!===============!
        # 3 ! .2. !8. .4!5.9. ! !(6,7)    .-    .(6,7)  !-          .(1,3)    .-      !-      .-.(1,3)!
        # 4 !8.5.1!9. .7! .4.6! !-        .-    .-      !-          .(2,3)    .-      !(2,3)  .-.-    !
        # 5 !3.9.4!6. .5!8.7. ! !-        .-    .-      !-          .(1,2)    .-      !-      .-.(1,2)!
        #   !=====!=====!=====! !=======================!=============================!===============!
        # 6 !5.6.3! .4. !9.8.7! !-        .-    .-      !(1,2)      .-        .(1,2)  !-      .-.-    !
        # 7 !2. . ! . . ! .1.5! !-        .(4,7).(7,8,9)!{3,7}      .(3,7,8)  .(6,8,9)!(3,4,6).-.-    !
        # 8 ! .1. ! .5. ! .2. ! !(4,7)    .-    .(7,8,9)!{3,7}      .-        .(6,8,9)!(3,4,6).-.(4,3)!
        #   ------------------- -----------------------------------------------------------------------
        # Number 7 is removed from candidates of cells in column 3 in row 0, 1, 2         

        # Arrange
        dut = self.create9x9TestSudokuNakedPairColumnAndGroup()
        dut.FindPossibleCandidates()
        dut.SetSingleCandidatesAsnewNumber()
        dut.DoChange() # now the sudoku should like above

        # Act
        candidatesrow0col3Before = dut.sudoku[0][3].Candidates
        candidatesrow1col3Before = dut.sudoku[1][3].Candidates
        candidatesrow2col3Before = dut.sudoku[2][3].Candidates
        dut.FindNakedPairsColumn()
        candidatesrow0col3After = dut.sudoku[0][3].NewCandidates
        candidatesrow1col3After = dut.sudoku[1][3].NewCandidates
        candidatesrow2col3After = dut.sudoku[2][3].NewCandidates

        # Assert
        self.assertTrue(7 in candidatesrow0col3Before)
        # Assert that the list of candidates holds 5 candidates before
        self.assertTrue(len(candidatesrow0col3Before) == 5)
        self.assertTrue(7 in candidatesrow1col3Before)
        self.assertTrue(7 in candidatesrow2col3Before)
        self.assertFalse(7 in candidatesrow0col3After)
        self.assertFalse(7 in candidatesrow1col3After)
        self.assertFalse(7 in candidatesrow2col3After)
        # Assert that the list of new candidates holds 4 candidates after
        self.assertTrue(len(candidatesrow0col3After) == 4)

    def testFindNakedPairsGroup(self):
        # Example from https://www.sudokuwiki.org/Naked_Candidates#NP
        # Two pairs in the group row 6-8 and column 0-3 
        #   ------------------- --------------------------------------------------------------------------------
        # 0 ! .8. ! .9. ! .3. ! !(1,4,6,7).-    .(5,6,7)!(1,2,4,5,7).-        .(1,2)  !(2,4,7).-.(2,4)!
        # 1 ! .3. ! . . ! .6.9! !(1,4,7)  .-    .(7,5)  !(1,2,4,5,7).(1,2,7,8).(1,2,8)!(2,4,7).-.-    !
        # 2 !9. .2! .6.6!1.5.8! !-        .(4,7).-      !(4,7)      .-        .-      !-      .-.-    !
        #   !=====!=====!=====! !=======================!=============================!===============!
        # 3 ! .2. !8. .4!5.9. ! !(6,7)    .-    .(6,7)  !-          .(1,3)    .-      !-      .-.(1,3)!
        # 4 !8.5.1!9. .7! .4.6! !-        .-    .-      !-          .(2,3)    .-      !(2,3)  .-.-    !
        # 5 !3.9.4!6. .5!8.7. ! !-        .-    .-      !-          .(1,2)    .-      !-      .-.(1,2)!
        #   !=====!=====!=====! !=======================!=============================!===============!
        # 6 !5.6.3! .4. !9.8.7! !-      .-      .-      !(1,2)      .-        .(1,2)  !-      .-.-    !
        # 7 !2. . ! . . ! .1.5! !-      .{4,7}  .(7,8,9)!(3,7)      .(3,7,8)  .(6,8,9)!(3,4,6).-.-    !
        # 8 ! .1. ! .5. ! .2. ! !{4,7}  .-      .(7,8,9)!(3,7)      .-        .(6,8,9)!(3,4,6).-.(4,3)!
        #   ------------------- -----------------------------------------------------------------------
        # Number 7 is removed from column 2 in row 7 and 8

        # Arrange
        dut = self.create9x9TestSudokuNakedPairColumnAndGroup()
        dut.FindPossibleCandidates()
        dut.SetSingleCandidatesAsnewNumber()
        dut.DoChange() # now the sudoku should like above

        # Act
        candidatesrow7col2Before = dut.sudoku[7][2].Candidates
        candidatesrow8col2Before = dut.sudoku[8][2].Candidates
        dut.FindNakedPairsGroup()
        candidatesrow7col2After = dut.sudoku[7][2].NewCandidates
        candidatesrow8col2After = dut.sudoku[8][2].NewCandidates

        # Assert
        self.assertTrue(7 in candidatesrow7col2Before)
        # Assert that the list of candidates holds 3 candidates before
        self.assertTrue(len(candidatesrow7col2Before) == 3)
        self.assertTrue(7 in candidatesrow7col2Before)
        self.assertFalse(7 in candidatesrow7col2After)
        self.assertFalse(7 in candidatesrow7col2After)
        # Assert that the list of new candidates holds 2 candidates after
        self.assertTrue(len(candidatesrow7col2After) == 2)

    def create9x9TestSudokuNakedPairRowAndGroup(self):
        sudoku= NormalSudoku( 9)
        sudoku.Set( 0, 0, 4,True)
        sudoku.Set( 0, 6, 9,True)
        sudoku.Set( 0, 7, 3,True)
        sudoku.Set( 0, 8, 8,True)
        sudoku.Set( 1, 1, 3,True)
        sudoku.Set( 1, 2, 2,True)
        sudoku.Set( 1, 4, 9,True)
        sudoku.Set( 1, 5, 4,True)
        sudoku.Set( 1, 6, 1,True)
        sudoku.Set( 2, 1, 9,True)
        sudoku.Set( 2, 2, 5,True)
        sudoku.Set( 2, 3, 3,True)
        sudoku.Set( 2, 6, 2,True)
        sudoku.Set( 2, 7, 4,True)
        sudoku.Set( 3, 0, 3,True)
        sudoku.Set( 3, 1, 7,True)
        sudoku.Set( 3, 3, 6,True)
        sudoku.Set( 3, 5, 9,True)
        sudoku.Set( 3, 8, 4,True)
        sudoku.Set( 4, 0, 5,True)
        sudoku.Set( 4, 1, 2,True)
        sudoku.Set( 4, 2, 9,True)
        sudoku.Set( 4, 5, 1,True)
        sudoku.Set( 4, 6, 6,True)
        sudoku.Set( 4, 7, 7,True)
        sudoku.Set( 4, 8, 3,True)
        sudoku.Set( 5, 0, 6,True)
        sudoku.Set( 5, 2, 4,True)
        sudoku.Set( 5, 3, 7,True)
        sudoku.Set( 5, 5, 3,True)
        sudoku.Set( 5, 7, 9,True)
        sudoku.Set( 6, 0, 9,True)
        sudoku.Set( 6, 1, 5,True)
        sudoku.Set( 6, 2, 7,True)
        sudoku.Set( 6, 5, 8,True)
        sudoku.Set( 6, 6, 3,True)
        sudoku.Set( 7, 2, 3,True)
        sudoku.Set( 7, 3, 9,True)
        sudoku.Set( 7, 6, 4,True)
        sudoku.Set( 8, 0, 2,True)
        sudoku.Set( 8, 1, 4,True)
        sudoku.Set( 8, 4, 3,True)
        sudoku.Set( 8, 6, 7,True)
        sudoku.Set( 8, 8, 9,True)
        sudoku.DoChange()
        return sudoku

    def create9x9TestSudokuNakedPairColumnAndGroup(self):
        sudoku= NormalSudoku( 9)
        sudoku.Set( 0, 1, 8,True)
        sudoku.Set( 0, 4, 9,True)
        sudoku.Set( 0, 7, 3,True)
        sudoku.Set( 1, 1, 3,True)
        sudoku.Set( 1, 7, 6,True)
        sudoku.Set( 1, 8, 9,True)
        sudoku.Set( 2, 0, 9,True)
        sudoku.Set( 2, 2, 2,True)
        sudoku.Set( 2, 4, 6,True)
        sudoku.Set( 2, 5, 3,True)
        sudoku.Set( 2, 6, 1,True)
        sudoku.Set( 2, 7, 5,True)
        sudoku.Set( 2, 8, 8,True)
        sudoku.Set( 3, 1, 2,True)
        sudoku.Set( 3, 3, 8,True)
        sudoku.Set( 3, 5, 4,True)
        sudoku.Set( 3, 6, 5,True)
        sudoku.Set( 3, 7, 9,True)
        sudoku.Set( 4, 0, 8,True)
        sudoku.Set( 4, 1, 5,True)
        sudoku.Set( 4, 2, 1,True)
        sudoku.Set( 4, 3, 9,True)
        sudoku.Set( 4, 5, 7,True)
        sudoku.Set( 4, 7, 4,True)
        sudoku.Set( 4, 8, 6,True)
        sudoku.Set( 5, 0, 3,True)
        sudoku.Set( 5, 1, 9,True)
        sudoku.Set( 5, 2, 4,True)
        sudoku.Set( 5, 3, 6,True)
        sudoku.Set( 5, 5, 5,True)
        sudoku.Set( 5, 6, 8,True)
        sudoku.Set( 5, 7, 7,True)
        sudoku.Set( 6, 0, 5,True)
        sudoku.Set( 6, 1, 6,True)
        sudoku.Set( 6, 2, 3,True)
        sudoku.Set( 6, 5, 4,True)
        sudoku.Set( 6, 6, 9,True)
        sudoku.Set( 6, 7, 8,True)
        sudoku.Set( 6, 8, 7,True)
        sudoku.Set( 7, 0, 2,True)
        sudoku.Set( 7, 7, 1,True)
        sudoku.Set( 7, 8, 5,True)
        sudoku.Set( 8, 1, 1,True)
        sudoku.Set( 8, 4, 5,True)
        sudoku.Set( 8, 7, 2,True)
        sudoku.DoChange()
        return sudoku

    def create4x4TestSudoku(self, dimension):
        # 4x4 sudoku for test
        #    Sudoku     Candidates  
        #    0 1 2 3    0
        #   ---------  -----------------------------------------
        # 0 ! . !3. !  !(1,2,3,4).(1,2,3,4)!-        .(1,2,3,4)!
        # 1 !4. ! . !  !-        .(1,2,3,4)!(1,2,3,4).(1,2,3,4)!
        #   !-.-!-.-!  !---------.---------!---------.---------! 
        # 2 ! . ! .1!  !(1,2,3,4)!(1,2,3,4)!(1,2,3,4).-        !
        # 3 ! .4! . !  !(1,2,3,4)!-        !(1,2,3,4).(1,2,3,4)!
        #   ---------  -----------------------------------------
        sudoku= NormalSudoku( dimension)
        sudoku.Set( 0, 2, 3,True)
        sudoku.Set( 1, 0, 4,True)
        sudoku.Set( 2, 3, 1,True)
        sudoku.Set( 3, 1, 4,True)
        sudoku.DoChange()
        return sudoku
    
