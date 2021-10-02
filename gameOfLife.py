# Implementation of Cellular Automata project "Game of Life" in Python 3.x

#Todolist:
#Add button for start/stop functionality
#Add edit capabilities with clicking
#Optimise the code so that it doesn't use two for loops every time

"""
Rules:  Any live cell with <2 live neighbours dies.
        Any live cell with 2 or 3 live neighbours lives to next generation.
        Any live cell with >3 live neighbours dies.
        Any dead cell with exactly 3 live neighbours becomes alive.
"""

import pprint,random,copy
import tkinter as tk


class GameOfLife():


    def __init__(self,rows,cols):
        
        self.rows = rows
        self.cols = cols


    def graphicsSetup(self):
        
        self.window = tk.Tk()
        self.res = 20
        self.width = self.cols * self.res
        self.height = self.rows * self.res
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.title("Game of Life")
        self.window.resizable(0,0)
        self.canvas = tk.Canvas(self.window, width = self.width, height = self.height)
        self.canvas.pack()
        
    def start_loop(self):    
      self.window.mainloop()
        

    def drawArray(self):
        arr = self.grid
        for i in range(self.cols):
            for j in range(self.rows):
                x = i*self.res
                y = j*self.res
                if (arr[i][j] == 1):
                    self.canvas.create_rectangle(x,y,x+self.res-1,y+self.res-1, fill="black")
                else:
                    self.canvas.create_rectangle(x,y,x+self.res-1,y+self.res-1, fill="white")


    def makeArray(self):
        
        self.grid = [[random.randint(0,1) for i in range(self.cols)] for j in range(self.rows)]
        

    def nextState(self):

        self.next = copy.copy(self.grid)
        for i in range(self.cols):
            for j in range(self.rows):
                state = self.grid[i][j]
                neighbors = self.countNeighbors(i,j)
                if (state == 0 and neighbors == 3):
                    self.next[i][j] = 1
                elif (state == 1 and (neighbors == 2 or neighbors == 3)):
                    self.next[i][j] = 1
                else:
                    self.next[i][j] = 0
        self.grid = self.next


    def run(self):
      self.nextState()
      self.drawArray()
      self.window.after(100, self.run)


    def countNeighbors(self,x,y):
    
        thesum = 0
        for i in range(-1,2):
            for j in range(-1,2):
                col = (x+i+self.cols) % self.cols
                row = (y+j+self.rows) % self.rows
                thesum += self.grid[col][row]
        thesum -= self.grid[x][y]
        return thesum
    
    
    def main(self):

        self.makeArray()
        self.graphicsSetup()
        self.run()
        self.start_loop()
       

if __name__ == "__main__":
    game = GameOfLife(40, 40)
    game.main()
