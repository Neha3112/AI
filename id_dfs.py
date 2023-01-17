import itertools
import random
import time

def id_dfs(puzzle, goal, get_moves):
    def idfs(path, depth):
        
        if depth == 0:
            return
        
        if path[-1] == goal:
            return path
        
        for move in get_moves(path[-1]):
            
            if move not in path:
                next_path = idfs(path + [move], depth - 1)
                if next_path:
                    return next_path
    
    
    for depth in itertools.count():
        path = idfs([puzzle], depth)
        if path:
            return path
            
def num_matrix(rows, cols, steps=25):
    
    # nums = list(range(1, rows * cols)) + [0]
    # goal = [ nums[i:i+rows] for i in range(0, len(nums), rows) ]
    nums = [[1, 2, 3],[5, 6, 0],[7, 8, 4]]
    goal = [[1, 2, 3],[5, 8, 6],[0, 7, 4]]
    get_moves = num_moves(rows, cols)
    puzzle = goal
    
    for steps in range(steps):
        puzzle = random.choice(get_moves(puzzle))

    return nums, goal
    
def num_moves(rows, cols):
    def get_moves(subject):
        moves = []

        zrow, zcol = next((r, c)
            for r, l in enumerate(subject)
                for c, v in enumerate(l) if v == 0)

        def swap(row, col):
            import copy
            s = copy.deepcopy(subject)
            s[zrow][zcol], s[row][col] = s[row][col], s[zrow][zcol]
            return s

        
        if zrow > 0:
            moves.append(swap(zrow - 1, zcol))
        
        if zcol < cols - 1:
            moves.append(swap(zrow, zcol + 1))
        
        if zrow < rows - 1:
            moves.append(swap(zrow + 1, zcol))
        
        if zcol > 0:
            moves.append(swap(zrow, zcol - 1))

        return moves
    return get_moves
        
if __name__ == '__main__':
    reps = 25
    print('Average solution times: ')
    total_time = 0
    puzzle, goal = num_matrix(3, 3)
    print("\nStart state : ")
    for i in puzzle:
        print(i)
    print("\nGoal state : ")
    for i in goal:
        print(i)
    t0 = time.time()
    solution = id_dfs(puzzle, goal, num_moves(3, 3))
    t1 = time.time()
    print("\nBoard after each move")
    for i in solution:
        print("")
        print("  | ")
        print("  | ")
        print(" \\\'/ \n")
        for j in i:
            print(j)
    print("Number of moves :",len(solution)-1)
    total_time += t1 - t0
    print('Puzzle solved using iterative depth first search in', total_time, 'seconds.') 
    
    
    