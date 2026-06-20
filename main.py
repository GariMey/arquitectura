from modelos.proceso import (
    Proceso, TipoPaciente,
    crear_paciente_rojo, crear_paciente_amarillo,
    crear_paciente_embarazada, crear_paciente_verde,
    crear_paciente_cita, crear_paciente_seguimiento,
    crear_pacientes_ejemplo_hospital
)
from algoritmos.fifo import PlanificadorFIFO
from algoritmos.sjf import PlanificadorSJF
from algoritmos.round_robin import PlanificadorRoundRobin
from algoritmos.mlq import PlanificadorMLQ
from utils.gestor_archivos import GestorArchivos

# Variable global para almacenar los procesos de la última ejecución
procesos_actuales = []

# ============================================
# FUNCIONES DE EJECUCIÓN DE ALGORITMOS
# ============================================

def ejecutar_fifo_ejemplo():
    """Ejecuta FIFO con datos de ejemplo con nombres de pacientes"""
    global procesos_actuales
    
    print("\nPACIENTES DE EJEMPLO:")
    procesos = crear_pacientes_ejemplo_hospital()[:4]  # Tomar los primeros 4
    
    for p in procesos:
        print(f"  {p}")
    
    print("\n" + "=" * 70)
    print("  EJECUTANDO FIFO...")
    print("=" * 70)
    
    planificador = PlanificadorFIFO(procesos)
    planificador.planificar()
    mostrar_resultados(planificador, procesos, "FIFO")
    
    procesos_actuales = procesos


def ejecutar_sjf_ejemplo():
    """Ejecuta SJF con datos de ejemplo con nombres de pacientes"""
    global procesos_actuales
    
    print("\n📋 PACIENTES DE EJEMPLO:")
    procesos = crear_pacientes_ejemplo_hospital()[:4]
    
    for p in procesos:
        print(f"  {p}")
    
    print("\n" + "=" * 70)
    print("  EJECUTANDO SJF (No Preventivo)...")
    print("=" * 70)
    
    planificador = PlanificadorSJF(procesos)
    planificador.planificar()
    mostrar_resultados(planificador, procesos, "SJF")
    
    procesos_actuales = procesos


def ejecutar_rr_ejemplo():
    """Ejecuta Round Robin con datos de ejemplo con nombres de pacientes"""
    global procesos_actuales
    
    print("\n📋 PACIENTES DE EJEMPLO:")
    procesos = crear_pacientes_ejemplo_hospital()[:4]
    
    for p in procesos:
        print(f"  {p}")
    
    print("\n" + "=" * 70)
    
    try:
        quantum = int(input("  Ingresa el quantum (ejemplo: 2): ") or 2)
    except ValueError:
        quantum = 2
        print("  Usando quantum por defecto: 2")
    
    print(f"  Quantum: {quantum} unidades")
    print("=" * 70)
    
    print("  EJECUTANDO ROUND ROBIN...")
    print("=" * 70)
    
    planificador = PlanificadorRoundRobin(procesos, quantum)
    planificador.planificar()
    
    print(f"\n📊 DIAGRAMA DE GANTT (Round Robin - Quantum={quantum}):")
    print(planificador.mostrar_gantt())
    
    print(f"\n📋 DETALLE DE SEGMENTOS:")
    print(planificador.mostrar_gantt_detallado())
    
    print(f"\n📈 ESTADÍSTICAS (Round Robin):")
    stats = planificador.calcular_estadisticas()
    print(f"  • Quantum: {stats['quantum']} unidades")
    print(f"  • Procesos ejecutados: {stats['num_procesos']}")
    print(f"  • Tiempo promedio de espera: {stats['tiempo_promedio_espera']:.2f} unidades")
    print(f"  • Tiempo promedio de retorno: {stats['tiempo_promedio_retorno']:.2f} unidades")
    print(f"  • Tiempo total de CPU: {stats['tiempo_total_cpu']} unidades")
    
    print("\n📋 DETALLES POR PROCESO:")
    print("  ID  | Nombre              | Tipo | Llegada | Ráfaga | Prioridad | Espera | Retorno | Finalización")
    print("  " + "-" * 100)
    for p in procesos:
        prioridad_str = str(p.prioridad) if p.prioridad > 0 else "-"
        tipo_str = p.tipo_paciente[:8] if p.tipo_paciente else "-"
        nombre_str = p.nombre_paciente[:18] if p.nombre_paciente else f"Paciente {p.id}"
        print(f"  P{p.id:2} | {nombre_str:18} | {tipo_str:5} | {p.tiempo_llegada:7} | {p.rafaga:6} | {prioridad_str:9} | {p.tiempo_espera:6} | {p.tiempo_retorno:7} | {p.tiempo_finalizacion:12}")
    
    procesos_actuales = procesos


