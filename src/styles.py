from tkinter import ttk

def setup_styles(root):
    style = ttk.Style(root)

    style.theme_use('aqua')

    style.configure(
        "Custom.Horizontal.TProgressbar",
        troughcolor="#444444", 
        background="#096880", 
        thickness = 20
    )

    style.configure(
        "Custom.TButton", 
        font=("Trebuchet MS", 12), 
        padding=5
    )

    style.configure(
        "Custom.TLabel", 
        font=("Trebuchet MS", 12),
        foreground="FFFFFF"
    )

    return style