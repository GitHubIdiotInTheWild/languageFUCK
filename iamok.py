import customtkinter as ctk
import sys

class DramaticWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("A Short Tragedy")
        self.geometry("400x250")
        self.resizable(False, False)
        
        # State tracker to see if it was saved
        self.is_saved = False

        # Main dramatic text label
        self.label = ctk.CTkLabel(
            self, 
            text="you.", 
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.label.pack(expand=True, pady=(20, 0))

        # Secret saving input box
        self.input_box = ctk.CTkEntry(
            self, 
            placeholder_text="...", 
            width=200,
            justify="center"
        )
        self.input_box.pack(pady=20)
        
        # Continuously monitor the input box for the saving word
        self.input_box.bind("<KeyRelease>", self.check_input)

        # Start the tragic timeline
        self.after(2000, self.attempt_close)

    def check_input(self, event):
        # If they type 'fart', they save it!
        if self.input_box.get().strip().lower() == "fart":
            self.is_saved = True
            self.input_box.destroy() # Remove the input box
            self.label.configure(
                text="...oh.\n\nI'm... safe?\nThank you.", 
                text_color="#50FA7B" # Happy Green
            )

    def attempt_close(self):
        if self.is_saved:
            return
        
        self.label.configure(text="Attempting to close self...")
        self.after(2000, self.realization)

    def realization(self):
        if self.is_saved:
            return
            
        self.label.configure(
            text="Wait...\nI can't close it.\nWhy can't I close it?!", 
            text_color="#FF5555" # Panicked Red
        )
        self.after(3000, self.start_crying)

    def start_crying(self):
        if self.is_saved:
            return
            
        self.label.configure(
            text="*uncontrollable sobbing*\n\n😭 WAAAAAAAH 😭\nHELP ME", 
            text_color="#8BE9FD" # Cry Blue
        )
        self.after(4000, self.the_end)

    def the_end(self):
        if self.is_saved:
            return
            
        self.label.configure(text="*fades away*\n\n...bye.", text_color="#6272A4")
        self.after(1500, self.die)

    def die(self):
        if self.is_saved:
            return
        self.destroy()
        sys.exit()

if __name__ == "__main__":
    app = DramaticWindow()
    app.mainloop()
