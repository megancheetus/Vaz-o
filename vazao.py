import os
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class CalculadoraVazaoApp(ttk.Window):
    def __init__(self):
        # --- Main Window Setup ---
        super().__init__(
            title="Calculadora de Vazão",
            themename="flatly",
            size=(750, 900)
        )
        # Set the application icon
        self._set_icon()

        # --- Data for the drug table ---
        # Using a list of dictionaries for easier data access
        self.drogas = [
            {"nome": "Dopamina", "mg": 250, "vol": None, "amp": "5 amp"},
            {"nome": "Noradrenalina", "mg": 8, "vol": None, "amp": "4 amp"},
            {"nome": "Dobutamina", "mg": 250, "vol": None, "amp": "1 amp"},
            {"nome": "Midazolam", "mg": 30, "vol": None, "amp": "2 amp"},
            {"nome": "Fentanil", "mg": 1.5, "vol": None, "amp": "3 amp"}, 
            {"nome": "Ancoron", "mg": None, "vol": None, "amp": ""},
            {"nome": "Precedex", "mg": None, "vol": None, "amp": ""},
            {"nome": "Xylocaína", "mg": None, "vol": None, "amp": ""},
            {"nome": "Tridil", "mg": None, "vol": None, "amp": ""},
            {"nome": "Heparina", "mg": None, "vol": None, "amp": ""},
            {"nome": "Oxygen", "mg": None, "vol": None, "amp": ""},
        ]

        # --- Create UI Widgets ---
        self._criar_widgets()

    def _resource_path(self, relative_path):
        """ Helper function to get correct path for resources, works for script and for PyInstaller .exe """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def _set_icon(self):
        """ Sets the window icon. """
        try:
            icon_path = self._resource_path("icone.ico")
            self.iconbitmap(icon_path)
        except Exception:
            print("Icon 'icone.ico' not found, using default.")

    def _criar_widgets(self):
        """ Creates and arranges all the UI widgets in the window. """
        frame_banner = ttk.Frame(self, padding=10)
        frame_banner.pack(side=TOP, fill=X)
        try:
            banner_img = Image.open(self._resource_path("banner.png"))
            banner_img = banner_img.resize((450, 150))
            self.banner_tk = ImageTk.PhotoImage(banner_img)
            banner_label = ttk.Label(frame_banner, image=self.banner_tk)
            banner_label.pack()
        except Exception:
            banner_label = ttk.Label(frame_banner, text="[Banner não encontrado]", font=("Helvetica", 16), bootstyle=WARNING)
            banner_label.pack()

        subtitle = ttk.Label(frame_banner, text="Versão feita por Edvaldo", font=("Helvetica", 12, "italic"))
        subtitle.pack(pady=(5, 15))

        frame_inputs = ttk.Frame(self, padding=10)
        frame_inputs.pack(side=TOP, fill=X)

        vcmd = (self.register(self._validar_entrada_numerica), '%P')

        ttk.Label(frame_inputs, text="Peso (kg):").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.entry_peso = ttk.Entry(frame_inputs, width=15, validate='key', validatecommand=vcmd)
        self.entry_peso.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Dose desejada (mcg/kg/min):").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.entry_dose = ttk.Entry(frame_inputs, width=15, validate='key', validatecommand=vcmd)
        self.entry_dose.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Total de mg no soro:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.entry_total_mg = ttk.Entry(frame_inputs, width=15, validate='key', validatecommand=vcmd)
        self.entry_total_mg.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_inputs, text="Volume do soro (ml):").grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.entry_volume_ml = ttk.Entry(frame_inputs, width=15, validate='key', validatecommand=vcmd)
        self.entry_volume_ml.grid(row=3, column=1, padx=5, pady=5)

        btn_calcular = ttk.Button(frame_inputs, text="Calcular Vazão", bootstyle=PRIMARY, command=self._calcular_vazao)
        btn_calcular.grid(row=4, column=0, columnspan=2, pady=10)

        self.resultado_label = ttk.Label(frame_inputs, text="", font=("Helvetica", 14))
        self.resultado_label.grid(row=5, column=0, columnspan=2, pady=10)

        frame_tabela = ttk.Frame(self, padding=10)
        frame_tabela.pack(side=TOP, fill=BOTH, expand=True)

        # --- CORRECTION: Added the requested header text before the table ---
        table_header1 = ttk.Label(frame_tabela, text="Fórmula para cálculo da concentração de drogas.", font=("Helvetica", 12, "bold"))
        table_header1.pack(pady=(0, 5))
        table_header2 = ttk.Label(frame_tabela, text="Tabela - Infusões padronizadas em SF/SG em 250/500 ml", font=("Helvetica", 10))
        table_header2.pack(pady=(0, 10))

        colunas = ("Droga", "Ampolas", "Quantidade Total")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", bootstyle=INFO)
        self.tree.pack(fill=BOTH, expand=True)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER)

        for droga in self.drogas:
            qtde_total = f"{droga['mg']} mg" if droga['mg'] is not None else ""
            self.tree.insert("", END, values=(droga['nome'], droga['amp'], qtde_total), iid=droga['nome'])
        
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_droga)

    def _validar_entrada_numerica(self, valor_potencial):
        """ Validation function to allow only numbers (and empty string). """
        return valor_potencial.replace('.', '', 1).isdigit() or valor_potencial == ""

    def _ao_selecionar_droga(self, event):
        """ CORRECTION: Event handler for when a drug is selected, now with error checking. """
        # Check if there is any selection, otherwise do nothing.
        if not self.tree.selection():
            return
            
        # Get selected item's IID (which we set as the drug's name)
        selected_iid = self.tree.selection()[0]
        
        droga_selecionada = next((d for d in self.drogas if d["nome"] == selected_iid), None)

        if droga_selecionada:
            self.entry_total_mg.delete(0, END)
            self.entry_volume_ml.delete(0, END)

            if droga_selecionada.get("mg") is not None:
                self.entry_total_mg.insert(0, str(droga_selecionada["mg"]))
            if droga_selecionada.get("vol") is not None:
                self.entry_volume_ml.insert(0, str(droga_selecionada["vol"]))

    def _calcular_vazao(self):
        """ Calculation function for the flow rate. """
        try:
            peso = float(self.entry_peso.get())
            dose = float(self.entry_dose.get())
            total_mg = float(self.entry_total_mg.get())
            volume_ml = float(self.entry_volume_ml.get())

            concentracao = (total_mg * 1000) / volume_ml
            vazao = (dose * peso * 60) / concentracao

            self.resultado_label.config(
                text=f"Vazão necessária: {vazao:.2f} ml/h",
                bootstyle=SUCCESS
            )
        except ValueError:
            self.resultado_label.config(
                text="Erro: Preencha todos os campos com números válidos.",
                bootstyle=DANGER
            )
        except ZeroDivisionError:
            self.resultado_label.config(
                text="Erro: O volume do soro não pode ser zero.",
                bootstyle=DANGER
            )
        except Exception as e:
            self.resultado_label.config(text=f"Ocorreu um erro: {e}", bootstyle=DANGER)

if __name__ == "__main__":
    app = CalculadoraVazaoApp()
    app.mainloop()