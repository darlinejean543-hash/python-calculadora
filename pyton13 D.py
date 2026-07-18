import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import time
import threading
import os
import sys

# Sonido nativo de Windows (Alarma)
if sys.platform == "win32":
    import winsound
else:
    winsound = None

class AplicacionCalculos:
    def __init__(self, root):
        self.root = root
        self.root.title("Acceso Requerido - V3")
        
        # Tamaño inicial para el Login (V3)
        self.root.geometry("320x200")
        
        # Variables de control de límites (V2)
        self.limite_inferior = tk.DoubleVar(value=0.0)
        self.limite_superior = tk.DoubleVar(value=100.0)
        self.intentos_password = 0
        self.pulsando = False
        
        # Variables para los sliders de operación (V1)
        self.val1 = tk.DoubleVar(value=0.0)
        self.val2 = tk.DoubleVar(value=0.0)
        
        # Operación seleccionada y control de resultados
        self.operacion_seleccionada = tk.StringVar(value="Suma")
        self.resultado_var = tk.StringVar(value="Resultado: Esperando acción...")
        self.ultimo_resultado = None  
        
        # Mostrar pantalla de login inicial (V3)
        self.mostrar_login_inicial()

    # --- SISTEMA DE ALARMA Y CIERRE DE SEGURIDAD (V3) ---
    def activar_alarma_y_cerrar_absoluto(self):
        def reproducir_alarma():
            if winsound:
                for _ in range(30):
                    winsound.Beep(4000, 400)
                    time.sleep(0.1)
            else:
                sys.stdout.write('\a')
                sys.stdout.flush()

        hilo_sonido = threading.Thread(target=reproducir_alarma)
        hilo_sonido.start()
        
        messagebox.showerror("ACCESO DENEGADO", "Demasiados intentos fallidos. Cerrando aplicación.")
        
        hilo_sonido.join(timeout=1.5)
        self.root.destroy()
        os._exit(0)

    # --- PANTALLA DE LOGIN INICIAL (V3) ---
    def mostrar_login_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        frame_login = tk.Frame(self.root)
        frame_login.pack(pady=20, padx=20, fill="both", expand=True)
            
        tk.Label(frame_login, text="Ingrese la contraseña para iniciar:", font=("Arial", 10, "bold")).pack(pady=10)
        self.entry_pass = tk.Entry(frame_login, show="*")
        self.entry_pass.pack(pady=5)
        self.entry_pass.focus()
        
        self.entry_pass.bind("<Return>", lambda event: self.validar_acceso_inicial())
        
        btn_validar = tk.Button(frame_login, text="Ingresar", command=self.validar_acceso_inicial, width=15, bg="#d3d3d3")
        btn_validar.pack(pady=15)

    def validar_acceso_inicial(self):
        # Contraseña única requerida por pauta: 1234
        if self.entry_pass.get() == "1234":
            for widget in self.root.winfo_children():
                widget.destroy()
                
            # Nombre establecido según las pautas de evaluación del proyecto
            self.root.title("Programa de Cálculos")
            self.root.geometry("520x790") 
            
            # Inicializar la interfaz principal estructurada
            self.crear_menu()
            self.crear_interfaz_v1()
            self.actualizar_reloj()
        else:
            self.intentos_password += 1
            if self.intentos_password >= 2:
                self.activar_alarma_y_cerrar_absoluto()
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.\nÚltimo intento disponible.")
                self.entry_pass.delete(0, tk.END)

    # --- MENÚ SUPERIOR ---
    def crear_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opciones", menu=menu_archivo)
        menu_archivo.add_command(label="Salir", command=self.root.quit)

    # --- INTERFAZ PRINCIPAL (V1) ---
    def crear_interfaz_v1(self):
        # 1. Reloj en tiempo real
        self.lbl_reloj = tk.Label(self.root, font=("Courier", 12, "bold"), fg="blue")
        self.lbl_reloj.pack(pady=10)
        
        # 2. Selección de operaciones (con colores diferenciados por botón)
        frame_op = tk.LabelFrame(self.root, text=" Seleccione Operación Algorítmica ", padx=10, pady=10)
        frame_op.pack(pady=10, fill="x", padx=20)
        
        operaciones = [
            ("Suma (+)", "Suma", "#9CE29C"),            
            ("Resta (-)", "Resta", "#FF9E9E"),          
            ("Multiplicación (*)", "Multiplicación", "#FFD27F"), 
            ("División (/)", "División", "#9EE1FF")      
        ]
        
        for texto, valor, color in operaciones:
            r_btn = tk.Radiobutton(
                frame_op, 
                text=texto, 
                value=valor, 
                variable=self.operacion_seleccionada,
                indicatoron=0,           
                selectcolor="#636363",   
                bg=color, 
                fg="black",
                font=("Arial", 9, "bold"),
                width=14,
                bd=2,
                relief="raised"
            )
            r_btn.pack(side="left", padx=5, expand=True)

        # 3. Deslizadores de Variables (Sliders) con los nombres de la pauta corregidos
        frame_sliders = tk.LabelFrame(self.root, text=" Magnitud de Variables ", padx=10, pady=10)
        frame_sliders.pack(pady=10, fill="x", padx=20)
        
        tk.Label(frame_sliders, text="Variable de Entrada (X):", font=("Arial", 9, "bold")).pack(anchor="w")
        self.slider1 = tk.Scale(frame_sliders, from_=-100, to=100, orient="horizontal", resolution=0.1, variable=self.val1)
        self.slider1.pack(fill="x")
        
        tk.Label(frame_sliders, text="Factor de Ajuste (Y):", font=("Arial", 9, "bold")).pack(anchor="w")
        self.slider2 = tk.Scale(frame_sliders, from_=-100, to=100, orient="horizontal", resolution=0.1, variable=self.val2)
        self.slider2.pack(fill="x")

        # 4. Indicador de Alerta Visual (Luz de advertencia)
        self.canvas_luz = tk.Canvas(self.root, width=40, height=40)
        self.canvas_luz.pack(pady=5)
        self.ovalo_luz = self.canvas_luz.create_oval(5, 5, 35, 35, fill="gray")

        # 5. Visualizador de resultados
        self.lbl_resultado = tk.Label(self.root, textvariable=self.resultado_var, font=("Arial", 16, "bold"))
        self.lbl_resultado.pack(pady=5)

        # Botón de Cálculo principal
        self.btn_calcular = tk.Button(self.root, text="¡CALCULAR OPERACIÓN!", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, command=self.ejecutar_calculo)
        self.btn_calcular.pack(pady=10)

        # 6. Identificador de límite de cálculo (Botón de Estado)
        self.btn_identificar = tk.Button(
            self.root, 
            text="Verificar Estado de Límites", 
            font=("Arial", 10, "bold"), 
            bg="#2196F3", 
            fg="white", 
            command=self.identificar_limite_calculo
        )
        self.btn_identificar.pack(pady=5)

        # Acceso a Configuración de Límites (V2)
        btn_limites = tk.Button(self.root, text="Configurar Límites (V2)", font=("Arial", 10, "bold"), bg="#d3d3d3", command=self.abrir_ventana_2_limites)
        btn_limites.pack(pady=10)

        # 7. Autores visibles de forma permanente en la parte inferior (Requisito de diseño)
        lbl_autores = tk.Label(
            self.root, 
            text="Programa desarrollado por:Darline J.", 
            font=("Arial", 9, "italic"), 
            fg="#555555"
        )
        lbl_autores.pack(side="bottom", pady=15)

    # --- ACTUALIZACIÓN DE RELOJ ---
    def actualizar_reloj(self):
        if self.root.winfo_exists():
            ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.lbl_reloj.config(text=ahora)
            self.root.after(1000, self.actualizar_reloj)

    # --- VENTANA DE CONFIGURACIÓN DE LÍMITES (V2) ---
    def abrir_ventana_2_limites(self):
        self.v2 = tk.Toplevel(self.root)
        self.v2.title("Configuración de Límites - V2")
        self.v2.geometry("400x250")
        self.v2.grab_set()  
        
        tk.Label(self.v2, text="Ajuste los límites permitidos para los resultados", font=("Arial", 10, "italic")).pack(pady=10)
        
        tk.Label(self.v2, text="Límite Inferior:").pack(anchor="w", padx=20)
        slider_inf = tk.Scale(self.v2, from_=-500, to=500, orient="horizontal", variable=self.limite_inferior)
        slider_inf.pack(fill="x", padx=20)
        
        tk.Label(self.v2, text="Límite Superior:").pack(anchor="w", padx=20)
        slider_sup = tk.Scale(self.v2, from_=-500, to=500, orient="horizontal", variable=self.limite_superior)
        slider_sup.pack(fill="x", padx=20)
        
        btn_cerrar = tk.Button(self.v2, text="Guardar y Cerrar", command=self.v2.destroy)
        btn_cerrar.pack(pady=15)

    # --- FUNCIÓN: IDENTIFICADOR DE LÍMITES ---
    def identificar_limite_calculo(self):
        if self.ultimo_resultado is None:
            messagebox.showinfo("Estado de Límites", "No se ha realizado ningún cálculo aún.\nPor favor, ejecute una operación primero.")
            return
            
        lim_inf = self.limite_inferior.get()
        lim_sup = self.limite_superior.get()
        
        if self.ultimo_resultado < lim_inf:
            messagebox.showwarning(
                "Límite Excedido", 
                f"ALERTA: El resultado ({self.ultimo_resultado}) está por DEBAJO del límite inferior permitido ({lim_inf})."
            )
        elif self.ultimo_resultado > lim_sup:
            messagebox.showwarning(
                "Límite Excedido", 
                f"ALERTA: El resultado ({self.ultimo_resultado}) está por ENCIMA del límite superior permitido ({lim_sup})."
            )
        else:
            messagebox.showinfo(
                "Límite Seguro", 
                f"OK: El resultado ({self.ultimo_resultado}) se encuentra dentro del rango seguro.\nRango: [{lim_inf} a {lim_sup}]"
            )

    # --- LÓGICA DE CÁLCULO ---
    def ejecutar_calculo(self):
        d1 = self.val1.get()
        d2 = self.val2.get()
        op = self.operacion_seleccionada.get()
        res = 0.0
        
        if op == "Suma":
            res = d1 + d2
        elif op == "Resta":
            res = d1 - d2
        elif op == "Multiplicación":
            res = d1 * d2
        elif op == "División":
            if d2 != 0:
                res = d1 / d2
            else:
                self.resultado_var.set("Error: Div / 0")
                self.ultimo_resultado = None
                self.guardar_en_txt(d1, d2, op, "Error: Div / 0")
                return

        res = round(res, 2)
        self.ultimo_resultado = res
        self.resultado_var.set(f"Resultado: {res}")
        
        lim_inf = self.limite_inferior.get()
        lim_sup = self.limite_superior.get()
        
        # Gestión de alerta visual
        if res < lim_inf or res > lim_sup:
            if not self.pulsando:
                self.pulsando = True
                threading.Thread(target=self.loop_luz_pulsante, daemon=True).start()
        else:
            self.pulsando = False
            self.canvas_luz.itemconfig(self.ovalo_luz, fill="gray")
            
        self.guardar_en_txt(d1, d2, op, res)

    def loop_luz_pulsante(self):
        color = "red"
        while self.pulsando:
            if not self.root.winfo_exists(): 
                break
            self.canvas_luz.itemconfig(self.ovalo_luz, fill=color)
            color = "gray" if color == "red" else "red"
            time.sleep(0.4)

    # Registro de transacciones
    def guardar_en_txt(self, d1, d2, op, res):
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro = f"[{ahora}] Operación: {d1} {op} {d2} = {res} | Límites: [{self.limite_inferior.get()}, {self.limite_superior.get()}]\n"
        
        with open("nombre.txt", "a", encoding="utf-8") as archivo:
            archivo.write(registro)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionCalculos(root)
    root.mainloop()
