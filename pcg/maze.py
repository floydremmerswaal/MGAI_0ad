import random as rnd
from colorama import init
from colorama import Fore, Back, Style

class Maze:
    def __init__(self, height=10, width=10):
        self.height = height
        self.width = width

        self.cell = 'C'
        self.wall = 'W'
        self.unvisited = 'U'
        self.exit = 'E'

        self.maze = self.init_maze()

    def init_maze(self):
        return [[self.unvisited for _ in range(self.width)] for _ in range(self.height)]

    def print_maze(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == self.unvisited):
                    print(Fore.WHITE + str(self.maze[i][j]), end=" ")
                elif (self.maze[i][j] == self.cell):
                    print(Fore.GREEN + str(self.maze[i][j]), end=" ")
                elif (self.maze[i][j] == self.exit):
                    print(Fore.BLUE + str(self.maze[i][j]), end=" ")
                else:
                    print(Fore.RED + str(self.maze[i][j]), end=" ")
            print('\n')

    def surrounding_cells(self, rnd_wall):
        cells = 0
        if self.maze[rnd_wall[0]-1][rnd_wall[1]] == self.cell:
            cells += 1
        if self.maze[rnd_wall[0]+1][rnd_wall[1]] == self.cell:
            cells += 1
        if self.maze[rnd_wall[0]][rnd_wall[1]-1] == self.cell:
            cells +=1
        if self.maze[rnd_wall[0]][rnd_wall[1]+1] == self.cell:
            cells += 1

        return cells

    def generate(self):
        starting_height = int(rnd.random()*self.height)
        starting_width = int(rnd.random()*self.width)
        
        if (starting_height == 0):
            starting_height += 1
        if (starting_height == self.height-1):
            starting_height -= 1
        if (starting_width == 0):
            starting_width += 1
        if (starting_width == self.width-1):
            starting_width -= 1

        self.maze[starting_height][starting_width] = self.cell

        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height + 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])

        self.maze[starting_height - 1][starting_width] = self.wall
        self.maze[starting_height + 1][starting_width] = self.wall
        self.maze[starting_height][starting_width - 1] = self.wall
        self.maze[starting_height][starting_width + 1] = self.wall

        while walls:
            rnd_wall = rnd.choice(walls)

            if rnd_wall[1] != 0:
                if self.maze[rnd_wall[0]][rnd_wall[1] - 1] == self.unvisited and self.maze[rnd_wall[0]][rnd_wall[1] + 1] == self.cell:
                    surrounding_cells = self.surrounding_cells(rnd_wall)

                    if surrounding_cells < 2:
                        self.maze[rnd_wall[0]][rnd_wall[1]] = self.cell

                        if rnd_wall[0] != 0:
                            if self.maze[rnd_wall[0] - 1][rnd_wall[1]] != self.cell:
                                self.maze[rnd_wall[0] - 1][rnd_wall[1]] = self.wall
                            if [rnd_wall[0] - 1, rnd_wall[1]] not in walls:
                                walls.append([rnd_wall[0] - 1, rnd_wall[1]])

                        if rnd_wall[0] != self.height - 1:
                            if self.maze[rnd_wall[0] + 1][rnd_wall[1]] != self.cell:
                                self.maze[rnd_wall[0] + 1][rnd_wall[1]] = self.wall
                            if [rnd_wall[0] + 1, rnd_wall[1]] not in walls:
                                walls.append([rnd_wall[0] + 1, rnd_wall[1]])

                        if rnd_wall[1] != 0:
                            if self.maze[rnd_wall[0]][rnd_wall[1] - 1] != self.cell:
                                self.maze[rnd_wall[0]][rnd_wall[1] - 1] = self.wall
                            if [rnd_wall[0], rnd_wall[1] - 1] not in walls:
                                walls.append([rnd_wall[0], rnd_wall[1] - 1])

                    for wall in walls:
                        if wall[0] == rnd_wall[0] and wall[1] == rnd_wall[1]:
                            walls.remove(wall)
                    continue

            if rnd_wall[0] != 0:
                if self.maze[rnd_wall[0] - 1][rnd_wall[1]] == self.unvisited and self.maze[rnd_wall[0] + 1][rnd_wall[1]] == self.cell:
                    surrounding_cells = self.surrounding_cells(rnd_wall)

                    if surrounding_cells < 2:
                        self.maze[rnd_wall[0]][rnd_wall[1]] = self.cell

                        if rnd_wall[0] != 0:
                            if self.maze[rnd_wall[0]-1][rnd_wall[1]] != self.cell:
                                self.maze[rnd_wall[0]-1][rnd_wall[1]] = self.wall
                            if ([rnd_wall[0]-1, rnd_wall[1]] not in walls):
                                walls.append([rnd_wall[0]-1, rnd_wall[1]])

                        if (rnd_wall[1] != 0):
                            if (self.maze[rnd_wall[0]][rnd_wall[1]-1] != self.cell):
                                self.maze[rnd_wall[0]][rnd_wall[1]-1] = self.wall
                            if ([rnd_wall[0], rnd_wall[1]-1] not in walls):
                                walls.append([rnd_wall[0], rnd_wall[1]-1])

                        if (rnd_wall[1] != self.width - 1):
                            if (self.maze[rnd_wall[0]][rnd_wall[1]+1] != self.cell):
                                self.maze[rnd_wall[0]][rnd_wall[1]+1] = self.wall
                            if ([rnd_wall[0], rnd_wall[1]+1] not in walls):
                                walls.append([rnd_wall[0], rnd_wall[1]+1])

                    for wall in walls:
                        if (wall[0] == rnd_wall[0] and wall[1] == rnd_wall[1]):
                            walls.remove(wall)

                    continue

            if (rnd_wall[0] != self.height-1):
                if (self.maze[rnd_wall[0]+1][rnd_wall[1]] == self.unvisited and self.maze[rnd_wall[0]-1][rnd_wall[1]] == self.cell):

                    surrounding_cells = self.surrounding_cells(rnd_wall)
                    if (surrounding_cells < 2):
                        self.maze[rnd_wall[0]][rnd_wall[1]] = self.cell

                        if (rnd_wall[0] != self.height-1):
                            if (self.maze[rnd_wall[0]+1][rnd_wall[1]] != self.cell):
                                self.maze[rnd_wall[0]+1][rnd_wall[1]] = self.wall
                            if ([rnd_wall[0]+1, rnd_wall[1]] not in walls):
                                walls.append([rnd_wall[0]+1, rnd_wall[1]])
                        if (rnd_wall[1] != 0):
                            if (self.maze[rnd_wall[0]][rnd_wall[1]-1] != self.cell):
                                self.maze[rnd_wall[0]][rnd_wall[1]-1] = self.wall
                            if ([rnd_wall[0], rnd_wall[1]-1] not in walls):
                                walls.append([rnd_wall[0], rnd_wall[1]-1])
                        if (rnd_wall[1] != self.width-1):
                            if (self.maze[rnd_wall[0]][rnd_wall[1]+1] != self.cell):
                                self.maze[rnd_wall[0]][rnd_wall[1]+1] = self.wall
                            if ([rnd_wall[0], rnd_wall[1]+1] not in walls):
                                walls.append([rnd_wall[0], rnd_wall[1]+1])

                    for wall in walls:
                        if (wall[0] == rnd_wall[0] and wall[1] == rnd_wall[1]):
                            walls.remove(wall)


                    continue

            if (rnd_wall[1] != self.width-1):
                if (self.maze[rnd_wall[0]][rnd_wall[1]+1] == self.unvisited and self.maze[rnd_wall[0]][rnd_wall[1]-1] == self.cell):

                    surrounding_cells = self.surrounding_cells(rnd_wall)
                    if (surrounding_cells < 2):
                        self.maze[rnd_wall[0]][rnd_wall[1]] = self.cell

                        if (rnd_wall[1] != self.width-1):
                            if (self.maze[rnd_wall[0]][rnd_wall[1]+1] != self.cell):
                                self.maze[rnd_wall[0]][rnd_wall[1]+1] = self.wall
                            if ([rnd_wall[0], rnd_wall[1]+1] not in walls):
                                walls.append([rnd_wall[0], rnd_wall[1]+1])
                        if (rnd_wall[0] != self.height-1):
                            if (self.maze[rnd_wall[0]+1][rnd_wall[1]] != self.cell):
                                self.maze[rnd_wall[0]+1][rnd_wall[1]] = self.wall
                            if ([rnd_wall[0]+1, rnd_wall[1]] not in walls):
                                walls.append([rnd_wall[0]+1, rnd_wall[1]])
                        if (rnd_wall[0] != 0):	
                            if (self.maze[rnd_wall[0]-1][rnd_wall[1]] != self.cell):
                                self.maze[rnd_wall[0]-1][rnd_wall[1]] = self.wall
                            if ([rnd_wall[0]-1, rnd_wall[1]] not in walls):
                                walls.append([rnd_wall[0]-1, rnd_wall[1]])

                    for wall in walls:
                        if (wall[0] == rnd_wall[0] and wall[1] == rnd_wall[1]):
                            walls.remove(wall)

                    continue

            for wall in walls:
                if (wall[0] == rnd_wall[0] and wall[1] == rnd_wall[1]):
                    walls.remove(wall)

        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == self.unvisited):
                    self.maze[i][j] = self.wall

        for i in range(0, self.width):
            if self.maze[1][i] == self.cell:
                self.maze[0][i] = self.exit
                break

        for i in range(self.width - 1, 0, -1):
            if self.maze[self.height-2][i] == self.cell:
                self.maze[self.height-1][i] = self.exit
                break


if __name__ == '__main__':
    init()
    maze = Maze(10, 10)
    maze.generate()
    maze.print_maze()