from heapq import heappop, heappush
from utils import goal_reached, get_valid_moves
import time
import utils
import time
import tracemalloc
import sys


sys.setrecursionlimit(999999)



def heuristic(position, stones, goal_positions, heaviest_stone_weight):
    total_dist = 0
    for stone_pos, weight in stones.items():
        distances = [
            abs(stone_pos[0] - goal[0]) + abs(stone_pos[1] - goal[1])
            for goal in goal_positions
        ]
        
        if weight == heaviest_stone_weight:
            dist_to_stone = abs(position[0] - stone_pos[0]) + abs(position[1] - stone_pos[1])
            dist_weighted = min(distances) * weight + dist_to_stone
        else:
            dist_weighted = min(distances)  

        total_dist += dist_weighted
    return total_dist

def A_star(maze, start, goal_positions, stones):
    start_time = time.time()
    tracemalloc.start()
    
    frontier = [(0, start, frozenset(stones.items()), [])]
    visited = set()
    numNodes = 1
    
    while frontier:
        total_cost, current_pos, current_stones, path = heappop(frontier)

        if goal_reached(dict(current_stones), goal_positions):
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            memory_peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            peak_in_MB = memory_peak / (1024 ** 2)
            return ''.join(path), total_cost, numNodes, execution_time, peak_in_MB

        state = (current_pos, current_stones)
        if state in visited:
            continue
        visited.add(state)

        for next_pos, next_stones, move in get_valid_moves(current_pos, dict(current_stones), maze, stones):
            heaviest_stone = max(stones.values())
            stone_weight = stones.get(next_pos, 1)
            new_path = path + [move]
            numNodes += 1
            if move.isupper(): 
                step_cost = stone_weight
            else:  
                step_cost = 1
            
            heuristic_cost = heuristic(current_pos, dict(next_stones), goal_positions, heaviest_stone)
            heappush(frontier, (total_cost + step_cost + heuristic_cost, next_pos, frozenset(next_stones.items()), new_path))

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)
    return None, total_cost, numNodes, execution_time, peak_in_MB


def DFS(map:utils.Maze):
    start_time =time.time()
    tracemalloc.start()
    points_rock = map.find_rock()
    points_switch = map.find_destination()
    tmp = map.create_list_node(points_rock)
    S = utils.Statu_rock(tmp)
    tmp = map.create_list_node(points_switch)
    G = utils.Statu_rock(tmp)
    Open = [S]
    closed = []
    statu_ston,numNode = map.DFS_step_rock(Open,closed)
    tmp = statu_ston
    if statu_ston is None:
        map.reset()
        return None, "không thể đẩy đá"
    statu_ston = statu_ston[::-1]
    map.reset()
    Lo_Trinh, weight = map.find_road(statu_ston)
    duration = (time.time() - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak/ (1024 ** 2)
    if Lo_Trinh != None:
        return f'''Steps: {len(Lo_Trinh)}, Weight: {weight}, Node: {numNode}, Time(ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
        {Lo_Trinh}''', Lo_Trinh
    return f'''Steps: {0}, Weight: {weight}, Node: {numNode}, Time(ms): {duration:.2f}, Memory (MB): {peak_in_MB:.2f}
        {None}''', None