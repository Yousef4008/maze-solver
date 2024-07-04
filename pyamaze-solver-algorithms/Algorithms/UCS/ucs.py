from pyamaze import maze, agent, COLOR, textLabel
from queue import PriorityQueue

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
    fwdPath = {}
    cell = m._goal
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    return searchPath, aPath, fwdPath

if _name_ == '_main_':
    m = maze(4, 4)
    m.CreateMaze()

    # Set the goal manually when creating the agent
    a_goal = (m.rows, m.cols)
    
    searchPath, aPath, fwdPath = uniform_cost(m)
    a = agent(m, footprints=True, color=COLOR.blue, filled=True)
    b = agent(m, 1, 1, footprints=True, color=COLOR.yellow, filled=True, goal=a_goal)
    c = agent(m, footprints=True, color=COLOR.red)

    m.tracePath({a: searchPath}, delay=300)
    m.tracePath({b: aPath}, delay=300)
    m.tracePath({c: fwdPath}, delay=300)

    l = textLabel(m, 'Uniform Cost Path Length', len(fwdPath) + 1)
    l = textLabel(m, 'Uniform Cost Search Length', len(searchPath))
    m.run()