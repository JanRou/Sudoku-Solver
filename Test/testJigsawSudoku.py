import unittest
import math

from context import jigsaw
from jigsaw.jigsawSudoku import JigsawSudoku

if __name__ == '__main__':
    unittest.main()

class TestJigsawSudoku(unittest.TestCase):

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

    def testCheckShapeOk(self):
        # Arrange
        dimension = 4
        shape = self.createShape(dimension)
        dut = JigsawSudoku( dimension, shape)

        # Act
        checkShapeResult = dut.CheckShape(shape)

        # Assert
        self.assertTrue(checkShapeResult[0])
        self.assertEqual( "", checkShapeResult[1])

    def testCheckShapeFail(self):
        # Arrange
        dimension = 4
        shape = self.createShape(dimension)
        dut = JigsawSudoku( dimension, shape)
        # change shape to a failing shape
        shape[dimension-1][dimension-1] = 2 # overwrites 3 with 2

        # Act
        checkShapeResult = dut.CheckShape(shape)

        # Assert
        self.assertFalse(checkShapeResult[0])
        self.assertNotEqual("", checkShapeResult[1])

    def testConstructorFails(self):
        # Arrange
        dimension = 4
        shape = self.createShape(dimension)
        dut = JigsawSudoku( 4, shape)
        # change shape to a failing shape
        shape[dimension-1][dimension-1] = 2 # overwrites 3 with 2

        # Act and Assert
        with self.assertRaises(ValueError):
            dut = JigsawSudoku( dimension, shape)

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
        shape = self.createShape(dimension)
        sudoku= JigsawSudoku( dimension, shape)
        sudoku.Set( 0, 2, 3,True)
        sudoku.Set( 1, 0, 4,True)
        sudoku.Set( 2, 3, 1,True)
        sudoku.Set( 3, 1, 4,True)
        sudoku.DoChange()
        return sudoku

    def createShape(self, dimension):
        shape = []
        rho = round(math.sqrt(dimension))
        for r in range(dimension):
            row = []
            for c in range(dimension):
                row.append( ( r // rho )* rho + (c // rho ) )  # operator // is integer division 
            shape.append(row)
        return shape

    # def test(self):
    #     # Arrange

    #     # Act

    #     # Assert