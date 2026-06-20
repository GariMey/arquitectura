from modelos.proceso import Proceso

class PlanificadorRoundRobin:
    """Algoritmo de planificación Round Robin (Preventivo)"""
    
    def __init__(self, procesos, quantum):
        self.procesos = procesos
        self.quantum = quantum
        self.linea_tiempo = []
        self.tiempo_actual = 0
        self.procesos_completados = []
        self.cola_listos = []
    
    def planificar(self):
        """Ejecuta la planificación Round Robin"""
        # Reiniciar todos los procesos
        for p in self.procesos:
            p.reiniciar()
            p.tiempo_restante = p.rafaga  # Asegurar que tiempo_restante = ráfaga
        
        self.linea_tiempo = []
        self.tiempo_actual = 0
        self.procesos_completados = []
        self.cola_listos = []
        
        # Crear copia de procesos pendientes
        procesos_pendientes = self.procesos.copy()
        
        # Variable para rastrear el último proceso ejecutado
        proceso_anterior = None
        
        while procesos_pendientes or self.cola_listos:
            # Agregar a la cola de listos los procesos que han llegado
            procesos_llegaron = [p for p in procesos_pendientes if p.tiempo_llegada <= self.tiempo_actual]
            for p in procesos_llegaron:
                if p not in self.cola_listos:
                    self.cola_listos.append(p)
                    procesos_pendientes.remove(p)
            
            # Si no hay procesos en la cola de listos, avanzar el tiempo
            if not self.cola_listos:
                if procesos_pendientes:
                    siguiente_llegada = min(p.tiempo_llegada for p in procesos_pendientes)
                    self.tiempo_actual = siguiente_llegada
                    # Agregar procesos que llegaron en este tiempo
                    procesos_llegaron = [p for p in procesos_pendientes if p.tiempo_llegada <= self.tiempo_actual]
                    for p in procesos_llegaron:
                        self.cola_listos.append(p)
                        procesos_pendientes.remove(p)
                else:
                    break
            
            # Tomar el primer proceso de la cola
            proceso_actual = self.cola_listos.pop(0)
            
            # Registrar inicio si es la primera vez
            if proceso_actual.tiempo_inicio is None:
                proceso_actual.tiempo_inicio = self.tiempo_actual
                proceso_actual.tiempo_espera = self.tiempo_actual - proceso_actual.tiempo_llegada
            
            # Calcular tiempo de ejecución (quantum o lo que queda)
            tiempo_ejecucion = min(self.quantum, proceso_actual.tiempo_restante)
            
            # Registrar en la línea de tiempo
            self.linea_tiempo.append((self.tiempo_actual, f"P{proceso_actual.id}"))
            
            # Ejecutar el proceso
            self.tiempo_actual += tiempo_ejecucion
            proceso_actual.tiempo_restante -= tiempo_ejecucion
            
            # Verificar si el proceso ha terminado
            if proceso_actual.tiempo_restante <= 0:
                # Proceso completado
                proceso_actual.tiempo_finalizacion = self.tiempo_actual
                proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_llegada
                proceso_actual.completado = True
                self.procesos_completados.append(proceso_actual)
                
                # Si este proceso tenía tiempo de espera acumulado, actualizar
                # (los procesos en RR pueden tener múltiples períodos de espera)
                
            else:
                # El proceso no terminó, debe volver a la cola
                # Primero, verificar si llegaron nuevos procesos mientras se ejecutaba
                nuevos_procesos = [p for p in procesos_pendientes if p.tiempo_llegada <= self.tiempo_actual]
                for p in nuevos_procesos:
                    if p not in self.cola_listos:
                        self.cola_listos.append(p)
                        procesos_pendientes.remove(p)
                
                # Agregar el proceso actual al final de la cola
                self.cola_listos.append(proceso_actual)
        
        return self.linea_tiempo
    
    def mostrar_gantt(self):
        """Muestra el diagrama de Gantt en consola con formato mejorado"""
        if not self.linea_tiempo:
            return "No hay datos de ejecución"
        
        # Determinar el ancho máximo
        max_ancho = 7
        
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
        
        # Línea de tiempo
        tiempos = []
        for tiempo, _ in self.linea_tiempo:
            tiempos.append(f"{tiempo:^{max_ancho}}")
        tiempos.append(f"{self.tiempo_actual:^{max_ancho}}")
        
        gantt += " " + "".join(tiempos)
        
        return gantt
    
    def mostrar_gantt_detallado(self):
        """Muestra el diagrama de Gantt con detalles de quantum"""
        if not self.linea_tiempo:
            return "No hay datos de ejecución"
        
        # Crear una versión más detallada con los tiempos de cada segmento
        resultado = []
        for i, (tiempo, proceso) in enumerate(self.linea_tiempo):
            # Determinar hasta dónde va este segmento
            if i < len(self.linea_tiempo) - 1:
                tiempo_fin = self.linea_tiempo[i + 1][0]
            else:
                tiempo_fin = self.tiempo_actual
            duracion = tiempo_fin - tiempo
            
            # Mostrar el segmento
            resultado.append(f"{proceso} [{tiempo}->{tiempo_fin}] (duración: {duracion})")
        
        return "\n".join(resultado)
    
    def calcular_estadisticas(self):
        """Calcula estadísticas de la planificación"""
        if not self.procesos_completados:
            return {}
        
        tiempos_espera = [p.tiempo_espera for p in self.procesos_completados]
        tiempos_retorno = [p.tiempo_retorno for p in self.procesos_completados]
        
        # Para Round Robin, el tiempo de espera se calcula como:
        # Tiempo de espera total = Tiempo de finalización - Tiempo de llegada - Tiempo de ejecución total
        # Pero ya lo calculamos en el proceso de planificación
        
        return {
            'tiempo_promedio_espera': sum(tiempos_espera) / len(tiempos_espera),
            'tiempo_promedio_retorno': sum(tiempos_retorno) / len(tiempos_retorno),
            'tiempo_total_cpu': self.tiempo_actual,
            'num_procesos': len(self.procesos_completados),
            'quantum': self.quantum
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
                'prioridad': p.prioridad,
                'restante_final': p.tiempo_restante
            })
        return detalles