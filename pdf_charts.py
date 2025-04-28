# pdf_charts.py
# Generación de gráficos para informes PDF
# Contiene funciones para crear gráficos específicos para el informe

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import BytesIO
from reportlab.lib.units import inch
from reportlab.platypus import Image

def add_duration_histogram(elements, df):
    """Agrega un histograma de duración de servicios al PDF"""
    plt.figure(figsize=(7, 4))
    plt.hist(df['Duración (minutos)'].dropna(), bins=20, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Distribución de Tiempos de Servicio')
    plt.xlabel('Duración (minutos)')
    plt.ylabel('Frecuencia')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Guardar la figura en un buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    plt.close()

    # Agregar la imagen al PDF
    img = Image(img_buffer, width=6 * inch, height=3 * inch)
    elements.append(img)

def add_technician_chart(elements, tech_data):
    """Agrega un gráfico de barras para los técnicos al PDF"""
    # Tomar solo los primeros 10 técnicos
    top_n = min(10, len(tech_data))

    plt.figure(figsize=(7, 4))
    bars = plt.barh(tech_data['Técnico'].head(top_n)[::-1],
                    tech_data['Promedio (min)'].head(top_n)[::-1],
                    alpha=0.7, color='green')

    # Añadir etiquetas
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width if width > 0 else 0
        plt.text(label_x_pos + 1, bar.get_y() + bar.get_height() / 2,
                 f'{width:.1f}',
                 va='center')

    plt.title('Duración Promedio por Técnico (Top 10)')
    plt.xlabel('Duración Promedio (minutos)')
    plt.ylabel('Técnico')
    plt.grid(True, linestyle='--', alpha=0.7, axis='x')
    plt.tight_layout()

    # Guardar la figura en un buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    plt.close()

    # Agregar la imagen al PDF
    img = Image(img_buffer, width=6 * inch, height=3 * inch)
    elements.append(img)

def add_terminal_model_chart(elements, terminal_data):
    """Agrega un gráfico de barras para los modelos de terminal al PDF"""
    # Tomar solo los primeros 10 modelos
    top_n = min(10, len(terminal_data))

    plt.figure(figsize=(7, 4))
    bars = plt.barh(terminal_data['Modelo de Terminal'].head(top_n)[::-1],
                    terminal_data['Promedio (min)'].head(top_n)[::-1],
                    alpha=0.7, color='purple')

    # Añadir etiquetas
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width if width > 0 else 0
        plt.text(label_x_pos + 1, bar.get_y() + bar.get_height() / 2,
                 f'{width:.1f}',
                 va='center')

    plt.title('Duración Promedio por Modelo de Terminal (Top 10)')
    plt.xlabel('Duración Promedio (minutos)')
    plt.ylabel('Modelo de Terminal')
    plt.grid(True, linestyle='--', alpha=0.7, axis='x')
    plt.tight_layout()

    # Guardar la figura en un buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    plt.close()

    # Agregar la imagen al PDF
    img = Image(img_buffer, width=6 * inch, height=3 * inch)
    elements.append(img)

def add_anomalies_chart(elements, anomalies_df):
    """Agrega un gráfico de dispersión para las anomalías al PDF"""
    plt.figure(figsize=(7, 4))

    # Colores para cada tipo de anomalía
    colors = {'Corta': 'blue', 'Larga': 'red', 'Normal': 'green'}

    # Aplanar los índices para el gráfico
    x = range(len(anomalies_df))

    # Graficar por tipo de anomalía
    for anomaly_type in anomalies_df['Tipo de Anomalía'].unique():
        mask = anomalies_df['Tipo de Anomalía'] == anomaly_type
        plt.scatter(
            [i for i, m in zip(x, mask) if m],
            anomalies_df.loc[mask, 'Duración (minutos)'].values,
            c=colors.get(anomaly_type, 'gray'),
            label=anomaly_type,
            alpha=0.7
        )

    plt.title('Distribución de Anomalías')
    plt.xlabel('Índice de Servicio')
    plt.ylabel('Duración (minutos)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()

    # Guardar la figura en un buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300)
    img_buffer.seek(0)
    plt.close()

    # Agregar la imagen al PDF
    img = Image(img_buffer, width=6 * inch, height=3 * inch)
    elements.append(img)