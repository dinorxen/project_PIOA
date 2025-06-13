import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import tkinter as tk
from tkinter import ttk, messagebox
import textwrap

class SleepHealthAnalyzer:
    def __init__(self, path="Sleep_health_and_lifestyle_dataset.csv"):
        self.df = self.read_file(path)
        self.setup_quality_categories()

    def read_file(self, path):
        try:
            df = pd.read_csv(path, encoding='utf-8')
            return df.dropna()
        except FileNotFoundError:
            self.show_error_message(f"Файл '{path}' не найден. Проверь путь и повтори попытку.")
            return pd.DataFrame()
        except Exception as e:
            self.show_error_message(f"Не удалось загрузить данные:\n{e}")
            return pd.DataFrame()

    def setup_quality_categories(self):
        if not self.df.empty:
            sleep_quality_bins = [0, 3, 6, 10]
            sleep_quality_labels = ['Плохое', 'Среднее', 'Хорошее']
            self.df['Категория качества сна'] = pd.cut(
                self.df['Quality of Sleep'],
                bins=sleep_quality_bins,
                labels=sleep_quality_labels,
                include_lowest=True
            )

    def show_error_message(self, message):
        messagebox.showerror("Ошибка", textwrap.fill(message, width=60))

    def show_full_dataset(self):
        if self.df.empty:
            self.show_error_message("Нет данных для отображения")
            return

        root = tk.Tk()
        root.title('Полный датасет')
        root.geometry('1000x600')

        tree = ttk.Treeview(root, columns=list(self.df.columns), show='headings')
        vsb = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
        hsb = ttk.Scrollbar(root, orient='horizontal', command=tree.xview)
        
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        for col in self.df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='w')

        for idx, row in enumerate(self.df.head(200).itertuples(index=False), start=1):
            tree.insert('', 'end', values=row, tags=('evenrow' if idx % 2 == 0 else 'oddrow',))

        tree.tag_configure('oddrow', background='#f9f9f9')
        tree.tag_configure('evenrow', background='#ffffff')

        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        tree.pack(fill='both', expand=True)
        
        root.mainloop()

    def show_analytics(self):
        if self.df.empty:
            messagebox.showerror("Ошибка", "Нет данных для анализа")
            return

        fig1 = px.bar(self.df, 
                     x='Stress Level', 
                     y='Quality of Sleep', 
                     color='Stress Level', 
                     title='Уровень стресса и качество сна',
                     labels={'Stress Level': 'Уровень стресса', 'Quality of Sleep': 'Качество сна'})
        fig1.show()


        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Daily Steps', y='Sleep Duration', data=self.df, hue='Quality of Sleep', palette='viridis')
        plt.title('Качество сна в зависимости от количества шагов в день')
        plt.xlabel('Количество шагов в день')
        plt.ylabel('Качество сна (часы)')
        plt.legend(title='Качество сна')
        plt.show()

        color_palette = {'Male': 'lightblue', 'Female': 'lightcoral'}
        plt.figure(figsize=(10, 6))
        sns.violinplot(x='Gender', y='Quality of Sleep', data=self.df, palette=color_palette)
        plt.title('Распределение качества сна по полу', fontsize=16)
        plt.xlabel('Пол', fontsize=12)
        plt.ylabel('Качество сна', fontsize=12)
        plt.show()

        categories = ['Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Stress Level', 'Heart Rate', 'Daily Steps']
        colors = ["#59a6dd", "#ffa75b", "#80f580", "#f76666", "#c792f8", "#fd9d89"]

        normalized_values = []
        for category in categories:
            max_val = self.df[category].max()
            min_val = self.df[category].min()
            norm_val = ((self.df[category].mean() - min_val) / (max_val - min_val)) * 100
            normalized_values.append(norm_val)

        width = 2 * np.pi / len(categories)
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        angles = np.arange(len(categories)) * width
        bars = ax.bar(angles, normalized_values, width=width, color=colors, alpha=1, edgecolor='black', linewidth=1.5)

        circle_angles = np.linspace(0, 2 * np.pi, 100)
        circle_radius = np.full_like(circle_angles, 100)
        ax.plot(circle_angles, circle_radius, linestyle='--', color='grey', linewidth=1)

        ax.text(np.pi/2, 105, '100 — максимум', ha='center', va='bottom', fontsize=9, color='grey')

        for i, (label, angle) in enumerate(zip(categories, angles)):
            x = angle
            y = normalized_values[i] + 5
            ax.text(x, y, f"{label}\n{normalized_values[i]:.1f}", ha='center', va='center', fontsize=8, color='black')

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_ylim(0, 110)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.spines['polar'].set_visible(False)
        plt.title('Нормализованные средние значения признаков (100 = максимум)')
        plt.tight_layout()
        plt.show()


    def run(self):
        while True:
            print('Меню:')
            print('1. Показать датасет')
            print('2. Показать диаграммы')
            print('3. Выйти из программы')
            
            choice = input('Введите значение: ').strip()
            
            if choice == '1':
                self.show_full_dataset()
            elif choice == '2':
                self.show_analytics()
            elif choice == '3':
                print("Завершение работы")
                break
            else:
                print('Неверный ввод')

if __name__ == '__main__':
    analyzer = SleepHealthAnalyzer()
    analyzer.run()