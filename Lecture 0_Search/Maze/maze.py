import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action 


class StackFrontier():

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze():

    def __init__(self, filename):

        with open(filename) as f:
            contents = f.read()
        
        # Validation
        if contents.count("A") != 1:
            raise Exception("Maze must have one start.")
        if contents.count("B") != 1:
            raise Exception("Maze must have one goal.")

        # Count height and width
        # .splitlines() make a string into a list
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row =[]
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

        
    def neighbours(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Looping until solution found
        while True:

            # Step1: if norhing left in frontier, then no path
            if frontier.empty():
                raise Exception("No solution!")

            # Step2: choose a node from the frontier and remove it
            node = frontier.remove()
            self.num_explored += 1

            # Step3.1: if node is the goal, then we get the solution
            if node.state == self.goal:
                actions = []
                cells = []
                # Backtracking to find the solution with "parent"
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            # Step3.2: if not, make node as explored
            self.explored.add(node.state)

            # Step4: add neighbours to frontier
            for action, state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
    
    
# Make sure the count of input is 2          
if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

# Initial maze
m = Maze(sys.argv[1])
print("Maze:")
m.print()

# Solve
print("Solving:")
m.solve()
m.print()
print("States explored:", m.num_explored)

