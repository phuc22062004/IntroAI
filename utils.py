def goal_reached(stones, goal_positions):
    for pos in goal_positions:
        if pos not in stones:
            return False
    return True

def is_valid_move(position, stones, maze):
    x, y = position
    if maze[x][y] == "#" or position in stones:
        return False
    return True

def get_valid_moves(position, stones, maze):
    moves = []
    directions = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
    
    for move, (dx, dy) in directions.items():
        next_pos = (position[0] + dx, position[1] + dy)

        if is_valid_move(next_pos, stones, maze):
            moves.append((next_pos, stones.copy(), move))  

        if next_pos in stones:
            stone_pos = next_pos
            after_stone_pos = (stone_pos[0] + dx, stone_pos[1] + dy)

            if is_valid_push(stone_pos, after_stone_pos, stones, maze):
                new_stones = stones.copy()
                new_stones[after_stone_pos] = new_stones.pop(stone_pos)
                moves.append((next_pos, new_stones, move))

    return moves

def is_valid_push(stone_pos, after_stone_pos, stones, maze):
    x, y = after_stone_pos
    if maze[x][y] == "#" or after_stone_pos in stones:
        return False
    return True  