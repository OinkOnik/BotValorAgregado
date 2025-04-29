# excel_processor.py
# Módulo para procesar archivos Excel y extraer/calcular datos de tiempo

import pandas as pd
from datetime import datetime, timedelta
from collections import Counter


def process_excel_file(file_path):
    """
    Procesa un archivo Excel para calcular tiempos de estadía basados en hora de llegada y salida,
    y analiza información de afiliados con problemas y sus razones.

    Args:
        file_path: Ruta al archivo Excel a procesar

    Returns:
        Un diccionario con datos procesados organizados por oficial técnico y análisis de afiliados
    """
    try:
        # Cargar el archivo Excel
        df = pd.read_excel(file_path)

        # Verificar que las columnas necesarias existan
        required_columns = ['Nombre del oficial técnico que brinda servicio',
                            'Hora de llegada', 'Hora de salida']

        # Columnas adicionales para el análisis de afiliados
        additional_columns = ['Nombre del Afiliado', 'Evaluaciones a realizar']

        # Verificar columnas requeridas
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"El archivo Excel no contiene la columna: {col}")

        # Verificar si existen las columnas adicionales para análisis de afiliados
        afiliados_analysis_possible = all(col in df.columns for col in additional_columns)

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

        # Análisis de afiliados con problemas
        afiliados_analysis = None
        if afiliados_analysis_possible:
            afiliados_analysis = analyze_affiliates_issues(df)

        for officer, group in df_filtered.groupby('Nombre del oficial técnico que brinda servicio'):
            records = []
            valid_records_seconds = []  # Lista para almacenar solo los tiempos válidos (positivos)

            for _, row in group.iterrows():
                # Calcular tiempo de estadía en formato legible (horas y minutos)
                tiempo_estadia = row['Tiempo de estadía']
                segundos_estadia = tiempo_estadia.total_seconds()

                # Determinar si el tiempo es válido (positivo)
                es_tiempo_valido = segundos_estadia > 0

                horas = int(abs(segundos_estadia) // 3600)
                minutos = int((abs(segundos_estadia) % 3600) // 60)

                # Para tiempo negativo, agregar indicador
                if segundos_estadia < 0:
                    tiempo_texto = f"-{horas} horas, {minutos} minutos (anomalía)"
                else:
                    tiempo_texto = f"{horas} horas, {minutos} minutos"

                # Agregar el registro a la lista de todos los registros
                records.append({
                    'Hora de llegada': row['Hora de llegada'],
                    'Hora de salida': row['Hora de salida'],
                    'Tiempo de estadía': tiempo_texto,
                    'Tiempo de estadía (segundos)': segundos_estadia,  # Para ordenar
                    'Es tiempo válido': es_tiempo_valido  # Para filtrar en estadísticas
                })

                # Si el tiempo es válido (positivo), agregarlo a la lista para estadísticas
                if es_tiempo_valido:
                    valid_records_seconds.append(segundos_estadia)

            # Ordenar por hora de llegada
            records.sort(key=lambda x: x['Hora de llegada'])

            # Calcular estadísticas solo con tiempos válidos
            total_valid_records = len(valid_records_seconds)

            if total_valid_records > 0:
                total_seconds = sum(valid_records_seconds)
                avg_seconds = total_seconds / total_valid_records
            else:
                total_seconds = 0
                avg_seconds = 0

            avg_hours = int(avg_seconds // 3600)
            avg_minutes = int((avg_seconds % 3600) // 60)

            result[officer] = {
                'records': records,
                'total_records': len(records),  # Total de registros incluyendo anomalías
                'valid_records': total_valid_records,  # Solo registros con tiempo positivo
                'avg_time': f"{avg_hours} horas, {avg_minutes} minutos",
                'total_time': format_seconds_to_time(total_seconds)
            }

        # Agregar el análisis de afiliados al resultado
        if afiliados_analysis:
            result['afiliados_analysis'] = afiliados_analysis

        return result

    except Exception as e:
        # Re-lanzar la excepción para manejarla en el nivel superior
        raise Exception(f"Error al procesar el archivo Excel: {str(e)}")


def analyze_affiliates_issues(df):
    """
    Analiza los afiliados con más problemas y las razones principales

    Args:
        df: DataFrame con los datos del Excel

    Returns:
        Diccionario con análisis de afiliados y sus problemas
    """
    try:
        # Verificar que existan las columnas necesarias
        if 'Nombre del Afiliado' not in df.columns or 'Evaluaciones a realizar' not in df.columns:
            return None

        # Eliminar filas con valores faltantes en las columnas de interés
        df_analysis = df.dropna(subset=['Nombre del Afiliado', 'Evaluaciones a realizar'])

        if df_analysis.empty:
            return None

        # Contar la frecuencia de cada afiliado
        afiliado_counts = Counter(df_analysis['Nombre del Afiliado'])

        # Obtener los 5 afiliados con más problemas (o todos si hay menos de 5)
        top_afiliados = afiliado_counts.most_common(5)

        # Para cada afiliado, analizar las razones de sus problemas
        afiliados_data = []

        for afiliado, count in top_afiliados:
            # Filtrar el DataFrame para este afiliado
            afiliado_df = df_analysis[df_analysis['Nombre del Afiliado'] == afiliado]

            # Contar la frecuencia de cada razón para este afiliado
            razones = Counter(afiliado_df['Evaluaciones a realizar'])
            top_razones = razones.most_common(3)  # Top 3 razones

            afiliados_data.append({
                'nombre': afiliado,
                'total_casos': count,
                'razones': [{'razon': razon, 'frecuencia': freq} for razon, freq in top_razones]
            })

        return {
            'top_afiliados': afiliados_data,
            'total_afiliados': len(afiliado_counts)
        }

    except Exception as e:
        # Si ocurre algún error, simplemente retornar None
        print(f"Error en análisis de afiliados: {str(e)}")
        return None


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