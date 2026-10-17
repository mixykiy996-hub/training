import csv
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

# csvを読み込む
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
                "CSVに2行目がありません。",
                parent=master,
            )
            master.destroy()
            return

        headers = rows[0]
        record = rows[1]

        if len(headers) != len(record):
            messagebox.showerror(
                "CSV読み込みエラー",
                "ヘッダー行とデータ行の項目数が一致しません。",
                parent=master,
            )
            master.destroy()
            return

        self.create_widgets(headers, record) # コピーさせないようにする

    def create_widgets(self, headers, record):  # コピーさせないようにする
        tk.Label(
            self,
            text="CSVの2行目",
            font=("", 14, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        # 項目名と値を1行ずつ表示する
        for header, value in zip(headers, record):
            tk.Label(
                self,
                text=f"{header}：{value}",
                anchor="w",
                justify="left",
                font=("", 11),
            ).pack(anchor="w", pady=2)

        tk.Button(
            self,
            text="終了",
            fg="red",
            command=self.master.destroy,
        ).pack(anchor="e", pady=(8, 0))


root = tk.Tk()
root.title("CSV取引先一覧")
root.geometry("600x400")
app = Application(master=root)
root.mainloop()
