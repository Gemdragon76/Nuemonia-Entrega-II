import tkinter as tk
from tkinter import ttk, font, filedialog, Text, StringVar , messagebox
from PIL import ImageTk, Image
import numpy as np
from tensorflow.keras.models import load_model
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
#from PIL import Image as PILImage, ImageTk
import os
import io
from datetime import datetime

import csv




class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Herramienta para la detección rápida de neumonía")

        # BOLD FONT
        fonti = font.Font(weight="bold")

        self.root.geometry("815x560")
        self.root.resizable(0, 0)

        # LABELS
        self.lab1 = ttk.Label(self.root, text="Imagen Radiográfica", font=fonti)
        self.lab2 = ttk.Label(self.root, text="Imagen con Heatmap", font=fonti)
        self.lab3 = ttk.Label(self.root, text="Resultado:", font=fonti)
        self.lab4 = ttk.Label(self.root, text="Cédula Paciente:", font=fonti)
        self.lab5 = ttk.Label(
            self.root,
            text="SOFTWARE PARA EL APOYO AL DIAGNÓSTICO MÉDICO DE NEUMONÍA",
            font=fonti,
        )
        self.lab6 = ttk.Label(self.root, text="Probabilidad:", font=fonti)

        # STRING VARIABLES
        self.ID = StringVar()
        self.result = StringVar()

        # INPUT BOXES
        self.text1 = ttk.Entry(self.root, textvariable=self.ID, width=10)

        # IMAGE BOXES
        self.text_img1 = Text(self.root, width=31, height=15)
        self.text_img2 = Text(self.root, width=31, height=15)
        self.text2 = Text(self.root)
        self.text3 = Text(self.root)

        # BUTTONS
        self.button1 = ttk.Button(
            self.root, text="Predecir", state="disabled", command=self.run_model
        )
        self.button2 = ttk.Button(
            self.root, text="Cargar Imagen", command=self.load_img_file
        )
        self.button3 = ttk.Button(self.root, text="Borrar", command=self.delete)
        self.button4 = ttk.Button(self.root, text="PDF", command=self.create_pdf)
        self.button6 = ttk.Button(
            self.root, text="Guardar", command=self.save_results_csv
        )

        # WIDGETS POSITIONS
        self.lab1.place(x=110, y=65)
        self.lab2.place(x=545, y=65)
        self.lab3.place(x=500, y=350)
        self.lab4.place(x=65, y=350)
        self.lab5.place(x=122, y=25)
        self.lab6.place(x=500, y=400)
        self.button1.place(x=220, y=460)
        self.button2.place(x=70, y=460)
        self.button3.place(x=670, y=460)
        self.button4.place(x=520, y=460)
        self.button6.place(x=370, y=460)
        self.text1.place(x=200, y=350)
        self.text2.place(x=610, y=350, width=90, height=30)
        self.text3.place(x=610, y=400, width=90, height=30)
        self.text_img1.place(x=65, y=90)
        self.text_img2.place(x=500, y=90)

        # FOCUS ON PATIENT ID
        self.text1.focus_set()

        # Load pre-trained model
        self.model = load_model(r'mi_modelo_entrenado.h5')

        self.root.mainloop()

    def load_img_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((256, 256))
            self.photo = ImageTk.PhotoImage(self.image)
            self.text_img1.image_create("1.0", image=self.photo)
            self.button1.config(state="normal")
            self.file_path = file_path

    def run_model(self):

    
        print('mdb 1')
        image_array = np.array(self.image.resize((150, 150))) / 255.0
        print('mdb 2')
        image_array = np.expand_dims(image_array, axis=0)
        print('mdb 3')
        prediction = self.model.predict(image_array)
        print('mdb 4')
        probability = prediction[0][0]
        print('mdb 5')
        #print('mdb 6'+probability)

        result = "Neumonía" if probability > 0.5 else "Normal"
        self.text2.delete("1.0", tk.END)
        self.text2.insert(tk.END, result)
        self.text3.delete("1.0", tk.END)
        self.text3.insert(tk.END, f"{probability:.2f}")

    def delete(self):
        self.text_img1.delete("1.0", tk.END)
        self.text_img2.delete("1.0", tk.END)
        self.text1.delete(0, tk.END)
        self.text2.delete("1.0", tk.END)
        self.text3.delete("1.0", tk.END)
        self.button1.config(state="disabled")


    def create_pdf(self):
        
        # Verificar si se ha realizado una predicción
        if not self.ID.get() or not self.text2.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "Por favor, asegúrese de ingresar la cédula del paciente y realizar una predicción antes de crear el PDF.")
            return

        # Solicitar al usuario que elija dónde guardar el archivo PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return  # El usuario canceló la operación

        # Crear el documento PDF
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        normal_style = styles['Normal']

        # Título
        elements.append(Paragraph("Informe de Detección de Neumonía", title_style))
        elements.append(Paragraph("<br/><br/>", normal_style))

        # Información del paciente y resultados
        data = [
            ["Cédula del Paciente:", self.ID.get()],
            ["Fecha del Análisis:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Resultado:", self.text2.get("1.0", tk.END).strip()],
            ["Probabilidad:", self.text3.get("1.0", tk.END).strip()]
        ]

        # Crear tabla
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)

        # Generar el PDF
        try:
            doc.build(elements)
            messagebox.showinfo("Éxito", f"El PDF ha sido creado exitosamente en {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al crear el PDF: {str(e)}")

    def save_results_csv(self):
        # Verificar si se ha realizado una predicción
        if not hasattr(self, 'image') or not self.ID.get() or not self.text2.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "Por favor, asegúrese de cargar una imagen, ingresar la cédula del paciente y realizar una predicción antes de exportar a CSV.")
            return

        # Solicitar al usuario que elija dónde guardar el archivo CSV
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return  # El usuario canceló la operación

        # Preparar los datos para el CSV
        data = [
            ["Cédula del Paciente", self.ID.get()],
            ["Fecha del Análisis", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Resultado", self.text2.get("1.0", tk.END).strip()],
            ["Probabilidad", self.text3.get("1.0", tk.END).strip()],
            ["Ruta de la Imagen", getattr(self, 'file_path', 'No disponible')]
        ]

        # Escribir los datos en el archivo CSV
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            
            messagebox.showinfo("Éxito", f"Los resultados han sido guardados exitosamente en {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error al guardar el archivo CSV: {str(e)}")

if __name__ == "__main__":
    App()


