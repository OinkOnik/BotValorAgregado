# excel_processor.py
# Módulo para procesar archivos Excel y extraer/calcular datos de tiempo

import pandas as pd
from datetime import datetime, timedelta


def process_excel_file(file_path):
    """
    Procesa un archivo Excel para calcular tiempos de estadía basados en hora de llegada y salida

    Args:
        file_path: Ruta al archivo Excel a procesar

    Returns:
        Un diccionario con datos procesados organizados por oficial técnico
    """
    try:
        # Cargar el archivo Excel
        df = pd.read_excel(file_path)

        # Verificar que las columnas necesarias existan
        required_columns = ['Nombre del oficial técnico que brinda servicio',
                            'Hora de llegada', 'Hora de salida']

        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"El archivo Excel no contiene la columna: {col}")

        # Filtrar filas con datos faltantes en columnas cruciales
        df_filtered = df.dropna(subset=required_columns)

        if df_filtered.empty:
            return None

        # Asegurarse de que las columnas de tiempo sean del tipo datetime
        for col in ['Hora de llegada', 'Hora de salida']:
            if not pd.api.types.is_datetime64_any_dtype(df_filtered[col]):
                df_filtered[col] = pd.to_datetime(df_filtered[col], errors='coerce')

        # Filtrar filas donde la conversión de fecha/hora falló
        df_filtered = df_filtered.dropna(subset=['Hora de llegada', 'Hora de salida'])

        # Calcular el tiempo de estadía
        df_filtered['Tiempo de estadía'] = df_filtered['Hora de salida'] - df_filtered['Hora de llegada']

        # Organizar los datos por oficial técnico
        result = {}

        for officer, group in df_filtered.groupby('Nombre del oficial técnico que brinda servicio'):
            records = []

            for _, row in group.iterrows():
                # Calcular tiempo de estadía en formato legible (horas y minutos)
                tiempo_estadia = row['Tiempo de estadía']
                horas = int(tiempo_estadia.total_seconds() // 3600)
                minutos = int((tiempo_estadia.total_seconds() % 3600) // 60)

                records.append({
                    'Hora de llegada': row['Hora de llegada'],
                    'Hora de salida': row['Hora de salida'],
                    'Tiempo de estadía': f"{horas} horas, {minutos} minutos",
                    'Tiempo de estadía (segundos)': tiempo_estadia.total_seconds()  # Para ordenar
                })

            # Ordenar por hora de llegada
            records.sort(key=lambda x: x['Hora de llegada'])

            # Calcular estadísticas
            total_seconds = sum(record['Tiempo de estadía (segundos)'] for record in records)
            avg_seconds = total_seconds / len(records) if records else 0

            avg_hours = int(avg_seconds // 3600)
            avg_minutes = int((avg_seconds % 3600) // 60)

            result[officer] = {
                'records': records,
                'total_records': len(records),
                'avg_time': f"{avg_hours} horas, {avg_minutes} minutos",
                'total_time': format_seconds_to_time(total_seconds)
            }

        return result

    except Exception as e:
        # Re-lanzar la excepción para manejarla en el nivel superior
        raise Exception(f"Error al procesar el archivo Excel: {str(e)}")


def format_seconds_to_time(seconds):
    """
    Convierte segundos a un formato legible de horas y minutos

    Args:
        seconds: Tiempo en segundos

    Returns:
        String con formato "X horas, Y minutos"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours} horas, {minutes} minutos"