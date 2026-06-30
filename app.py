import customtkinter as ctk
from gui.Home import HomeScreen

def main():
    # Set dark theme and blue color scheme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create main application window
    app = ctk.CTk()
    app.title("Excel Logic Analyzer")
    app.geometry("1000x700")

    # Load HomeScreen (GUI entry point)
    HomeScreen(app)

    # Start the application loop
    app.mainloop()

if __name__ == "__main__":
    main()
