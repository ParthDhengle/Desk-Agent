# src/ui/app_window.py

import tkinter as tk
from tkinter import scrolledtext, Entry, Button
import asyncio
from src.processing.intent_parser import parse_intent
from src.processing.action_router import route_action

class AppWindow(tk.Tk):
    def __init__(self, loop):
        super().__init__()
        self.loop = loop
        self.title("DeskAgent")
        self.geometry("700x500")

        # This will store a command that is waiting for a 'yes' or 'no'.
        self.pending_confirmation_command = None

        # --- UI Elements ---
        self.conversation_display = scrolledtext.ScrolledText(self, state='disabled', wrap=tk.WORD, font=("Helvetica", 11))
        self.conversation_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        self.input_entry = Entry(self.input_frame, font=("Helvetica", 11))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind("<Return>", self.on_submit)

        self.send_button = Button(self.input_frame, text="Send", command=self.on_submit)
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))

        self.add_message("System", "Welcome to DeskAgent. I'm ready for your commands.")

    def add_message(self, sender: str, message: str):
        self.conversation_display.config(state='normal')
        self.conversation_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.conversation_display.config(state='disabled')
        self.conversation_display.yview(tk.END)

    def on_submit(self, event=None):
        user_input = self.input_entry.get()
        if not user_input.strip():
            return
        
        self.add_message("You", user_input)
        self.input_entry.delete(0, tk.END)

        # Schedule the async command processing
        self.loop.create_task(self.process_command(user_input))

    async def process_command(self, user_input: str):
        # First, check if we are waiting for a confirmation.
        if self.pending_confirmation_command:
            if user_input.lower() in ["yes", "y"]:
                # User confirmed. Route the stored command for execution.
                command_to_execute = self.pending_confirmation_command
                self.pending_confirmation_command = None # Clear state
                result_message = await route_action(command_to_execute)
                self.add_message("System", result_message)
            else:
                # User denied.
                self.pending_confirmation_command = None # Clear state
                self.add_message("System", "Action cancelled.")
            return

        # If not waiting for confirmation, this is a new command.
        parsed_command = await parse_intent(user_input)
        if not parsed_command:
            self.add_message("System", "Sorry, I had trouble understanding that command.")
            return

        # Now, check the 'requires_confirmation' flag from the LLM's response.
        if parsed_command.get("requires_confirmation"):
            self.pending_confirmation_command = parsed_command
            confirmation_prompt = parsed_command.get("message", "Are you sure?")
            self.add_message("System", f"{confirmation_prompt} (yes/no)")
        else:
            # If no confirmation is needed, route it for execution immediately.
            result_message = await route_action(parsed_command)
            self.add_message("System", result_message)