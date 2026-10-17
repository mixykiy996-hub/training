import csv
import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


CSV_PATH = Path(__file__).resolve().with_name("roster_bk.csv")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padx=12, pady=12)
        self.master = master
        self.pack(fill="both", expand=True)

        try:
            with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
                rows = list(csv.reader(csv_file))
        except (OSError, csv.Error) as error:
            messagebox.showerror(
                "CSV読み込みエラー",
                f"CSVファイルを読み込めませんでした。\n{CSV_PATH}\n{error}",
                parent=master,
            )
            master.destroy()
            return

        if len(rows) < 2:
            messagebox.showerror(
                "CSV読み込みエラー",
                "CSVにデータがありません。",
                parent=master,
            )
            master.destroy()
            return

        self.headers = rows[0]
        self.records = [
            row for row in rows[1:]
            if any(value.strip() for value in row)
        ]

        if not self.records:
            messagebox.showerror(
                "CSV読み込みエラー",
                "CSVに表示できるデータがありません。",
                parent=master,
            )
            master.destroy()
            return

        if any(len(row) != len(self.headers) for row in self.records):
            messagebox.showerror(
                "CSV読み込みエラー",
                "ヘッダー行とデータ行の項目数が一致しない行があります。",
                parent=master,
            )
            master.destroy()
            return

        self.create_widgets()
        self.show_random_record()

    def create_widgets(self):
        tk.Label(
            self,
            text="CSVデータランダム表示",
            font=("", 14, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        self.record_frame = tk.Frame(self)
        self.record_frame.pack(fill="both", expand=True, anchor="nw")

        tk.Button(
            self,
            text="次へ",
            command=self.show_random_record,
        ).pack(anchor="e", pady=(8, 0))

    def show_random_record(self):
        # 現在表示中の項目を消す
        for widget in self.record_frame.winfo_children():
            widget.destroy()

        record = random.choice(self.records)

        # 選んだデータを項目名と値の縦並びで表示
        for header, value in zip(self.headers, record):
            tk.Label(
                self.record_frame,
                text=f"{header}：{value}",
                anchor="w",
                justify="left",
                font=("", 11),
            ).pack(anchor="w", pady=2)


root = tk.Tk()
root.title("CSV取引先一覧")
root.geometry("600x400")

app = Application(master=root)
root.mainloop()

# 取引先IDの表示された内容を入力して処理するアルゴリズムをこちらのファイルに移動させる
# 右側に入力していくように表示する
