import copy
import numpy as np

class Node:
    def __init__(self, agent_pos: tuple[int], prev_state: int = -1, stone_id: int = 0,
                 steps: int = 0, weight: int = 0, move_label: str = '') -> None:
        self.agent_pos = agent_pos
        self.prev_state = prev_state    # ID in state list
        self.stones_stone_id = stone_id
        self.steps = steps
        self.weight = weight
        self.move_label = move_label

    def cost(self):
        return self.steps + self.weight

    def __repr__(self) -> str:
        return (f'({self.agent_pos}, {self.prev_state}, {self.stones_stone_id}, '
                + f'{self.steps}, {self.weight}, \'{self.move_label}\')')

    def __str__(self) -> str:
        return self.__repr__()
    
    def __lt__(self, other):
        return self.prev_state < other.prev_state
    
def agent_stone_distance(agent_pos: tuple[int], stones_state: list[tuple[int]]):
    np_stones_state = np.array(stones_state)
    agent_stone_diff = np_stones_state - np.array(agent_pos)
    Manhattan_dist = np.sum(np.abs(agent_stone_diff), axis = -1)
    return Manhattan_dist

def write_output(output_file,data):
    with open(output_file,"a",encoding="utf-8") as file:
        file.write(data)
    
class SearchSpace:
    def __init__(self, input: list[str]) -> None:
        # Extract stones' weight
        self.stone_weights: list[int] = [int(x) for x in input[0].split(' ')]
        self.stones_state_list: list[tuple[int]] = []

        self.row: int = len(input) - 1
        self.column: int = len(input[1])

        self.start: tuple[int] = None
        self.switches: list[tuple[int]] = []

        def create_map(input: list[str]) -> list[bool]:
            isWall: list[bool] = []
            currentStone = 0
            firstStoneState = []

            for i in range(self.row):
                new_row = [input[i + 1][j] in r'#' for j in range(self.column)]
                for j in range(self.column):

                    if input[i + 1][j] == r'@':
                        self.start = (i, j)

                    elif input[i + 1][j] == r'$':
                        firstStoneState.append((i, j))
                        currentStone += 1

                    elif input[i + 1][j] == r'.':
                        self.switches.append((i, j))

                    elif input[i + 1][j] == r'+':
                        self.start = (i, j)
                        self.switches.append((i, j))

                    elif input[i + 1][j] == r'*':
                        firstStoneState.append((i, j))
                        currentStone += 1
                        self.switches.append((i, j))
                    
                isWall.append(new_row)
            
            self.stones_state_list.append(firstStoneState)
            
            return isWall
        
        self.wall_map: list[bool] = create_map(input)

        # Open set appendment should be implemented in the algorithm
        self.open_set: list[Node] = [Node(self.start)]
        self.closed_set: list[Node] = []

    def get_neighbors(self, position: tuple[int]):
        # Get all valid directions
        up = (position[0] - 1, position[1]) if position[0] > 0 else None
        down = (position[0] + 1, position[1]) if position[0] < self.row - 1 else None
        left = (position[0], position[1] - 1) if position[1] > 0 else None
        right = (position[0], position[1] + 1) if position[1] < self.column - 1 else None
        
        return [up, right, down, left]
    
    def stonesState(self, node: Node) -> list[tuple[int]]:
        return self.stones_state_list[node.stones_stone_id]
    
    def isWall(self, position: tuple[int]):
        if (position is None or position[0] < 0 or position[1] < 0
            or position[0] >= self.row or position[1] >= self.column):
            return True
        
        return self.wall_map[position[0]][position[1]]

    # Check if there is any stone at given position on current stone state
    def isStone(self, position: tuple[int], stones_state: list[tuple[int]]) -> bool:
        return (position in stones_state)

    def isEmpty(self, position: tuple[int], stones_state: list[tuple[int]]) -> bool:
        return (not (self.isWall(position) or self.isStone(position, stones_state)))

    # Check if this stone state is already exists
    def isOldStoneState(self, stones_state: list[tuple[int]]) -> bool:
        if stones_state in self.stones_state_list:
            return True
        
        return False
    
    def goalReached(self, node: Node):
        stones_state = np.array(stonesState(node))
        stones_flag = np.all(stones_state.reshape(stones_state.shape[0], 1, -1) == np.array(switches), axis = -1)
        return np.all(np.any(stones_flag, axis = -1))
    
    # Check if the agent is moving into loops
    def isLooped(self, curr_agent_pos: tuple[int], stones_state_id: int, prev_of_prev_id: int):
        check_states = set()

        while prev_of_prev_id > -1:
            prev_of_prev_state = self.closed_set[prev_of_prev_id]
            state = (prev_of_prev_state.agent_pos,prev_of_prev_state.stones_stone_id)
            if state in check_states:
                return True
            check_states.add(state)
            prev_of_prev_id = prev_of_prev_state.prev_state
        return False
    
    # Check if there is any stone being pushed "back and forth"
    def stoneInLoop(self, node: Node, stones_state: list[tuple[int]]):
        if self.stonesState(node) == stones_state:
            return False
        check_stone_states = set()
        prev_state = node.prev_state
        
        while prev_state > -1:
            prev_node = self.closed_set[prev_state]
            stone_state_key = tuple(self.stones_state_list[prev_node.stones_stone_id])
            if stone_state_key == tuple(stones_state):
                return True
            check_stone_states.add(stone_state_key)
            prev_state = prev_node.prev_state
            
        return False
    
    # Check if there is any alternative move exists
    def isAlternativeMove(self, curr_agent_pos: tuple[int], stones_state: list[tuple[int]], steps: int, weight: int):
        alter_detected = np.array([(curr_agent_pos == state.agent_pos
                                    and stones_state == self.stonesState(state)) for state in self.closed_set])
        if np.any(alter_detected):
            return True

        alter_detected = np.array([(curr_agent_pos == state.agent_pos and stones_state == self.stonesState(state)
                                    and steps == state.steps and weight == state.weight) for state in self.open_set])
        if np.any(alter_detected):
            return True
        
        return False
    
    # Check for deadlock pattern
    def isDeadlocked(self, stones_state: tuple[int]) -> bool:
        for stone_pos in stones_state:
            if stone_pos in self.switches:
                return False

            stone_neighbors = self.get_neighbors(stone_pos)
            for i in range(4):
                if self.isWall(stone_neighbors[i]) and self.isWall(stone_neighbors[i - 1]):
                    return True

                corner_1 = (stone_neighbors[i - 1][0], stone_neighbors[i][1])
                corner_2 = (stone_neighbors[i][0], stone_neighbors[i - 1][1])
                if not (self.isEmpty(stone_neighbors[i], stones_state) or self.isEmpty(stone_neighbors[i - 1], stones_state)
                        or self.isEmpty(corner_1, stones_state) or self.isEmpty(corner_2, stones_state)):
                    return True

        return False

    
    # Check if the surrounding has any obstacle
    def neighborStatus(self, position: tuple[int], stones_state: list[tuple[int]]) -> list[bool]:
        neighbor_cells = self.get_neighbors(position)
        neighbors_isObstacle = [(neighbor is None or (neighbor is not None
                                 and not self.isEmpty(neighbor, stones_state))) for neighbor in neighbor_cells]
        
        return neighbors_isObstacle
    
    def isRedundant(self, new_agent_pos: tuple[int], prev_node: Node, stones_state: list[tuple[int]]):       
        # Check non-pushing moves
        if (self.isLooped(new_agent_pos, prev_node.stones_stone_id, prev_node.prev_state)
            or self.isAlternativeMove(new_agent_pos, stones_state, prev_node.steps + 1, prev_node.weight)):
            return True
        
        # Check pushing moves
        elif self.stoneInLoop(prev_node, stones_state) or self.isDeadlocked(stones_state):
            return True

        # This is quite awkward, I'm just gonna let the agent move freely by itself
        else:
            # Check if agent is moving further from all stones
            agent_stone_dist_curr = agent_stone_distance(self.closed_set[-1].agent_pos, self.stonesState(prev_node))
            
            surrounding_isEmpty = 1
            for neighbor in self.get_neighbors(new_agent_pos):
                surrounding_isEmpty &= np.all(np.array(self.neighborStatus(neighbor, stones_state)))

            agent_stone_dist_new = agent_stone_distance(new_agent_pos, stones_state)
            if surrounding_isEmpty and np.all(agent_stone_dist_curr + 1 < agent_stone_dist_new):
                return True
        
        return False

    # Agent move
    def move_up(self, node: Node):
        if node.agent_pos[0] > 0 and self.isEmpty((node.agent_pos[0] - 1, node.agent_pos[1]), self.stonesState(node)):
            new_pos = (node.agent_pos[0] - 1, node.agent_pos[1])
            if self.isRedundant(new_pos, node, self.stonesState(node)):
                return None

            newState = Node(new_pos, len(self.closed_set) - 1, node.stones_stone_id,
                            node.steps + 1, node.weight, 'u')
            return newState
        
        return None

    def move_down(self, node: Node):
        if node.agent_pos[0] < self.row - 1 and self.isEmpty((node.agent_pos[0] + 1, node.agent_pos[1]), self.stonesState(node)):
            new_pos = (node.agent_pos[0] + 1, node.agent_pos[1])
            if self.isRedundant(new_pos, node, self.stonesState(node)):
                return None

            newState = Node(new_pos, len(self.closed_set) - 1, node.stones_stone_id,
                            node.steps + 1, node.weight, 'd')
            return newState
        
        return None

    def move_left(self, node: Node):
        if node.agent_pos[1] > 0 and self.isEmpty((node.agent_pos[0], node.agent_pos[1] - 1), self.stonesState(node)):
            new_pos = (node.agent_pos[0], node.agent_pos[1] - 1)
            if self.isRedundant(new_pos, node, self.stonesState(node)):
                return None

            newState = Node(new_pos, len(self.closed_set) - 1, node.stones_stone_id,
                            node.steps + 1, node.weight, 'l')
            return newState
        
        return None

    def move_right(self, node: Node):
        if node.agent_pos[1] < self.column - 1 and self.isEmpty((node.agent_pos[0], node.agent_pos[1] + 1), self.stonesState(node)):
            new_pos = (node.agent_pos[0], node.agent_pos[1] + 1)
            if self.isRedundant(new_pos, node, self.stonesState(node)):
                return None

            newState = Node(new_pos, len(self.closed_set) - 1, node.stones_stone_id,
                            node.steps + 1, node.weight, 'r')
            return newState
        
        return None

    # Push stone
    def push_up(self, node: Node):
        new_pos = (node.agent_pos[0] - 1, node.agent_pos[1])

        if new_pos[0] > 0 and self.isStone(new_pos, self.stonesState(node)):
            # Valid stone
            new_stone_pos = (new_pos[0] - 1, new_pos[1])

            if self.isEmpty(new_stone_pos, self.stonesState(node)):
                new_stones_state = copy.deepcopy(self.stonesState(node))
                stoneID = new_stones_state.index(new_pos)

                # Add new stone state to the list
                new_stones_state[stoneID] = new_stone_pos
                
                if self.isRedundant(new_pos, node, new_stones_state):
                    return None
                if not self.isOldStoneState(new_stones_state):
                    self.stones_state_list.append(new_stones_state)
                    new_stones_state_id = len(self.stones_state_list) - 1
                else:
                    new_stones_state_id = self.stones_state_list.index(new_stones_state)

                newState = Node(new_pos, len(self.closed_set) - 1, new_stones_state_id,
                                node.steps + 1, node.weight + self.stone_weights[stoneID], 'U')
                
                return newState
        
        return None

    def push_down(self, node: Node):
        new_pos = (node.agent_pos[0] + 1, node.agent_pos[1])

        if new_pos[0] < self.row - 1 and self.isStone(new_pos, self.stonesState(node)):
            # Valid stone
            new_stone_pos = (new_pos[0] + 1, new_pos[1])

            if self.isEmpty(new_stone_pos, self.stonesState(node)):
                new_stones_state = copy.deepcopy(self.stonesState(node))
                stoneID = new_stones_state.index(new_pos)

                # Add new stone state to the list
                new_stones_state[stoneID] = new_stone_pos
                
                if self.isRedundant(new_pos, node, new_stones_state):
                    return None
                if not self.isOldStoneState(new_stones_state):
                    self.stones_state_list.append(new_stones_state)
                    new_stones_state_id = len(self.stones_state_list) - 1
                else:
                    new_stones_state_id = self.stones_state_list.index(new_stones_state)

                newState = Node(new_pos, len(self.closed_set) - 1, new_stones_state_id,
                                node.steps + 1, node.weight + self.stone_weights[stoneID], 'D')
                
                return newState
        
        return None

    def push_left(self, node: Node):
        new_pos = (node.agent_pos[0], node.agent_pos[1] - 1)

        if new_pos[1] > 0 and self.isStone(new_pos, self.stonesState(node)):
            # Valid stone
            new_stone_pos = (new_pos[0], new_pos[1] - 1)

            if self.isEmpty(new_stone_pos, self.stonesState(node)):
                new_stones_state = copy.deepcopy(self.stonesState(node))
                stoneID = new_stones_state.index(new_pos)

                # Add new stone state to the list
                new_stones_state[stoneID] = new_stone_pos
                
                if self.isRedundant(new_pos, node, new_stones_state):
                    return None
                if not self.isOldStoneState(new_stones_state):
                    self.stones_state_list.append(new_stones_state)
                    new_stones_state_id = len(self.stones_state_list) - 1
                else:
                    new_stones_state_id = self.stones_state_list.index(new_stones_state)

                newState = Node(new_pos, len(self.closed_set) - 1, new_stones_state_id,
                                node.steps + 1, node.weight + self.stone_weights[stoneID], 'L')
                
                return newState
        
        return None

    def push_right(self, node: Node):
        new_pos = (node.agent_pos[0], node.agent_pos[1] + 1)

        if new_pos[1] < self.column - 1 and self.isStone(new_pos, self.stonesState(node)):
            # Valid stone
            new_stone_pos = (new_pos[0], new_pos[1] + 1)

            if self.isEmpty(new_stone_pos, self.stonesState(node)):
                new_stones_state = copy.deepcopy(self.stonesState(node))

                stoneID = new_stones_state.index(new_pos)

                # Add new stone state to the list
                new_stones_state[stoneID] = new_stone_pos

                if self.isRedundant(new_pos, node, new_stones_state):
                    return None
                if not self.isOldStoneState(new_stones_state):
                    self.stones_state_list.append(new_stones_state)
                    new_stones_state_id = len(self.stones_state_list) - 1
                else:
                    new_stones_state_id = self.stones_state_list.index(new_stones_state)

                newState = Node(new_pos, len(self.closed_set) - 1, new_stones_state_id,
                                node.steps + 1, node.weight + self.stone_weights[stoneID], 'R')
                
                return newState
        
        return None
    
    def nodeExpansion(self, node: Node) -> list[Node]:
        # Add current node to closed set
        self.closed_set.append(node)
        if self.goalReached(self.closed_set[-1]):
            return []

        move_up_node = self.move_up(node)
        move_right_node = self.move_right(node)
        move_down_node = self.move_down(node)
        move_left_node = self.move_left(node)
        push_up_node = self.push_up(node)
        push_right_node = self.push_right(node)
        push_down_node = self.push_down(node)
        push_left_node = self.push_left(node)
        validNodes = []

        if move_up_node is not None:
            validNodes.append(move_up_node)            
        elif push_up_node is not None:
            validNodes.append(push_up_node)           

        if move_right_node is not None:
            validNodes.append(move_right_node)            
        elif push_right_node is not None:
            validNodes.append(push_right_node)            

        if move_down_node is not None:
            validNodes.append(move_down_node)            
        elif push_down_node is not None:
            validNodes.append(push_down_node)            

        if move_left_node is not None:
            validNodes.append(move_left_node)            
        elif push_left_node is not None:
            validNodes.append(push_left_node)          
        
        # Remove current node from open set
        self.open_set.remove(node)
        return validNodes
    
    # Debug test replacement, in case the functions went wrong
    # def path_construction(self, goal: Node) -> str:
    
    def path_construction(self) -> str:
        goal = self.closed_set[-1]
        path_instruction = goal.move_label
        prev_node_id = goal.prev_state

        while prev_node_id > -1:
            prev_node = self.closed_set[prev_node_id]
            path_instruction = prev_node.move_label + path_instruction
            prev_node_id = prev_node.prev_state
        
        return path_instruction

    # Game reset
    def reset(self):
        self.open_set = [self.closed_set[0]]
        self.closed_set = []
        self.stones_state_list = [self.stones_state_list[0]]
