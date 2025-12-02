import unittest
import math

from normal import normal
from samurai.samuraiCell import SamuraiCell

if __name__ == '__main__':
    unittest.main()

class TestSamuraiCell(unittest.TestCase):

    def testConstructor(self):
            # Arrange
            dimension = 4
            group = 0
            row = 0
            column = 0
            expectedcandidates = []
            for c in range(1,dimension+1):
                expectedcandidates.append(c)
            dut = SamuraiCell( dimension, row, column, group)

            # Act
            solvedResult = dut.Solved
            candidatesResult = dut.Candidates
            groupResult = dut.Group
            rowResult = dut.Row
            columnResult = dut.Column

            # Assert
            self.assertFalse(solvedResult)
            self.assertEqual(expectedcandidates, candidatesResult)
            self.assertEqual(row, rowResult)
            self.assertEqual(column, columnResult)
            self.assertEqual(group, groupResult)


    def testRemoveOk(self):
        # Arrange
        dimension = 4
        group = 0
        row = 0
        column = 0
        expectedcandidates = []
        # removes 1, so start from 2
        for c in range( 2, dimension+1):
            expectedcandidates.append(c)
        dut = SamuraiCell( dimension, row, column, group)

        # Act
        dut.Remove(1)

        # Assert
        self.assertEqual(expectedcandidates, dut.NewCandidates)

    def testRemoveFail(self):
        # Arrange
        dimension = 4
        group = 0
        row = 0
        column = 0
        numberLow = 0
        numberHigh = 5
        dut = SamuraiCell( dimension, row, column, group)

        # Assert
        with self.assertRaises(ValueError):
            dut.Remove(numberLow)

        with self.assertRaises(ValueError):
            dut.Remove(numberHigh)

    def testSetAndGetNumberOk(self):
        # Arrange
        dimension = 4
        group = 0
        row = 0
        column = 0
        number = 2
        dut = SamuraiCell( dimension, row, column, group)

        # Act
        getResult1 = dut.Number
        dut.Number = number
        changeResult = dut.Changed
        dut.DoChange()
        getResult2 = dut.Number
        solvedResult = dut.Solved

        # Assert
        self.assertEqual( 0, getResult1)
        self.assertEqual( number, getResult2)
        self.assertTrue(solvedResult)

    def testSetAndGetNumberFail(self):
        # Arrange
        dimension = 4
        group = 0
        row = 0
        column = 0
        numberLow = 0
        numberHigh = 5
        dut = SamuraiCell( dimension, row, column, group)

        # Assert
        with self.assertRaises(ValueError):
            dut.Number = numberHigh

        with self.assertRaises(ValueError):
            dut.Number = numberLow

    def testSetSingleCandidateToNewNumberOk(self):
        # Arrange
        dimension = 4
        group = 0
        row = 0
        column = 0
        dut = SamuraiCell( dimension, row, column, group)

        # Act
        dut.Remove(1)
        dut.Remove(2)
        dut.Remove(3)
        resultNewCandidates = dut.NewCandidates.copy()
        dut.DoChange()
        resultCandidates = dut.Candidates.copy()
        dut.SetSingleCandidateToNewNumber()
        resultNewNumber = dut.NewNumber
        dut.DoChange()

        # Assert
        self.assertEqual( 1, len(resultNewCandidates))
        self.assertIn( 4, resultNewCandidates)
        self.assertEqual( 1, len(resultCandidates))
        self.assertIn( 4, resultCandidates)
        self.assertEqual( 4, resultNewNumber)
        self.assertTrue( dut.Solved)

    def testSetAndGetNumberWithSharedOk(self):
            # Arrange
            dimension = 4
            group = 0
            row = 0
            column = 0
            number = 2
            dut = SamuraiCell( dimension, row, column, group)

            sharedGroup = 0
            sharedRow = 0
            sharedColumn = 0
            shared = SamuraiCell( dimension, sharedRow, sharedColumn, sharedGroup)
            dut.SetShared(shared)
            shared.SetShared(dut)

            getResult1 = dut.Number
            dut.Number = number
            changeResult = dut.Changed
            sharedChangeResult = dut.Changed
            dut.DoChange()
            getResult2 = dut.Number
            sharedGetResult2 = dut.Number
            solvedResult = dut.Solved

            # Assert
            self.assertEqual( 0, getResult1)
            self.assertTrue(changeResult)
            self.assertTrue(sharedChangeResult)
            self.assertEqual( number, getResult2)
            self.assertEqual( number, sharedGetResult2)
            self.assertTrue(solvedResult)

    def testRemoveWithSharedOk(self):
        # Arrange
        dimension = 4
        group = 0
        row = 0
        column = 0
        number = 2
        sharedGroup = 0
        sharedRow = 0
        sharedColumn = 0
        expectedcandidates = []

        # removes 1, so start from 2
        for c in range( 2, dimension+1):
            expectedcandidates.append(c)

        dut = SamuraiCell( dimension, row, column, group)
        shared = SamuraiCell( dimension, sharedRow, sharedColumn, sharedGroup)
        dut.SetShared(shared)
        shared.SetShared(dut)

        # Act
        dut.Remove(1)

        # Assert
        self.assertEqual(expectedcandidates, dut.NewCandidates)
        self.assertEqual(expectedcandidates, shared.NewCandidates)

    def testSetSingleCandidateToNewNumberWithShared(self):
        # Arrange
        dimension = 4
        group = 0
        row = 0
        column = 0
        number = 2
        sharedGroup = 0
        sharedRow = 0
        sharedColumn = 0
        expectedcandidates = []

        # removes 1, so start from 2
        for c in range( 2, dimension+1):
            expectedcandidates.append(c)

        dut = SamuraiCell( dimension, row, column, group)
        shared = SamuraiCell( dimension, sharedRow, sharedColumn, sharedGroup)
        dut.SetShared(shared)
        shared.SetShared(dut)

        # Act
        dut.Remove(1)
        dut.Remove(2)
        dut.Remove(3)
        resultNewCandidates = dut.NewCandidates.copy() # copy, because the list is cleared in DoChange()
        resultSharedNewCandidates = shared.NewCandidates.copy()
        dut.DoChange()
        resultCandidates = dut.Candidates.copy()
        resultSharedCandidates = shared.Candidates.copy()
        dut.SetSingleCandidateToNewNumber()
        resultNewNumber = dut.NewNumber
        resultSharedNewNumber = shared.NewNumber
        dut.DoChange()

        # Assert
        self.assertEqual( 1, len(resultNewCandidates))
        self.assertIn( 4, resultNewCandidates)
        self.assertEqual( 1, len(resultCandidates))
        self.assertIn( 4, resultCandidates)
        self.assertEqual( 4, resultNewNumber)
        self.assertTrue( dut.Solved)
        self.assertEqual( 1, len(resultSharedNewCandidates))
        self.assertIn( 4, resultSharedNewCandidates)
        self.assertEqual( 1, len(resultSharedCandidates))
        self.assertIn( 4, resultSharedCandidates)
        self.assertEqual( 4, resultSharedNewNumber)
        self.assertTrue( shared.Solved)