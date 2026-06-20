# modelos/planificador.py
from abc import ABC, abstractmethod

class Planificador(ABC):
    """Clase base abstracta para todos los planificadores"""
    
    def __init__(self, procesos):
        self.procesos = procesos
        self.linea_tiempo = []  # Lista de (tiempo, id_proceso)
        self.tiempo_actual = 0
        
    @abstractmethod
    def planificar(self):
        """Método que debe implementar cada algoritmo"""
        pass
    
    def calcular_estadisticas(self):
        """Calcula estadísticas después de la planificación"""
        if not self.procesos:
            return {}
            
        tiempos_espera = [p.tiempo_espera for p in self.procesos if p.completado]
        tiempos_retorno = [p.tiempo_retorno for p in self.procesos if p.completado]
        
        return {
            'tiempo_promedio_espera': sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0,
            'tiempo_promedio_retorno': sum(tiempos_retorno) / len(tiempos_retorno) if tiempos_retorno else 0,
            'tiempo_total_cpu': max([p.tiempo_finalizacion for p in self.procesos if p.completado], default=0)
        }
    
    def generar_gantt(self):
        """Genera representación del diagrama de Gantt"""
        if not self.linea_tiempo:
            return "No hay datos de ejecución"
        
        # Crear representación en texto
        resultado = ""
        tiempo_anterior = 0
        for tiempo, id_proceso in self.linea_tiempo:
            if tiempo > tiempo_anterior:
                resultado += f"| {id_proceso} "
                tiempo_anterior = tiempo
        
        # Agregar línea de tiempo
        resultado += "|\n"
        tiempos = [str(t) for t, _ in self.linea_tiempo]
        resultado += " ".join(tiempos)
        
        return resultado