def ejecutar_mlq_ejemplo():
    """Ejecuta MLQ con datos de ejemplo con nombres de pacientes"""
    global procesos_actuales
    
    print("\n" + "=" * 70)
    print("  MLQ - MULTI-LEVEL QUEUE")
    print("=" * 70)
    
    procesos = crear_pacientes_ejemplo_hospital()[:6]
    
    print("\nPACIENTES:")
    for p in procesos:
        print(f"  {p}")
    
    print("\n" + "=" * 70)
    print("CONFIGURANDO MLQ")
    print("=" * 70)
    
    planificador = PlanificadorMLQ()
    planificador.cargar_procesos(procesos)
    
    print("\n  📌 Configuración de colas:")
    print("  ----------------------------------------")
    
    print("\n  🔴 Cola 1: ALTA PRIORIDAD (Rojo, Embarazada)")
    planificador.configurar_cola(
        nombre="Cola Alta",
        prioridad=1,
        algoritmo="RR",
        quantum=2,
        procesos_ids=[1, 3, 5]
    )
    print("     Algoritmo: Round Robin (Quantum=2)")
    print("     Procesos: P1, P3, P5")
    
    print("\n  🟡 Cola 2: MEDIA PRIORIDAD (Amarillo)")
    planificador.configurar_cola(
        nombre="Cola Media",
        prioridad=2,
        algoritmo="SJF",
        procesos_ids=[2, 6]
    )
    print("     Algoritmo: SJF")
    print("     Procesos: P2, P6")
    
    print("\n  🟢 Cola 3: BAJA PRIORIDAD (Verde, Cita, Seguimiento)")
    planificador.configurar_cola(
        nombre="Cola Baja",
        prioridad=3,
        algoritmo="FIFO",
        procesos_ids=[4]
    )
    print("     Algoritmo: FIFO")
    print("     Procesos: P4")
    
    planificador.mostrar_configuracion()
    
    print("\n" + "=" * 70)
    print("  ▶️ EJECUTANDO MLQ...")
    print("=" * 70)
    
    planificador.planificar()
    
    print("\n📊 DIAGRAMA DE GANTT GLOBAL:")
    print(planificador.mostrar_gantt())
    
    print("\n📊 DIAGRAMA DE GANTT POR COLAS:")
    print(planificador.mostrar_gantt_por_colas())
    
    print("\n📈 ESTADÍSTICAS GLOBALES:")
    stats = planificador.calcular_estadisticas_globales()
    print(f"  • Procesos ejecutados: {stats['num_procesos']}")
    print(f"  • Tiempo promedio de espera: {stats['tiempo_promedio_espera']:.2f} unidades")
    print(f"  • Tiempo promedio de retorno: {stats['tiempo_promedio_retorno']:.2f} unidades")
    print(f"  • Tiempo total de CPU: {stats['tiempo_total_cpu']} unidades")
    print(f"  • Número de colas: {stats['num_colas']}")
    
    print("\n📋 DETALLES POR PROCESO:")
    print("  ID  | Nombre              | Tipo | Llegada | Ráfaga | Espera | Retorno | Finalización | Estado")
    print("  " + "-" * 110)
    
    for detalle in planificador.obtener_detalles_procesos():
        estado = "✅ Completado" if detalle['completado'] else "⏳ Pendiente"
        prioridad_str = str(detalle['prioridad']) if detalle['prioridad'] > 0 else "-"
        # Buscar el nombre del proceso
        nombre = f"Paciente {detalle['id']}"
        tipo = "-"
        for p in procesos:
            if p.id == detalle['id']:
                nombre = p.nombre_paciente[:18] if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
                tipo = p.tipo_paciente[:8] if hasattr(p, 'tipo_paciente') and p.tipo_paciente else "-"
                break
        print(f"  P{detalle['id']:2} | {nombre:18} | {tipo:5} | {detalle['llegada']:7} | {detalle['rafaga']:6} | {detalle['espera']:6} | {detalle['retorno']:7} | {detalle['finalizacion']:12} | {estado}")
    
    procesos_actuales = procesos


def ejecutar_mlq_manual(procesos):
    """Ejecuta MLQ con procesos creados manualmente"""
    print("\n" + "=" * 70)
    print("  ⚙️ CONFIGURANDO MLQ MANUAL")
    print("=" * 70)
    
    planificador = PlanificadorMLQ()
    planificador.cargar_procesos(procesos)
    
    print("\n📋 Procesos disponibles:")
    for p in procesos:
        nombre = p.nombre_paciente if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
        print(f"  P{p.id}: {nombre} - Prioridad {p.prioridad}")
    
    try:
        num_colas = int(input("\n¿Cuántas colas deseas configurar? "))
    except ValueError:
        num_colas = 2
        print("  Usando 2 colas por defecto")
    
    for i in range(num_colas):
        print(f"\n📌 Configurando Cola {i+1}:")
        nombre = input(f"  Nombre de la cola: ")
        
        try:
            prioridad = int(input(f"  Prioridad (1 = más alta, {i+1} = más baja): "))
        except ValueError:
            prioridad = i + 1
            print(f"  Usando prioridad {prioridad}")
        
        print("  Algoritmos disponibles:")
        print("    1. FIFO")
        print("    2. SJF")
        print("    3. Round Robin")
        alg_opcion = input("  Selecciona algoritmo (1-3): ")
        
        if alg_opcion == "1":
            algoritmo = "FIFO"
            quantum = None
        elif alg_opcion == "2":
            algoritmo = "SJF"
            quantum = None
        elif alg_opcion == "3":
            algoritmo = "RR"
            try:
                quantum = int(input("  Quantum para Round Robin: "))
            except ValueError:
                quantum = 2
                print("  Usando quantum 2 por defecto")
        else:
            print("  ❌ Opción inválida, usando FIFO")
            algoritmo = "FIFO"
            quantum = None
            
        procesos_ids_input = input("  IDs de procesos en esta cola (ej: 1,3,5): ")
        procesos_ids = [int(x.strip()) for x in procesos_ids_input.split(",") if x.strip()]
        
        planificador.configurar_cola(
            nombre=nombre,
            prioridad=prioridad,
            algoritmo=algoritmo,
            quantum=quantum,
            procesos_ids=procesos_ids
        )
    
    planificador.mostrar_configuracion()
    
    print("\n" + "=" * 70)
    print("  ▶️ EJECUTANDO MLQ...")
    print("=" * 70)
    
    planificador.planificar()
    
    print("\n📊 DIAGRAMA DE GANTT:")
    print(planificador.mostrar_gantt())
    
    print("\n📈 ESTADÍSTICAS GLOBALES:")
    stats = planificador.calcular_estadisticas_globales()
    print(f"  • Tiempo promedio de espera: {stats['tiempo_promedio_espera']:.2f} unidades")
    print(f"  • Tiempo promedio de retorno: {stats['tiempo_promedio_retorno']:.2f} unidades")
    print(f"  • Tiempo total de CPU: {stats['tiempo_total_cpu']} unidades")
    
    print("\n📋 DETALLES POR PROCESO:")
    print("  ID  | Nombre              | Tipo | Llegada | Ráfaga | Espera | Retorno | Finalización")
    print("  " + "-" * 90)
    for detalle in planificador.obtener_detalles_procesos():
        if detalle['completado']:
            nombre = "Paciente " + str(detalle['id'])
            tipo = "-"
            for p in procesos:
                if p.id == detalle['id']:
                    nombre = p.nombre_paciente[:18] if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
                    tipo = p.tipo_paciente[:8] if hasattr(p, 'tipo_paciente') and p.tipo_paciente else "-"
                    break
            print(f"  P{detalle['id']:2} | {nombre:18} | {tipo:5} | {detalle['llegada']:7} | {detalle['rafaga']:6} | {detalle['espera']:6} | {detalle['retorno']:7} | {detalle['finalizacion']:12}")


