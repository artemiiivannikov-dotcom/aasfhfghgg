import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("600x500")
        
        self.file_path = "weather_data.json"
        self.records = self.load_data()

        # Поля ввода
        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=10, pady=5)
        self.entry_date = tk.Entry(root)
        self.entry_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.entry_date.grid(row=0, column=1)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0, padx=10, pady=5)
        self.entry_temp = tk.Entry(root)
        self.entry_temp.grid(row=1, column=1)

        tk.Label(root, text="Описание:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_desc = tk.Entry(root)
        self.entry_desc.grid(row=2, column=1)

        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Осадки", variable=self.precip_var).grid(row=3, column=1, sticky="w")

        # Кнопки
        tk.Button(root, text="Добавить запись", command=self.add_record).grid(row=4, column=0, columnspan=2, pady=10)
        
        # Фильтры
        filter_frame = tk.LabelFrame(root, text="Фильтрация")
        filter_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        tk.Label(filter_frame, text="Мин. темп:").pack(side="left")
        self.filter_temp = tk.Entry(filter_frame, width=5)
        self.filter_temp.pack(side="left", padx=5)
        
        tk.Button(filter_frame, text="Применить", command=self.update_table).pack(side="left", padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.reset_filter).pack(side="left")

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Темп.")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.update_table()

    def add_record(self):
        date_str = self.entry_date.get()
        temp_str = self.entry_temp.get()
        desc = self.entry_desc.get()
        precip = "Да" if self.precip_var.get() else "Нет"

        # Валидация
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            temp = float(temp_str)
            if not desc: raise ValueError("Пустое описание")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {e}")
            return

        new_record = {"date": date_str, "temp": temp, "desc": desc, "precip": precip}
        self.records.append(new_record)
        self.save_data()
        self.update_table()
        
        # Очистка полей
        self.entry_temp.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)

    def update_table(self):
        # Очистка
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Фильтрация по температуре
        min_t = self.filter_temp.get()
        
        for r in self.records:
            if min_t:
                try:
                    if r['temp'] < float(min_t): continue
                except: pass
            
            self.tree.insert("", tk.END, values=(r['date'], r['temp'], r['desc'], r['precip']))

    def reset_filter(self):
        self.filter_temp.delete(0, tk.END)
        self.update_table()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
