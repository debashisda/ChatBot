import brain

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

class ChatUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat")
        self.root.geometry("420x560")
        self.root.configure(bg="#7D7DB2")

        self.messages = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#1e1e2e",
            fg="#e0e0e0",
            font=("Segoe UI", 11),
            bd=0,
            padx=12,
            pady=12,
        )
        self.messages.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))

        # Speaker name styles
        self.messages.tag_config("you_name", foreground="#89b4fa", font=("Segoe UI", 11, "bold"))
        self.messages.tag_config("bot_name", foreground="#a6e3a1", font=("Segoe UI", 11, "bold"))
        self.messages.tag_config("time", foreground="#6c7086", font=("Segoe UI", 8))
        # Justification styles (applied across the whole message block)
        self.messages.tag_config("right", justify=tk.RIGHT, lmargin1=60, rmargin=4)
        self.messages.tag_config("left", justify=tk.LEFT, lmargin1=4, rmargin=60)

        # --- Bottom input bar ---
        bottom = tk.Frame(root, bg="#1e1e2e")
        bottom.pack(fill=tk.X, padx=8, pady=8)

        self.entry = tk.Entry(
            bottom,
            bg="#313244",
            fg="#e0e0e0",
            font=("Segoe UI", 11),
            insertbackground="#e0e0e0",
            relief=tk.FLAT,
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 6))
        self.entry.bind("<Return>", self.send)
        self.entry.focus()

        send_btn = tk.Button(
            bottom,
            text="Send",
            command=self.send,
            bg="#89b4fa",
            fg="#1e1e2e",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            activebackground="#74a0f0",
            padx=16,
            cursor="hand2",
        )
        send_btn.pack(side=tk.RIGHT)

        self.add_message("Bot", "Hi! Type a message and press Enter.", side="left")

    def add_message(self, sender, text, side):
        self.messages.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")
        name_tag = "you_name" if side == "right" else "bot_name"
        start = self.messages.index(tk.END + "-1c")
        self.messages.insert(tk.END, f"{sender} ", name_tag)
        self.messages.insert(tk.END, f"{timestamp}\n", "time")
        self.messages.insert(tk.END, f"{text}\n\n")
        end = self.messages.index(tk.END + "-1c")
        self.messages.tag_add(side, start, end)
        self.messages.config(state=tk.DISABLED)
        self.messages.see(tk.END)

    def send(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.add_message("You", text, side="right")
        self.entry.delete(0, tk.END)
        reply = self.get_response(text)
        self.add_message("Bot", reply, side="left")

    def get_response(self, message):
        return brain.get_response(message)


if __name__ == "__main__":
    root = tk.Tk()
    ChatUI(root)
    root.mainloop()