def ejecutar_comparativo():
    """Ejecuta todos los algoritmos con los mismos procesos y muestra comparativa"""
    print("\n" + "=" * 70)
    print("REPORTE COMPARATIVO DE ALGORITMOS")
    print("=" * 70)
    
    procesos = [
        Proceso(1, 0, 5, 1, "Rojo", "Carlos Méndez"),
        Proceso(2, 1, 3, 2, "Amarillo", "Laura Sánchez"),
        Proceso(3, 2, 8, 1, "Rojo", "Ana Rodríguez"),
        Proceso(4, 3, 6, 3, "Verde", "Miguel Ángel"),
    ]
    
    print("\n📋 PACIENTES DE PRUEBA:")
    for p in procesos:
        print(f"  {p}")
    
    resultados = {}
    algoritmos = {
        'FIFO': PlanificadorFIFO,
        'SJF': PlanificadorSJF,
        'Round Robin (Q=2)': lambda p: PlanificadorRoundRobin(p, 2),
        'Round Robin (Q=4)': lambda p: PlanificadorRoundRobin(p, 4),
    }
    
    print("\n" + "=" * 70)
    print("  EJECUTANDO TODOS LOS ALGORITMOS...")
    print("=" * 70)
    
    for nombre, planificador_class in algoritmos.items():
        print(f"\n  ▶️ Ejecutando {nombre}...")
        
        procesos_copia = []
        for p in procesos:
            copia = Proceso(p.id, p.tiempo_llegada, p.rafaga, p.prioridad, p.tipo_paciente, p.nombre_paciente)
            procesos_copia.append(copia)
        
        if nombre == 'Round Robin (Q=2)':
            planificador = planificador_class(procesos_copia)
        elif nombre == 'Round Robin (Q=4)':
            planificador = planificador_class(procesos_copia)
        else:
            planificador = planificador_class(procesos_copia)
        
        planificador.planificar()
        stats = planificador.calcular_estadisticas()
        resultados[nombre] = stats
        
        print(f"    Espera promedio: {stats['tiempo_promedio_espera']:.2f}")
        print(f"    Retorno promedio: {stats['tiempo_promedio_retorno']:.2f}")
    
    print("\n" + "=" * 70)
    print("TABLA COMPARATIVA")
    print("=" * 70)
    print("\n  Algoritmo              | Espera Prom. | Retorno Prom. | CPU Total")
    print("  " + "-" * 70)
    
    for nombre, stats in resultados.items():
        nombre_ajustado = nombre.ljust(22)
        espera = f"{stats['tiempo_promedio_espera']:.2f}".rjust(12)
        retorno = f"{stats['tiempo_promedio_retorno']:.2f}".rjust(13)
        cpu = f"{stats['tiempo_total_cpu']}".rjust(10)
        print(f"  {nombre_ajustado} | {espera} | {retorno} | {cpu}")
    
    mejor_espera = min(resultados.items(), key=lambda x: x[1]['tiempo_promedio_espera'])
    mejor_retorno = min(resultados.items(), key=lambda x: x[1]['tiempo_promedio_retorno'])
    
    print("\n" + "=" * 70)
    print("RESULTADOS")
    print("=" * 70)
    print(f"\n  ✅ Mejor tiempo de espera: {mejor_espera[0]} ({mejor_espera[1]['tiempo_promedio_espera']:.2f})")
    print(f"  ✅ Mejor tiempo de retorno: {mejor_retorno[0]} ({mejor_retorno[1]['tiempo_promedio_retorno']:.2f})")


# ============================================
# FUNCIONES DE CARGA DESDE ARCHIVO
# ============================================

def cargar_procesos_desde_archivo():
    """Carga procesos desde un archivo .txt"""
    print("\n" + "=" * 70)
    print("  CARGAR PROCESOS DESDE ARCHIVO")
    print("=" * 70)
    
    nombre_archivo = input("\n  Nombre del archivo (ej: datos/procesos.txt): ")
    if not nombre_archivo:
        nombre_archivo = "datos/procesos.txt"
    
    procesos = GestorArchivos.cargar_procesos_desde_archivo(nombre_archivo)
    
    if not procesos:
        print("\n  ❌ No se cargaron procesos. Verifica el archivo.")
        return None
    
    print(f"\n  ✅ Se cargaron {len(procesos)} pacientes:")
    for p in procesos:
        print(f"     {p}")
    
    return procesos


def ejecutar_con_archivo():
    """Ejecuta un algoritmo con procesos cargados desde archivo"""
    global procesos_actuales
    
    procesos = cargar_procesos_desde_archivo()
    if not procesos:
        return
    
    procesos_actuales = procesos
    
    print("\n¿Qué algoritmo deseas usar?")
    print("  1. FIFO")
    print("  2. SJF")
    print("  3. Round Robin")
    print("  4. MLQ")
    alg = input("  Selecciona: ")
    
    if alg == "4":
        ejecutar_mlq_manual(procesos)
    elif alg in ["1", "2", "3"]:
        ejecutar_con_algoritmo(procesos, alg)
    else:
        print("❌ Opción inválida")


