import tkinter as tk
import random

GRID_SIZE = 5
NUM_MINES = 5

def launch_minesweeper_game(root, get_points_callback, add_points_callback=None):
    if get_points_callback() < 25:
        tk.messagebox.showinfo("条件未達", "このミニゲームはやる気ポイント25以上で開放されます！")
        return

    game = tk.Toplevel(root)
    game.title("マインスイーパー（5×5）")
    game.geometry("300x300")
    game.resizable(False, False)

    # --- 地雷配置 ---
    mines = set(random.sample(range(GRID_SIZE * GRID_SIZE), NUM_MINES))
    revealed = set()
    buttons = {}

    def count_adjacent_mines(index):
        row, col = divmod(index, GRID_SIZE)
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    idx = r * GRID_SIZE + c
                    if idx in mines:
                        count += 1
        return count

    def reveal_cell(index):
        if index in revealed:
            return
        revealed.add(index)
        btn = buttons[index]
        if index in mines:
            btn.config(text="💣", bg="red", state="disabled")
            tk.messagebox.showinfo("ゲームオーバー", "地雷を踏みました！")
            game.destroy()
        else:
            count = count_adjacent_mines(index)
            btn.config(text=str(count) if count > 0 else "", bg="lightgray", state="disabled")
            if len(revealed) == GRID_SIZE * GRID_SIZE - NUM_MINES:
                tk.messagebox.showinfo("クリア！", "すべての安全なマスを開けました！")
                if add_points_callback:
                    add_points_callback(5)
                    tk.messagebox.showinfo("報酬", "やる気ポイント +5！")
                game.destroy()

    # --- グリッド生成 ---
    for i in range(GRID_SIZE * GRID_SIZE):
        row, col = divmod(i, GRID_SIZE)
        btn = tk.Button(game, width=4, height=2, command=lambda idx=i: reveal_cell(idx))
        btn.grid(row=row, column=col)
        buttons[i] = btn

# © openmurasystem