import tkinter as tk
import tkinter.ttk as ttk
import pyperclip

hvs_for_gvs = 45.9
hvs = 45.9
heating = 2858.45
t1 = 6.16
t2 = 2.43
internet = 675

table = ""



def calc_service():
    results = calculate_totals()

    result_label.config(text=f"Итого включая интернет 675р : {results[6]}")


def calculate_totals():
    in_hvs = float(hvs_entry.get())
    in_hvs_for_gvs = float(hvs_for_gvs_entry.get())
    in_heating = float(heating_entry.get())
    in_t1 = float(t1_entry.get())
    in_t2 = float(t2_entry.get())

    total_hvs = in_hvs * hvs
    total_hvs_for_gvs = in_hvs_for_gvs * hvs_for_gvs
    total_heating = in_heating * heating
    total_t1 = in_t1 * t1
    total_t2 = in_t2 * t2

    rounded_hvs = round(total_hvs, 2)
    rounded_hvs_for_gvs = round(total_hvs_for_gvs, 2)
    rounded_heating = round(total_heating, 2)
    rounded_t1 = round(total_t1, 2)
    rounded_t2 = round(total_t2, 2)

    total_price = rounded_hvs + rounded_hvs_for_gvs + rounded_heating + rounded_t1 + rounded_t2 + internet
    rounded_total_price = round(total_price, 2)

    return rounded_hvs, rounded_hvs_for_gvs, rounded_heating, rounded_t1, rounded_t2, internet, rounded_total_price


def show_table():
    results = calculate_totals()
    table_window = tk.Toplevel()
    table_window.title("Таблица расчета")
    table_window.resizable(True, True)

    # Создаем Treeview
    global table
    table = ttk.Treeview(table_window, columns=("Расход", "Цена", "Стоимость", "Счетчик"))
    table.heading("#0", text="Источник")
    table.heading("Расход", text="Расход")
    table.heading("Цена", text="Цена")
    table.heading("Стоимость", text="Стоимость")
    table.heading("Счетчик", text="Счетчик")
    table.pack(side="left", fill="both", expand=True)

    # Добавляем строки в Treeview
    table.insert("", "end", text="ХВС", values=(hvs_entry.get(), hvs, results[0], ""))
    table.insert("", "end", text="ХВС для ГВС", values=(hvs_for_gvs_entry.get(), hvs_for_gvs, results[1], ""))
    table.insert("", "end", text="Нагрев воды", values=(heating_entry.get(), heating, results[2], ""))
    table.insert("", "end", text="Тариф 1", values=(t1_entry.get(), t1, results[3], ""))
    table.insert("", "end", text="Тариф 2", values=(t2_entry.get(), t2, results[4], ""))
    table.insert("", "end", text="Интернет", values=("", "", internet, ""))
    table.insert("", "end", text="Итого к оплате", values=("", "", "", results[6]))

    copy_button = tk.Button(table_window, text="Скопировать", command=copy_table_to_clipboard)
    copy_button.pack()


def copy_table_to_clipboard():
    # Создаем временный виджет для копирования данных в буфер обмена
    temp = tk.Tk()
    temp.withdraw()

    # Получаем выделенные ячейки
    selected = table.selection()

    # Получаем заголовки столбцов
    headers = [table.heading(col)["text"] for col in table["columns"]]

    # Создаем строку с заголовками, разделенными табуляцией
    headers_row = "\t".join(headers) + "\n"

    # Создаем строку с данными, разделенными табуляцией

    data_rows = ""
    for row_id in selected:
        data = [table.item(row_id)["text"]] + [table.set(row_id, col) for col in table["columns"][1:]]
        data_rows += "\t".join(data) + "\n"

        # Соединяем заголовки и данные
    clipboard_data = headers_row + data_rows

    # Копируем данные в буфер обмена

    table.clipboard_append(clipboard_data)



root = tk.Tk()
root.title("Расчет услуг")
root.geometry("400x300")

# ХВС
hvs_label = tk.Label(root, text="Кол-во расхода холодной воды:")
hvs_label.pack()

hvs_entry = tk.Entry(root)
hvs_entry.pack()

# ГВС
hvs_for_gvs_label = tk.Label(root, text="Кол-во расхода горячей воды:")
hvs_for_gvs_label.pack()

hvs_for_gvs_entry = tk.Entry(root)
hvs_for_gvs_entry.pack()

# Нагрев
heating_label = tk.Label(root, text="Расход нагрева воды:")
heating_label.pack()

heating_entry = tk.Entry(root)
heating_entry.pack()

# T1
t1_label = tk.Label(root, text="Расход Т1:")
t1_label.pack()

t1_entry = tk.Entry(root)
t1_entry.pack()

# T2
t2_label = tk.Label(root, text="Расход Т2:")
t2_label.pack()

t2_entry = tk.Entry(root)
t2_entry.pack()

# Кнопка "Рассчитать"
calc_button = tk.Button(root, text="Рассчитать", command=calc_service)
calc_button.pack()

# Кнопка "Вывести в таблицу"

table_button = tk.Button(root, text="Вывести в таблицу", command=show_table)
table_button.pack()

# Результат расчета
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()