def guardar_historial(procesos):
    """Guarda los procesos en el historial"""
    if not procesos:
        print("❌ No hay procesos para guardar")
        return
        
    nombre_archivo = input("  Nombre del archivo de historial (ej: historial.txt): ") or "historial.txt"
    GestorArchivos.guardar_historial(procesos, nombre_archivo)


def mostrar_historial():
    """Muestra el historial de procesos completados"""
    nombre_archivo = input("  Nombre del archivo de historial (ej: historial.txt): ") or "historial.txt"
    GestorArchivos.mostrar_historial(nombre_archivo)


# ============================================
# FUNCIONES DE TIPOS DE PACIENTES
# ============================================

def crear_pacientes_con_tipo():
    """Crea pacientes con tipos específicos (contexto hospitalario)"""
    print("\n" + "=" * 70)
    print("  🏥 CREAR PACIENTES CON TIPO")
    print("=" * 70)
    
    # Mostrar tipos disponibles
    TipoPaciente.listar_tipos()
    
    procesos = []
    
    try:
        n = int(input("\n  ¿Cuántos pacientes deseas crear? "))
    except ValueError:
        n = 3
        print("  Usando 3 pacientes por defecto")
    
    for i in range(n):
        print(f"\n  Paciente {i+1}:")
        
        try:
            llegada = int(input("    Tiempo de llegada: "))
        except ValueError:
            llegada = i
            print(f"    Usando llegada {llegada}")
        
        try:
            rafaga = int(input("    Tiempo de ráfaga (duración de atención): "))
        except ValueError:
            rafaga = 5
            print(f"    Usando ráfaga {rafaga}")
        
        nombre = input("    Nombre del paciente (opcional, Enter para auto): ")
        if not nombre:
            nombre = None
        
        print("    Tipos disponibles:")
        print("      1. Rojo (🔴) - Emergencia máxima")
        print("      2. Amarillo (🟡) - Urgencia")
        print("      3. Embarazada (🤰) - Prioridad especial")
        print("      4. Verde (🟢) - Atención normal")
        print("      5. Cita (📋) - Programado")
        print("      6. Seguimiento (📝) - Control")
        
        tipo_opcion = input("    Selecciona tipo (1-6): ")
        
        tipo_map = {
            "1": "Rojo",
            "2": "Amarillo",
            "3": "Embarazada",
            "4": "Verde",
            "5": "Cita",
            "6": "Seguimiento"
        }
        
        tipo = tipo_map.get(tipo_opcion)
        if not tipo:
            print("    ❌ Opción inválida, usando Verde por defecto")
            tipo = "Verde"
        
        # Crear el proceso con el tipo seleccionado
        proceso = Proceso(i+1, llegada, rafaga, tipo_paciente=tipo, nombre_paciente=nombre)
        procesos.append(proceso)
        print(f"    ✅ Creado: {proceso}")
    
    return procesos


def ejecutar_con_pacientes_tipo():
    """Ejecuta un algoritmo con pacientes que tienen tipo"""
    global procesos_actuales
    
    procesos = crear_pacientes_con_tipo()
    if not procesos:
        return
    
    procesos_actuales = procesos
    
    print("\n¿Qué algoritmo deseas usar?")
    print("  1. FIFO")
    print("  2. SJF")
    print("  3. Round Robin")
    print("  4. MLQ")
    alg = input("  Selecciona: ")
    
    if alg == "4":
        ejecutar_mlq_manual(procesos)
    elif alg in ["1", "2", "3"]:
        ejecutar_con_algoritmo(procesos, alg)
    else:
        print("❌ Opción inválida")


# ============================================
# EJECUCIÓN PASO A PASO
# ============================================

