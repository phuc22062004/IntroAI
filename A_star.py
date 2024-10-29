from heapq import heappop, heappush
from utils import goal_reached, get_valid_moves

def heuristic(position, goal_positions):
    return min(abs(position[0] - gx) + abs(position[1] - gy)for gx, gy in goal_positions)

def A_star(maze, start, goal_positions, stones):
    priority_queue = [(0, 0, start, frozenset(stones.items()), [])]  
    visited = set()

    while priority_queue:
        _, g, current_pos, current_stones, path = heappop(priority_queue)

        if goal_reached(dict(current_stones), goal_positions):
            return path

        state = (current_pos, current_stones)  
        if state in visited:
            continue
        visited.add(state)

        for next_pos, next_stones, move in get_valid_moves(current_pos, dict(current_stones), maze):
            new_path = path + [move]
            stone_weight = stones.get(next_pos, 1)
            new_g = g + stone_weight
            h = heuristic(next_pos, goal_positions)
            heappush(priority_queue, (new_g + h, new_g, next_pos, frozenset(next_stones.items()), new_path))

    return None
