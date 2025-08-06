# main.py

import asyncio
from src.ui.app_window import AppWindow

class AsyncTkinterLoop:
    """A class to bridge asyncio and Tkinter's mainloop."""
    def __init__(self, app):
        self.app = app
        self.loop = app.loop
        self.running = True

    def run(self):
        try:
            self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.loop.run_until_complete(self.tk_loop())
        except KeyboardInterrupt:
            self.on_closing()

    async def tk_loop(self):
        while self.running:
            try:
                self.app.update()
                await asyncio.sleep(0.01)
            except tk.TclError: # Handle window being closed
                self.running = False

    def on_closing(self):
        self.running = False

if __name__ == "__main__":
    print("🚀 Initializing DeskAgent...")
    print("   Please ensure Ollama and Everything services are running.")

    event_loop = asyncio.get_event_loop()
    app_window = AppWindow(loop=event_loop)
    
    async_loop = AsyncTkinterLoop(app_window)
    async_loop.run()
    
    print("DeskAgent has shut down.")