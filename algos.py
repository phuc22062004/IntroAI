from maze import *
import time
import tracemalloc

def DFS(game: SearchSpace):
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = 1
    goal = None
    nodes_created = 1

    while open_set_capacity > 0:
        new_nodes = game.nodeExpansion(game.open_set[0])
        new_nodes_count = len(new_nodes)
        nodes_created += new_nodes_count

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break

        game.open_set = new_nodes + game.open_set
        open_set_capacity += new_nodes_count - 1

    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)

    path = game.path_construction()
    game.reset()
    if goal is None:
        return (f'''Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
No solution!''', '')
    return (f'''Steps: {goal.steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{path}''', path)

def BFS(game: SearchSpace):
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = 1
    goal = None
    nodes_created = 1

    while open_set_capacity > 0:
        new_nodes = game.nodeExpansion(game.open_set[0])
        new_nodes_count = len(new_nodes)
        nodes_created += new_nodes_count

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break

        game.open_set += new_nodes
        open_set_capacity += new_nodes_count - 1

    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)

    path = game.path_construction()
    game.reset()
    if goal is None:
        return (f'''Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
No solution!''', '')
    return (f'''Steps: {goal.steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{path}''', path)

def UCS(game: SearchSpace):
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = 1
    goal = None
    nodes_created = 1

    while open_set_capacity > 0:
        new_nodes = game.nodeExpansion(min(game.open_set, key = lambda x: x.cost()))
        new_nodes_count = len(new_nodes)
        nodes_created += new_nodes_count

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break

        game.open_set += new_nodes
        open_set_capacity += new_nodes_count - 1
    
    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)

    path = game.path_construction()
    game.reset()
    if goal is None:
        return (f'''Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
No solution!''', '')
    return (f'''Steps: {goal.steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{path}''', path)

def AStar(game: SearchSpace):
    def heuristic(node: Node) -> int:
        agent_pos = node.agent_pos
        stones_state = game.stonesState(node)
        stone_count = len(stones_state)
        agent_to_stone = agent_stone_distance(agent_pos, stones_state)
        np_stones_state = np.array(stones_state).reshape(stone_count, 1, -1)
        np_switches = np.array(game.switches)
        stone_to_switches = np.sum(np.abs(np_stones_state - np_switches), axis = -1)
        np_stone_weights = np.array(game.stone_weights)

        total = 0
        for _ in range(stone_count):
            max_stone_weight_id = np.argmax(np_stone_weights)
            closest_switch_id = np.argmin(stone_to_switches[max_stone_weight_id])
            total += (stone_to_switches[max_stone_weight_id, closest_switch_id] * np_stone_weights[max_stone_weight_id]
                      + agent_to_stone[max_stone_weight_id]) * int(stones_state[max_stone_weight_id] not in game.switches)

            np_stone_weights[max_stone_weight_id] = np.min(np_stone_weights - 1)
            stone_to_switches[:,closest_switch_id] = np.max(stone_to_switches + 1, axis = 1)

        return total
    
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = 1
    goal = None
    nodes_created = 1

    while open_set_capacity > 0:
        new_nodes = game.nodeExpansion(min(game.open_set, key = lambda x: x.cost() + heuristic(x)))
        new_nodes_count = len(new_nodes)
        nodes_created += new_nodes_count

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break

        game.open_set += new_nodes
        open_set_capacity += new_nodes_count - 1
    
    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)

    path = game.path_construction()
    game.reset()
    if goal is None:
        return (f'''Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
No solution!''', '')
    return (f'''Steps: {goal.steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{path}''', path)
