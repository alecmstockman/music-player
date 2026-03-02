from tkinter import ttk

def setup_styles(root):
    style = ttk.Style(root)

    style.theme_use('aqua')

    style.configure(
        "Border.TFrame",
        bordercolor="white",
        relief="solid",
        borderwidth=2,
        padx=10
    )

    style.configure(
        "Custom.Horizontal.TProgressbar",
        troughcolor="#444444", 
        background="#096880", 
        thickness = 20
    )

    style.configure(
        "Custom.TButton", 
        font=("Trebuchet MS", 15), 
        padding=5
    )

    style.configure(
        "Custom.TLabel", 
        font=("Trebuchet MS", 15),
        foreground="#FFFFFF"
    )

    style.configure(
        "Header.TFrame",
        background="#2b2b2b"
    )
    
    style.configure(
        "Header.TLabel",
        font=("Trebuchet MS", 20, "bold"),
        padding=(10, 6)
    )

    return style