def ejecutar_paso_a_paso(procesos):
    """
    Ejecuta la planificación paso a paso
    """
    print("\n" + "=" * 70)
    print("  🎬 EJECUCIÓN PASO A PASO")
    print("=" * 70)
    
    if not procesos:
        print("  No hay procesos para ejecutar")
        return
    
    print("\n📋 Procesos a ejecutar:")
    for p in procesos:
        print(f"  {p}")
    
    print("\n📌 ¿Qué algoritmo deseas usar para el paso a paso?")
    print("  1. FIFO")
    print("  2. SJF")
    print("  3. Round Robin")
    alg = input("  Selecciona: ")
    
    # Crear copia de los procesos
    procesos_copia = []
    for p in procesos:
        copia = Proceso(p.id, p.tiempo_llegada, p.rafaga, p.prioridad, 
                        p.tipo_paciente if hasattr(p, 'tipo_paciente') else None,
                        p.nombre_paciente if hasattr(p, 'nombre_paciente') else None)
        procesos_copia.append(copia)
    
    tiempo_actual = 0
    
    if alg == "1":
        # FIFO paso a paso
        procesos_ordenados = sorted(procesos_copia, key=lambda p: p.tiempo_llegada)
        
        print("\n" + "=" * 70)
        print("  ▶️ EJECUTANDO FIFO - PASO A PASO")
        print("=" * 70)
        
        for i, proceso in enumerate(procesos_ordenados):
            input(f"\n  Presiona Enter para ejecutar {proceso}...")
            
            if tiempo_actual < proceso.tiempo_llegada:
                print(f"  ⏳ CPU inactivo hasta t={proceso.tiempo_llegada}")
                tiempo_actual = proceso.tiempo_llegada
            
            proceso.tiempo_inicio = tiempo_actual
            proceso.tiempo_espera = tiempo_actual - proceso.tiempo_llegada
            proceso.estado = "Ejecucion"
            
            print(f"  ▶️ {proceso} inicia en t={tiempo_actual}")
            print(f"     Ráfaga: {proceso.rafaga}, Espera: {proceso.tiempo_espera}")
            
            mostrar_dashboard(procesos_copia, tiempo_actual)
            
            tiempo_actual += proceso.rafaga
            
            proceso.tiempo_finalizacion = tiempo_actual
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
            proceso.completado = True
            proceso.estado = "Completado"
            
            print(f"  ✅ {proceso} finaliza en t={tiempo_actual}")
            print(f"     Retorno: {proceso.tiempo_retorno}")
            
            mostrar_dashboard(procesos_copia, tiempo_actual)
        
        print("\n" + "=" * 70)
        print("  ✅ EJECUCIÓN COMPLETADA")
        print("=" * 70)
        mostrar_resultados_finales(procesos_copia, "FIFO")
        
    elif alg == "2":
        # SJF paso a paso
        pendientes = procesos_copia.copy()
        for p in pendientes:
            p.reiniciar()
        
        print("\n" + "=" * 70)
        print("  ▶️ EJECUTANDO SJF - PASO A PASO")
        print("=" * 70)
        
        while pendientes:
            disponibles = [p for p in pendientes if p.tiempo_llegada <= tiempo_actual]
            
            if not disponibles:
                siguiente = min(p.tiempo_llegada for p in pendientes)
                print(f"  ⏳ CPU inactivo hasta t={siguiente}")
                tiempo_actual = siguiente
                disponibles = [p for p in pendientes if p.tiempo_llegada <= tiempo_actual]
            
            proceso = min(disponibles, key=lambda p: p.rafaga)
            
            input(f"\n  Presiona Enter para ejecutar {proceso}...")
            
            proceso.tiempo_inicio = tiempo_actual
            proceso.tiempo_espera = tiempo_actual - proceso.tiempo_llegada
            proceso.estado = "Ejecucion"
            
            print(f"  ▶️ {proceso} inicia en t={tiempo_actual}")
            print(f"     Ráfaga: {proceso.rafaga}, Espera: {proceso.tiempo_espera}")
            
            mostrar_dashboard(procesos_copia, tiempo_actual)
            
            tiempo_actual += proceso.rafaga
            
            proceso.tiempo_finalizacion = tiempo_actual
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
            proceso.completado = True
            proceso.estado = "Completado"
            pendientes.remove(proceso)
            
            print(f"  ✅ {proceso} finaliza en t={tiempo_actual}")
            print(f"     Retorno: {proceso.tiempo_retorno}")
            
            mostrar_dashboard(procesos_copia, tiempo_actual)
        
        print("\n" + "=" * 70)
        print("  ✅ EJECUCIÓN COMPLETADA")
        print("=" * 70)
        mostrar_resultados_finales(procesos_copia, "SJF")
        
    elif alg == "3":
        # Round Robin paso a paso
        try:
            quantum = int(input("  Ingresa el quantum: ") or 2)
        except ValueError:
            quantum = 2
        
        for p in procesos_copia:
            p.reiniciar()
            p.tiempo_restante = p.rafaga
        
        cola = []
        pendientes = procesos_copia.copy()
        tiempo_actual = 0
        
        print("\n" + "=" * 70)
        print(f"  ▶️ EJECUTANDO ROUND ROBIN (Q={quantum}) - PASO A PASO")
        print("=" * 70)
        
        while pendientes or cola:
            # Agregar procesos que han llegado
            llegaron = [p for p in pendientes if p.tiempo_llegada <= tiempo_actual]
            for p in llegaron:
                if p not in cola:
                    cola.append(p)
                    pendientes.remove(p)
            
            if not cola and pendientes:
                siguiente = min(p.tiempo_llegada for p in pendientes)
                print(f"  ⏳ CPU inactivo hasta t={siguiente}")
                tiempo_actual = siguiente
                llegaron = [p for p in pendientes if p.tiempo_llegada <= tiempo_actual]
                for p in llegaron:
                    cola.append(p)
                    pendientes.remove(p)
            
            if not cola:
                break
            
            proceso = cola.pop(0)
            
            input(f"\n  Presiona Enter para ejecutar {proceso}...")
            
            if proceso.tiempo_inicio is None:
                proceso.tiempo_inicio = tiempo_actual
                proceso.tiempo_espera = tiempo_actual - proceso.tiempo_llegada
                proceso.estado = "Ejecucion"
            
            ejecucion = min(quantum, proceso.tiempo_restante)
            
            print(f"  ▶️ {proceso} ejecuta de t={tiempo_actual} a t={tiempo_actual + ejecucion}")
            print(f"     Restante antes: {proceso.tiempo_restante}, Ejecuta: {ejecucion}")
            
            mostrar_dashboard(procesos_copia, tiempo_actual)
            
            tiempo_actual += ejecucion
            proceso.tiempo_restante -= ejecucion
            
            if proceso.tiempo_restante <= 0:
                proceso.tiempo_finalizacion = tiempo_actual
                proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.tiempo_llegada
                proceso.completado = True
                proceso.estado = "Completado"
                print(f"  ✅ {proceso} COMPLETADO en t={tiempo_actual}")
                print(f"     Retorno: {proceso.tiempo_retorno}")
            else:
                # Agregar nuevos procesos que llegaron
                llegaron = [p for p in pendientes if p.tiempo_llegada <= tiempo_actual]
                for p in llegaron:
                    if p not in cola:
                        cola.append(p)
                        pendientes.remove(p)
                
                cola.append(proceso)
                proceso.estado = "Espera"
                print(f"  ⏳ {proceso} vuelve a la cola con {proceso.tiempo_restante} restante")
            
            mostrar_dashboard(procesos_copia, tiempo_actual)
        
        print("\n" + "=" * 70)
        print("  ✅ EJECUCIÓN COMPLETADA")
        print("=" * 70)
        mostrar_resultados_finales(procesos_copia, f"Round Robin (Q={quantum})")
    
    else:
        print("❌ Algoritmo no válido")


