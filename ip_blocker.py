import sys
import os
import tkinter as tk
from tkinter import messagebox
import subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f'{width}x{height}+{x}+{y}')

def validate_ip_prefix(ip):
    if not ip:
        return False
    if not all(c.isdigit() or c == '.' for c in ip):
        return False
    if ip.count('.') != 1:
        return False
    if ip.startswith('.') or ip.endswith('.'):
        return False
    segments = ip.split('.')
    if len(segments) != 2:
        return False
    for segment in segments:
        if not segment.isdigit():
            return False
        value = int(segment)
        if value < 1 or value > 255:
            return False
    return True

def validate_ip_prefixes(ips_text):
    ips = []
    lines = ips_text.strip().splitlines()
    for line in lines:
        ip = line.strip()
        if not ip:
            continue
        if not validate_ip_prefix(ip):
            return False, f"Invalid IP detected: {ip}"
        ips.append(ip)
    if not ips:
        return False, "No valid IP detected."
    return True, ips

def get_existing_ips(rule_name):
    try:
        result = subprocess.run(['netsh', 'advfirewall', 'firewall', 'show', 'rule', f'name={rule_name}'], capture_output=True, text=True, check=True)
        output = result.stdout
        for line in output.splitlines():
            if line.strip().startswith("RemoteIP"):
                ips = line.split(':', 1)[1].strip()
                return ips
    except subprocess.CalledProcessError:
        return None

def on_block_ip():
    rule_name = rule_name_box.get().strip()
    ips_text = ip_box.get("1.0", "end").strip()

    if not rule_name or rule_name == "RULES NAME":
        messagebox.showerror("Error", "You must enter a valid rule name.")
        return

    if placeholder_active and (not ips_text or ips_text == ip_placeholder):
        messagebox.showerror("Error", "You must enter at least one IP prefix.")
        return

    valid, result = validate_ip_prefixes(ips_text)
    if not valid:
        messagebox.showerror("Error", result)
        return

    ips = result

    existing_ips_str = get_existing_ips(rule_name)
    existing_ips = []
    if existing_ips_str:
        existing_ips = [ip.strip() for ip in existing_ips_str.split(',')]

    new_ranges = []
    for ip_prefix in ips:
        ip_range = f"{ip_prefix}.1.1-{ip_prefix}.255.255"
        if ip_range not in existing_ips:
            new_ranges.append(ip_range)

    if not new_ranges:
        messagebox.showinfo("Info", "All IP ranges are already in the rule.")
        return

    all_ips = existing_ips + new_ranges
    seen = set()
    all_ips = [x for x in all_ips if not (x in seen or seen.add(x))]

    try:
        if existing_ips:
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', f'name={rule_name}'], check=True)
        ips_str = ','.join(all_ips)
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', f'name={rule_name}', 'dir=in', 'action=block', f'remoteip={ips_str}'], check=True)
        subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', f'name={rule_name}', 'dir=out', 'action=block', f'remoteip={ips_str}'], check=True)
        messagebox.showinfo("Success", f"Blocking rule '{rule_name}' updated with {len(new_ranges)} new IP range(s).")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Execution error: {e}")

root = tk.Tk()
root.title("IP BLOCKER")
root.geometry("500x400")
root.configure(bg="#2e2e2e")
root.minsize(400, 300)

root.iconbitmap(resource_path("icon.ico"))

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)

title = tk.Label(root, text="IP BLOCKER", font=("Segoe UI", 24, "bold"), fg="#ff4747", bg="#2e2e2e")
title.grid(row=0, column=0, pady=(10,5), sticky="n")

rule_name_box = tk.Entry(root, font=("Segoe UI", 12), bd=2, relief="solid", fg="white", bg="#444", insertbackground="white", justify="center")
rule_name_box.insert(0, "RULES NAME")
rule_name_box.grid(row=1, column=0, padx=20, sticky="ew")

ip_placeholder = (
    "Enter one or more IP prefixes, one per line\n"
    "Example:\n"
    "199.199\n"
    "1.1\n"
    "255.255"
)

ip_box = tk.Text(root, font=("Segoe UI", 12), fg="white", bg="#444", insertbackground="white", wrap="none")
ip_box.insert("1.0", ip_placeholder)
ip_box.tag_add('center', "1.0", "end")
ip_box.tag_configure('center', justify='center')
ip_box.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

placeholder_active = True

def ip_box_click(event):
    global placeholder_active
    if placeholder_active:
        ip_box.delete("1.0", "end")
        placeholder_active = False

def ip_box_focus_out(event):
    global placeholder_active
    if ip_box.get("1.0", "end-1c").strip() == "":
        ip_box.insert("1.0", ip_placeholder)
        ip_box.tag_add('center', "1.0", "end")
        ip_box.tag_configure('center', justify='center')
        placeholder_active = True

def on_entry_click(event):
    widget = event.widget
    if widget == rule_name_box and widget.get() == "RULES NAME":
        widget.delete(0, "end")

rule_name_box.bind("<FocusIn>", on_entry_click)
ip_box.bind("<Button-1>", ip_box_click)
ip_box.bind("<FocusOut>", ip_box_focus_out)

block_button = tk.Button(root, text="BLOCK IP", font=("Segoe UI", 12, "bold"), fg="white", bg="#ff4747", relief="flat", command=on_block_ip)
block_button.grid(row=3, column=0, pady=(0, 20), ipadx=10, ipady=5)

center_window(root)
root.mainloop()
