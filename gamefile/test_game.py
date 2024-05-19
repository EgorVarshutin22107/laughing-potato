from tkinter import *
import random
from tkinter import messagebox

class GameButton:
    def __init__(self, canvas, x0, y0, x1, y1, cols, row_index, col_index, is_top_left=False, update_game_app=None):
        self.canvas = canvas
        self.clicks = 0
        self.cols = cols
        self.row_index = row_index
        self.col_index = col_index
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.update_game_app = update_game_app

        fill_color = "white"
        if is_top_left:
            fill_color = "#FFFF99"

        self.id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color)
        self.text_id = self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=self.generate_random_text())

        self.canvas.tag_bind(self.id, "<Button-1>", lambda event: self.rotate_text())

    def rotate_text(self):
        self.clicks += 1
        if self.clicks % 4 == 0:
            self.clicks = 0
        rotation = 90 * self.clicks
        self.canvas.itemconfig(self.text_id, angle=rotation)

        self.update_game_app()

    def update_color(self, color):
        self.canvas.itemconfig(self.id, fill=color)

    def generate_random_text(self):
        if self.col_index == 0:
                return "|_"
        elif self.col_index == self.cols - 1:
                return "|_"
        else:
            return random.choice(["---", "|"])


class GameApp:
    def __init__(self, master):
        self.master = master
        master.title("Да будет свет!")
        master['bg'] = '#E0FFFF'

        self.size = 10  # Изначальный размер поля
        self.window_width = 600
        self.window_height = 600

        self.settings_frame = Frame(master, bg="#E0FFFF")
        self.settings_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        self.size_label = Label(self.settings_frame, text="Size:", bg="#E0FFFF")
        self.size_label.grid(row=0, column=0, padx=5, pady=5)
        self.size_entry = Entry(self.settings_frame)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5)
        self.size_entry.insert(0, self.size)

        self.update_button = Button(self.settings_frame, text="Обновить", command=self.update_game_size)
        self.update_button.grid(row=1, columnspan=2, pady=10)

        self.timer_frame = Frame(master, bg="#E0FFFF")
        self.timer_frame.pack(side=TOP, fill=X)

        self.timer = 120
        self.timer_label = Label(self.timer_frame, text=f"Time left: {self.timer} seconds", font=("Arial", 14), bg="#E0FFFF")
        self.timer_label.pack(pady=10)

        self.canvas = Canvas(master, bg='#E0FFFF', width=self.window_width, height=self.window_height - 50)
        self.canvas.pack(fill=BOTH, expand=YES)

        self.buttons = []
        self.create_buttons()

        self.timer_job = master.after(1000, self.update_timer)
        self.game_over = False


    def create_buttons(self):
        for i in range(self.size):
            for j in range(self.size):
                x0 = j * (self.window_width / self.size)
                y0 = i * (self.window_height / self.size)
                x1 = x0 + (self.window_width / self.size)
                y1 = y0 + (self.window_height / self.size)
                is_top_left = (i == 0 and j == 0)
                button = GameButton(self.canvas, x0, y0, x1, y1, self.size, i, j, is_top_left, self.update_game_app)
                self.buttons.append(button)


# В функции update_game_app() я присвоил каждому виду содержимого квадратика свой индекс и по ним ориентировался,
# находится ли содержимое строки в правильном положении для ее закрашивания или нет

    def update_game_app(self):
        for i in range(self.size):
            row = []  # Список для хранения значений текущей строки
            for j in range(self.size):
                button = self.get_button(i, j)
                text = button.generate_random_text()
                angle = button.clicks * 90  # Угол поворота
                if text == "---" and (angle == 0 or angle == 180):
                    value = 1
                elif text == "|" and (angle == 90 or angle == 270):
                    value = 2
                elif text == "|_" and angle == 0:
                    value = 3
                elif text == "|_" and angle == 180:
                    value = 4
                elif text == "|_" and angle == 270:
                    value = 5
                elif text == "|_" and angle == 90:
                    value = 6
                row.append(value)

            # Проверяем условия для строки
            if i % 2 == 0:
                if 3 in row and 1 in row and 4 in row and 2 in row:
                    for button in self.buttons[i*self.size:(i+1)*self.size]:
                        button.update_color("#FFFF99")
            else:
                if 6 in row and 1 in row and 2 in row and 5 in row:
                    for button in self.buttons[i*self.size:(i+1)*self.size]:
                        button.update_color("#FFFF99")

            self.check_if_game_won()


    def get_button(self, row, col):
        index = row * self.size + col
        return self.buttons[index]

    def update_game_size(self):
        self.size = int(self.size_entry.get())
        self.window_width = min(600, self.master.winfo_screenwidth() - 100)
        self.window_height = min(600, self.master.winfo_screenheight() - 100)
        self.canvas.config(width=self.window_width, height=self.window_height)
        self.buttons.clear()  # Очищаем старые кнопки
        self.create_buttons()  # Создаем новые кнопки

    def update_timer(self):
        self.timer -= 1
        self.timer_label.config(text=f"Осталось: {self.timer} секунд")
        if self.timer == 0:
            self.master.after_cancel(self.timer_job)
            messagebox.showinfo("Вы проиграли", "Время вышло, увы...")
            self.master.destroy()
        else:
            self.timer_job = self.master.after(1000, self.update_timer)


# Я добавил функцию check_if_game_won() для проверки на заполнение всех квадратиков желтым цветом, тем самым
# показать пользователю о том, что он выиграл
    def check_if_game_won(self):
        all_yellow = all(button.canvas.itemcget(button.id, "fill") == "#FFFF99" for button in self.buttons)
        if all_yellow and not self.game_over:  # Check if game is not already over
            self.game_over = True  # Set game over flag to True
            self.stop_timer()  # Stop the timer
            messagebox.showinfo("Вы выиграли!", "Поздравляем с победой.")
            self.master.destroy()

    def stop_timer(self):
        if self.timer_job is not None:
            self.master.after_cancel(self.timer_job)

if __name__ == "__main__":
    root = Tk()
    app = GameApp(root)
    root.mainloop()
