import os
from datetime import datetime
from modelos.proceso import Proceso

class GestorArchivos:
    """Clase para manejar la carga y guardado de procesos desde/hacia archivos"""
    
    @staticmethod
    def cargar_procesos_desde_archivo(nombre_archivo):
        """
        Carga procesos desde un archivo .txt
        Formato esperado por línea: ID,Llegada,Ráfaga,Prioridad,Tipo
        Ejemplo:
            1,0,5,1,Rojo
            2,1,3,2,Amarillo
            3,2,8,1,Verde
        """
        procesos = []
        
        if not os.path.exists(nombre_archivo):
            print(f"❌ Error: El archivo '{nombre_archivo}' no existe")
            return procesos
            
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                for linea_num, linea in enumerate(archivo, 1):
                    linea = linea.strip()
                    if not linea or linea.startswith('#'):  # Ignorar líneas vacías y comentarios
                        continue
                        
                    partes = linea.split(',')
                    if len(partes) < 3:
                        print(f"⚠️ Línea {linea_num}: Formato inválido (se necesitan al menos 3 campos)")
                        continue
                        
                    try:
                        id_proceso = int(partes[0].strip())
                        llegada = int(partes[1].strip())
                        rafaga = int(partes[2].strip())
                        prioridad = int(partes[3].strip()) if len(partes) > 3 else 0
                        tipo_paciente = partes[4].strip() if len(partes) > 4 else None
                        
                        # Crear el proceso con tipo si existe
                        if tipo_paciente:
                            proceso = Proceso(id_proceso, llegada, rafaga, tipo_paciente=tipo_paciente)
                        else:
                            proceso = Proceso(id_proceso, llegada, rafaga, prioridad)
                        procesos.append(proceso)
                    except ValueError as e:
                        print(f"⚠️ Línea {linea_num}: Error al parsear - {e}")
                        
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")
            
        return procesos
    
    @staticmethod
    def guardar_historial(procesos, nombre_archivo='historial.txt'):
        """
        Guarda los procesos completados en un archivo de historial
        """
        if not procesos:
            print("❌ No hay procesos para guardar")
            return False
            
        try:
            # Verificar si el archivo ya existe para añadir o crear
            modo = 'a' if os.path.exists(nombre_archivo) else 'w'
            
            with open(nombre_archivo, modo, encoding='utf-8') as archivo:
                # Si es nuevo, escribir encabezado
                if modo == 'w':
                    archivo.write("ID,Llegada,Ráfaga,Prioridad,Tipo,Espera,Retorno,Finalizacion,Fecha\n")
                
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                for p in procesos:
                    if hasattr(p, 'completado') and p.completado:
                        tipo_str = p.tipo_paciente if hasattr(p, 'tipo_paciente') and p.tipo_paciente else ""
                        archivo.write(f"{p.id},{p.tiempo_llegada},{p.rafaga},{p.prioridad},{tipo_str},{p.tiempo_espera},{p.tiempo_retorno},{p.tiempo_finalizacion},{fecha}\n")
                        
            print(f"✅ Historial guardado en '{nombre_archivo}'")
            return True
        except Exception as e:
            print(f"❌ Error al guardar historial: {e}")
            return False
    
    @staticmethod
    def mostrar_historial(nombre_archivo='historial.txt'):
        """Muestra el contenido del historial"""
        if not os.path.exists(nombre_archivo):
            print("📋 No hay historial disponible")
            return
            
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                print("\n📋 HISTORIAL DE PROCESOS COMPLETADOS")
                print("=" * 80)
                print(contenido)
        except Exception as e:
            print(f"❌ Error al leer historial: {e}")
    
    @staticmethod
    def guardar_procesos_txt(procesos, nombre_archivo='procesos_guardados.txt'):
        """
        Guarda procesos en un archivo .txt con el formato estándar
        """
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                # Escribir encabezado
                archivo.write("# Archivo de procesos guardados\n")
                archivo.write("# Formato: ID,Llegada,Ráfaga,Prioridad,Tipo\n")
                archivo.write("# Tipos disponibles: Rojo, Amarillo, Embarazada, Verde, Cita, Seguimiento\n\n")
                
                for p in procesos:
                    tipo_str = p.tipo_paciente if hasattr(p, 'tipo_paciente') and p.tipo_paciente else ""
                    archivo.write(f"{p.id},{p.tiempo_llegada},{p.rafaga},{p.prioridad},{tipo_str}\n")
                    
            print(f"✅ Procesos guardados en '{nombre_archivo}'")
            return True
        except Exception as e:
            print(f"❌ Error al guardar procesos: {e}")
            return False