def mostrar_resultados_finales(procesos, nombre_algoritmo):
    """Muestra los resultados finales después de una ejecución paso a paso"""
    print(f"\nRESULTADOS FINALES ({nombre_algoritmo})")
    print("=" * 70)
    
    completados = [p for p in procesos if p.completado]
    if not completados:
        print("  No hay procesos completados")
        return
    
    tiempos_espera = [p.tiempo_espera for p in completados]
    tiempos_retorno = [p.tiempo_retorno for p in completados]
    tiempo_total = max(p.tiempo_finalizacion for p in completados)
    
    print(f"\nESTADÍSTICAS:")
    print(f"  • Procesos ejecutados: {len(completados)}")
    print(f"  • Tiempo promedio de espera: {sum(tiempos_espera)/len(tiempos_espera):.2f} unidades")
    print(f"  • Tiempo promedio de retorno: {sum(tiempos_retorno)/len(tiempos_retorno):.2f} unidades")
    print(f"  • Tiempo total de CPU: {tiempo_total} unidades")
    
    print("\n📋 DETALLES POR PROCESO:")
    print("  ID  | Nombre              | Tipo | Llegada | Ráfaga | Espera | Retorno | Finalización")
    print("  " + "-" * 90)
    for p in completados:
        nombre_str = p.nombre_paciente[:18] if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
        tipo_str = p.tipo_paciente[:8] if hasattr(p, 'tipo_paciente') and p.tipo_paciente else "-"
        print(f"  P{p.id:2} | {nombre_str:18} | {tipo_str:5} | {p.tiempo_llegada:7} | {p.rafaga:6} | {p.tiempo_espera:6} | {p.tiempo_retorno:7} | {p.tiempo_finalizacion:12}")


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def mostrar_resultados(planificador, procesos, nombre_algoritmo):
    """Muestra los resultados de la planificación"""
    print(f"\nDIAGRAMA DE GANTT ({nombre_algoritmo}):")
    print(planificador.mostrar_gantt())
    
    print(f"\nESTADÍSTICAS ({nombre_algoritmo}):")
    stats = planificador.calcular_estadisticas()
    print(f"  • Procesos ejecutados: {stats['num_procesos']}")
    print(f"  • Tiempo promedio de espera: {stats['tiempo_promedio_espera']:.2f} unidades")
    print(f"  • Tiempo promedio de retorno: {stats['tiempo_promedio_retorno']:.2f} unidades")
    print(f"  • Tiempo total de CPU: {stats['tiempo_total_cpu']} unidades")
    
    print("\nDETALLES POR PROCESO:")
    print("  ID  | Nombre              | Tipo | Llegada | Ráfaga | Prioridad | Espera | Retorno | Finalización")
    print("  " + "-" * 100)
    for p in procesos:
        prioridad_str = str(p.prioridad) if p.prioridad > 0 else "-"
        tipo_str = p.tipo_paciente[:8] if hasattr(p, 'tipo_paciente') and p.tipo_paciente else "-"
        nombre_str = p.nombre_paciente[:18] if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
        print(f"  P{p.id:2} | {nombre_str:18} | {tipo_str:5} | {p.tiempo_llegada:7} | {p.rafaga:6} | {prioridad_str:9} | {p.tiempo_espera:6} | {p.tiempo_retorno:7} | {p.tiempo_finalizacion:12}")


def crear_procesos_manual():
    """Crea procesos manualmente"""
    print("\n" + "=" * 70)
    print("  CREAR PROCESOS MANUALMENTE")
    print("=" * 70)
    
    procesos = []
    
    try:
        n = int(input("  ¿Cuántos pacientes deseas crear? "))
    except ValueError:
        n = 3
        print("  Usando 3 pacientes por defecto")
    
    for i in range(n):
        print(f"\n  Paciente {i+1}:")
        
        try:
            llegada = int(input("    Tiempo de llegada: "))
        except ValueError:
            llegada = i
            print(f"    Usando llegada {llegada}")
        
        try:
            rafaga = int(input("    Tiempo de ráfaga (duración de atención): "))
        except ValueError:
            rafaga = 5
            print(f"    Usando ráfaga {rafaga}")
        
        nombre = input("    Nombre del paciente (opcional, Enter para auto): ")
        if not nombre:
            nombre = None
        
        print("    ¿Quieres asignar un tipo de paciente? (s/n): ")
        asignar_tipo = input("    ").lower()
        
        if asignar_tipo == 's' or asignar_tipo == 'si':
            print("    Tipos disponibles:")
            print("      1. Rojo (🔴) - Emergencia máxima")
            print("      2. Amarillo (🟡) - Urgencia")
            print("      3. Embarazada (🤰) - Prioridad especial")
            print("      4. Verde (🟢) - Atención normal")
            print("      5. Cita (📋) - Programado")
            print("      6. Seguimiento (📝) - Control")
            
            tipo_opcion = input("    Selecciona tipo (1-6): ")
            
            tipo_map = {
                "1": "Rojo",
                "2": "Amarillo",
                "3": "Embarazada",
                "4": "Verde",
                "5": "Cita",
                "6": "Seguimiento"
            }
            
            tipo = tipo_map.get(tipo_opcion)
            if not tipo:
                print("    ❌ Opción inválida, usando Verde por defecto")
                tipo = "Verde"
            
            proceso = Proceso(i+1, llegada, rafaga, tipo_paciente=tipo, nombre_paciente=nombre)
        else:
            prioridad_input = input("    Prioridad (1-5, opcional, 0 si no aplica): ")
            try:
                prioridad = int(prioridad_input) if prioridad_input else 0
            except ValueError:
                prioridad = 0
            proceso = Proceso(i+1, llegada, rafaga, prioridad, nombre_paciente=nombre)
        
        procesos.append(proceso)
        print(f"    ✅ Creado: {proceso}")
    
    return procesos


