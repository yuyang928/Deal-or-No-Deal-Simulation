import tkinter as tk
from tkinter import messagebox
import random
from briefcase import Briefcase

# Briefcase values
briefcase_values = [
    0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500,
    750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
    200000, 300000, 400000, 500000, 750000, 1000000
]

# Shuffle values
briefcases = list(range(1, 27))
random.shuffle(briefcase_values)
case_values = dict(zip(briefcases, briefcase_values))

# Game state
player_case = None
available_cases = set(briefcases)
opened_cases = set()
rounds = [6, 5, 4, 3, 2, 1, 1, 1, 1]
current_round = 0
cases_to_open = rounds[current_round]

# Calculate banker offer
def calculate_offer():
    remaining_values = [case_values[case] for case in available_cases if case != player_case]
    return round(sum(remaining_values) / len(remaining_values), 2)

# Animated banker popup
def show_banker_offer(offer, callback):
    popup = tk.Toplevel(root)
    popup.title("Banker's Offer")
    popup.geometry("300x200")
    tk.Label(popup, text="Banker's Offer", font=("Arial", 16)).pack(pady=10)
    amount_label = tk.Label(popup, text="$0", font=("Arial", 20))
    amount_label.pack(pady=10)

    def animate_offer(current=0):
        if current < offer:
            current += max(1, int(offer / 50))  # increment
            amount_label.config(text=f"${current:,.2f}")
            popup.after(30, lambda: animate_offer(current))
        else:
            amount_label.config(text=f"${offer:,.2f}")

    animate_offer()

    def deal():
        popup.destroy()
        callback("yes")

    def no_deal():
        popup.destroy()
        callback("no")

    tk.Button(popup, text="Deal", command=deal, width=10).pack(side="left", padx=20, pady=20)
    tk.Button(popup, text="No Deal", command=no_deal, width=10).pack(side="right", padx=20, pady=20)

# Handle selection
def select_case(briefcase):
    global player_case, cases_to_open, current_round
    if player_case is None:
        player_case = briefcase.number
        available_cases.remove(briefcase.number)
        briefcase.keep()
        status_label.config(text=f"You kept briefcase #{briefcase.number}. Now open {cases_to_open} cases.")
    elif briefcase.number in available_cases and cases_to_open > 0:
        available_cases.remove(briefcase.number)
        opened_cases.add(briefcase.number)
        briefcase.open()
        # Strike-through and color the corresponding value
        value = briefcase.value
        value_labels[value].config(font=("Arial", 12, "overstrike"), fg="red")
        cases_to_open -= 1
        if cases_to_open == 0:
            offer = calculate_offer()
            show_banker_offer(offer, handle_banker_response)

def handle_banker_response(response):
    global current_round, cases_to_open
    if response == "yes":
        messagebox.showinfo("Deal Accepted", f"You accepted the deal. Your case had ${case_values[player_case]:,.2f}.")
        root.quit()
    else:
        current_round += 1
        if current_round < len(rounds):
            cases_to_open = rounds[current_round]
            status_label.config(text=f"Round {current_round + 1}: Open {cases_to_open} cases.")
        else:
            messagebox.showinfo("Game Over", f"All cases opened. Your case had ${case_values[player_case]:,.2f}.")
            root.quit()

# GUI setup
root = tk.Tk()
root.title("Deal or No Deal")

status_label = tk.Label(root, text="Choose your briefcase to keep.", font=("Arial", 14))
status_label.pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack()

briefcase_frame = tk.Frame(main_frame)
briefcase_frame.grid(row=0, column=0, padx=10)

briefcase_objects = {}
for i in range(1, 27):
    bc = Briefcase(briefcase_frame, i, case_values[i], select_case)
    bc.grid(row=(i-1)//7, column=(i-1)%7)
    briefcase_objects[i] = bc

values_frame = tk.Frame(main_frame)
values_frame.grid(row=0, column=1, padx=20)

sorted_values = sorted(briefcase_values)
value_labels = {}
half = len(sorted_values) // 2
for idx, val in enumerate(sorted_values):
    col = 0 if idx < half else 1
    row = idx if idx < half else idx - half
    lbl = tk.Label(values_frame, text=f"${val:,.2f}", font=("Arial", 12), fg="green")
    lbl.grid(row=row, column=col, padx=5, pady=2, sticky="w")
    value_labels[val] = lbl

root.mainloop()