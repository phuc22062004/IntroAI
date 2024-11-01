from heapq import heappop, heappush
from utils import goal_reached, get_valid_moves
import time
import utils
import time
import tracemalloc
import sys


sys.setrecursionlimit(999999)

def calculateHeuristic(stones, goal_positions):
    distance = 0
    stone_positions = sorted(stones.keys())
    goal_positions = sorted(goal_positions)
    for stone_pos, goal_pos in zip(stone_positions, goal_positions):
        distance += abs(stone_pos[0] - goal_pos[0]) + abs(stone_pos[1] - goal_pos[1])    
    return distance

def A_star(maze, start, goal_positions, stones):
    start_time = time.time()
    tracemalloc.start()
    priority_queue = [(0, 0, start, frozenset(stones.items()), [])]
    visited = set()
    numNodes = 1 
    while priority_queue:
        total_cost, g, current_pos, current_stones, path = heappop(priority_queue)

        if goal_reached(dict(current_stones), goal_positions):
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000 
            memory_peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            peak_in_MB = memory_peak / (1024 ** 2)
            return ''.join(path),total_cost, numNodes, execution_time,peak_in_MB

        state = (current_pos, current_stones)
        if state in visited:
            continue
        visited.add(state)

        for next_pos, next_stones, move in get_valid_moves(current_pos, dict(current_stones), maze):
            stone_weight = stones.get(next_pos, 1)
            new_path = path + [move]
            new_g = g + stone_weight
            numNodes+=1
            heuristic_cost = calculateHeuristic(dict(next_stones), goal_positions)
            total_cost = new_g + heuristic_cost

            heappush(priority_queue, (total_cost, new_g, next_pos, frozenset(next_stones.items()), new_path))

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    memory_peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    peak_in_MB = memory_peak / (1024 ** 2)
    return None, total_cost, numNodes, execution_time,peak_in_MB


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
    if Lo_Trinh != None:
        return Lo_Trinh,duration,memory_peak,weight,numNode
    return None,duration, memory_peak, weight,numNode