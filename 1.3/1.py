import customtkinter as ctk
import tkinter as tk


class MainWindow(ctk.CTk):
    def __init__(self):

        super().__init__()

        # Создаем пустые строки для хранения температур
        self.fahrenheit_str = ''
        self.celsius_str = ''
        self.kelvin_str = ''
        # Устанавливаем заголовок окна
        self.title("Конвертер градусов")
        # Устанавливаем размеры окна
        self.geometry("580x200")
        self.minsize(580, 200)

        # Настройка шириной колонок и строк для оформления сетки
        self.grid_columnconfigure((1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 4), weight=2)
        self.grid_rowconfigure((0, 5), weight=1)

        # Создаем метку с текстом "Введите градусы Fahrenheit"
        self.label_fahrenheit = ctk.CTkLabel(self, text="Градусы Фаренгейта: ")
        self.label_fahrenheit.grid(row=1, column=1, padx=(25, 10), pady=(25, 10), sticky='e')

        # Создаем поле ввода
        self.entry_fahrenheit = ctk.CTkEntry(self, placeholder_text="Введите температуру")
        self.entry_fahrenheit.grid(row=1, column=2, padx=(10, 10), pady=(25, 10), sticky='we')

        # Создаем кнопку "Преобразовать"
        self.button_convert = ctk.CTkButton(self, text="Преобразовать", command=self.convert)
        self.button_convert.grid(row=1, column=3, rowspan=3, padx=(10, 10), pady=(25, 10), sticky='we')

        # Создаем метку для вывода результата
        self.label_celsius = ctk.CTkLabel(self, text="Градусы Цельсия: ")
        self.label_celsius.grid(row=2, column=1, padx=(25, 10), pady=(10, 10), sticky='e')

        # Создаем поле вывода градусов Цельсия
        self.entry_celsius = ctk.CTkEntry(self, placeholder_text="Введите температуру")
        self.entry_celsius.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky='we')

        # Создаем метку для вывода результата
        self.label_kelvin = ctk.CTkLabel(self, text="Градусы Кельвина: ")
        self.label_kelvin.grid(row=3, column=1, padx=(25, 10), pady=(10, 10), sticky='e')

        # Создаем поле вывода градусов Кельвина
        self.entry_kelvin = ctk.CTkEntry(self, placeholder_text="Введите температуру")
        self.entry_kelvin.grid(row=3, column=2, padx=(10, 10), pady=(10, 10), sticky='we')

        # Создаем метку для вывода предупреждения
        self.label_warning = ctk.CTkLabel(self, text="")
        self.label_warning.grid(row=4, column=1, columnspan=3,  padx=(25, 25), pady=(10, 25), sticky='we')

    def convert(self):
        """Функция для преобразования градусов Фаренгейта и градусов Цельсия"""
        # Получаем значение из поля ввода Fahrenheit
        if self.fahrenheit_str != self.entry_fahrenheit.get():
            print('будем преобразовывать из F')
            self.fahrenheit_str = self.entry_fahrenheit.get()
            fahrenheit = self.entry_fahrenheit.get() # Получаем значение из поля ввода

            try:
                fahrenheit = float(fahrenheit)  # Преобразуем строку в число с плавающей запятой
                self.label_warning.configure(text="")  # Убираем предупреждение при правильном вводе
                # Вычисляем значение в градусах Цельсия
                celsius = (fahrenheit - 32) * 5 / 9
                kelvin = celsius + 273.15 # Переводим в Кельвины

                # Устанавливаем результат в поле вывода Celsius
                self.entry_celsius.delete(0, tk.END)  # Очищаем поле вывода
                self.entry_celsius.insert(0, str(round(celsius, 2)))  # Вставляем результат
                self.celsius_str = str(round(celsius, 2))  # Сохраняем результат в строку

                # Устанавливаем результат в поле вывода Kelvin
                self.entry_kelvin.delete(0, tk.END)
                self.entry_kelvin.insert(0, str(round(kelvin, 2)))
                self.kelvin_str = str(round(kelvin, 2))
            except ValueError:
                # Выводим предупреждение о некорректных данных
                self.label_warning.configure(text="Введите числовое значение", text_color='red')

        elif self.celsius_str != self.entry_celsius.get():
            print('будем преобразовывать из C')
            self.celsius_str = self.entry_celsius.get()
            celsius = self.entry_celsius.get()

            try:
                celsius = float(celsius)
                self.label_warning.configure(text="")
                fahrenheit = 9 / 5 * celsius + 32
                kelvin = celsius + 273.15

                # Устанавливаем результат в поле вывода Fahrenheit
                self.entry_fahrenheit.delete(0, tk.END)
                self.entry_fahrenheit.insert(0, str(round(fahrenheit, 2)))
                self.fahrenheit_str = str(round(fahrenheit, 2))

                # Устанавливаем результат в поле вывода Kelvin
                self.entry_kelvin.delete(0, tk.END)
                self.entry_kelvin.insert(0, str(round(kelvin, 2)))
                self.kelvin_str = str(round(kelvin, 2))
            except ValueError:
                # Выводим предупреждение о некорректных данных
                self.label_warning.configure(text="Введите числовое значение", text_color='red')

        elif self.kelvin_str != self.entry_kelvin.get():
            print('будем преобразовывать из K')
            self.kelvin_str = self.entry_kelvin.get()
            kelvin = self.entry_kelvin.get()

            try:
                kelvin = float(kelvin)
                if kelvin < 0:
                    self.label_warning.configure(text="Температура в Кельвинах > 0", text_color='red')
                else:
                    self.label_warning.configure(text="")
                    fahrenheit = 9 / 5 * (kelvin - 273.15) + 32
                    celsius = kelvin - 273.15

                    # Устанавливаем результат в поле вывода Fahrenheit
                    self.entry_fahrenheit.delete(0, tk.END)
                    self.entry_fahrenheit.insert(0, str(round(fahrenheit, 2)))
                    self.fahrenheit_str = str(round(fahrenheit, 2))

                    # Устанавливаем результат в поле вывода Celsius
                    self.entry_celsius.delete(0, tk.END)
                    self.entry_celsius.insert(0, str(round(celsius, 2)))
                    self.celsius_str = str(round(celsius, 2))
            except ValueError:
                # Выводим предупреждение о некорректных данных
                self.label_warning.configure(text="Введите числовое значение", text_color='red')


if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
