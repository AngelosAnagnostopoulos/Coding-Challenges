# Implementation of Cellular Automata project "Game of Life" in Python 3.x

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
        self.state = 0 
        self.rows = rows
        self.cols = cols
        self.play = False 
        self.makeArray()
        self.graphicsSetup()
        self.drawArray()

    def graphicsSetup(self):
        
        self.window = tk.Tk()
        self.res = 20
        self.width = self.cols * self.res + 100
        self.height = self.rows * self.res
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.title("Game of Life")
        self.window.resizable(0,0)
        self.canvas = tk.Canvas(self.window, width = self.width, height = self.height)
        self.button = tk.Button(self.window, text = "Start/Stop", command=self.buttonFunc)
        self.button.place(x=805,y=400)
        self.canvas.bind("<Button-1>",self.callback)
        self.canvas.pack()
        
    def start_loop(self):    
        self.window.mainloop()

    def drawArray(self):
        print(self.state)
        self.state += 1
        arr = self.grid
        for i in range(self.cols):
            for j in range(self.rows):
                x = i*self.res
                y = j*self.res
                if (arr[i][j] == 1):
                    self.canvas.create_rectangle(x,y,x+self.res-1,y+self.res-1, fill="black")
                else:
                    self.canvas.create_rectangle(x,y,x+self.res-1,y+self.res-1, fill="white")
        self.state -= 1

    def callback(self,event):
        x = event.x
        y = event.y
        ind_x = x // self.res
        ind_y = y // self.res
        self.toggle(ind_x,ind_y)
        self.drawArray()

    def makeArray(self):
        self.grid = [[random.randint(0,0) for i in range(self.cols)] for j in range(self.rows)]

    def nextState(self):

        self.next = copy.deepcopy(self.grid)
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
        del self.next

    def toggle(self,i,j):
        if self.grid[i][j] == 0:
            self.grid[i][j] = 1
        elif self.grid[i][j] == 1:
            self.grid[i][j] = 0

    def buttonFunc(self):
        self.play = not self.play      
        self.run()

    def run(self):
        if self.play:
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
        self.start_loop()
       

if __name__ == "__main__":
    game = GameOfLife(40, 40)
    game.main()
