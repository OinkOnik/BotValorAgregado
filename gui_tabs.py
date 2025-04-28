# gui_tabs.py
# Funciones para actualizar las pestañas de la interfaz
# Cada función se encarga de llenar una pestaña con los datos correspondientes

from PyQt5.QtWidgets import QLabel
from gui_components import clear_layout, create_table_from_dataframe, create_figure
from time_analyzer import (get_average_duration_by_technician,
                          get_average_duration_by_terminal_model,
                          identify_anomalies)

def update_summary_tab(layout, df):
    """Actualiza la pestaña de resumen con estadísticas generales"""
    # Limpiamos el layout
    clear_layout(layout)

    if df is None or 'Duración (minutos)' not in df.columns:
        return

    # Calculamos estadísticas básicas
    total_services = len(df)
    avg_duration = df['Duración (minutos)'].mean()
    min_duration = df['Duración (minutos)'].min()
    max_duration = df['Duración (minutos)'].max()

    # Creamos el contenido del resumen
    layout.addWidget(QLabel(f"<h2>Estadísticas de Tiempos de Servicio</h2>"))
    layout.addWidget(QLabel(f"<b>Total de servicios:</b> {total_services}"))
    layout.addWidget(QLabel(f"<b>Duración promedio:</b> {avg_duration:.2f} minutos"))
    layout.addWidget(QLabel(f"<b>Duración mínima:</b> {min_duration:.2f} minutos"))
    layout.addWidget(QLabel(f"<b>Duración máxima:</b> {max_duration:.2f} minutos"))

    # Creamos un histograma de duración
    fig, canvas = create_figure()
    ax = fig.add_subplot(111)

    ax.hist(df['Duración (minutos)'].dropna(), bins=20, alpha=0.7, color='blue')
    ax.set_title('Distribución de Tiempos de Servicio')
    ax.set_xlabel('Duración (minutos)')
    ax.set_ylabel('Frecuencia')
    ax.grid(True, linestyle='--', alpha=0.7)
    fig.tight_layout()

    layout.addWidget(canvas)
    layout.addStretch()