def ejecutar_con_algoritmo(procesos, algoritmo):
    """Ejecuta la planificación con el algoritmo seleccionado"""
    if algoritmo == "1":
        planificador = PlanificadorFIFO(procesos)
        nombre = "FIFO"
        planificador.planificar()
        mostrar_resultados(planificador, procesos, nombre)
    elif algoritmo == "2":
        planificador = PlanificadorSJF(procesos)
        nombre = "SJF"
        planificador.planificar()
        mostrar_resultados(planificador, procesos, nombre)
    elif algoritmo == "3":
        try:
            quantum = int(input("  Ingresa el quantum: ") or 2)
        except ValueError:
            quantum = 2
            print("  Usando quantum 2 por defecto")
        
        planificador = PlanificadorRoundRobin(procesos, quantum)
        nombre = f"Round Robin (Quantum={quantum})"
        planificador.planificar()
        print(f"\nDIAGRAMA DE GANTT ({nombre}):")
        print(planificador.mostrar_gantt())
        print(f"\nDETALLE DE SEGMENTOS:")
        print(planificador.mostrar_gantt_detallado())
        print(f"\nESTADÍSTICAS:")
        stats = planificador.calcular_estadisticas()
        print(f"  • Procesos ejecutados: {stats['num_procesos']}")
        print(f"  • Tiempo promedio de espera: {stats['tiempo_promedio_espera']:.2f} unidades")
        print(f"  • Tiempo promedio de retorno: {stats['tiempo_promedio_retorno']:.2f} unidades")
        print(f"  • Tiempo total de CPU: {stats['tiempo_total_cpu']} unidades")
        print("\nDETALLES POR PROCESO:")
        print("  ID  | Nombre              | Tipo | Llegada | Ráfaga | Prioridad | Espera | Retorno | Finalización")
        print("  " + "-" * 100)
        for p in procesos:
            prioridad_str = str(p.prioridad) if p.prioridad > 0 else "-"
            tipo_str = p.tipo_paciente[:8] if hasattr(p, 'tipo_paciente') and p.tipo_paciente else "-"
            nombre_str = p.nombre_paciente[:18] if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
            print(f"  P{p.id:2} | {nombre_str:18} | {tipo_str:5} | {p.tiempo_llegada:7} | {p.rafaga:6} | {prioridad_str:9} | {p.tiempo_espera:6} | {p.tiempo_retorno:7} | {p.tiempo_finalizacion:12}")
    else:
        print("❌ Algoritmo no válido")


# ============================================
# DASHBOARD DE PACIENTES MEJORADO
# ============================================

def mostrar_dashboard(procesos, tiempo_actual=None):
    """Muestra el estado actual de todos los procesos (Dashboard mejorado)"""
    print("\n" + "=" * 80)
    print("  DASHBOARD DE PACIENTES - CENTRO DE EMERGENCIAS")
    print("=" * 80)
    
    if not procesos:
        print("  No hay pacientes en el sistema")
        return
    
    # Dividir procesos por estado
    espera = []
    ejecucion = []
    completados = []
    
    for p in procesos:
        if p.completado:
            completados.append(p)
        elif p.tiempo_inicio is not None and not p.completado:
            ejecucion.append(p)
        else:
            espera.append(p)
    
    # ============================================
    # 1. RESUMEN GENERAL
    # ============================================
    print(f"\n  RESUMEN DEL DÍA:")
    print(f"  ──────────────────────────────────────────────────────")
    print(f"     🟥 En espera:  {len(espera):3} pacientes")
    print(f"     🟩 En atención: {len(ejecucion):3} pacientes")
    print(f"     ✅ Completados: {len(completados):3} pacientes")
    print(f"     📍 Total:       {len(procesos):3} pacientes")
    if tiempo_actual is not None:
        print(f"     ⏱️  Tiempo actual: {tiempo_actual} unidades")
    print("  ──────────────────────────────────────────────────────")
    
    # ============================================
    # 2. PACIENTES EN ESPERA (con tiempo de espera)
    # ============================================
    if espera:
        print("\n  ⏳ PACIENTES EN ESPERA:")
        print("  ┌────┬────────────────────┬──────────────┬──────────┬────────────┬─────────────┐")
        print("  │ ID │ Nombre              │ Tipo         │ Llegada  │ Ráfaga     │ Tiempo Espera│")
        print("  ├────┼────────────────────┼──────────────┼──────────┼────────────┼─────────────┤")
        for p in espera:
            tiempo_espera = tiempo_actual - p.tiempo_llegada if tiempo_actual is not None else 0
            tipo_str = p.tipo_paciente[:12] if hasattr(p, 'tipo_paciente') and p.tipo_paciente else "Normal"
            nombre_mostrar = p.nombre_paciente[:18] if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
            emoji = p.get_emoji() if hasattr(p, 'get_emoji') else ""
            print(f"  │ {emoji}P{p.id:2} │ {nombre_mostrar:<18} │ {tipo_str:<12} │ {p.tiempo_llegada:>8} │ {p.rafaga:>10} │ {tiempo_espera:>11} │")
        print("  └────┴────────────────────┴──────────────┴──────────┴────────────┴─────────────┘")
    
    # ============================================
    # 3. PACIENTES EN ATENCIÓN (con tiempo restante)
    # ============================================
    if ejecucion:
        print("\n  🟢 PACIENTES EN ATENCIÓN:")
        print("  ┌────┬────────────────────┬──────────────┬──────────┬────────────┬─────────────────┐")
        print("  │ ID │ Nombre              │ Tipo         │ Llegada  │ Ráfaga     │ Tiempo Restante │")
        print("  ├────┼────────────────────┼──────────────┼──────────┼────────────┼─────────────────┤")
        for p in ejecucion:
            restante = p.tiempo_restante if hasattr(p, 'tiempo_restante') else p.rafaga
            tipo_str = p.tipo_paciente[:12] if hasattr(p, 'tipo_paciente') and p.tipo_paciente else "Normal"
            nombre_mostrar = p.nombre_paciente[:18] if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
            emoji = p.get_emoji() if hasattr(p, 'get_emoji') else ""
            print(f"  │ {emoji}P{p.id:2} │ {nombre_mostrar:<18} │ {tipo_str:<12} │ {p.tiempo_llegada:>8} │ {p.rafaga:>10} │ {restante:>15} │")
        print("  └────┴────────────────────┴──────────────┴──────────┴────────────┴─────────────────┘")
    
    # ============================================
    # 4. PACIENTES COMPLETADOS
    # ============================================
    if completados:
        print("\n  ✅ PACIENTES ATENDIDOS:")
        print("  ┌────┬────────────────────┬──────────────┬──────────┬────────────┬──────────────┬─────────────┐")
        print("  │ ID │ Nombre              │ Tipo         │ Espera   │ Retorno    │ Finalización │ Estado       │")
        print("  ├────┼────────────────────┼──────────────┼──────────┼────────────┼──────────────┼─────────────┤")
        for p in completados:
            tipo_str = p.tipo_paciente[:12] if hasattr(p, 'tipo_paciente') and p.tipo_paciente else "Normal"
            nombre_mostrar = p.nombre_paciente[:18] if hasattr(p, 'nombre_paciente') else f"Paciente {p.id}"
            emoji = p.get_emoji() if hasattr(p, 'get_emoji') else ""
            estado_emoji = "✅" if p.completado else "⏳"
            print(f"  │ {emoji}P{p.id:2} │ {nombre_mostrar:<18} │ {tipo_str:<12} │ {p.tiempo_espera:>8} │ {p.tiempo_retorno:>10} │ {p.tiempo_finalizacion:>12} │ {estado_emoji} Completado │")
        print("  └────┴────────────────────┴──────────────┴──────────┴────────────┴──────────────┴─────────────┘")
    
    # ============================================
    # 5. ESTADÍSTICAS DEL DASHBOARD
    # ============================================
    if completados:
        tiempos_espera = [p.tiempo_espera for p in completados]
        tiempos_retorno = [p.tiempo_retorno for p in completados]
        print(f"\n  📈 ESTADÍSTICAS DEL DÍA:")
        print(f"     ⏱️  Promedio de espera:  {sum(tiempos_espera)/len(tiempos_espera):.2f} unidades")
        print(f"     ⏱️  Promedio de retorno: {sum(tiempos_retorno)/len(tiempos_retorno):.2f} unidades")
    
    print("\n" + "=" * 80)


