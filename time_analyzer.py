#time_analyzer.py

import pandas as pd
import numpy as np


def calculate_service_duration(df):
    """
    Calcula la duración de cada servicio basado en la hora de llegada y salida.
    """
    # Verificamos que las columnas necesarias existan
    required_columns = ['Hora de llegada', 'Hora de salida']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(
            f"Faltan columnas necesarias: {', '.join([col for col in required_columns if col not in df.columns])}")

    # Creamos una copia para no modificar el original
    df_result = df.copy()

    # Calculamos la duración en minutos
    df_result['Duración (minutos)'] = (df_result['Hora de salida'] - df_result[
        'Hora de llegada']).dt.total_seconds() / 60

    # Manejamos valores negativos o nulos (posibles errores de datos)
    df_result.loc[df_result['Duración (minutos)'] < 0, 'Duración (minutos)'] = np.nan

    return df_result


def get_average_duration_by_technician(df):
    """
    Calcula la duración promedio de servicio por técnico.
    """
    if 'Duración (minutos)' not in df.columns:
        raise ValueError("El DataFrame debe tener la columna 'Duración (minutos)'")

    # Cambiamos para usar la columna 'Nombre del oficial técnico que brinda servicio'
    if 'Nombre del oficial técnico que brinda servicio' not in df.columns:
        raise ValueError("El DataFrame debe tener la columna 'Nombre del oficial técnico que brinda servicio'")

    avg_by_tech = df.groupby('Nombre del oficial técnico que brinda servicio')['Duración (minutos)'].agg(
        ['mean', 'count', 'min', 'max']).reset_index()
    avg_by_tech.columns = ['Técnico', 'Promedio (min)', 'Cantidad', 'Mínimo (min)', 'Máximo (min)']

    return avg_by_tech.sort_values('Promedio (min)')


def get_average_duration_by_terminal_model(df):
    """
    Calcula la duración promedio por modelo de terminal.
    """
    if 'Duración (minutos)' not in df.columns:
        raise ValueError("El DataFrame debe tener la columna 'Duración (minutos)'")

    # Buscamos columnas que contengan "Terminal - Modelo"
    terminal_columns = [col for col in df.columns if 'Terminal - Modelo' in col]

    if not terminal_columns:
        # Intenta buscar otras columnas que puedan contener información del modelo
        terminal_columns = [col for col in df.columns if 'Modelo de Terminal' in col]

    if not terminal_columns:
        raise ValueError("No se encontraron columnas de modelo de terminal")

    # Usamos la primera columna de modelo de terminal
    terminal_col = terminal_columns[0]

    avg_by_model = df.groupby(terminal_col)['Duración (minutos)'].agg(
        ['mean', 'count', 'min', 'max']).reset_index()
    avg_by_model.columns = ['Modelo de Terminal', 'Promedio (min)', 'Cantidad', 'Mínimo (min)', 'Máximo (min)']

    return avg_by_model.sort_values('Promedio (min)')


def identify_anomalies(df, threshold_factor=1.5):
    """
    Identifica servicios con duraciones anómalas (muy largas o muy cortas).
    """
    if 'Duración (minutos)' not in df.columns:
        raise ValueError("El DataFrame debe tener la columna 'Duración (minutos)'")

    # Calculamos el rango intercuartílico
    Q1 = df['Duración (minutos)'].quantile(0.25)
    Q3 = df['Duración (minutos)'].quantile(0.75)
    IQR = Q3 - Q1

    # Definimos los umbrales para anomalías
    lower_bound = Q1 - threshold_factor * IQR
    upper_bound = Q3 + threshold_factor * IQR

    # Identificamos anomalías
    anomalies = df[(df['Duración (minutos)'] < lower_bound) |
                   (df['Duración (minutos)'] > upper_bound)].copy()

    # Marcamos el tipo de anomalía
    anomalies['Tipo de Anomalía'] = 'Normal'
    anomalies.loc[anomalies['Duración (minutos)'] < lower_bound, 'Tipo de Anomalía'] = 'Corta'
    anomalies.loc[anomalies['Duración (minutos)'] > upper_bound, 'Tipo de Anomalía'] = 'Larga'

    return anomalies