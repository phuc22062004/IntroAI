from maze import *
import time
import tracemalloc

def BFS(game: SearchSpace) -> str:
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = 1
    goal = None
    nodes_created = 1

    while open_set_capacity > 0:
        new_nodes_count = game.nodeExpansion(game.open_set[0])
        nodes_created += new_nodes_count

        open_set_capacity += new_nodes_count - 1

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break

    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)
    if goal is None:
        return f'''Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
No solution!'''
    return f'''Steps: {goal.steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{game.path_construction()}'''

def UCS(game: SearchSpace) -> str:
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = 1
    goal = None
    nodes_created = 1

    while open_set_capacity > 0:
        new_nodes_count = game.nodeExpansion(min(game.open_set, key = lambda x: x.steps + x.weight))
        nodes_created += new_nodes_count

        open_set_capacity += new_nodes_count - 1

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break
    
    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)
    if goal is None:
        return f'''Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
No solution!'''
    return f'''Steps: {goal.steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{game.path_construction()}'''
