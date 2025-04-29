# excel_processor.py
# Módulo para procesar archivos Excel y extraer/calcular datos de tiempo de manera robusta

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

        # Validar columnas requeridas
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"El archivo Excel no contiene la columna: {col}")

        # Filtrar filas con datos faltantes en columnas cruciales
        df_filtered = df.dropna(subset=required_columns)

        if df_filtered.empty:
            return {}  # Retornar diccionario vacío en lugar de None

        # Asegurarse de que las columnas de tiempo sean del tipo datetime
        # Especificamos el formato de fecha/hora para evitar warnings y mejorar la precisión
        # Probamos múltiples formatos comunes para mayor robustez
        for col in ['Hora de llegada', 'Hora de salida']:
            if not pd.api.types.is_datetime64_any_dtype(df_filtered[col]):
                # Intentar con diferentes formatos de hora comunes, incluido el formato "03:22 PM GMT-06:00"
                try:
                    # Primero intentamos con el formato específico del error
                    df_filtered[col] = pd.to_datetime(df_filtered[col], format='%I:%M %p GMT%z', errors='raise')
                except ValueError:
                    # Si falla, probamos con formato de 12 horas (AM/PM)
                    try:
                        df_filtered[col] = pd.to_datetime(df_filtered[col], format='%I:%M %p', errors='raise')
                    except ValueError:
                        # Si también falla, probamos con formato de 24 horas
                        try:
                            df_filtered[col] = pd.to_datetime(df_filtered[col], format='%H:%M', errors='raise')
                        except ValueError:
                            # Si todo falla, caemos de nuevo en coerce pero ya evitamos el warning
                            df_filtered[col] = pd.to_datetime(df_filtered[col], errors='coerce')

        # Filtrar filas donde la conversión de fecha/hora falló
        df_filtered = df_filtered.dropna(subset=['Hora de llegada', 'Hora de salida'])

        # Calcular el tiempo de estadía
        df_filtered['Tiempo de estadía'] = df_filtered['Hora de salida'] - df_filtered['Hora de llegada']

        # Organizar los datos por oficial técnico
        result = {}

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
                record_entry = {
                    'Hora de llegada': row['Hora de llegada'],
                    'Hora de salida': row['Hora de salida'],
                    'Tiempo de estadía': tiempo_texto,
                    'Tiempo de estadía (segundos)': segundos_estadia,  # Para ordenar
                    'Es tiempo válido': es_tiempo_valido  # Para filtrar en estadísticas
                }
                records.append(record_entry)

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

            # Formatear tiempo total y promedio
            avg_hours = int(avg_seconds // 3600)
            avg_minutes = int((avg_seconds % 3600) // 60)

            # Formatear tiempo total
            total_hours = int(total_seconds // 3600)
            total_minutes = int((total_seconds % 3600) // 60)

            result[officer] = {
                'records': records,
                'total_records': len(records),  # Total de registros incluyendo anomalías
                'valid_records': total_valid_records,  # Solo registros con tiempo positivo
                'avg_time': f"{avg_hours} horas, {avg_minutes} minutos" if total_valid_records > 0 else "N/A",
                'total_time': f"{total_hours} horas, {total_minutes} minutos" if total_valid_records > 0 else "N/A"
            }

        return result

    except Exception as e:
        # Re-lanzar la excepción con un mensaje más descriptivo
        raise Exception(f"Error al procesar el archivo Excel: {str(e)}")


def format_seconds_to_time(seconds):
    """
    Convierte segundos a un formato legible de horas y minutos

    Args:
        seconds: Tiempo en segundos

    Returns:
        String con formato "X horas, Y minutos"
    """
    if seconds is None or seconds < 0:
        return "N/A"

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours} horas, {minutes} minutos"