from maze import *
import time
import tracemalloc
import numpy as np

def BFS(game: SearchSpace) -> str:
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = len(game.open_set)
    goal = None
    nodes_created = len(game.open_set)

    # def agent_stone_distance(node: Node):
    #     stone_pos = np.array(game.stones_state_list[node.stones_list_id])
    #     agent_stone_diff = stone_pos - np.array(node.agent_pos)
    #     Manhattan_dist = np.sum(np.abs(agent_stone_diff), axis = -1)
    #     return Manhattan_dist

    # def remove_redundant_moves(node_set: list[Node]) -> list[Node]:
    #     agent_stone_dist_curr = agent_stone_distance(game.closed_set[-1])

    #     # Check if agent is moving further from all stones
    #     # Remove moves that are not stone pushing
    #     for node in node_set:
    #         neighbor_cells = game.get_neighbors(node.agent_pos)
            
    #         surrounding_isEmpty = True
    #         for neighbor in neighbor_cells:
    #             for surrounding in game.surroundingCheck(neighbor):
    #                 surrounding_isEmpty = surrounding_isEmpty and surrounding

    #         agent_stone_dist_new = agent_stone_distance(node)
    #         if surrounding_isEmpty and np.all(agent_stone_dist_curr + 1 < agent_stone_dist_new):
    #             node_set.remove(node)

    #     return node_set

    while open_set_capacity > 0:
        new_nodes = game.nodeExpansion(game.open_set[0])
        nodes_created += len(new_nodes)
        
        # Remove redundant moves
        # new_nodes = remove_redundant_moves(new_nodes)

        game.open_set += new_nodes

        open_set_capacity = len(game.open_set)

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break
    
    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)
    return f'''Steps: {goal.steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{game.path_construction(goal)}'''

def UCS(game: SearchSpace) -> str:
    start_time = time.time()
    tracemalloc.start()
    open_set_capacity = len(game.open_set)
    goal = None
    nodes_created = len(game.open_set)

    def agent_stone_distance(node: Node):
        stone_pos = np.array(game.stones_state_list[node.stones_list_id])
        agent_stone_diff = stone_pos - np.array(node.agent_pos)
        Manhattan_dist = np.sum(np.abs(agent_stone_diff), axis = -1)
        return Manhattan_dist

    def remove_redundant_moves(node_set: list[Node]) -> list[Node]:
        agent_stone_dist_curr = agent_stone_distance(game.closed_set[-1])

        # Check if agent is moving further from all stones
        # Remove moves that are not stone pushing
        for node in node_set:
            neighbor_cells = game.get_neighbors(node.agent_pos)
            
            surrounding_isEmpty = True
            for neighbor in neighbor_cells:
                for surrounding in game.surroundingCheck(neighbor):
                    surrounding_isEmpty = surrounding_isEmpty and surrounding

            agent_stone_dist_new = agent_stone_distance(node)
            if surrounding_isEmpty and np.all(agent_stone_dist_curr + 1 < agent_stone_dist_new):
                node_set.remove(node)

        return node_set

    while open_set_capacity > 0:
        new_nodes = game.nodeExpansion(game.open_set[0])
        nodes_created += len(new_nodes)
        
        # Remove redundant moves
        new_nodes = remove_redundant_moves(new_nodes)

        game.open_set += new_nodes
        game.open_set = sorted(game.open_set, key = lambda node: node.steps + node.weight)

        open_set_capacity = len(game.open_set)

        if game.goalReached(game.closed_set[-1]):
            goal = game.closed_set[-1]
            break
    
    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)
    return f'''Steps: {goal.steps}, Weight: {goal.weight}, Node: {nodes_created}, Time (ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
{game.path_construction(goal)}'''

input_test = 'input.txt'
input_map = open(input_test, 'r', encoding = 'utf-8').read().strip().split('\n')
new_game = SearchSpace(input_map)
output = BFS(new_game)
print(output)

# Output conversion !?
moves = output.split('\n')[1]
moves = moves.replace('L', 'Left ').replace('l', 'Left ')
moves = moves.replace('U', 'Up ').replace('u', 'Up ')
moves = moves.replace('R', 'Right ').replace('r', 'Right ')
moves = moves.replace('D', 'Down ').replace('d', 'Down ')
moves = moves.strip().split(' ')
print(moves)