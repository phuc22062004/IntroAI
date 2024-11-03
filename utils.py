import copy


def write_output(output_file,data):
    with open(output_file,"w",encoding="utf-8") as file:
        file.write(data)
    

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

def get_valid_moves(position, stones, maze, stone_weights):
    moves = []
    directions = {'u': (-1, 0), 'd': (1, 0), 'l': (0, -1), 'r': (0, 1)}
    for move, (dx, dy) in directions.items():
        next_pos = (position[0] + dx, position[1] + dy)

        if is_valid_move(next_pos, stones, maze):
            moves.append((next_pos, stones.copy(), move.lower()))  

        if next_pos in stones:
            stone_pos = next_pos
            after_stone_pos = (stone_pos[0] + dx, stone_pos[1] + dy)

            if is_valid_push(stone_pos, after_stone_pos, stones, maze):
                new_stones = stones.copy()
                new_stones[after_stone_pos] = new_stones.pop(stone_pos)
                moves.append((next_pos, new_stones, move.upper()))

    return moves


def is_valid_push(stone_pos, after_stone_pos, stones, maze):
    x, y = after_stone_pos
    if maze[x][y] == "#" or after_stone_pos in stones:
        return False
    return True  

class Node:
    def __init__(self, point, parent=None, direction=None, tracking=None):
        self.point = point
        self.parent = parent
        self.direction = direction
        self.tracking = tracking
    def road(self):
        tmp = self
        road = []
        while tmp.parent != None:
            road.append(tmp)
            tmp = tmp.parent
        road = road[::-1]
        return road

class Statu_rock:
    def __init__(self, statu, par=None,ID_rock = None):
        self.statu = statu
        self.par = par
        self.ID_rock = ID_rock
    def get_points(self):
        list_tmp = []
        for i in self.statu:
            list_tmp.append(i.point)
        return list_tmp
    def get_point_move(self):
        if self.ID_rock is None:
            return None
        return self.statu[self.ID_rock]


