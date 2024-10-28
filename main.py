from tkinter import ttk
from tkinter import *
from types import SimpleNamespace
import os
import time
import copy
from tkinter import messagebox

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
    def display(self):
        a = None
        if self.parent is not None:
            a = self.parent.point
        print(self.point, a,self.direction,self.tracking)

class Statu_rock:
    def __init__(self, statu, par=None,ID_rock = None):
        self.statu = statu
        self.par = par
        self.ID_rock = ID_rock
    def display(self):
        print("Trang thai: ")
        for i in self.statu:
            print(i.point)
    def get_points(self):
        list_tmp = []
        for i in self.statu:
            list_tmp.append(i.point)
        return list_tmp
    def get_point_move(self):
        if self.ID_rock is None:
            return None
        return self.statu[self.ID_rock]
    
    

#class GUI dùng cho giao diện
class GameGUI:
    def __init__(self, root, name_map):
        self.UP = "Up"
        self.DOWN = "Down"
        self.Right = "Right"
        self.Left = "Left"
        self.ID_rock = {}
        self.count_rock = 0
        self.cac_huong_rock = {}#lu cac hướng viên đá có thể đi và bật 1 nếu viên đá đã đi hướng đó rồi
        self.root = root  # Assign the root to an instance attribute
        self.is_day_da = False
        #tạo bảng điều khiển
        self.left_frame = Frame(root,width=500,height=700, bg="grey")
        self.left_frame.grid(row=0,column=0,padx=10,pady=5)
        self.tool_bar = Frame(self.left_frame,width=00,height=700,bg="grey")
        self.tool_bar.grid(row=2,column=0,padx=5,pady=5)

        Label(self.left_frame,text="Bảng Điều Khiển").grid(row=1,column=0,padx=5,pady=5)
        self.pause_image = PhotoImage(file=("images/pause.png")).subsample(6,6)
        self.play_image = PhotoImage(file="images/play.png").subsample(6,6)

        # Biến lưu trạng thái
        self.is_paused = False  # Bắt đầu ở trạng thái pause
        #tạo button
        self.button_DFS = Button(self.tool_bar,width=5,height=2, text="DFS",command=self.Run_DFS)
        self.button_BFS = Button(self.tool_bar,width=5,height=2, text="BFS",command=self.BFS)
        self.button_UCS = Button(self.tool_bar, width=5,height=2,text="UCS",command=self.UCS)
        self.button_A_star = Button(self.tool_bar,width=5,height=2,text="A*",command=self.A_star)
        self.button_pause = Button(self.tool_bar,width=37,height=37,image=self.play_image,command=self.pause)
        self.button_reset = Button(self.tool_bar,width=5,height=2,text="reset",command=self.reset_this)

        self.button_DFS.grid(row=2,column=0)
        self.button_BFS.grid(row=3,column=0)
        self.button_UCS.grid(row=4,column=0)
        self.button_A_star.grid(row=5,column=0)
        self.button_pause.grid(row=6,column=0)
        self.button_reset.grid(row=7,column=0)

        #tạo map
        self.right_frame = Frame(root,width=900,height=600,bg="grey")
        self.right_frame.grid(row=0,column=1,padx=10,pady=5)

        self.map_GUI = Frame(self.right_frame,width=900,height=600,bg="grey")
        self.map_GUI.grid(row=0,column=0,padx=20,pady=5)

        self.images = {}  # Store images to prevent garbage collection
        self.list_map  = name_map
        self.load_map(name_map=name_map[0])
        self.player_position = self.find_player_position()
        self.create_grid()
        self.root.focus_set()
        self.root.bind("<KeyPress>", self.move_player)
        # Ràng buộc phím Enter
        self.root.bind("<Return>", self.on_enter_key)
        
        #tạo Frame chứ danh sách map
        self.frame_choose_map = Frame(self.left_frame,width=1000,height=500,padx=10,pady=10,bg="white")
        self.frame_choose_map.grid(row=1,column=0)
        #hiển thị lable
        Label(self.frame_choose_map,text="select map",font=("Arial", 13)).grid(row=0,column=0)

        #compobox hiển thị danh sách list
        self.listbox = ttk.Combobox(self.frame_choose_map,values=name_map, state="readonly")
        self.listbox.current(0)
        self.listbox.grid(row=1,column=0)
        self.listbox.bind("<<ComboboxSelected>>", self.on_select)
        self.listbox.bind("<Up>", self.change_focus)
        self.listbox.bind("<Down>", self.change_focus)
        self.listbox.bind("<Left>", self.change_focus)
        self.listbox.bind("<Right>", self.change_focus)
        #frame in điểm trọng số, số bước đi (kết quả):
        self.display_result = Frame(self.right_frame,width=900,height=200,padx=5,pady=10, bg="white")
        self.display_result.grid(row=1,column=0)
        Label(self.display_result,text="Result: ",font=("Arial", 13, "bold")).grid(row=0,column=0)
        self.label_result = Label(self.display_result,text="weigth = 0 \n distant = 0",font=("Arial", 13),width=60)
        self.label_result.grid(row=1,column=0)
