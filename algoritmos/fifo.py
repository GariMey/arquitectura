from modelos.proceso import Proceso

class PlanificadorFIFO:
    """Algoritmo de planificación First In First Out"""
    
    def __init__(self, procesos):
        self.procesos = procesos
        self.linea_tiempo = []
        self.tiempo_actual = 0
        self.procesos_completados = []
    
    def planificar(self):
        """Ejecuta la planificación FIFO"""
        # Ordenar procesos por tiempo de llegada
        procesos_ordenados = sorted(self.procesos, key=lambda p: p.tiempo_llegada)
        
        for proceso in procesos_ordenados:
            # Si el CPU está inactivo, avanzar el tiempo
            if self.tiempo_actual < proceso.tiempo_llegada:
                self.tiempo_actual = proceso.tiempo_llegada
            
            # Registrar inicio
            proceso.tiempo_inicio = self.tiempo_actual
            proceso.tiempo_espera = self.tiempo_actual - proceso.tiempo_llegada
            
            # Ejecutar proceso
            self.linea_tiempo.append((self.tiempo_actual, f"P{proceso.id}"))
            self.tiempo_actual += proceso.rafaga
            
            # Registrar finalización
            proceso.tiempo_finalizacion = self.tiempo_actual
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
            proceso.completado = True
            self.procesos_completados.append(proceso)
            
        return self.linea_tiempo
    
    def mostrar_gantt(self):
        """Muestra el diagrama de Gantt en consola"""
        if not self.linea_tiempo:
            return "No hay datos de ejecución"
        
        # Construir el diagrama
        gantt = "┌"
        for _, proceso in self.linea_tiempo:
            gantt += "─────┬"
        gantt = gantt[:-1] + "┐\n"
        
        # Nombres de procesos
        gantt += "│"
        for _, proceso in self.linea_tiempo:
            gantt += f" {proceso} │"
        gantt += "\n"
        
        # Línea inferior
        gantt += "└"
        for _ in self.linea_tiempo:
            gantt += "─────┴"
        gantt = gantt[:-1] + "┘\n"
        
        # Línea de tiempo (números)
        tiempos = []
        for tiempo, _ in self.linea_tiempo:
            tiempos.append(f"{tiempo:^5}")
        tiempos.append(f"{self.tiempo_actual:^5}")
        
        gantt += " " + "".join(tiempos)
        
        return gantt
    
    def calcular_estadisticas(self):
        """Calcula estadísticas de la planificación"""
        if not self.procesos_completados:
            return {}
        
        tiempos_espera = [p.tiempo_espera for p in self.procesos_completados]
        tiempos_retorno = [p.tiempo_retorno for p in self.procesos_completados]
        
        return {
            'tiempo_promedio_espera': sum(tiempos_espera) / len(tiempos_espera),
            'tiempo_promedio_retorno': sum(tiempos_retorno) / len(tiempos_retorno),
            'tiempo_total_cpu': self.tiempo_actual,
            'num_procesos': len(self.procesos_completados)
        }
    
    def obtener_detalles_procesos(self):
        """Obtiene detalles de cada proceso"""
        detalles = []
        for p in self.procesos:
            detalles.append({
                'id': p.id,
                'llegada': p.tiempo_llegada,
                'rafaga': p.rafaga,
                'espera': p.tiempo_espera,
                'retorno': p.tiempo_retorno,
                'finalizacion': p.tiempo_finalizacion
            })
        return detalles