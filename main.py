from tkinter import ttk
from tkinter import *
from types import SimpleNamespace
import os
from tkinter import messagebox
from PIL import Image,ImageTk
import maze
import algos
from maze import write_output
from utils import write_output
import threading
    
#class GUI dùng cho giao diện
class GameGUI:
    def __init__(self, root, name_map):
        self.go_to = {
            'u': "Up",
            'd': "Down",
            'r': "Right",
            'l': "Left"
        }
        self.map_tmp = []
        self.bfs = ''
        self.dfs = ''
        self.a_star = ''
        self.ucs = ''
        self.step = 0
        self.weight = 0
        self.ID_rock = {}
        self.count_rock = 0
        self.root = root  
        self.label_num = []
        self.init___ = True
        self.list_map  = name_map
        self.load_map(name_map=name_map[0])
        self.out_road()
        print("xong thuat toan")
        self.left_frame = Frame(root,width=500,height=700, bg="grey")
        self.left_frame.grid(row=0,column=0,padx=10,pady=5)
        self.tool_bar = Frame(self.left_frame,width=00,height=700,bg="grey")
        self.tool_bar.grid(row=2,column=0,padx=5,pady=5)

        Label(self.left_frame,text="Bảng Điều Khiển").grid(row=1,column=0,padx=5,pady=5)
        self.pause_image = PhotoImage(file=("images/pause.png")).subsample(6,6)
        self.play_image = PhotoImage(file="images/play.png").subsample(6,6)

        # Biến lưu trạng thái
        self.is_paused = False  

        self.button_DFS = Button(self.tool_bar,width=5,height=2, text="DFS",command=self.DFS)
        self.button_BFS = Button(self.tool_bar,width=5,height=2, text="BFS",command=self.BFS)
        self.button_UCS = Button(self.tool_bar, width=5,height=2,text="UCS",command=self.UCS)
        self.button_A_star = Button(self.tool_bar,width=5,height=2,text="A*",command=self.A_star)
        self.button_pause = Button(self.tool_bar,width=38.5,height=38,image=self.play_image,command=self.pause)
        self.button_reset = Button(self.tool_bar,width=5,height=2,text="Reset",command=self.reset_this)

        self.button_DFS.grid(row=2,column=0)
        self.button_BFS.grid(row=3,column=0)
        self.button_UCS.grid(row=4,column=0)
        self.button_A_star.grid(row=5,column=0)
        self.button_pause.grid(row=6,column=0)
        self.button_reset.grid(row=7,column=0)

        #tạo map
        self.right_frame = Frame(root,width=900,height=900,bg="grey")
        self.right_frame.grid(row=0,column=1,padx=10,pady=5)

        self.map_GUI = Frame(self.right_frame,width=900,height=900,bg="grey")
        self.map_GUI.grid(row=0,column=0,padx=20,pady=5)

        self.images = {}  # Store images to prevent garbage collection
        self.player_position = self.find_player_position()
        self.root.focus_set()
        self.root.bind("<KeyPress>", self.move_player)
        #tạo Frame chứ danh sách map
        self.frame_choose_map = Frame(self.left_frame,width=1000,height=500,padx=10,pady=10,bg="white")
        self.frame_choose_map.grid(row=1,column=0)
        #hiển thị lable
        Label(self.frame_choose_map,text="Select map",font=("Time News Roman", 13)).grid(row=0,column=0)
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
        Label(self.display_result,text="Result: ",font=("Time News Roman", 13, "bold")).grid(row=0,column=0)
        self.label_result = Label(self.display_result,text="weigth = 0\nstep = 0",font=("Time News Roman", 13),width=60)
        self.label_result.grid(row=1,column=0)
        self.create_grid()
        self.init___ = False

    def reset_this(self):
        selected_item = self.listbox.get()
        self.reset_game(selected_item)

    def run_dfs(self):
        new_game = maze.SearchSpace(self.map_tmp)
        tmp, self.dfs = algos.DFS(new_game)
        print("complete DFS: ")
        print(self.dfs)
        return f"DFS\t\n{tmp}\t\n"

    def run_bfs(self):
        new_game = maze.SearchSpace(self.map_tmp)
        tmp, self.bfs = algos.BFS(new_game)
        print("complete BFS: ")
        print(self.bfs)
        return f"BFS\t\n{tmp}\t\n"

    def run_ucs(self):
        new_game = maze.SearchSpace(self.map_tmp)
        tmp, self.ucs = algos.UCS(new_game)
        print("complete UCS:")
        print(self.ucs)
        return f"UCS\t\n{tmp}\t\n"

    def run_a_star(self):
        new_game = maze.SearchSpace(self.map_tmp)
        tmp, self.a_star = algos.AStar(new_game)
        print("complete A*:")
        print(self.a_star)
        return f"A*\t\n{tmp}\t\n"
    
    def out_road(self):
        print("Start searching...")

        # Khởi tạo các luồng cho từng thuật toán
        dfs_thread = threading.Thread(target=self.run_dfs)
        bfs_thread = threading.Thread(target=self.run_bfs)
        ucs_thread = threading.Thread(target=self.run_ucs)
        a_star_thread = threading.Thread(target=self.run_a_star)

        # Bắt đầu các luồng
        dfs_thread.start()
        bfs_thread.start()
        ucs_thread.start()
        a_star_thread.start()

        # Chờ các luồng hoàn thành
        dfs_thread.join()
        bfs_thread.join()
        ucs_thread.join()
        a_star_thread.join()
        print("xong")
        # Tạo nội dung kết quả
        result = (
            self.run_dfs() +
            self.run_bfs() +
            self.run_ucs() +
            self.run_a_star()
        )

        #write to output 
        if self.init___:
            index = 0   
        else:
            index = self.listbox.current()
        name_file_out = f"output-{index+1:02}.txt"
        write_output(name_file_out,result)
        print("All algorithms completed and output written.")


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

    #dùng để di chuyển khi truyền giá trị up, left right
    def move(self, direction):
        self.player_position = self.find_player_position()
        event = SimpleNamespace()
        event.keysym = direction
        self.move_player(event)

    def BFS(self):
        self.read_road(self.bfs,0)
    
    def UCS(self):
        self.read_road(self.ucs,0)


    def A_star(self):
        self.read_road(self.a_star, 0)
    
    def DFS(self):
        self.read_road(self.dfs,0)
    
    def read_road(self, road,index):
        if road is None:
            return
        if self.is_paused:            
            self.root.after(1000, lambda: self.read_road(road,index))  
            return       
        if index < len(road):
            self.move(self.go_to[road[index].lower()])
            self.root.after(1000, lambda: self.read_road(road,index+1))
        if index == len(road) - 1:
            messagebox.showinfo("Thông báo", "Hoàn thành")

    def load_map(self,name_map):
        self.map = self.readmap(name_map)

    def readmap(self,name_map):
        map__ = []
        self.full = []
        with open(name_map, 'r') as file:
            lines = file.readlines()
            self.map_tmp = [line.strip() for line in lines]
            self.full.append(lines)
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
                self.weight += self.khoi_luong_da[i]
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
        self.step += 1
        self.update_grid()
        if self.check_game_completed():
            print("Hoàn thành")
    
    #reset map
    def reset_game(self,name_map):
        self.count_rock = 0
        for row in self.labels:
            for label in row:
                label.destroy()
        self.load_map(name_map)
        self.player_position = self.find_player_position()
        self.create_grid()
        self.update_grid()
    
    #update map
    def get_key_from_value(self,d, value):
        for key, val in d.items():
            if val == value:
                return key
        return None  # Trả về None nếu không tìm thấy
    def update_grid(self):
        self.label_result.config(text=f"weight = {self.weight}\nstep={self.step}")
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                # Cập nhật hình ảnh trên mỗi ô
                self.labels[i][j].delete("all")  # Xóa tất cả nội dung trong Canvas hiện tại
                self.labels[i][j].create_image(0, 0, anchor="nw", image=self.images[cell])  # Đặt lại ảnh

                # Nếu là ô chứa đá, cập nhật số ngẫu nhiên
                if cell == "$" or cell == "*":
                    random_number = self.khoi_luong_da[self.get_key_from_value(self.ID_rock,(i,j))]
                    # Vẽ hình tròn trắng (nền)
                    x0, y0 = 20, 20  # Tọa độ góc trên trái của hình tròn
                    x1, y1 = 50, 50  # Tọa độ góc dưới phải của hình tròn
                    self.labels[i][j].create_oval(x0, y0, x1, y1, fill="white", outline="black")
                    self.labels[i][j].create_text(
                        35, 35,  # Giữa ô
                        text=str(random_number),
                        font=("Arial", 12, 'bold'),
                        fill="black"
                    )


    def check_game_completed(self):
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if(cell == '.' or cell == '+'):
                    return False
        return True
    
    def create_grid(self):
        cell_size = 70
        self.step = 0
        self.weight = 0
        self.images = {
            '#': ImageTk.PhotoImage(Image.open("images/wall.png").resize((cell_size, cell_size))),
            '@': ImageTk.PhotoImage(Image.open("images/player.png").resize((cell_size, cell_size))),
            '$': ImageTk.PhotoImage(Image.open("images/rock.png").resize((cell_size, cell_size))),
            '.': ImageTk.PhotoImage(Image.open("images/target.png").resize((cell_size, cell_size))),
            ' ': ImageTk.PhotoImage(Image.open("images/empty.png").resize((cell_size, cell_size))),
            '*': ImageTk.PhotoImage(Image.open("images/rock.png").resize((cell_size, cell_size))),
            '+': ImageTk.PhotoImage(Image.open("images/player.png").resize((cell_size, cell_size)))
        }
        
        self.labels = []
        self.destination = []
        self.vi_tri_da = []
        h = 0
        
        for i, row in enumerate(self.map):
            label_row = []
            for j, cell in enumerate(row):
                if cell == "$" or cell == "*":
                    self.ID_rock[self.count_rock] = (i, j)
                    self.count_rock += 1
                if cell == "." or cell == "+":
                    self.destination.append((i, j))
                if cell in ("+", "@"):
                    self.start = (i, j)
                    
                image = self.images.get(cell)
                if image:
                    canvas = Canvas(self.map_GUI, width=cell_size, height=cell_size, highlightthickness=0)
                    canvas.grid(row=i, column=j)
                    canvas.create_image(0, 0, anchor="nw", image=image)
                    
                    if cell == "$" or cell == "*":
                        random_number = self.khoi_luong_da[h]
                        h += 1
                        canvas.create_oval(cell_size // 4, cell_size // 4, 3 * cell_size // 4, 3 * cell_size // 4, fill="white", outline="black")
                        canvas.create_text(cell_size // 2, cell_size // 2, text=str(random_number), font=("Arial", 12, 'bold'), fill="black")
                        self.label_num.append(canvas)
                    label_row.append(canvas)
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
    root.config(bg = "black")
    root.grid_columnconfigure(0,weight=1)
    root.grid_columnconfigure(1,weight=2)

    list_map = load_file()
    app = GameGUI(root, list_map)
    root.mainloop()