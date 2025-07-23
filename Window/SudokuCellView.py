import math
import tkinter as tk
from tkinter import font


class SudokuCellView(tk.Canvas):
    def __init__(self, root, bgcolour, cell, **kwargs):
        super().__init__( root, width=20, height=20, relief='solid',  background=bgcolour, **kwargs)
        self.cell = cell
        self.candidatesFont = font.Font(family='arial', size=7)
        self.initialFont = font.Font(family='arial', size=12, weight="bold" )
        self.solvedFont = font.Font(family='arial', size=12, slant="italic")
        self.MarkedFont = font.Font(family='arial', size=7)
        self.rho = round(math.sqrt(cell.Dimension)) # rho x rho dimension of cell = 2, 3, 4 ...

    def show(self):
        self.delete('all')

        if self.cell.Solved and self.cell.IsInitial:
            # display final number in black in center
            self.create_text( 16, 13 , text=str(self.cell.Number), anchor='nw', font=self.initialFont, fill='black')
        elif self.cell.Solved and not self.cell.IsInitial:
            self.create_text( 16, 13 , text=str(self.cell.Number), anchor='nw', font=self.solvedFont, fill='black')
        elif self.cell.Changed and self.cell.NewNumber != 0:
            self.create_text( 16, 13 , text=str(self.cell.NewNumber), anchor='nw', font=self.solvedFont, fill='teal')
        else:
            candidates = self.cell.Candidates
            candidateFill = 'black'
            if self.cell.Changed:
                candidates = self.cell.NewCandidates
                candidateFill = 'teal'
            for row in range(self.rho): # y direction for text in canvas
                for col in range(self.rho): # x direction for text in canvas
                    c = row*self.rho + col + 1
                    if c in candidates:
                        if self.cell.IsMarked:
                            text = self.create_text( 14*col + 5 , 13*row + 3 , text=str(c), anchor='nw', font=self.candidatesFont, fill=candidateFill)
                            rect=self.create_rectangle(self.bbox(text),outline='', fill='#BFBFBF')
                            self.tag_lower(rect,text)
                        else:
                            self.create_text( 14*col + 5 , 13*row + 3 , text=str(c), anchor='nw', font=self.candidatesFont, fill=candidateFill)
                        if c in self.cell.Candidates and self.cell.Changed and c not in self.cell.NewCandidates:
                            self.create_text( 14*col + 5 , 13*row + 3 , text=str(c), anchor='nw', font=self.candidatesFont, fill='#FF0000')