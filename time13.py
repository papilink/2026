# Papiweb desarrollos informaticos
# Papitime
import tkinter as tk
from tkinter import messagebox, colorchooser, filedialog, ttk
import calendar
import json
import os
import vlc
from datetime import datetime
import pytz
from PIL import Image, ImageTk, ImageDraw

# Configuración de Idioma
calendar.setfirstweekday(calendar.SUNDAY)
MESES_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
DIAS_ES = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]

COLORS = {
    'bg_dark': '#020617', 'bg_card': '#0f172a', 'win_header': '#1e3a8a',
    'primary': '#1e40af', 'gold': '#93c5fd', 'taskbar': '#000000',
    'start_btn': '#2563eb', 'today': '#fbbf24', 'text': '#f8fafc'
}

class PapiwebProOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Papiweb Sapphire OS 2026 - Ultra Edition")
        self.root.geometry("1600x900")
        
        self.data = self.load_data()
        self.tz = pytz.timezone('America/Argentina/Buenos_Aires')
        self.windows = {}
        self.pen_color = "#00d4ff"
        self.pen_size = 2

        self.setup_desktop()
        self.setup_taskbar()
        self.init_start_menu()

    def setup_desktop(self):
        self.desktop = tk.Canvas(self.root, highlightthickness=0)
        self.desktop.place(x=0, y=0, relwidth=1, relheight=0.95)
        
        # Cargar fondo.png
        try:
            img = Image.open("fondo.png").resize((1600, 900), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(img)
            self.desktop.create_image(0, 0, image=self.bg_img, anchor="nw")
        except:
            self.desktop.configure(bg=COLORS['bg_dark'])

    def setup_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg=COLORS['taskbar'], height=45)
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.btn_container = tk.Frame(self.taskbar, bg=COLORS['taskbar'])
        self.btn_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def init_start_menu(self):
        self.mb = tk.Menubutton(self.taskbar, text="💎 PAPIWEB", bg=COLORS['start_btn'], 
                               fg="white", font=("Arial", 10, "bold"), relief="flat", padx=20)
        self.menu = tk.Menu(self.mb, tearoff=0, bg=COLORS['bg_card'], fg="white", activebackground=COLORS['primary'])
        apps = [("📅 Agenda", self.open_calendar), ("🎨 Paint Pro", self.open_paint), 
                ("🔢 Calculadora", self.open_calc), ("📝 Notas", self.open_notes),
                ("🎬 Media Player", self.open_media), ("💾 Exportar JSON", self.export_full_json)]
        for label, cmd in apps: self.menu.add_command(label=label, command=cmd)
        self.mb.config(menu=self.menu)
        self.mb.pack(side=tk.LEFT, fill=tk.Y)

    # --- MOTOR DE VENTANAS ---
    def create_win(self, wid, title, w, h, content_func):
        if wid in self.windows: return self.windows[wid]['f'].lift()
        
        f = tk.Frame(self.desktop, bg=COLORS['bg_card'], highlightthickness=1, highlightbackground=COLORS['gold'])
        f.place(x=100, y=50, width=w, height=h)
        
        bar = tk.Frame(f, bg=COLORS['win_header'], height=32, cursor="fleur")
        bar.pack(side=tk.TOP, fill=tk.X)
        tk.Label(bar, text=title, bg=COLORS['win_header'], fg="white", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=10)

        # Botones de control
        tk.Button(bar, text="✕", command=lambda: self.close_win(wid), bg="#7f1d1d", fg="white", bd=0, width=3).pack(side=tk.RIGHT)
        tk.Button(bar, text="▢", command=lambda: self.toggle_fs(wid), bg="#334155", fg="white", bd=0, width=3).pack(side=tk.RIGHT)

        def move(e): f.place(x=f.winfo_x()+(e.x-f._x), y=f.winfo_y()+(e.y-f._y))
        bar.bind("<Button-1>", lambda e: (setattr(f, '_x', e.x), setattr(f, '_y', e.y), f.lift()))
        bar.bind("<B1-Motion>", move)

        self.windows[wid] = {'f': f, 'orig': (100, 50, w, h), 'fs': False}
        content = tk.Frame(f, bg=COLORS['bg_card'])
        content.pack(fill=tk.BOTH, expand=True)
        content_func(content)

    def toggle_fs(self, wid):
        w_data = self.windows[wid]
        if not w_data['fs']:
            w_data['f'].place(x=0, y=0, relwidth=1, relheight=1)
            w_data['fs'] = True
        else:
            x, y, w, h = w_data['orig']
            w_data['f'].place(x=x, y=y, width=w, height=h, relwidth=0, relheight=0)
            w_data['fs'] = False

    def close_win(self, wid):
        self.windows[wid]['f'].destroy()
        del self.windows[wid]

    # --- APP: AGENDA ESPAÑOL ---
    def open_calendar(self):
        self.create_win("cal", "AGENDA MASTER 2026", 1100, 750, self.setup_cal_ui)

    def setup_cal_ui(self, p):
        container = tk.Frame(p, bg=COLORS['bg_card'])
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        now = datetime.now()
        
        for m in range(1, 13):
            f = tk.Frame(container, bg=COLORS['bg_card'], bd=1, relief="flat", highlightthickness=1, highlightbackground="#1e293b")
            f.grid(row=(m-1)//4, column=(m-1)%4, sticky="nsew", padx=3, pady=3)
            tk.Label(f, text=MESES_ES[m-1].upper(), fg=COLORS['gold'], bg=COLORS['bg_card'], font=("Arial", 9, "bold")).pack()
            
            d_frame = tk.Frame(f, bg=COLORS['bg_card'])
            d_frame.pack()
            
            for i, d in enumerate(DIAS_ES):
                tk.Label(d_frame, text=d, fg="#475569", bg=COLORS['bg_card'], font=("Arial", 6)).grid(row=0, column=i)
            
            cal = calendar.monthcalendar(2026, m)
            for r, week in enumerate(cal):
                for c, day in enumerate(week):
                    if day == 0: continue
                    is_today = (day == now.day and m == now.month)
                    btn = tk.Button(d_frame, text=str(day), width=2, relief="flat", 
                                   bg=COLORS['today'] if is_today else COLORS['bg_card'],
                                   fg="black" if is_today else "white", font=("Arial", 7),
                                   command=lambda d=day, m=m: self.edit_event(d, m))
                    btn.grid(row=r+1, column=c)

    # --- APP: PAINT PRO CON FONDO ---
    def open_paint(self):
        self.create_win("paint", "PAINT PRO", 800, 600, self.setup_paint_ui)

    def setup_paint_ui(self, p):
        tools = tk.Frame(p, bg="#0f172a", height=40)
        tools.pack(side=tk.TOP, fill=tk.X)
        
        icons = [("🎨", self.pick_color), ("✏️", lambda: self.set_tool(2)), 
                 ("🖌️", lambda: self.set_tool(5)), ("🧽", lambda: self.set_tool(20, "#000000"))]
        for icon, cmd in icons:
            tk.Button(tools, text=icon, command=cmd, bg="#1e293b", fg="white", width=3).pack(side=tk.LEFT, padx=2, pady=2)
            
        self.cv = tk.Canvas(p, bg="black", highlightthickness=0)
        self.cv.pack(fill=tk.BOTH, expand=True)
        
        try:
            p_img = Image.open("paint.png").resize((1200, 800))
            self.p_bg = ImageTk.PhotoImage(p_img)
            self.cv.create_image(0,0, image=self.p_bg, anchor="nw")
        except: pass

        self.cv.bind("<B1-Motion>", self.draw_paint)
        self.cv.bind("<Button-1>", lambda e: setattr(self, 'lx', e.x) or setattr(self, 'ly', e.y))

    def draw_paint(self, e):
        self.cv.create_line(self.lx, self.ly, e.x, e.y, fill=self.pen_color, width=self.pen_size, capstyle="round", smooth=True)
        self.lx, self.ly = e.x, e.y

    # --- APP: CALCULADORA COMPLETA ---
    def open_calc(self):
        self.create_win("calc", "CALCULADORA", 350, 480, self.setup_calc_ui)

    def setup_calc_ui(self, p):
        disp = tk.Entry(p, font=("Arial", 24), justify="right", bg="#020617", fg="white", bd=10, relief="flat")
        disp.pack(fill=tk.X, padx=10, pady=10)
        
        grid = tk.Frame(p, bg=COLORS['bg_card'])
        grid.pack(fill=tk.BOTH, expand=True)
        
        btns = [('sin', 'cos', 'tan', 'log'), ('7', '8', '9', '/'), ('4', '5', '6', '*'), 
                ('1', '2', '3', '-'), ('0', '.', '=', '+'), ('C', '(', ')', 'sqrt')]
        
        for r, row in enumerate(btns):
            for c, txt in enumerate(row):
                tk.Button(grid, text=txt, bg="#1e293b", fg=COLORS['gold'], font=("Arial", 10, "bold"),
                          command=lambda t=txt: self.calc_logic(disp, t)).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
        for i in range(4): grid.grid_columnconfigure(i, weight=1)
        for i in range(6): grid.grid_rowconfigure(i, weight=1)

    def calc_logic(self, disp, char):
        if char == '=':
            try:
                res = eval(disp.get().replace('sqrt', 'math.sqrt').replace('sin', 'math.sin'))
                disp.delete(0, tk.END); disp.insert(tk.END, str(res))
            except: disp.delete(0, tk.END); disp.insert(tk.END, "Error")
        elif char == 'C': disp.delete(0, tk.END)
        else: disp.insert(tk.END, char)

    # --- APP: BLOC DE NOTAS ---
    def open_notes(self):
        self.create_win("notes", "NOTAS", 500, 500, self.setup_notes_ui)

    def setup_notes_ui(self, p):
        bar = tk.Frame(p, bg="#1e293b")
        bar.pack(fill=tk.X)
        tk.Button(bar, text="💾", command=self.save_data_json, bg="#1e293b", fg="white").pack(side=tk.LEFT)
        
        self.txt = tk.Text(p, bg="#0f172a", fg="white", font=("Consolas", 12), padx=10, pady=10)
        self.txt.pack(fill=tk.BOTH, expand=True)
        self.txt.insert("1.0", self.data.get('notes', ''))

    # --- FUNCIONES DE SISTEMA ---
    def pick_color(self): self.pen_color = colorchooser.askcolor()[1]
    def set_tool(self, size, color=None): 
        self.pen_size = size
        if color: self.pen_color = color

    def export_full_json(self):
        filename = f"Papiweb_Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(self.data, f, indent=4)
        messagebox.showinfo("Exportar", f"Sistema exportado a {filename}")

    def load_data(self):
        if os.path.exists("db_sapphire.json"):
            with open("db_sapphire.json", "r") as f: return json.load(f)
        return {"events": {}, "notes": "", "drawings": []}

    def save_data_json(self):
        self.data['notes'] = self.txt.get("1.0", tk.END)
        with open("db_sapphire.json", "w") as f: json.dump(self.data, f)

    def open_media(self):
        self.create_win("media", "MEDIA PLAYER", 600, 400, lambda p: tk.Label(p, text="VLC PLAYER ACTIVO", bg="black", fg="white").pack(expand=True))

if __name__ == "__main__":
    root = tk.Tk()
    app = PapiwebProOS(root)
    root.mainloop()