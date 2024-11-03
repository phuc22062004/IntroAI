from maze import *
import time
import tracemalloc

def BFS(game: SearchSpace) -> str:
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = len(game.open_set)
    goal = None
    nodes_created = len(game.open_set)

    while open_set_capacity > 0:
        new_nodes = game.nodeExpansion(game.open_set[0])
        nodes_created += len(new_nodes)
        game.open_set += new_nodes
        open_set_capacity = len(game.open_set)

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break

    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)
    if goal is None:
        return f'''Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
No solution!''',None
    steps = goal.steps
    return f'''Steps: {steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{game.path_construction()}''',steps

def UCS(game: SearchSpace) -> str:
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = len(game.open_set)
    goal = None
    nodes_created = len(game.open_set)

    while open_set_capacity > 0:
        new_nodes = game.nodeExpansion(game.open_set[0])
        nodes_created += len(new_nodes)

        game.open_set = sorted(game.open_set + new_nodes, key = lambda node: node.steps + node.weight)
        open_set_capacity = len(game.open_set)

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break
    
    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)
    if goal is None:
        return f'''Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
No solution!''',None
    steps = goal.steps
    return f'''Steps: {steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{game.path_construction()}''',steps