# ============================================
# MENÚ PRINCIPAL
# ============================================

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 70)
    print("  🏥 SIMULADOR DE PLANIFICACIÓN DE PROCESOS - CENTRO DE EMERGENCIAS")
    print("=" * 70)
    print("  1. FIFO (First In First Out)")
    print("  2. SJF (Shortest Job First)")
    print("  3. Round Robin")
    print("  4. MLQ (Multi-Level Queue)")
    print("  5. Crear pacientes manualmente")
    print("  6. Crear pacientes con tipo (especial para contexto hospitalario) ")
    print("  7. Cargar pacientes desde archivo ")
    print("  8. Reporte Comparativo de Algoritmos ")
    print("  9. Dashboard de pacientes ")
    print("  10. Ejecución paso a paso ")
    print("  11. Guardar historial ")
    print("  12. Ver historial ")
    print("  13. Salir")
    print("=" * 70)


def main():
    """Función principal del programa"""
    global procesos_actuales
    
    while True:
        mostrar_menu()
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == "1":
            ejecutar_fifo_ejemplo()
        elif opcion == "2":
            ejecutar_sjf_ejemplo()
        elif opcion == "3":
            ejecutar_rr_ejemplo()
        elif opcion == "4":
            ejecutar_mlq_ejemplo()
        elif opcion == "5":
            procesos = crear_procesos_manual()
            if procesos:
                procesos_actuales = procesos
                print("\n¿Qué algoritmo deseas usar?")
                print("  1. FIFO")
                print("  2. SJF")
                print("  3. Round Robin")
                print("  4. MLQ")
                alg = input("  Selecciona: ")
                
                if alg == "4":
                    ejecutar_mlq_manual(procesos)
                elif alg in ["1", "2", "3"]:
                    ejecutar_con_algoritmo(procesos, alg)
                else:
                    print("❌ Opción inválida")
        elif opcion == "6":
            ejecutar_con_pacientes_tipo()
        elif opcion == "7":
            ejecutar_con_archivo()
        elif opcion == "8":
            ejecutar_comparativo()
        elif opcion == "9":
            if procesos_actuales:
                mostrar_dashboard(procesos_actuales)
            else:
                print("\n❌ No hay pacientes para mostrar. Ejecuta un algoritmo primero.")
                print("   Puedes crear pacientes con la opción 5 o 6, o ejecutar un algoritmo de ejemplo.")
        elif opcion == "10":
            if procesos_actuales:
                ejecutar_paso_a_paso(procesos_actuales)
            else:
                print("\n❌ No hay pacientes para ejecutar paso a paso. Ejecuta un algoritmo primero.")
                print("   Puedes crear pacientes con la opción 5 o 6, o ejecutar un algoritmo de ejemplo.")
        elif opcion == "11":
            if procesos_actuales:
                guardar_historial(procesos_actuales)
            else:
                print("\n❌ No hay pacientes para guardar. Ejecuta un algoritmo primero.")
        elif opcion == "12":
            mostrar_historial()
        elif opcion == "13":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n❌ Opción inválida. Intenta de nuevo.")


# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    main()