#---------------------------tạo hàm-----------------------------
#---------------------------------------------------------------
    def reset_this(self):
        selected_item = self.listbox.get()
        self.reset_game(selected_item)
    #hàm xử lý sự kiện khi chọn một phần tử trong Listbox
    def on_select(self,event):
        selected_item = self.listbox.get()
        self.reset_game(selected_item)
    # Đưa focus về cửa sổ chính để bỏ focus khỏi Combobox
    def change_focus(self,event):
        self.root.focus() 
    #hàm dùng để pause lại
    def pause(self):
        if self.is_paused:
            self.button_pause.config(image=self.play_image)  # Chuyển thành nút play
            self.is_paused = False
        else:
            self.button_pause.config(image=self.pause_image)  # Chuyển thành nút pause
            self.is_paused = True
    # Khi nhấn Enter, tiếp tục bước tiếp theo
    def on_enter_key(self,event):
        if hasattr(self, 'current_step'):
            self.current_step()
    #xuất ra vị trí các up, down, left, right
    def pointed_up(self,i, j):
        return i-1,j
    def pointed_down(self,i,j):
        return i+1,j
    def pointed_left(self,i,j):
        return i , j-1
    def pointed_right(self ,i, j):
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
        tracking = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}[direct]
        return [(new_row, new_col), (row, col), direct, tracking]
    
    #lấy ra tập con khả có thể đi được trong một điểm
    def get_subset(self, point):
        row, col = point
        directions = [
            ("Up", self.pointed_up),
            ("Right", self.pointed_right),
            ("Down", self.pointed_down),
            ("Left", self.pointed_left)
        ]
        subset = [self.check_map(row, col, func, direction) for direction, func in directions]
        return [item for item in subset if item is not None]
    #hàm dùng để kiểm tra đó có phải là đích hay không thỏa điều kiện dừng chứ
    def is_destination(self):
        for row, col in self.destination:
            if self.map[row][col] in (".","+"):
                return False
        return True
    #hàm dùng để in ra đường đi từ đích đế O
    def path(self,O,road):
        road.append(O)
        if O.par != None:
            return self.path(O.par,road)
        else:
            return road
    #check một điểm của viên đá có trong mảng hay không
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


    #dùng để di chuyển khi truyền giá trị up, left right
    def move(self, direction):
        self.player_position = self.find_player_position()
        event = SimpleNamespace()
        event.keysym = direction
        self.move_player(event)

    #xuất ra tập vị trí của viên đá
    def find_rock(self):
        vi_tri_da = []
        for i in range(self.count_rock):
            vi_tri_da.append(self.ID_rock[i])
        return vi_tri_da
    #tim tap dich.
    def find_destination(self):
        vi_tri_dich = []
        for i in range(self.count_rock):
            vi_tri_dich.append(self.ID_rock[i])
        return vi_tri_dich
    #kiểm tra đá còn đường đi hay không
    def check_can_move_rock(self):
        vi_tri_da = self.find_rock()
        for x in vi_tri_da:
            tap_con_vi_x_y = self.get_subset(x)
            if len(tap_con_vi_x_y) > 2:
                return True
        return False
    #di chuyển đá đến vị trí mong muốn
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

    #hàm get ra tập con của tất cả viên đá
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
        tracking = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
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
                    if  self.DFS_step_player(Open,closed,G):
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
            print("dua vao khong dung")
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

    #thực hiện BFS
    def BFS(self):
        print(self.ID_rock)
        print("BFS")
        return
    
    def Run_DFS(self):
        Lo_trinh,info = self.DFS()
        distant = 0
        if Lo_trinh == None:
            messagebox.showerror("Lỗi", info)
            return
        distant = len(Lo_trinh)
        self.label_result.config(text=f"weight = 0\ndistant={distant}")
        self.read_road(Lo_trinh,0)

    def read_road(self, road,index):
        if self.is_paused:            
            self.root.after(1000, lambda: self.read_road(road,index))  
            return       
        if index < len(road):
            self.move(road[index])
            self.root.after(1000, lambda: self.read_road(road,index+1))
        if index == len(road) - 1:
            messagebox.showinfo("Thông báo", "hoàn thành đường đi")
    #dfs mới chế tạo lại
    def DFS(self):
        points_rock = self.find_rock()
        points_switch = self.find_destination()
        tmp = self.create_list_node(points_rock)
        S = Statu_rock(tmp)
        tmp = self.create_list_node(points_switch)
        G = Statu_rock(tmp)
        Open = [S]
        closed = []
        statu_ston = self.DFS_step_rock(Open,closed)
        statu_ston = statu_ston[::-1]
        tmp_map = copy.deepcopy(self.map)
        selected_item = self.listbox.get()
        self.reset_game(selected_item)
        Lo_Trinh = self.find_road(statu_ston)
        if Lo_Trinh != None:
            return Lo_Trinh,"hoàn thành chúc mừng"
        self.map = tmp_map
        return None, "không thể đẩy đá"
    def ve_map(self, map):
        for x in map:
            print(x)
        print("\t\n")

    def find_road(self,statu_ston):
        Open = []
        closed = []
        Lo_trinh = []
        selected_item = self.listbox.get()
        for i in range(1,len(statu_ston)):
            ID_rock = statu_ston[i].ID_rock
            point_ston = statu_ston[i-1].statu[ID_rock].point
            direct_ston = statu_ston[i].statu[ID_rock].tracking
            point_player = self.get_point_direction(point_ston,direct_ston)
            Open.clear()
            closed.clear()
            G = Node(point_player[0])
            S = Node(self.player_position)
            Open.append(S)
            tmp_map = copy.deepcopy(self.map)
            destination = self.DFS_step_player(Open,closed,G)
            if destination is None:
                print("ket thuc lo trinh")
                return None
            self.map = tmp_map
            road = destination.road()
            for x in road:
                Lo_trinh.append(x.direction)
                self.move(x.direction)
            Lo_trinh.append(point_player[3])
            self.move(point_player[3])
        self.reset_game(selected_item)
        return Lo_trinh

    def get_point_direction(self,point,direct):
        row, col = point
        directions = {
            "Up": self.pointed_up,
            "Down": self.pointed_down,
            "Left": self.pointed_left,
            "Right": self.pointed_right
        }
        return self.check_map(row,col,directions[direct],direct)

    def DFS_step_player(self, Open,closed,G):
        if(len(Open) == 0):
            # print("hiep si ko co duong di !")
            return None
        O = Open.pop(0)
        self.move_player_to(O)
        self.update_grid()
        closed.append(O)
        if(self.equal(O,G)):
            # print("tim thay duong di cua hiep si")
            return O  
        pos = 0
        for x in self.get_subset_player():
            tmp = x
            tmp.parent = O
            ok1 = self.checkInArray_player(tmp,Open)
            ok2 = self.checkInArray_player(tmp, closed)
            if not ok1 and not ok2:
                Open.insert(pos,tmp)
                pos +=1
        return self.DFS_step_player(Open,closed,G)

    # dùng DFS để tìm đường đi cho đá
    def DFS_step_rock(self, Open, Closed):
        if len(Open) == 0:
            # print("tiềm kiếm trạng thái thất bại")
            return None
        O = Open.pop(0)
        self.move_rock_to(O.statu)
        Closed.append(O)
        if self.is_destination():
            # print("tim thấy trạng thái đá phù hợp")
            road = []
            Closed.pop()
            return self.path(O,road)
        pos = 0
        list__ = []
        for x in self.get_subset_rock(O):
            tmp = x
            tmp.par = O
            list__.append(tmp)
            ok1 = self.checkInArray_rock(tmp,Open)
            ok2 = self.checkInArray_rock(tmp,Closed)
            if not ok1 and not ok2:
                Open.insert(pos,tmp)
                pos +=1
        return self.DFS_step_rock(Open,Closed)

    def add_x_to_label(self,label, text="X", color="red"):
        # Sử dụng màu nền của label cha
        x_label = Label(label, text=text, fg=color, font=("Arial", 24, "bold"), bg=label["bg"])
        x_label.place(x=20, y=20)  # Điều chỉnh vị trí chữ X sao cho phù hợp
        return x_label
    def update_rock(self, point):
        tmp = {point: {}}
        for x in self.get_subset(point):
            temp = {x[2]: False}
            tmp[point].update(temp)
        self.cac_huong_rock.update(tmp)
    
    def reset_point_rock(self,O):
        if O.is_day_da():
            row_current, col_current = O.vi_tri_vien_da_hien_tai
            row, col =O.point
            if self.map[row_current][col_current] == "*":
                self.map[row_current][col_current] = "."
            else:
                self.map[row_current][col_current] = " "
            if self.map[row][col] == ".":
                self.map[row][col] = "*"
            else:
                self.map[row][col] = "$"
        self.update_grid()


    def UCS(self):
        print("UCS")
        return
    def A_star(self):
        print("A*")
        return
    def load_map(self,name_map):
        self.map = self.readmap(name_map)

    def readmap(self,name_map):
        map__ = []
        with open(name_map, 'r') as file:
            lines = file.readlines()
            self.khoi_luong_da = [int(x) for x in lines[0].strip().split(" ")]
            for line in lines[1:]:
                line = line.split("\n")[0]
                list__ = list(line)
                map__.append(list__)
        return map__

    def find_player_position(self):
        for i, row in enumerate(self.map):
            for j, cell  in enumerate(row):
                if(cell == "@") or (cell == "+"):
                    return (i,j)
        return None

    #di chuyen player
    def move_player(self, event):
        row, col = self.player_position

        if event.keysym == "Up":
            new_row, new_col = row -1 , col
        elif event.keysym == "Down":
            new_row, new_col = row + 1, col
        elif event.keysym == "Left":
            new_row, new_col = row, col-1
        elif event.keysym == "Right":
            new_row, new_col = row, col + 1
        else:
            return
        
        if self.map[new_row][new_col] == "#":
            return
        rock_new_row = new_row + (new_row - row)
        rock_new_col = new_col + (new_col - col)
        if self.map[new_row][new_col] == "$" :
            if self.map[rock_new_row][rock_new_col] == '.':
                self.map[rock_new_row][rock_new_col] = '*'
                self.map[new_row][new_col] = ' '
            elif self.map[rock_new_row][rock_new_col] == ' ':
                self.map[rock_new_row][rock_new_col] = "$"
                self.map[new_row][new_col] = ' '
            elif self.map[rock_new_row][rock_new_col] == "$":
                return
            elif self.map[rock_new_row][rock_new_col] == "#":
                return
            self.is_day_da = True
        if self.map[new_row][new_col] == "*":
            if self.map[rock_new_row][rock_new_col] == '.':
                self.map[rock_new_row][rock_new_col] = '*'
                self.map[new_row][new_col] = '.'
            elif self.map[rock_new_row][rock_new_col] == ' ':
                self.map[rock_new_row][rock_new_col] = "$"
                self.map[new_row][new_col] = '.'
            elif self.map[rock_new_row][rock_new_col] == "$":
                return
            elif self.map[rock_new_row][rock_new_col] == "#":
                return 
        for i in range(self.count_rock):
            if self.ID_rock[i] == (new_row,new_col):
                self.ID_rock[i] = (rock_new_row,rock_new_col)
        if(self.map[row][col] == '+'):
            self.map[row][col] = '.'
        else:
            self.map[row][col] = ' '
        if self.map[new_row][new_col] == '.':
            self.map[new_row][new_col] = '+'
        else:
            self.map[new_row][new_col]= "@"
        self.player_position = (new_row, new_col)
        # print(f"{row,col} -> {new_row,new_col}")
        self.update_grid()
        if self.check_game_completed():
            print("hoàn thánh chúc mừng")
    
    #reset map
    def reset_game(self,name_map):
        self.count_rock = 0

        for row in self.labels:
            for label in row:
                label.destroy()
        self.load_map(name_map)
        self.player_position = self.find_player_position()
        self.create_grid()
    
    #update map
    def update_grid(self):
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                self.labels[i][j].config(image = self.images[cell])
                self.labels[i][j].image = self.images[cell]
    def check_game_completed(self):
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if(cell == '.' or cell == '+'):
                    return False
        return True
    def create_grid(self):
        # Load images for different types of cells
        self.images = {
            '#': PhotoImage(file="images/wall.png").subsample(5,5),
            '@': PhotoImage(file="images/player.png").subsample(5,5),
            '$': PhotoImage(file="images/rock.png").subsample(5,5),
            '.': PhotoImage(file="images/target.png").subsample(5,5),
            ' ': PhotoImage(file="images/empty.png").subsample(5,5),
            '*': PhotoImage(file="images/rock.png").subsample(5,5),
            '+': PhotoImage(file="images/player.png").subsample(5,5)
        }
        # Create the grid layout
        self.labels = []
        self.destination = []
        self.vi_tri_da = []
        for i, row in enumerate(self.map):
            label_row = []
            for j, cell in enumerate(row):
                if cell == "$" or cell == "*":
                    self.ID_rock[self.count_rock] = (i,j)
                    self.count_rock += 1
                if cell == "." or cell =="+":
                    self.destination.append((i,j))
                if cell in ("+","@"):
                    self.start = (i,j)
                image = self.images.get(cell)
                if image:  
                    lbl = Label(self.map_GUI, image=image)
                    lbl.grid(row=i, column=j)
                    lbl.image = image  # Store reference to avoid garbage collection
                    label_row.append(lbl)
            self.labels.append(label_row)

def load_file():
    folder_path = "input"
    array_name_file = []
    file_names = os.listdir(folder_path)
    # In tên các file
    for file_name in file_names:
        array_name_file.append(folder_path+"/"+file_name)
    return array_name_file

if __name__ == "__main__":
    root = Tk()
    root.config(bg = "skyblue")

    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)

    list_map = load_file()
    app = GameGUI(root, list_map)
    root.mainloop()