class Maze:
    def __init__(self,map,ID_rock,count_rock,cac_huong_rock,destination,start,weights):
        self.map = copy.deepcopy(map)
        self.root = copy.deepcopy(map)
        self.weights = weights
        self.start = start
        self.ID_rock = copy.deepcopy(ID_rock)
        self.count_rock = count_rock
        self.cac_huong_rock = cac_huong_rock#lu cac hướng viên đá có thể đi và bật 1 nếu viên đá đã đi hướng đó rồi
        self.destination = destination
        self.player_position = self.find_player_position()
    def reset(self):
        self.map = copy.deepcopy(self.root)
        self.player_position = self.start
    def pointed_u(self,i, j):
        return i-1,j
    def pointed_d(self,i,j):
        return i+1,j
    def pointed_l(self,i,j):
        return i , j-1
    def pointed_r(self ,i, j):
        return i, j + 1
    
    #kiểm tra vị trí đi hướng đó có thể đi được hay không
    def check_map(self, row, col, function_direct, direct):
        new_row, new_col = function_direct(row, col)
        if self.map[new_row][new_col] == "#":
            return None
        if self.map[new_row][new_col] in ("$", "*") :
            rock_new_row, rock_new_col = function_direct(new_row, new_col)
            if self.map[rock_new_row][rock_new_col] in ("$","*"):
                return None
            elif self.map[rock_new_row][rock_new_col] == "#":
                return None
        tracking = {"u": "d", "d": "u", "l": "r", "r": "l"}[direct]
        return [(new_row, new_col), (row, col), direct, tracking]
    
    #lấy ra tập con khả có thể đi được trong một điểm
    def get_subset(self, point):
        row, col = point
        directions = [
            ("u", self.pointed_u),
            ("r", self.pointed_r),
            ("d", self.pointed_d),
            ("l", self.pointed_l)
        ]
        subset = [self.check_map(row, col, func, direction) for direction, func in directions]
        return [item for item in subset if item is not None]
    def is_destination(self):
        # Kiểm tra nếu tất cả điểm đích đều được đá phủ
        return all(self.map[row][col] not in (".", "+") for row, col in self.destination)
    def path(self,O,road):
        road.append(O)
        if O.par != None:
            return self.path(O.par,road)
        else:
            return road
    
    def checkInArray_rock(self, tmp, Open):
        points_temp = tmp.get_points()  # Danh sách các `point` từ `tmp`
        list_tmp = []
        for statu in Open:
            point_rock = statu.get_points()  # Danh sách `point` từ `statu`
            list_tmp.append(point_rock)
        return points_temp in list_tmp  # Kiểm tra nếu `points_temp` nằm trong `list_tmp`
    #kiểm một điểm người chơi dự định đứng có trong mảng không
    def checkInArray_player(self,tmp, Open):
        for x in Open:
            if tmp.point == x.point:
                return True
        return False
    def move_rock_to_point(self,rock_point ,point ):   
        if rock_point == point:
            return True
        row_rock, col_rock = rock_point
        row, col = point
        if self.map[row_rock][col_rock] not in ("$","*"):
            return False
        if self.map[row][col] in ("$","*"):
            return False
        for i in range(self.count_rock):
            if self.ID_rock[i] == (row_rock,col_rock):
                self.ID_rock[i] = point
        if self.map[row_rock][col_rock] == "*":
            self.map[row_rock][col_rock] = "."
        else:
                self.map[row_rock][col_rock] = " "
        node = Node((row_rock,col_rock))
        self.move_player_to(node)
        if self.map[row][col] == ".":
            self.map[row][col] = "*"
        else:
            self.map[row][col] = "$"
        row, col = self.find_player_position()
        if(self.map[row][col] in ("$","*")):
            print("Da de")
        return True
    #hàm get ra tập con của tất cả viên đá(các hướng viên đá có thể đến được trong tương lai)
    def get_subset_rock(self,O):
        rockPointes = self.find_rock()#tìm vị trí đá
        subsetRockes = []
        subset_rock_statu = []
        if O.par is None:
            S = Node(self.start)
        else:
            point_rock = O.get_point_move()
            point = self.get_point_direction(point_rock.point,point_rock.tracking)
            S = Node(point[0])
            if self.move_player_to(S) == False:
                print("khong the di chuyen")
        #tạo ra tập vị trí các cục đá ở vị trí hiện tại
        for rockpoint in rockPointes:
            tmp = Node(rockpoint)
            subset_rock_statu.append(tmp)
        i =  0
        tracking = {"u": "d", "d": "u", "l": "r", "r": "l"}
        for rockPoint in rockPointes:#lấy ra tập vị trí của đá
            subsetRock_ = self.get_subset(rockPoint)#lấy ra các vị trí của vi đá có thể đi
            subsetRock_ = [x for x in subsetRock_ if self.map[x[0][0]][x[0][1]] not in ("$", "*")]
            cac_huong_di = []#lấy ra tập các hướng viên đá có thể đi
            for subsetRock in subsetRock_:
                cac_huong_di.append(subsetRock[2])
            for subsetRock in subsetRock_:
                if tracking[subsetRock[2]] in cac_huong_di:#loại bỏ các hướng mà viên đá không thể đi được
                    Open = [S]
                    closed = []
                    point = self.get_point_direction(rockPoint,subsetRock[3])
                    G = Node(point[0])
                    if  self.DFS_step_player(Open,closed,G):#kiểm tra xem nhân vật có thể đi vào hướng ngược lại để đẩy đá không
                        tmp = Node(subsetRock[0],subsetRock[1],subsetRock[2],subsetRock[3])
                        subset_tmp = subset_rock_statu.copy()
                        subset_tmp[i] = tmp
                        statu_ = Statu_rock(subset_tmp,ID_rock=i)
                        subsetRockes.append(statu_)
                    if self.move_player_to(S) == False:
                        print("khong the di")
            i += 1
        return subsetRockes
    #hàm lấy ra tập con của một player
    def get_subset_player(self):
        player = self.find_player_position()
        subset = self.get_subset(player)
        subset_player = []
        for point in subset:
            row, col = point[0]
            if self.map[row][col] not in ("$","*"):
                tmp = Node(point[0],point[1],point[2],point[3])
                subset_player.append(tmp)
        return subset_player
    
    # dùng DFS để tìm đường đi cho đá
    def DFS_step_rock(self, Open, Closed):
        numNode = 1
        while len(Open) > 0:
            O = Open.pop(0)
            self.move_rock_to(O.statu)
            Closed.append(O)

            if self.is_destination():
                road = []
                Closed.pop()
                return self.path(O, road),numNode

            pos = 0
            list__ = []
            for x in self.get_subset_rock(O):
                tmp = x
                tmp.par = O
                list__.append(tmp)
                ok1 = self.checkInArray_rock(tmp, Open)
                ok2 = self.checkInArray_rock(tmp, Closed)
                if not ok1 and not ok2:
                    numNode += 1
                    Open.insert(pos, tmp)
                    pos += 1
        return None, numNode

    #hàm tạo danh sách node
    def create_list_node(self,pointes):
        List = []
        for point in pointes:
            List.append(Node(point))
        return List
    #hàm dùng để di chuyển đá đễn điểm chỉ định
    def move_rock_to(self,point):
        vi_tri_da_s = self.find_rock()
        if len(vi_tri_da_s) != len(point):
            return False
        for i in range(len(vi_tri_da_s)):
            self.move_rock_to_point(vi_tri_da_s[i],point[i].point)
        return True
    #hàm dùng để di chuyển player đến vị trí mong muốn
    def move_player_to(self,point):
        current = self.find_player_position()
        new_row, new_col = point.point
        row, col = current
        if current == point.point:
            return True
        if self.map[new_row][new_col] in ("$","*","#"):
            return False
        if self.map[row][col] == "+":
            self.map[row][col] = "."
        else:
            self.map[row][col] = " "
        if self.map[new_row][new_col] == ".":
            self.map[new_row][new_col] = "+"
        else:
            self.map[new_row][new_col] = "@"
        self.player_position = (new_row,new_col)
    #kiểm tra vị trí đúng có phải vị trí đích không
    def equal(self,S,G):
        return S.point == G.point
    def find_player_position(self):
        for i, row in enumerate(self.map):
            for j, cell  in enumerate(row):
                if(cell == "@") or (cell == "+"):
                    return (i,j)
        return None
    def get_point_direction(self,point,direct):
        row, col = point
        directions = {
            "u": self.pointed_u,
            "d": self.pointed_d,
            "l": self.pointed_l,
            "r": self.pointed_r
        }
        return self.check_map(row,col,directions[direct],direct)
    def find_road(self,statu_ston):
        Open = []
        closed = []
        Lo_trinh = ''
        weight = 0
        for i in range(1,len(statu_ston)):
            ID_rock = statu_ston[i].ID_rock
            weight += self.weights[ID_rock]
            point_ston = statu_ston[i-1].statu[ID_rock].point
            direct_ston = statu_ston[i].statu[ID_rock].tracking
            point_ton_ = statu_ston[i].statu[ID_rock].point
            point_player = self.get_point_direction(point_ston,direct_ston)
            Open.clear()
            closed.clear()
            G = Node(point_player[0])
            S = Node(self.player_position)
            Open.append(S)
            tmp_map = copy.deepcopy(self.map)
            destination = self.DFS_step_player(Open,closed,G)
            if destination is None:
                return None
            self.map = tmp_map
            road = destination.road()
            self.move_rock_to_point(point_ston,point_ton_)
            self.move_player_to(Node(point_ston))
            for x in road:
                Lo_trinh += x.direction.lower()
            Lo_trinh += point_player[3].upper()
        self.reset()
        return Lo_trinh,weight
    
    def find_destination(self):
        vi_tri_dich = []
        for i in range(self.count_rock):
            vi_tri_dich.append(self.ID_rock[i])
        return vi_tri_dich
    
    def find_rock(self):
        vi_tri_da = []
        for i in range(self.count_rock):
            vi_tri_da.append(self.ID_rock[i])
        return vi_tri_da
    
    def DFS_step_player(self, Open, closed, G):
        while len(Open) > 0:
            O = Open.pop(0)
            self.move_player_to(O)
            closed.append(O)
            if self.equal(O, G):
                return O  
            pos = 0
            for x in self.get_subset_player():
                tmp = x
                tmp.parent = O
                
                ok1 = self.checkInArray_player(tmp, Open)
                ok2 = self.checkInArray_player(tmp, closed)
                if not ok1 and not ok2:
                    Open.insert(pos, tmp)
                    pos += 1
        return None
