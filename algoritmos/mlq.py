from modelos.proceso import Proceso
from algoritmos.fifo import PlanificadorFIFO
from algoritmos.sjf import PlanificadorSJF
from algoritmos.round_robin import PlanificadorRoundRobin


class PlanificadorMLQ:
    """
    Multi-Level Queue (MLQ) - Planificador multinivel por colas
    Cada cola tiene su propio algoritmo de planificación
    Las colas de mayor prioridad se ejecutan primero
    """
    
    def __init__(self):
        self.colas = []  # Lista de colas configuradas
        self.procesos_originales = []
        self.procesos_completados = []
        self.linea_tiempo = []
        self.tiempo_actual = 0
        self.detalle_ejecucion = []
        
    def configurar_cola(self, nombre, prioridad, algoritmo, quantum=None, procesos_ids=None):
        """
        Configura una cola en el planificador MLQ
        
        Args:
            nombre: Nombre descriptivo de la cola
            prioridad: Número (1 = más alta prioridad)
            algoritmo: 'FIFO', 'SJF', 'RR'
            quantum: Quantum para Round Robin (opcional)
            procesos_ids: Lista de IDs de procesos en esta cola
        """
        cola = {
            'nombre': nombre,
            'prioridad': prioridad,
            'algoritmo': algoritmo,
            'quantum': quantum,
            'procesos_ids': procesos_ids or [],
            'procesos': [],
            'resultados': None,
            'estadisticas': None
        }
        self.colas.append(cola)
        # Ordenar por prioridad (menor número = mayor prioridad)
        self.colas.sort(key=lambda x: x['prioridad'])
        
    def cargar_procesos(self, procesos):
        """Carga los procesos a planificar"""
        self.procesos_originales = procesos
        self.procesos_completados = []
        self.linea_tiempo = []
        self.tiempo_actual = 0
        self.detalle_ejecucion = []
        
    def asignar_procesos_a_colas(self):
        """Asigna cada proceso a su cola correspondiente"""
        for cola in self.colas:
            cola['procesos'] = []
            for proceso in self.procesos_originales:
                if proceso.id in cola['procesos_ids']:
                    # Crear una copia del proceso para esta cola
                    copia = Proceso(
                        proceso.id,
                        proceso.tiempo_llegada,
                        proceso.rafaga,
                        proceso.prioridad
                    )
                    cola['procesos'].append(copia)
                    
    def planificar(self):
        """
        Ejecuta la planificación MLQ
        Las colas se ejecutan en orden de prioridad
        """
        if not self.colas:
            print("❌ Error: No hay colas configuradas")
            return []
            
        if not self.procesos_originales:
            print("❌ Error: No hay procesos cargados")
            return []
            
        # Asignar procesos a colas
        self.asignar_procesos_a_colas()
        
        self.linea_tiempo = []
        self.tiempo_actual = 0
        self.procesos_completados = []
        self.detalle_ejecucion = []
        
        # Ejecutar cada cola en orden de prioridad
        for idx, cola in enumerate(self.colas):
            if not cola['procesos']:
                self.detalle_ejecucion.append({
                    'cola': cola['nombre'],
                    'prioridad': cola['prioridad'],
                    'algoritmo': cola['algoritmo'],
                    'procesos': [],
                    'inicio': self.tiempo_actual,
                    'fin': self.tiempo_actual,
                    'estadisticas': {'tiempo_promedio_espera': 0, 'tiempo_promedio_retorno': 0}
                })
                continue
                
            print(f"\n  ▶️ Cola {idx+1}: {cola['nombre']} (Prioridad {cola['prioridad']})")
            print(f"     Algoritmo: {cola['algoritmo']}")
            print(f"     Procesos: {[f'P{p.id}' for p in cola['procesos']]}")
            if cola['quantum']:
                print(f"     Quantum: {cola['quantum']}")
                
            # Seleccionar el planificador según el algoritmo
            if cola['algoritmo'] == 'FIFO':
                planificador = PlanificadorFIFO(cola['procesos'])
            elif cola['algoritmo'] == 'SJF':
                planificador = PlanificadorSJF(cola['procesos'])
            elif cola['algoritmo'] == 'RR':
                quantum = cola.get('quantum', 2)
                planificador = PlanificadorRoundRobin(cola['procesos'], quantum)
            else:
                print(f"  ❌ Algoritmo {cola['algoritmo']} no soportado")
                continue
                
            # Ejecutar la planificación de esta cola
            tiempo_inicio_cola = self.tiempo_actual
            planificador.planificar()
            
            # Guardar resultados de la cola
            cola['resultados'] = {
                'linea_tiempo': planificador.linea_tiempo,
                'tiempo_actual': planificador.tiempo_actual,
                'procesos': planificador.procesos
            }
            cola['estadisticas'] = planificador.calcular_estadisticas()
            
            # Ajustar tiempos de la línea de tiempo de esta cola
            linea_tiempo_ajustada = []
            for tiempo, proceso in planificador.linea_tiempo:
                linea_tiempo_ajustada.append((tiempo + self.tiempo_actual, proceso))
                
            # Agregar a la línea de tiempo global
            self.linea_tiempo.extend(linea_tiempo_ajustada)
            
            # Actualizar tiempo actual
            self.tiempo_actual += planificador.tiempo_actual
            
            # Registrar detalle de ejecución
            self.detalle_ejecucion.append({
                'cola': cola['nombre'],
                'prioridad': cola['prioridad'],
                'algoritmo': cola['algoritmo'],
                'quantum': cola['quantum'],
                'procesos': [p.id for p in cola['procesos']],
                'inicio': tiempo_inicio_cola,
                'fin': self.tiempo_actual,
                'duracion': self.tiempo_actual - tiempo_inicio_cola,
                'estadisticas': cola['estadisticas']
            })
            
            # Marcar procesos completados
            for p in planificador.procesos:
                if p.completado:
                    p.tiempo_finalizacion += tiempo_inicio_cola
                    self.procesos_completados.append(p)
                    
        return self.linea_tiempo
    
    def mostrar_gantt(self):
        """Muestra el diagrama de Gantt completo"""
        if not self.linea_tiempo:
            return "No hay datos de ejecución"
            
        max_ancho = 7
        
        # Construir el diagrama
        gantt = "┌"
        for _ in self.linea_tiempo:
            gantt += "─" * max_ancho + "┬"
        gantt = gantt[:-1] + "┐\n"
        
        gantt += "│"
        for _, proceso in self.linea_tiempo:
            gantt += f" {proceso:^{max_ancho-1}} │"
        gantt += "\n"
        
        gantt += "└"
        for _ in self.linea_tiempo:
            gantt += "─" * max_ancho + "┴"
        gantt = gantt[:-1] + "┘\n"
        
        tiempos = []
        for tiempo, _ in self.linea_tiempo:
            tiempos.append(f"{tiempo:^{max_ancho}}")
        tiempos.append(f"{self.tiempo_actual:^{max_ancho}}")
        
        gantt += " " + "".join(tiempos)
        
        return gantt
    
    def mostrar_gantt_por_colas(self):
        """Muestra el diagrama de Gantt con separación por colas"""
        if not self.detalle_ejecucion:
            return "No hay datos de ejecución"
            
        resultado = []
        resultado.append("\n" + "=" * 70)
        resultado.append("  📊 DIAGRAMA DE GANTT POR COLAS")
        resultado.append("=" * 70)
        
        for detalle in self.detalle_ejecucion:
            if not detalle['procesos']:
                continue
                
            resultado.append(f"\n  🏷️ {detalle['cola']} (Prioridad {detalle['prioridad']})")
            resultado.append(f"     Algoritmo: {detalle['algoritmo']}")
            if detalle.get('quantum'):
                resultado.append(f"     Quantum: {detalle['quantum']}")
            resultado.append(f"     Procesos: {detalle['procesos']}")
            resultado.append(f"     Inicio: {detalle['inicio']} → Fin: {detalle['fin']} (Duración: {detalle['duracion']})")
            
            stats = detalle['estadisticas']
            if stats:
                resultado.append(f"     📊 Espera: {stats.get('tiempo_promedio_espera', 0):.2f}")
                resultado.append(f"     📊 Retorno: {stats.get('tiempo_promedio_retorno', 0):.2f}")
                
        return "\n".join(resultado)
    
    def mostrar_configuracion(self):
        """Muestra la configuración actual de las colas"""
        print("\n" + "=" * 70)
        print("  📋 CONFIGURACIÓN DE COLAS MLQ")
        print("=" * 70)
        
        if not self.colas:
            print("  ❌ No hay colas configuradas")
            return
            
        for idx, cola in enumerate(self.colas):
            print(f"\n  🏷️ Cola {idx+1}: {cola['nombre']}")
            print(f"     Prioridad: {cola['prioridad']} {'⭐' * (5 - cola['prioridad'])}")
            print(f"     Algoritmo: {cola['algoritmo']}")
            if cola['quantum']:
                print(f"     Quantum: {cola['quantum']}")
            print(f"     Procesos: {cola['procesos_ids']}")
            
    def calcular_estadisticas_globales(self):
        """Calcula estadísticas globales del MLQ"""
        if not self.procesos_completados:
            return {
                'tiempo_promedio_espera': 0,
                'tiempo_promedio_retorno': 0,
                'tiempo_total_cpu': 0,
                'num_procesos': 0,
                'num_colas': len(self.colas)
            }
            
        tiempos_espera = [p.tiempo_espera for p in self.procesos_completados]
        tiempos_retorno = [p.tiempo_retorno for p in self.procesos_completados]
        
        return {
            'tiempo_promedio_espera': sum(tiempos_espera) / len(tiempos_espera),
            'tiempo_promedio_retorno': sum(tiempos_retorno) / len(tiempos_retorno),
            'tiempo_total_cpu': self.tiempo_actual,
            'num_procesos': len(self.procesos_completados),
            'num_colas': len(self.colas)
        }
        
    def obtener_detalles_procesos(self):
        """Obtiene detalles de todos los procesos"""
        detalles = []
        for p in self.procesos_originales:
            # Buscar el proceso en los completados
            p_completado = None
            for pc in self.procesos_completados:
                if pc.id == p.id:
                    p_completado = pc
                    break
                    
            if p_completado:
                detalles.append({
                    'id': p.id,
                    'llegada': p.tiempo_llegada,
                    'rafaga': p.rafaga,
                    'prioridad': p.prioridad,
                    'espera': p_completado.tiempo_espera,
                    'retorno': p_completado.tiempo_retorno,
                    'finalizacion': p_completado.tiempo_finalizacion,
                    'completado': True
                })
            else:
                detalles.append({
                    'id': p.id,
                    'llegada': p.tiempo_llegada,
                    'rafaga': p.rafaga,
                    'prioridad': p.prioridad,
                    'espera': 0,
                    'retorno': 0,
                    'finalizacion': '-',
                    'completado': False
                })
        return detalles