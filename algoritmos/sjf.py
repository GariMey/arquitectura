from modelos.proceso import Proceso

class PlanificadorSJF:
    """Algoritmo de planificación Shortest Job First (No preventivo)"""
    
    def __init__(self, procesos):
        self.procesos = procesos
        self.linea_tiempo = []
        self.tiempo_actual = 0
        self.procesos_completados = []
        self.procesos_pendientes = []
    
    def planificar(self):
        """Ejecuta la planificación SJF no preventivo"""
        # Crear copia de los procesos
        self.procesos_pendientes = self.procesos.copy()
        self.linea_tiempo = []
        self.tiempo_actual = 0
        self.procesos_completados = []
        
        # Reiniciar todos los procesos
        for p in self.procesos:
            p.reiniciar()
        
        while self.procesos_pendientes:
            # Filtrar procesos que ya han llegado
            disponibles = [p for p in self.procesos_pendientes 
                          if p.tiempo_llegada <= self.tiempo_actual]
            
            if not disponibles:
                # Si no hay procesos disponibles, avanzar al siguiente llegada
                siguiente_llegada = min(p.tiempo_llegada for p in self.procesos_pendientes)
                self.tiempo_actual = siguiente_llegada
                disponibles = [p for p in self.procesos_pendientes 
                              if p.tiempo_llegada <= self.tiempo_actual]
            
            # Seleccionar el proceso con la ráfaga más corta
            proceso_seleccionado = min(disponibles, key=lambda p: p.rafaga)
            
            # Registrar inicio
            proceso_seleccionado.tiempo_inicio = self.tiempo_actual
            proceso_seleccionado.tiempo_espera = self.tiempo_actual - proceso_seleccionado.tiempo_llegada
            
            # Ejecutar proceso (no preventivo)
            self.linea_tiempo.append((self.tiempo_actual, f"P{proceso_seleccionado.id}"))
            self.tiempo_actual += proceso_seleccionado.rafaga
            
            # Registrar finalización
            proceso_seleccionado.tiempo_finalizacion = self.tiempo_actual
            proceso_seleccionado.tiempo_retorno = proceso_seleccionado.tiempo_finalizacion - proceso_seleccionado.tiempo_llegada
            proceso_seleccionado.completado = True
            self.procesos_completados.append(proceso_seleccionado)
            
            # Eliminar de pendientes
            self.procesos_pendientes.remove(proceso_seleccionado)
        
        return self.linea_tiempo
    
    def mostrar_gantt(self):
        """Muestra el diagrama de Gantt en consola"""
        if not self.linea_tiempo:
            return "No hay datos de ejecución"
        
        # Calcular ancho máximo
        max_ancho = 7  # Ancho base para cada celda
        
        # Construir el diagrama
        gantt = "┌"
        for _ in self.linea_tiempo:
            gantt += "─" * max_ancho + "┬"
        gantt = gantt[:-1] + "┐\n"
        
        # Nombres de procesos
        gantt += "│"
        for _, proceso in self.linea_tiempo:
            gantt += f" {proceso:^{max_ancho-1}} │"
        gantt += "\n"
        
        # Línea inferior
        gantt += "└"
        for _ in self.linea_tiempo:
            gantt += "─" * max_ancho + "┴"
        gantt = gantt[:-1] + "┘\n"
        
        # Línea de tiempo (números)
        tiempos = []
        for tiempo, _ in self.linea_tiempo:
            tiempos.append(f"{tiempo:^{max_ancho}}")
        tiempos.append(f"{self.tiempo_actual:^{max_ancho}}")
        
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
                'finalizacion': p.tiempo_finalizacion,
                'prioridad': p.prioridad
            })
        return detalles