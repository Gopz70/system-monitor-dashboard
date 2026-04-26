import os
import time
import threading
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

running = False

# ----------- DATA STORAGE FOR ANALYSIS -----------
cpu_history = []
ram_history = []

# ----------- NETWORK GLOBALS -----------
prev_sent = 0
prev_received = 0

# ----------- SYSTEM FUNCTIONS -----------

def get_cpu():
    return int(os.popen("wmic cpu get loadpercentage").read().strip().split("\n")[-1])


def get_ram():
    output = os.popen("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value").read()
    lines = output.split()

    free = int(lines[0].split("=")[1])
    total = int(lines[1].split("=")[1])

    used = total - free

    used_gb = round(used / (1024 * 1024), 2)
    total_gb = round(total / (1024 * 1024), 2)

    percent = round((used / total) * 100, 2)

    return percent, used_gb, total_gb


def get_disk():
    total, used, free = shutil.disk_usage("C:\\")

    used_gb = round(used / (1024**3), 2)
    total_gb = round(total / (1024**3), 2)

    percent = round((used / total) * 100, 2)

    return percent, used_gb, total_gb


def get_network():
    global prev_sent, prev_received

    output = os.popen('netstat -e').read().split("\n")

    for line in output:
        if "Bytes" in line:
            parts = line.split()
            try:
                received = int(parts[1])
                sent = int(parts[2])
            except:
                return 0, 0

            if prev_sent == 0 and prev_received == 0:
                prev_sent = sent
                prev_received = received
                return 0, 0

            sent_rate = sent - prev_sent
            recv_rate = received - prev_received

            prev_sent = sent
            prev_received = received

            sent_mb = round(sent_rate / (1024 * 1024), 2)
            recv_mb = round(recv_rate / (1024 * 1024), 2)

            return sent_mb, recv_mb

    return 0, 0


def get_processes():
    output = os.popen("tasklist").read().split("\n")[3:]
    process_list = []

    for line in output:
        parts = line.split()
        if len(parts) < 5:
            continue

        name = parts[0]
        memory = parts[-2].replace(",", "")

        try:
            memory = int(memory)
        except:
            memory = 0

        if name.lower() in ["system", "registry", "smss.exe"]:
            continue

        process_list.append((name, memory))

    process_list.sort(key=lambda x: x[1], reverse=True)

    return [f"{p[0]}  -  {p[1]} KB" for p in process_list[:5]]


# ----------- ALERT SYSTEM -----------

def check_alerts(cpu, ram, disk):
    if cpu > 90:
        messagebox.showwarning("Alert", "⚠ High CPU Usage!")
    if ram > 90:
        messagebox.showwarning("Alert", "⚠ High RAM Usage!")
    if disk > 95:
        messagebox.showwarning("Alert", "⚠ Disk Almost Full!")


# ----------- SAVE DATA -----------

def save_data(cpu, ram):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("system_data.csv", "a") as f:
        f.write(f"{now},{cpu},{ram}\n")

    with open("system_log.txt", "a") as f:
        f.write(f"\nTime: {now}\nCPU: {cpu}%\nRAM: {ram}%\n")


# ----------- SUMMARY REPORT -----------

def generate_summary():
    if not cpu_history or not ram_history:
        return

    max_cpu = max(cpu_history)
    avg_cpu = round(sum(cpu_history) / len(cpu_history), 2)

    max_ram = max(ram_history)
    avg_ram = round(sum(ram_history) / len(ram_history), 2)

    with open("report.html", "w") as f:
        f.write(f"""
        <html><body style='background:black;color:white;font-family:Arial'>
        <h2>System Summary Report</h2>
        <p><b>Max CPU:</b> {max_cpu}%</p>
        <p><b>Avg CPU:</b> {avg_cpu}%</p>
        <p><b>Max RAM:</b> {max_ram}%</p>
        <p><b>Avg RAM:</b> {avg_ram}%</p>
        </body></html>
        """)


# ----------- MONITOR LOOP -----------

def monitor():
    global running
    while running:
        cpu = get_cpu()
        ram_percent, ram_used, ram_total = get_ram()
        disk_percent, disk_used, disk_total = get_disk()
        sent, received = get_network()
        processes = get_processes()

        # Store history
        cpu_history.append(cpu)
        ram_history.append(ram_percent)

        cpu_label.config(text=f"CPU Usage: {cpu}%")
        ram_label.config(text=f"RAM Usage: {ram_percent}% ({ram_used} GB / {ram_total} GB)")
        disk_label.config(text=f"Disk Usage: {disk_percent}% ({disk_used} GB / {disk_total} GB)")
        network_label.config(text=f"Network: ↑ {sent} MB | ↓ {received} MB")

        cpu_bar['value'] = cpu
        ram_bar['value'] = ram_percent
        disk_bar['value'] = disk_percent

        if cpu < 50:
            status_label.config(text="Status: Normal", fg="lightgreen")
        elif cpu < 80:
            status_label.config(text="Status: Medium Load", fg="yellow")
        else:
            status_label.config(text="Status: HIGH LOAD ⚠", fg="red")

        process_box.delete(0, tk.END)
        for p in processes:
            process_box.insert(tk.END, p)

        check_alerts(cpu, ram_percent, disk_percent)
        save_data(cpu, ram_percent)

        time.sleep(2)


# ----------- BUTTONS -----------

def start_monitor():
    global running
    if not running:
        running = True
        threading.Thread(target=monitor, daemon=True).start()


def stop_monitor():
    global running
    running = False
    generate_summary()
    root.destroy()


# ----------- GUI -----------

root = tk.Tk()
root.title("System Monitor")
root.geometry("520x700")
root.configure(bg="#121212")

title = tk.Label(root, text="System Health Dashboard",
                 font=("Arial", 16, "bold"),
                 bg="#121212", fg="white")
title.pack(pady=10)

cpu_label = tk.Label(root, text="CPU Usage: --%", bg="#121212", fg="white")
cpu_label.pack()

cpu_bar = ttk.Progressbar(root, length=350, maximum=100)
cpu_bar.pack(pady=5)

ram_label = tk.Label(root, text="RAM Usage: --%", bg="#121212", fg="white")
ram_label.pack()

ram_bar = ttk.Progressbar(root, length=350, maximum=100)
ram_bar.pack(pady=5)

disk_label = tk.Label(root, text="Disk Usage: --%", bg="#121212", fg="white")
disk_label.pack()

disk_bar = ttk.Progressbar(root, length=350, maximum=100)
disk_bar.pack(pady=5)

network_label = tk.Label(root, text="Network: --", bg="#121212", fg="cyan")
network_label.pack(pady=5)

status_label = tk.Label(root, text="Status: --",
                        font=("Arial", 12, "bold"),
                        bg="#121212")
status_label.pack(pady=10)

frame = tk.Frame(root, bg="#121212")
frame.pack(pady=10)

start_btn = tk.Button(frame, text="Start", command=start_monitor,
                      bg="green", fg="white", width=10)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(frame, text="Stop", command=stop_monitor,
                     bg="red", fg="white", width=10)
stop_btn.grid(row=0, column=1, padx=10)

proc_title = tk.Label(root, text="Top Processes (by Memory)",
                      bg="#121212", fg="white",
                      font=("Arial", 12, "bold"))
proc_title.pack(pady=5)

frame_list = tk.Frame(root)
frame_list.pack()

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

process_box = tk.Listbox(frame_list, width=65, height=10,
                         bg="#1e1e1e", fg="white",
                         yscrollcommand=scrollbar.set)

process_box.pack(side=tk.LEFT)
scrollbar.config(command=process_box.yview)

root.mainloop()