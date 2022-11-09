from pyamaze import agent, maze

class Robot(agent):

    def look(self, direction):
        while (direction != self._orient):
            self._RCW()
    
    def turnLeft(self):
        direction = (self._orient - 1)%4
        self.look(direction)
    
    def turnBack(self):
        self.turnLeft()
        self.turnLeft()

    def turnRight(self):
        self.turnBack()
        self.turnLeft()

    def forward(self):
        if self.blocked:
            raise Exception("Can't drive into a wall")
        [
            self.moveUp,
            self.moveRight,
            self.moveDown,
            self.moveLeft
        ][self._orient](None)

    @property
    def walls(self):
        return self._parentMaze.maze_map[self.position]
    
    @property
    def blocked(self):
        facing = ["N", "E", "S", "W"][self._orient]
        return self.walls[facing] == 0
    
    def navigate(self):
        self.turnLeft()
        while self.blocked: self.turnRight()
        self.forward()

    def escape(self):
        path = [self.position]
        while self.position != (1, 1):
            self.navigate()
            path.append(self.position)
        return path

def main():

    # Create maze and robot
    m = maze(20, 20)
    m.CreateMaze(loadMaze="20x20.csv")
    r = Robot(m, shape="arrow")

    # Find the path out of the maze
    start = r.position
    p = r.escape()
    r.position = start

    # Show the path out of the maze
    r.footprints = True
    m.tracePath({ r: p }, delay=20)
    m.run()

if __name__ == "__main__": main()