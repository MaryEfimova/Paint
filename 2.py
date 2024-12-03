import customtkinter as ctk
from tkinter.colorchooser import askcolor


class DrawingTools:
    """Класс используемого инструмента рисования"""

    def __init__(self):
        # Настройки инструмента рисования по умолчанию
        self.selected_tool = "pen"
        self.color = "#000000"
        self.width = 10

    def use_pen(self, pen_button, line_button):
        """Функция смены используемого инструмента на карандаш"""
        self.selected_tool = "pen"
        pen_button.configure(border_width=2)  # Увеличить ширину рамки кнопки карандаша
        line_button.configure(border_width=0)  # Уменьшить ширину рамки кнопки линии

    def use_line(self, pen_button, line_button):
        """Функция смены используемого инструмента на линию"""
        self.selected_tool = "line"
        pen_button.configure(border_width=0)
        line_button.configure(border_width=2)

    def choose_color(self):
        """Функция смены цвета используемого инструмента"""
        self.color = askcolor()[1]  # открыть диалог выбора цвета и сохранить выбранный цвет

    def choose_width(self, value):
        """Функция смены толщины используемого инструмента"""
        self.width = value  # Установить ширину инструмента на указанное значение


class PaintWindow(ctk.CTk):
    """Класс окна приложения для рисования"""

    def __init__(self):
        super().__init__()
        self.title("Редактор рисунков")

        # Устанавливаем размеры окна
        self.geometry("800x600")
        self.minsize(720, 200)

        # Настройка конфигурации строк и столбцов для сетки
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_columnconfigure((0, 2), weight=1)

        # Создаем экземпляр класса инструментов рисования
        self.tool = DrawingTools()

        # Создание и размещение холста
        self.canvas = ctk.CTkCanvas(self, bg="white")
        self.canvas.grid(row=0, column=1, padx=(10, 10), pady=(25, 10), sticky='nswe')

        # Создание и размещение фрейма настройки инструмента
        self.toolbar = ctk.CTkFrame(self)  # Создаем фрейм для кнопок
        self.toolbar.grid(row=1, column=0, columnspan=3, padx=(0, 0), pady=(10, 0), sticky='nswe')

        self.toolbar.grid_columnconfigure((0, 5), weight=1)

        # Создание и размещение кнопки выбора карандаша
        self.pen_button = ctk.CTkButton(self.toolbar, text="Карандаш", border_color='red', border_width=2)
        self.pen_button.grid(row=0, column=1, padx=(25, 10), pady=(25, 25))

        # Создание и размещение кнопки выбора линии
        self.line_button = ctk.CTkButton(self.toolbar, text="Линия", border_color='red')
        self.line_button.grid(row=0, column=2, padx=(10, 10), pady=(25, 25))

        # Подключаем вызов функций смены инструмента к кнопкам
        self.pen_button.configure(command=lambda: self.tool.use_pen(self.pen_button, self.line_button))
        self.line_button.configure(command=lambda: self.tool.use_line(self.pen_button, self.line_button))

        # Создание и размещение кнопки выбора цвета инструмента
        self.color_button = ctk.CTkButton(self.toolbar, text="Цвет", command=self.tool.choose_color)
        self.color_button.grid(row=0, column=3, padx=(10, 10), pady=(25, 25))

        # Создание и размещение кнопки выбора толщины инструмента
        self.width_slider = ctk.CTkSlider(self.toolbar, from_=10, to=100)
        self.width_slider.grid(row=0, column=4, padx=(10, 25), pady=(25, 25))
        self.width_slider.set(self.tool.width)   # Установить ползунок на текущее значение ширины

        # Обработка событий изменения ширины
        self.width_slider.bind("<B1-Motion>", lambda event: self.tool.choose_width(self.width_slider.get()))
        self.width_slider.bind("<Button-1>", lambda event: self.tool.choose_width(self.width_slider.get()))

        self.arr = []  # Массив линий на холсте(линия)
        self.past_x = None  # Координата по x предыдущей точки(карандаш)
        self.past_y = None  # Координата по y предыдущей точки(карандаш)

        # Привязка событий мыши к соответствующим методам
        self.canvas.bind("<Button-1>", self.start_draw)  # Вызов функции при зажатии левой кнопки мыши
        self.canvas.bind("<B1-Motion>", self.draw)  # Вызов функции при движении мыши с зажатой л. кн. мыши
        self.canvas.bind("<ButtonRelease>", self.delete)  # Вызов функции когда пользователь отпускает мышь

    def delete(self, event):
        """Функция сбрасывания координат последней точки"""
        self.past_x = None
        self.past_y = None

    def draw(self, event):
        """Функция осуществляющая рисование на холсте"""
        # Если используемый инструмент карандаш
        if self.tool.selected_tool == "pen":
            # Если предыдущей точки нет, берем координаты начальной точки
            if self.past_x is None:
                self.past_x = self.start_x
                self.past_y = self.start_y

            # Рисуем линию от предыдущей точки до текущей
            self.canvas.create_line(self.past_x, self.past_y, event.x, event.y, fill=self.tool.color,
                                    width=self.tool.width, capstyle=ctk.ROUND)

            # В переменные координат предыдущей точки записываем координаты текущей
            self.past_x = event.x
            self.past_y = event.y

        # Если используемый инструмент линия
        elif self.tool.selected_tool == "line":
            # Удаляем с холста последний элемент из массива тк будем создавать другой
            self.canvas.delete(self.arr.pop())
            # Рисуем линию от начальной точки до текущей и сохраняем ее
            self.arr.append(self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, capstyle=ctk.ROUND,
                                                    fill=self.tool.color, width=self.tool.width))

    def start_draw(self, event):
        """Функция сохранения координат начальной точки для рисования нового элемента"""
        self.arr.append('')
        self.start_x = event.x
        self.start_y = event.y


if __name__ == "__main__":
    app = PaintWindow()
    app.mainloop()

