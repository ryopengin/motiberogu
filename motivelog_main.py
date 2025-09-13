import tkinter as tk
from tkinter import messagebox, Toplevel
from motivelog_tasks import (
    init_tasks_table, add_task, update_task, mark_task_completed,
    get_all_incomplete_tasks_detailed, get_completed_tasks, search_tasks_by_keyword
)
from motivelog_rewards import (
    init_motivation_table, add_motivation_point, get_total_points
)
from motivelog_journal import (
    init_journal_table, add_journal_entry, get_journal_entries
)
from minigame_minesweeper import launch_minesweeper_game

# --- ポイントラベル更新 ---
def get_reward_message(points):
    if points >= 100:
        return "🌟 レジェンド級のやる気！"
    elif points >= 50:
        return "💡 応援ボイスをゲット！"
    elif points >= 25:
        return "🎮 マインスイーパー開放中！"
    elif points >= 10:
        return "🚀 やる気上昇中！"
    else:
        return "😄 一歩ずつ前進しよう！"

def update_points_label():
    points = get_total_points()
    points_var.set(f"やる気ポイント：{points}　{get_reward_message(points)}")

# --- タスク関連処理 ---
def complete_task_and_reward(task_id):
    mark_task_completed(task_id)
    add_motivation_point()
    refresh_task_list()
    update_points_label()

def refresh_task_list(filtered_tasks=None):
    for widget in task_frame.winfo_children():
        widget.destroy()
    tasks = filtered_tasks if filtered_tasks else get_all_incomplete_tasks_detailed()
    for i, (task_id, subject, desc, deadline, priority) in enumerate(tasks):
        text = f"{subject} | {desc} | 期限: {deadline} | 優先度: {priority}"
        tk.Label(task_frame, text=text).grid(row=i, column=0, sticky="w", padx=5)
        tk.Button(task_frame, text="完了", command=lambda t=task_id: complete_task_and_reward(t)).grid(row=i, column=1)
        tk.Button(task_frame, text="編集", command=lambda t=task_id, s=subject, d=desc, dl=deadline, p=priority:
                  open_edit_popup(t, s, d, dl, p)).grid(row=i, column=2)

def open_edit_popup(task_id, subject, desc, deadline, priority):
    popup = Toplevel(root)
    popup.title("課題を編集")
    labels = ["科目名", "内容", "期限", "優先度"]
    values = [subject, desc, deadline, priority]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(popup, text=label).grid(row=i, column=0)
        entry = tk.Entry(popup, width=30)
        entry.insert(0, values[i])
        entry.grid(row=i, column=1)
        entries[label] = entry
    tk.Button(popup, text="保存", command=lambda: save_edited_task(task_id, entries, popup)).grid(row=4, column=0, columnspan=2, pady=10)

def save_edited_task(task_id, entries, popup):
    update_task(
        task_id,
        entries["科目名"].get(),
        entries["内容"].get(),
        entries["期限"].get(),
        entries["優先度"].get()
    )
    popup.destroy()
    refresh_task_list()

def search_tasks():
    keyword = search_entry.get()
    if not keyword.strip():
        refresh_task_list()
    else:
        result = search_tasks_by_keyword(keyword)
        refresh_task_list(result)

def show_completed_tasks():
    popup = Toplevel(root)
    popup.title("完了済み課題")
    data = get_completed_tasks()
    if not data:
        tk.Label(popup, text="完了済みの課題はまだありません。").pack(pady=10)
        return
    for tid, subject, desc, deadline, priority in data:
        text = f"{subject} | {desc} | 期限: {deadline} | 優先度: {priority}"
        tk.Label(popup, text=text).pack(anchor="w", padx=10)

# --- 日記機能 ---
def open_journal_input():
    popup = Toplevel(root)
    popup.title("今日の日記を書く")
    tk.Label(popup, text="タイトル：").pack(anchor="w", padx=10)
    title_entry = tk.Entry(popup, width=40)
    title_entry.pack(padx=10)
    tk.Label(popup, text="内容：").pack(anchor="w", padx=10)
    content_text = tk.Text(popup, width=50, height=8)
    content_text.pack(padx=10)

    def save_entry():
        title = title_entry.get()
        body = content_text.get("1.0", tk.END).strip()
        if not title or not body:
            messagebox.showwarning("未入力", "タイトルと内容を入力してください。")
            return
        add_journal_entry(title, body)
        popup.destroy()
        messagebox.showinfo("保存完了", "日記を保存しました。")

    tk.Button(popup, text="保存", command=save_entry).pack(pady=10)

def open_journal_list():
    popup = Toplevel(root)
    popup.title("日記を読む")
    entries = get_journal_entries()
    if not entries:
        tk.Label(popup, text="まだ日記がありません。").pack(pady=10)
        return
    for date_str, title, content in entries:
        tk.Label(popup, text=f"{date_str} - {title}", font=("Helvetica", 10, "bold")).pack(anchor="w", padx=10, pady=(8,2))
        tk.Message(popup, text=content, width=500).pack(anchor="w", padx=20)

# --- アプリ起動 ---
def launch_app():
    global root, task_frame, search_entry, points_var
    root.title("モチべろぐ - 学習とやる気のデスクトップアシスタント")

    form = tk.Frame(root, padx=10, pady=5)
    form.pack()
    labels = ["科目名", "内容", "期限", "優先度"]
    inputs = {}
    for i, label in enumerate(labels):
        tk.Label(form, text=label).grid(row=i, column=0)
        entry = tk.Entry(form, width=30)
        entry.grid(row=i, column=1)
        inputs[label] = entry

    def add_new_task():
        add_task(
            inputs["科目名"].get(),
            inputs["内容"].get(),
            inputs["期限"].get(),
            inputs["優先度"].get()
        )
        for entry in inputs.values():
            entry.delete(0, tk.END)
        refresh_task_list()

    tk.Button(form, text="課題を追加", command=add_new_task).grid(row=4, column=0, columnspan=2, pady=8)

    points_var = tk.StringVar()
    tk.Label(root, textvariable=points_var, font=("Helvetica", 12, "bold"), fg="green").pack()
    update_points_label()

    control = tk.Frame(root)
    control.pack(pady=5)
    search_entry = tk.Entry(control, width=25)
    search_entry.grid(row=0, column=0, padx=5)
    tk.Button(control, text="検索", command=search_tasks).grid(row=0, column=1)
    tk.Button(control, text="すべて表示", command=refresh_task_list).grid(row=0, column=2, padx=2)
    tk.Button(control, text="完了履歴", command=show_completed_tasks).grid(row=0, column=3)

    actions = tk.Frame(root)
    actions.pack(pady=5)
    tk.Button(actions, text="今日の日記を書く", command=open_journal_input).pack(side="left", padx=5)
    tk.Button(actions, text="日記を読む", command=open_journal_list).pack(side="left", padx=5)
    tk.Button(actions, text="マインスイーパー 🎮", command=lambda: launch_minesweeper_game(root, get_total_points, add_motivation_point)).pack(side="left", padx=5)

    task_frame = tk.Frame(root, padx=10, pady=10)
    task_frame.pack()
    refresh_task_list()

    # 著作権表記（控えめ）
    tk.Label(root, text="© openmura_system", font=("Helvetica", 8), fg="gray").pack(side="bottom", pady=3)

    root.mainloop()

if __name__ == "__main__":
    init_tasks_table()
    init_motivation_table()
    init_journal_table()
    root = tk.Tk()
    launch_app()