from tkinter import *
from tkinter import filedialog
import cv2
import os
import json
import PIL
from PIL import Image, ImageTk

class ImageLabeling():
    def __init__(self, master):
        self.master = master
        self.master.title("图片标注")
        self.master.geometry("1920x1080")
        # 用于存储标注内容的字典
        self.labels = {}
        self.images = []
        self.images_ = []
        # 用于存储当前显示图片的名称和位置
        self.current_image = None
        self.current_index = 0
        self.label_path = ""
        # 构建GUI界面
        self.create_widgets()

    def create_widgets(self):
        # 添加选择读取文件路径的按钮
        self.load_button = Button(self.master, text="选择读取文件路径", command=self.load_folder)
        self.load_button.pack()

        # 添加选择保存文件路径的按钮
        self.save_button = Button(self.master, text="选择保存文件路径", command=self.save_folder)
        self.save_button.pack()

        # 添加显示图片的Canvas
        self.main_frame = Frame(self.master)
        self.main_frame.pack()
        self.image_frame = Frame(self.master)
        self.image_frame.pack(in_=self.main_frame)
        # self.image_frame.pack(expand=True, fill=BOTH)

        for i in range(5):
            row = i // 5
            col = i % 5

            # 使用Grid布局将Frame显示在Canvas上
            frame = Frame(self.image_frame, width=200, height=260) # 修改处
            frame.grid(row=row, column=col, padx=30, pady=30) # 修改处

            # 使用Pack布局将Canvas和label_name_label放置在Frame中
            canvas = Canvas(frame, width=200, height=200)
            canvas.pack()

            label_name_label = Label(frame, text="")
            label_name_label.pack(pady=5) # 修改处

            # 保存Canvas和标注框名称的引用，用于后续更新标注内容
            self.images.append({"canvas": canvas, "label_name_label": label_name_label, "photo": None})

        # 添加左右切换按钮
        self.prev_button = Button(self.master, text="<", command=self.prev_image)
        self.prev_button.config(width=10, height=10)
        # self.prev_button.pack(side=LEFT)
        self.prev_button.place(relx=0.05, rely=0.5, anchor=CENTER)
        self.master.bind("<KeyPress-Left>", lambda event: self.prev_image()) # 监控键盘的A键，代表上一张

        self.next_button = Button(self.master, text=">", command=self.next_image)
        self.next_button.config(width=10, height=10)
        # self.next_button.pack(side=RIGHT)
        self.next_button.place(relx=0.95, rely=0.5, anchor=CENTER)
        self.master.bind("<KeyPress-Right>", lambda event: self.next_image()) # 监控键盘的D键，代表下一张

        # 添加标注框的Frame
        self.label_frame = Frame(self.master)
        # self.label_frame.pack(side=BOTTOM)
        # self.label_frame.pack(side=BOTTOM,anchor=S,  padx=5, pady=(50, 5))
        self.label_frame.pack(in_=self.main_frame)
        # self.label_frame.place(relx=0.5, rely=0.9, anchor=CENTER)  # 修改
        for i in range(5):
            # 使用Frame布局将标注框放置在一个Frame中
            label_frame = Frame(self.label_frame, width=300)
            label_frame.grid(row=0, column=i, padx=50, pady=50)

            label_text = Label(label_frame, text="标注框{}".format(i + 1))
            label_text.pack()

            label_input = Entry(label_frame)
            label_input.pack()

            # 保存标注框和输入框的引用，用于后续更新和保存标注内容
            self.labels["标注框{}".format(i + 1)] = {"label_frame": label_frame, "label_input": label_input,"image_name":""}

        # 添加保存标注内容的按钮
        self.save_label_button = Button(self.master, text="保存标注", command=self.save_label)
        self.master.bind("<KeyPress-Return>", lambda event: self.save_label())  # 监控键盘，代表保存标注内容
        self.save_label_button.place(relx=0.5, rely=0.96, anchor=CENTER)
        # self.save_label_button.pack()

    def load_folder(self):
        # 打开文件夹选择对话框获取文件夹路径
        self.folder_path = filedialog.askdirectory()

        # 获取文件夹中的所有图片并显示第一张
        self.images_ = [i for i in os.listdir(self.folder_path) if i.endswith(".jpg")|i.endswith(".png")|i.endswith(".bmp")]
        self.current_index = 0
        self.display_images(self.current_index, self.images_)
        if len(self.label_path)==0:
            self.label_path = self.folder_path

    def save_folder(self):
        # 打开文件夹选择对话框获取文件夹路径
        self.label_path = filedialog.askdirectory()
        self.display_images(self.current_index, self.images_)

    def display_images(self, current_idx, images):
        # 显示5张图片
        self.prev_button["state"] = "disabled" if current_idx == 0 else "normal"
        self.next_button["state"] = "disabled" if current_idx + 4 >= len(images) else "normal"

        label_list = [self.labels[i]["label_input"] for i in self.labels]
        for i in range(5):
            idx = current_idx + i
            if idx < len(images):
                image_name = images[idx]

                # 使用OpenCV读取图片
                image_path = os.path.join(self.folder_path, image_name)
                image = cv2.imread(image_path)

                # 读取json加载到输入框中
                label_path = os.path.join(self.label_path, image_name.split(".")[0]+".json")

                label_input_2 = label_list[i]
                if os.path.exists(label_path):
                    try:
                        with open(label_path, 'r') as f:
                            label_value = str(json.load(f)['note_value'])

                    except:

                        label_value = ""
                    label_input_2.delete(0, END)
                    label_input_2.insert(0, label_value)

                else:
                    label_input_2.delete(0, END)


                # 将OpenCV格式的图片转换为Tkinter格式并显示在Canvas上
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                photo = ImageTk.PhotoImage(image=PIL.Image.fromarray(image))
                canvas = self.images[i]["canvas"]
                canvas.delete("all")
                canvas.create_image(0, 0, image=photo, anchor="nw")
                self.images[i]["photo"] = photo

                # 显示标注框名称
                label_name_label = self.images[i]["label_name_label"]
                label_name_label.config(text=image_name)
                # print(label_name_label)
                self.labels[[xx for xx in self.labels.keys()][i]]['image_name'] = image_name
                # # 显示标注内容
                # if label_name in self.labels:
                #     label_input = self.labels[label_name]["label_input"]
                #     label_input.delete(0, END)
                #     if image_name in self.labels[label_name]:
                #         label_input.insert(0, self.labels[label_name][image_name])

    def prev_image(self):
        # 切换到上一张图片
        if self.current_index > 0:
            self.current_index -= 5
            if self.current_index < 0:
                self.current_index = 0
            self.display_images(self.current_index, self.images_)

    def next_image(self):
        # 切换到下一张图片
        if self.current_index + 4 < len(self.images_):
            self.current_index += 5
            self.display_images(self.current_index, self.images_)

    def save_label(self):
        # 将所有标注内容保存到字典中
        label_dict = {}
        for label_name in self.labels:
            label_dict[label_name] = []
            for image_name, value in self.labels[label_name].items():
                if not isinstance(value, (Frame, Entry)):
                    value_dict = {}
                    value_dict["image_name"] = image_name
                    value_dict["value"] = value
                    label_dict[label_name].append(value_dict)
                elif isinstance(value, Entry):
                    value_dict = {}
                    value_dict["image_name"] = image_name
                    value_dict["value"] = value.get()
                    label_dict[label_name].append(value_dict)

        # 将标注内容以 json 格式保存到文件中
        print(type(self.labels))
        print(self.labels)
        for _,info in label_dict.items():
            note = info[0]["value"]
            image_real_name = info[1]["value"]
            label_path = os.path.join(self.label_path, image_real_name.split(".")[0]+".json")
            with open(label_path, "w") as f:
                json.dump({"image_name":image_real_name,"note_value":note}, f)
        # label_path = os.path.join(self.label_path, "labels.json")
        # with open(label_path, "w") as f:
        #     json.dump(label_dict, f)


if __name__ == "__main__":
    root = Tk()
    app = ImageLabeling(root)
    root.mainloop()