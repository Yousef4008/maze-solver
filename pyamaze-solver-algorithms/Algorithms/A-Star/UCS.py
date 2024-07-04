from pyamaze import maze, agent, COLOR, textLabel
from queue import PriorityQueue
import time

def cost(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def uniform_cost(m, start=None):
    if start is None:
        start = (m.rows, m.cols)
    open = PriorityQueue()
    open.put((0, start))
    aPath = {}
    searchPath = [start]
    
    start_time = time.time()  # Start timing
    while not open.empty():
        _, currCell = open.get()
        searchPath.append(currCell)
        if currCell == m._goal:
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])

                new_cost = cost(start, currCell) + 1
                if childCell not in aPath or new_cost < cost(start, aPath[childCell]):
                    aPath[childCell] = currCell
                    open.put((new_cost, childCell))
    end_time = time.time()  # Stop timing
    
    fwdPath = {}
    cell = m._goal
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    
    time_taken = (end_time - start_time) * 1000  # Time taken in milliseconds
    
    return searchPath, aPath, fwdPath, time_taken  # Return the path and the time taken

if __name__=='__main__':
    m = maze()
    m.CreateMaze(loadMaze='astardemo.csv')
    searchPath, aPath, fwdPath, time_taken = uniform_cost(m)  # Capture the time taken
    a_goal = (m.rows, m.cols)

    a = agent(m, footprints=True, color=COLOR.blue, filled=True, goal=a_goal)
    m.tracePath({a:fwdPath})
    l = textLabel(m, 'Uniform Cost Search Path Length', len(fwdPath) + 1)
    
    print("Time taken:", time_taken, "milliseconds")  # Print the time taken
    
    m.run()
