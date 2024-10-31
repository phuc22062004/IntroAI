import copy

class Node:
    def __init__(self, agent_pos: tuple[int], prev_state: int = -1, list_id: int = 0,
                 steps: int = 0, weight: int = 0, move_label: str = '') -> None:
        self.agent_pos = agent_pos
        self.prev_state = prev_state    # ID in state list
        self.stones_list_id = list_id
        self.steps = steps
        self.weight = weight
        self.move_label = move_label

    def __repr__(self) -> str:
        return (f'({self.agent_pos}, {self.prev_state}, {self.stones_list_id}, '
                + f'{self.steps}, {self.weight}, \'{self.move_label}\')')

    def __str__(self) -> str:
        return self.__repr__()
    
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
                new_row = []
                for j in range(self.column):

                    if input[i + 1][j] == r'#':
                        new_row.append(True)

                    elif input[i + 1][j] == r'@':
                        new_row.append(False)
                        self.start = (i, j)

                    elif input[i + 1][j] == r'$':
                        new_row.append(False)
                        firstStoneState.append((i, j))
                        currentStone += 1

                    elif input[i + 1][j] == r'.':
                        new_row.append(False)
                        self.switches.append((i, j))

                    elif input[i + 1][j] == r'+':
                        new_row.append(False)
                        self.start = (i, j)
                        self.switches.append((i, j))

                    elif input[i + 1][j] == r'*':
                        new_row.append(False)
                        firstStoneState.append((i, j))
                        currentStone += 1
                        self.switches.append((i, j))

                    else:
                        new_row.append(False)
                    
                isWall.append(new_row)
            
            self.stones_state_list.append(firstStoneState)
            
            return isWall
        
        self.wall_map: list[bool] = create_map(input)

        # Open set appendment should be implemented in the algorithm
        self.open_set: list[Node] = [Node(self.start)]
        self.closed_set: list[Node] = []

    def get_number_of_cells(self) -> int:
        return self.row * self.column
    
    # This function will be removed later if not needed
    def get_neighbors(self, position: tuple[int]):
        # Get all valid directions
        up = (position[0] - 1, position[1]) if position[0] > 0 else None
        down = (position[0] + 1, position[1]) if position[0] < self.row - 1 else None
        left = (position[0], position[1] - 1) if position[1] > 0 else None
        right = (position[0], position[1] + 1) if position[1] < self.column - 1 else None
        directions = [up, right, down, left]

        # Get all coordinates (or None)
        neighbors = []
        for direction in directions:
            neighbors.append(direction)
        
        return neighbors
    
    def isWall(self, position: tuple[int]):
        return self.wall_map[position[0]][position[1]]

    # Check if there is any stone at given position on current state
    def isStone(self, position: tuple[int], node: Node) -> bool:
        return (position in self.stones_state_list[node.stones_list_id])

    def isEmpty(self, position: tuple[int], node: Node) -> bool:
        return (not (self.isStone(position, node) or self.isWall(position)))

    # Check if this stone state is already exists
    def isOldStoneState(self, stones_state: list[tuple[int]]) -> bool:
        for state in self.stones_state_list:
            if stones_state == state:
                return True
        
        return False
    
    def goalReached(self, node: Node):
        for stone in self.stones_state_list[node.stones_list_id]:
            if stone not in self.switches:
                return False
            
        return True
    
    # Check if the agent is moving into loops
    def isLooped(self, curr_agent_pos: tuple[int], stones_state_id: int):
        prev_state_id = len(self.closed_set) - 1
        prev_of_prev_id = self.closed_set[prev_state_id].prev_state

        while prev_of_prev_id > -1:
            prev_of_prev_state = self.closed_set[prev_of_prev_id]
            if (curr_agent_pos == prev_of_prev_state.agent_pos
                and stones_state_id == prev_of_prev_state.stones_list_id):
                return True
            
            prev_state_id = prev_of_prev_state.prev_state
            if prev_state_id == -1:
                break

            prev_of_prev_id = self.closed_set[prev_state_id].prev_state
        
        return False
    
    # Check if 
    def surroundingCheck(self, position: tuple[int]) -> list[bool]:
        neighbor_cells = self.get_neighbors(position)

        neighbor_isWall = []
        for neighbor in neighbor_cells:
            if neighbor is None:
                neighbor_isWall.append(True)
            elif neighbor is not None and self.isWall(neighbor):
                neighbor_isWall.append(True)
            else:
                neighbor_isWall.append(False)
        
        return neighbor_isWall

    # Agent move
    def move_up(self, node: Node):
        if node.agent_pos[0] > 0 and self.isEmpty((node.agent_pos[0] - 1, node.agent_pos[1]), node):
            if self.isLooped((node.agent_pos[0] - 1, node.agent_pos[1]), node.stones_list_id):
                return None

            newState = Node((node.agent_pos[0] - 1, node.agent_pos[1]), len(self.closed_set) - 1,
                            node.stones_list_id, node.steps + 1, node.weight, 'u')
            return newState
        
        return None

    def move_down(self, node: Node):
        if node.agent_pos[0] < self.row - 1 and self.isEmpty((node.agent_pos[0] + 1, node.agent_pos[1]), node):
            if self.isLooped((node.agent_pos[0] + 1, node.agent_pos[1]), node.stones_list_id):
                return None

            newState = Node((node.agent_pos[0] + 1, node.agent_pos[1]), len(self.closed_set) - 1,
                            node.stones_list_id, node.steps + 1, node.weight, 'd')
            return newState
        
        return None

    def move_left(self, node: Node):
        if node.agent_pos[1] > 0 and self.isEmpty((node.agent_pos[0], node.agent_pos[1] - 1), node):
            if self.isLooped((node.agent_pos[0], node.agent_pos[1] - 1), node.stones_list_id):
                return None

            newState = Node((node.agent_pos[0], node.agent_pos[1] - 1), len(self.closed_set) - 1,
                            node.stones_list_id, node.steps + 1, node.weight, 'l')
            return newState
        
        return None

    def move_right(self, node: Node):
        if node.agent_pos[1] < self.column - 1 and self.isEmpty((node.agent_pos[0], node.agent_pos[1] + 1), node):
            if self.isLooped((node.agent_pos[0], node.agent_pos[1] + 1), node.stones_list_id):
                return None

            newState = Node((node.agent_pos[0], node.agent_pos[1] + 1), len(self.closed_set) - 1,
                            node.stones_list_id, node.steps + 1, node.weight, 'r')
            return newState
        
        return None

    # Push stone
    def push_up(self, node: Node):
        new_pos = (node.agent_pos[0] - 1, node.agent_pos[1])

        if new_pos[0] > 0 and self.isStone(new_pos, node):
            # Valid stone
            new_stone_pos = (new_pos[0] - 1, new_pos[1])

            if self.isEmpty(new_stone_pos, node):
                new_stones_state = copy.deepcopy(self.stones_state_list[node.stones_list_id])
                stoneID = new_stones_state.index(new_pos)

                # Add new stone state to the list
                new_stones_state[stoneID] = new_stone_pos
                if self.isOldStoneState(new_stones_state):
                    return None

                self.stones_state_list.append(new_stones_state)

                newState = Node(new_pos, len(self.closed_set) - 1, len(self.stones_state_list) - 1,
                                node.steps + 1, node.weight + self.stone_weights[stoneID], 'U')
                
                return newState
        
        return None

    def push_down(self, node: Node):
        new_pos = (node.agent_pos[0] + 1, node.agent_pos[1])

        if new_pos[0] < self.row - 1 and self.isStone(new_pos, node):
            # Valid stone
            new_stone_pos = (new_pos[0] + 1, new_pos[1])

            if self.isEmpty(new_stone_pos, node):
                new_stones_state = copy.deepcopy(self.stones_state_list[node.stones_list_id])
                stoneID = new_stones_state.index(new_pos)

                # Add new stone state to the list
                new_stones_state[stoneID] = new_stone_pos
                if self.isOldStoneState(new_stones_state):
                    return None
                
                self.stones_state_list.append(new_stones_state)

                newState = Node(new_pos, len(self.closed_set) - 1, len(self.stones_state_list) - 1,
                                node.steps + 1, node.weight + self.stone_weights[stoneID], 'D')
                
                return newState
        
        return None

    def push_left(self, node: Node):
        new_pos = (node.agent_pos[0], node.agent_pos[1] - 1)

        if new_pos[1] > 0 and self.isStone(new_pos, node):
            # Valid stone
            new_stone_pos = (new_pos[0], new_pos[1] - 1)

            if self.isEmpty(new_stone_pos, node):
                new_stones_state = copy.deepcopy(self.stones_state_list[node.stones_list_id])
                stoneID = new_stones_state.index(new_pos)

                # Add new stone state to the list
                new_stones_state[stoneID] = new_stone_pos
                if self.isOldStoneState(new_stones_state):
                    return None
                
                self.stones_state_list.append(new_stones_state)

                newState = Node(new_pos, len(self.closed_set) - 1, len(self.stones_state_list) - 1,
                                node.steps + 1, node.weight + self.stone_weights[stoneID], 'L')
                
                return newState
        
        return None

    def push_right(self, node: Node):
        new_pos = (node.agent_pos[0], node.agent_pos[1] + 1)

        if new_pos[1] < self.column - 1 and self.isStone(new_pos, node):
            # Valid stone
            new_stone_pos = (new_pos[0], new_pos[1] + 1)

            if self.isEmpty(new_stone_pos, node):
                new_stones_state = copy.deepcopy(self.stones_state_list[node.stones_list_id])
                stoneID = new_stones_state.index(new_pos)

                # Add new stone state to the list
                new_stones_state[stoneID] = new_stone_pos
                if self.isOldStoneState(new_stones_state):
                    return None
                
                self.stones_state_list.append(new_stones_state)

                newState = Node(new_pos, len(self.closed_set) - 1, len(self.stones_state_list) - 1,
                                node.steps + 1, node.weight + self.stone_weights[stoneID], 'R')
                
                return newState
        
        return None
    
    def nodeExpansion(self, node: Node) -> list[Node]:
        # Add current node to closed set
        self.closed_set.append(node)

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
    
    def path_construction(self, goal: Node) -> str:
        path_instruction = goal.move_label
        prev_node_id = goal.prev_state

        while prev_node_id > -1:
            prev_node = self.closed_set[prev_node_id]
            path_instruction = prev_node.move_label + path_instruction
            prev_node_id = prev_node.prev_state
        
        return path_instruction