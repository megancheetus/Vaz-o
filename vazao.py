import os
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk  # precisa instalar pillow: pip install pillow


# ----------------- Função auxiliar para recursos no .exe -----------------
def resource_path(relative_path):
    """Retorna o caminho correto do recurso, funciona no script e no .exe"""
    try:
        base_path = sys._MEIPASS  # quando está no .exe
    except Exception:
        base_path = os.path.abspath(".")  # quando roda como script normal
    return os.path.join(base_path, relative_path)


# ----------------- Função de cálculo -----------------
def calcular_vazao():
    try:
        peso = float(entry_peso.get())
        dose = float(entry_dose.get())
        total_mg = float(entry_total_mg.get())
        volume_ml = float(entry_volume_ml.get())

        concentracao = (total_mg * 1000) / volume_ml
        vazao = (dose * peso * 60) / concentracao

        resultado_label.config(
            text=f"Vazão necessária: {vazao:.2f} ml/h",
            bootstyle=SUCCESS
        )
    except Exception as e:
        resultado_label.config(text=f"Erro: {e}", bootstyle=DANGER)


# ----------------- Dados da tabela -----------------
drogas = [
    ("Dopamina", "5 amp", "250 mg"),
    ("Noradrenalina", "4 amp", "8 mg"),
    ("Dobutamina", "1 amp", "250 mg"),
    ("Midazolam", "2 amp", "30 mg"),
    ("Fentanil", "3 amp", "1500 mcg"),
    ("Ancoron", "", ""),
    ("Precedex", "", ""),
    ("Xylocaína", "", ""),
    ("Tridil", "", ""),
    ("Heparina", "", ""),
    ("Oxygen", "", ""),
]


# ----------------- Janela principal -----------------
app = ttk.Window(
    title="Calculadora de Vazão",
    themename="flatly",
    size=(750, 900)
)

# Definir ícone (vai funcionar se você passar --icon=icone.ico no PyInstaller)
try:
    app.iconbitmap(resource_path("icone.ico"))
except Exception:
    print("Ícone não encontrado, usando padrão.")


# ----------------- Banner -----------------
frame_banner = ttk.Frame(app, padding=10)
frame_banner.pack(side=TOP, fill=X)

try:
    banner_img = Image.open(resource_path("banner.png"))
    banner_img = banner_img.resize((450, 150))
    banner_tk = ImageTk.PhotoImage(banner_img)
    banner_label = ttk.Label(frame_banner, image=banner_tk)
    banner_label.pack()
except Exception:
    banner_label = ttk.Label(frame_banner, text="[Banner não encontrado]", font=("Helvetica", 16), bootstyle=WARNING)
    banner_label.pack()

# Subtítulo
subtitulo = ttk.Label(frame_banner, text="Versão feita por Edvaldo", font=("Helvetica", 12, "italic"))
subtitulo.pack(pady=(5, 15))


# ----------------- Frame de entrada -----------------
frame_inputs = ttk.Frame(app, padding=10)
frame_inputs.pack(side=TOP, fill=X)

ttk.Label(frame_inputs, text="Peso (kg):").grid(row=0, column=0, sticky=W, padx=5, pady=5)
entry_peso = ttk.Entry(frame_inputs, width=15)
entry_peso.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Dose desejada (mcg/kg/min):").grid(row=1, column=0, sticky=W, padx=5, pady=5)
entry_dose = ttk.Entry(frame_inputs, width=15)
entry_dose.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Total de mg no soro:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
entry_total_mg = ttk.Entry(frame_inputs, width=15)
entry_total_mg.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(frame_inputs, text="Volume do soro (ml):").grid(row=3, column=0, sticky=W, padx=5, pady=5)
entry_volume_ml = ttk.Entry(frame_inputs, width=15)
entry_volume_ml.grid(row=3, column=1, padx=5, pady=5)

btn_calcular = ttk.Button(frame_inputs, text="Calcular Vazão", bootstyle=PRIMARY, command=calcular_vazao)
btn_calcular.grid(row=4, column=0, columnspan=2, pady=10)

resultado_label = ttk.Label(frame_inputs, text="", font=("Helvetica", 14))
resultado_label.grid(row=5, column=0, columnspan=2, pady=10)


# ----------------- Tabela -----------------
frame_tabela = ttk.Frame(app, padding=10)
frame_tabela.pack(side=TOP, fill=BOTH, expand=True)

colunas = ("Droga", "Ampolas", "Quantidade Total")
tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", bootstyle=INFO)
tree.pack(fill=BOTH, expand=True)

for col in colunas:
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER)

for droga in drogas:
    tree.insert("", END, values=droga)


# ----------------- Rodar aplicação -----------------
app.mainloop()
