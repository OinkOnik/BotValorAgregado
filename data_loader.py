# data_loader.py
# Funciones para cargar y limpiar datos de archivos Excel
# Maneja la carga de archivos, limpieza de datos y validación de columnas

import pandas as pd
import os


def load_excel_file(file_path):
    """
    Carga un archivo Excel y lo convierte en un DataFrame de pandas.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe")

    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error al cargar el archivo Excel: {str(e)}")


def clean_time_data(df):
    """
    Limpia y formatea las columnas de tiempo (Hora de llegada y Hora de salida).
    """
    df_clean = df.copy()

    time_columns = ['Hora de llegada', 'Hora de salida']
    if all(col in df.columns for col in time_columns):
        for col in time_columns:
            # Intentamos convertir a datetime si no lo es ya
            if df_clean[col].dtype != 'datetime64[ns]':
                try:
                    df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                except:
                    pass

    return df_clean


def validate_required_columns(df, required_columns):
    """
    Verifica que el DataFrame tenga las columnas necesarias para el análisis.
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Faltan columnas necesarias: {', '.join(missing_columns)}")
    return True