def update_technician_tab(layout, df):
    """Actualiza la pestaña de análisis por técnico"""
    # Limpiamos el layout
    clear_layout(layout)

    # Cambiamos para usar 'Nombre del oficial técnico que brinda servicio'
    if df is None or 'Duración (minutos)' not in df.columns or 'Nombre del oficial técnico que brinda servicio' not in df.columns:
        layout.addWidget(QLabel("No hay datos disponibles o faltan columnas necesarias"))
        return

    try:
        # Obtenemos los datos por técnico
        tech_data = get_average_duration_by_technician(df)

        # Creamos la tabla
        table = create_table_from_dataframe(tech_data)
        layout.addWidget(QLabel("<h2>Duración Promedio por Técnico</h2>"))
        layout.addWidget(table)

        # Creamos un gráfico de barras
        fig, canvas = create_figure()
        ax = fig.add_subplot(111)

        # Ordenamos por promedio para el gráfico
        tech_data_sorted = tech_data.sort_values('Promedio (min)', ascending=False)
        top_n = min(10, len(tech_data_sorted))  # Mostrar top 10 o menos

        bars = ax.bar(tech_data_sorted['Técnico'].head(top_n),
                      tech_data_sorted['Promedio (min)'].head(top_n),
                      alpha=0.7)

        # Añadimos etiquetas
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.,
                    height + 1,
                    f'{height:.1f}',
                    ha='center', va='bottom', rotation=0)

        ax.set_title('Duración Promedio por Técnico (Top 10)')
        ax.set_xlabel('Técnico')
        ax.set_ylabel('Duración Promedio (minutos)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        layout.addWidget(canvas)

    except Exception as e:
        layout.addWidget(QLabel(f"Error al procesar datos: {str(e)}"))

    layout.addStretch()

def update_terminal_model_tab(layout, df):
    """Actualiza la pestaña de análisis por modelo de terminal"""
    # Limpiamos el layout
    clear_layout(layout)

    if df is None or 'Duración (minutos)' not in df.columns:
        layout.addWidget(QLabel("No hay datos disponibles o faltan columnas necesarias"))
        return

    try:
        # Obtenemos los datos por modelo de terminal
        terminal_data = get_average_duration_by_terminal_model(df)

        # Creamos la tabla
        table = create_table_from_dataframe(terminal_data)
        layout.addWidget(QLabel("<h2>Duración Promedio por Modelo de Terminal</h2>"))
        layout.addWidget(table)

        # Creamos un gráfico de barras
        fig, canvas = create_figure()
        ax = fig.add_subplot(111)

        # Ordenamos por promedio para el gráfico
        terminal_data_sorted = terminal_data.sort_values('Promedio (min)', ascending=False)
        top_n = min(10, len(terminal_data_sorted))  # Mostrar top 10 o menos

        bars = ax.bar(terminal_data_sorted['Modelo de Terminal'].head(top_n),
                      terminal_data_sorted['Promedio (min)'].head(top_n),
                      alpha=0.7,
                      color='purple')

        # Añadimos etiquetas
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.,
                    height + 1,
                    f'{height:.1f}',
                    ha='center', va='bottom', rotation=0)

        ax.set_title('Duración Promedio por Modelo de Terminal (Top 10)')
        ax.set_xlabel('Modelo de Terminal')
        ax.set_ylabel('Duración Promedio (minutos)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        layout.addWidget(canvas)

    except Exception as e:
        layout.addWidget(QLabel(f"Error al procesar datos: {str(e)}"))

    layout.addStretch()

def update_anomalies_tab(layout, df):
    """Actualiza la pestaña de anomalías"""
    # Limpiamos el layout
    clear_layout(layout)

    if df is None or 'Duración (minutos)' not in df.columns:
        layout.addWidget(QLabel("No hay datos disponibles o faltan columnas necesarias"))
        return

    try:
        # Obtenemos las anomalías
        anomalies_df = identify_anomalies(df)

        # Filtramos columnas relevantes para la tabla
        relevant_columns = [
            'Nombre del Afiliado', 'Nombre del oficial técnico que brinda servicio',
            'Hora de llegada', 'Hora de salida', 'Duración (minutos)', 'Tipo de Anomalía'
        ]

        # Filtramos solo las columnas que existen en el DataFrame
        filtered_columns = [col for col in relevant_columns if col in anomalies_df.columns]

        # Si no hay columnas relevantes, usamos todas
        if not filtered_columns:
            filtered_columns = anomalies_df.columns

        anomalies_display = anomalies_df[filtered_columns].copy()

        # Creamos la tabla
        table = create_table_from_dataframe(anomalies_display)

        layout.addWidget(QLabel("<h2>Servicios con Duraciones Anómalas</h2>"))
        layout.addWidget(QLabel(f"Total de anomalías detectadas: {len(anomalies_df)}"))
        layout.addWidget(table)

        # Creamos un gráfico de dispersión
        fig, canvas = create_figure()
        ax = fig.add_subplot(111)

        # Colores para cada tipo de anomalía
        colors = {'Corta': 'blue', 'Larga': 'red', 'Normal': 'green'}

        # Aplanamos los índices para el gráfico
        x = range(len(anomalies_df))

        for anomaly_type in anomalies_df['Tipo de Anomalía'].unique():
            mask = anomalies_df['Tipo de Anomalía'] == anomaly_type
            filtered_indices = [i for i, m in zip(x, mask) if m]
            filtered_durations = anomalies_df.loc[mask, 'Duración (minutos)'].values

            if len(filtered_indices) > 0:
                ax.scatter(
                    filtered_indices,
                    filtered_durations,
                    c=colors.get(anomaly_type, 'gray'),
                    label=anomaly_type,
                    alpha=0.7
                )

        ax.set_title('Distribución de Anomalías')
        ax.set_xlabel('Índice de Servicio')
        ax.set_ylabel('Duración (minutos)')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        fig.tight_layout()

        layout.addWidget(canvas)

    except Exception as e:
        layout.addWidget(QLabel(f"Error al procesar anomalías: {str(e)}"))

    layout.addStretch()