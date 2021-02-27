from BaseAI import BaseAI


# AI that will play 2048
class PlayerAI(BaseAI):
    def getMove(self, grid):
        # take the current grid and expand it four moves ahead
        game = Grid_Tree(grid)
        game.expand()
        game.expand()
        game.expand()

        # get the best move from the tree
        return game.get_best_move()


# keeps track of all boards checked and their score
class Grid_Tree(object):
    def __init__(self, grid):
        self.root = Tree_Node(grid)
        self.dirs = [1, 3, 2, 0]
        self.fringe = []
        self.best_node = None
        self.best_score = 0

        nodes = self.root.expand()
        for n in nodes:
            n.evaluate()
            self.fringe.append(n)

    # plays 1 computer move and then all player moves
    def expand(self):
        self.computer_move()
        self.player_move()

    # returns the best move, the AI wants the highest tile in the lower right corner
    # so it will prioritize moving down or right and avoid moving up of left unless it is safe to do so
    def get_best_move(self):
        node = self.best_node
        if node:
            while node.get_parent() != self.root:
                node = node.get_parent()
            return node.get_move()
        else:
            root_grid = self.root.get_grid()
            moves = root_grid.getAvailableMoves()
            if 1 in moves:
                return 1
            elif 3 in moves:
                return 3
            elif 2 in moves:
                return 2
            else:
                return 0

    # plays all possible moves and keeps track of node with the best score
    def player_move(self):
        for i in range(len(self.fringe)):
            node = self.fringe.pop(0)
            added_nodes = node.expand()
            for n in added_nodes:
                self.fringe.append(n)
                score = n.get_score()
                if score > self.best_score:
                    self.best_node = n
                    self.best_score = score
        if self.best_score == 0:
            print("WE GOT A 0!!!!")

    # plays a computer move
    # computer will place the new block in the most disadvantageous spot possible
    # i.e. as close to the lower right corner as possible
    def computer_move(self):
        for i in range(len(self.fringe)):
            node = self.fringe.pop(0)
            added_node = node.computer_placement()
            self.fringe.append(added_node)


# tree to keep track of the different board configs and their scores
class Tree_Node(object):
    def __init__(self, grid):
        self.parent = None
        self.children = [None, None, None, None]
        self.grid = grid
        self.dirs = [1, 3, 2, 0]
        self.move = None
        self.score = None
        self.leaf = False

    def set_move(self, m):
        self.move = m

    def set_parent(self, p):
        self.parent = p

    def set_score(self, s):
        self.score = s

    def set_leaf(self, bool):
        self.leaf = bool

    def get_parent(self):
        return self.parent

    def get_grid(self):
        return self.grid

    def get_move(self):
        return self.move

    def get_score(self):
        return self.score

    # plays every possible move given the current node
    # returns all nodes added to the tree
    def expand(self):
        added_nodes = []
        if self.leaf == False:
            for x in self.dirs:
                clone = self.grid.clone()
                if clone.move(x):
                    child = Tree_Node(clone)
                    self.children[x] = child
                    child.set_move(x)
                    child.set_parent(self)
                    child.evaluate()
                    added_nodes.append(child)

        return added_nodes

    # finds all empty tiles and returns their location in the game board
    def zeros(self, grid):
        if grid.getCellValue([3, 3]) * grid.getCellValue([2, 3]) * grid.getCellValue([3, 2]) * grid.getCellValue(
                [2, 2]) == 0:
            return True
        else:
            return False

    # returns the score of the board
    # scores are calculate by multiplying the value of a tile by the multiplier of that specific tile
    # multipliers are highest in the lower right corner
    # multipliers are lowest in the upper left corner
    def evaluate(self):
        score = 0
        if self.grid.getMaxTile() > 32 and self.zeros(self.grid):
            score = 0
            self.leaf = True
        elif self.parent.get_score == 0:
            score = 0
            self.leaf = True
        else:
            for x in range(4):
                multiplier = x + 1
                for y in range(4):
                    score += 4 ** (multiplier + y) * self.grid.getCellValue([x, y])
        self.score = score

    # computer turn places a 2 or 4 in an empty tile
    # it will prioritize the worst possible scenario: as close to the bottom right corner as possible
    def computer_placement(self):
        options = self.grid.getAvailableCells()
        best_value = 0
        best_position = None
        for o in options:
            value = o[0] + o[1] + 1
            if value > best_value:
                best_position = o
                best_value = value

        new_grid = self.grid.clone()
        new_grid.insertTile(best_position, 2)
        node = Tree_Node(new_grid)
        node.set_parent(self)
        if self.score == 0:
            node.set_score(0)
            node.set_leaf(True)
        self.children = [node]
        return node