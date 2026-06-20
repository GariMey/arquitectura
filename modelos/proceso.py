class TipoPaciente:
    """Tipos de pacientes con sus prioridades para el contexto hospitalario"""
    ROJO = "Rojo"                    # Emergencia máxima (Prioridad 1)
    AMARILLO = "Amarillo"            # Urgencia (Prioridad 2)
    EMBARAZADA = "Embarazada"        # Prioridad especial (Prioridad 1)
    VERDE = "Verde"                  # Atención normal (Prioridad 3)
    CITA = "Cita"                    # Programado (Prioridad 4)
    SEGUIMIENTO = "Seguimiento"      # Seguimiento (Prioridad 5)
    
    # Mapeo de prioridades (menor número = mayor prioridad)
    PRIORIDADES = {
        ROJO: 1,
        EMBARAZADA: 1,
        AMARILLO: 2,
        VERDE: 3,
        CITA: 4,
        SEGUIMIENTO: 5
    }
    
    # Descripción de cada tipo
    DESCRIPCIONES = {
        ROJO: "🔴 Paciente crítico - Atención inmediata",
        AMARILLO: "🟡 Paciente urgente - Atención prioritaria",
        EMBARAZADA: "🤰 Embarazada - Atención prioritaria",
        VERDE: "🟢 Paciente estable - Atención normal",
        CITA: "📋 Cita programada - Atención según agenda",
        SEGUIMIENTO: "📝 Seguimiento - Atención de control"
    }
    
    # Emojis por tipo
    EMOJIS = {
        ROJO: "🔴",
        AMARILLO: "🟡",
        EMBARAZADA: "🤰",
        VERDE: "🟢",
        CITA: "📋",
        SEGUIMIENTO: "📝"
    }
    
    # Nombres sugeridos para pacientes (contexto hospitalario)
    NOMBRES_SUGERIDOS = {
        ROJO: ["Carlos Méndez", "Ana Rodríguez", "Luis Pérez", "María Gómez", "Jorge Ramírez", "Elena Castro", "Roberto Mora", "Diana Rojas"],
        AMARILLO: ["Laura Sánchez", "Pedro Jiménez", "Diana Castro", "Roberto Mora", "Elena Rojas", "Mario Chacón", "Lorena Brenes", "Rafael Alvarado"],
        EMBARAZADA: ["Sofía Herrera", "Valentina Mora", "Camila Rojas", "Lucía Jiménez", "Isabella Pérez", "Mariana Castro", "Andrea Solano", "Daniela Vargas"],
        VERDE: ["Miguel Ángel", "Paula Quirós", "Andrés Blanco", "Karla Fonseca", "Daniel Salas", "Fernando Arroyo", "Mónica Calderón", "Oscar Vega"],
        CITA: ["Mario Chacón", "Lorena Brenes", "Rafael Alvarado", "Patricia Ureña", "Enrique Vargas", "Tatiana Mora", "Alberto Quirós", "María Jiménez"],
        SEGUIMIENTO: ["Fernando Arroyo", "Mónica Calderón", "Oscar Vega", "Tatiana Mora", "Alberto Quirós", "Luis Fernández", "Ana Cordero", "José Solís"]
    }
    
    @classmethod
    def get_prioridad(cls, tipo):
        """Obtiene la prioridad según el tipo de paciente"""
        return cls.PRIORIDADES.get(tipo, 3)  # Por defecto prioridad 3 (Verde)
    
    @classmethod
    def get_descripcion(cls, tipo):
        """Obtiene la descripción del tipo de paciente"""
        return cls.DESCRIPCIONES.get(tipo, f"Tipo: {tipo}")
    
    @classmethod
    def get_emoji(cls, tipo):
        """Obtiene el emoji del tipo de paciente"""
        return cls.EMOJIS.get(tipo, "🏥")
    
    @classmethod
    def get_nombre_sugerido(cls, tipo, indice=0):
        """Obtiene un nombre sugerido para el tipo de paciente"""
        nombres = cls.NOMBRES_SUGERIDOS.get(tipo, ["Paciente Desconocido"])
        return nombres[indice % len(nombres)]
    
    @classmethod
    def listar_tipos(cls):
        """Lista todos los tipos de pacientes disponibles"""
        print("\n📋 TIPOS DE PACIENTES:")
        print("=" * 60)
        for tipo, descripcion in cls.DESCRIPCIONES.items():
            emoji = cls.EMOJIS.get(tipo, "")
            print(f"  {emoji} {tipo:<12} - {descripcion}")
        print("=" * 60)


class Proceso:
    """
    Clase que representa un proceso/paciente en el sistema
    Incluye tipo de paciente, nombre real y estado para el contexto hospitalario
    """
    
    def __init__(self, id_proceso, tiempo_llegada, rafaga, prioridad=0, tipo_paciente=None, nombre_paciente=None):
        """
        Inicializa un nuevo proceso/paciente
        
        Args:
            id_proceso: Identificador único del proceso
            tiempo_llegada: Momento en que el proceso entra al sistema
            rafaga: Duración total de ejecución requerida
            prioridad: Nivel de prioridad (opcional)
            tipo_paciente: Tipo de paciente (Rojo, Amarillo, Embarazada, Verde, Cita, Seguimiento)
            nombre_paciente: Nombre real del paciente (opcional)
        """
        self.id = id_proceso
        
        # Si se especifica tipo de paciente, usar su prioridad
        if tipo_paciente:
            self.tipo_paciente = tipo_paciente
            self.prioridad = TipoPaciente.get_prioridad(tipo_paciente)
            # Asignar nombre sugerido si no se proporciona uno
            if nombre_paciente is None:
                self.nombre_paciente = TipoPaciente.get_nombre_sugerido(tipo_paciente, id_proceso - 1)
            else:
                self.nombre_paciente = nombre_paciente
        else:
            self.tipo_paciente = None
            self.prioridad = prioridad if prioridad > 0 else 3  # Prioridad por defecto
            self.nombre_paciente = nombre_paciente or f"Paciente {id_proceso}"
        
        self.tiempo_llegada = tiempo_llegada
        self.rafaga = rafaga
        self.tiempo_restante = rafaga
        self.tiempo_inicio = None
        self.tiempo_finalizacion = None
        self.tiempo_espera = 0
        self.tiempo_retorno = 0
        self.completado = False
        self.estado = "Espera"  # "Espera", "Ejecucion", "Completado"
    
    def __str__(self):
        """Representación legible del proceso"""
        emoji = TipoPaciente.get_emoji(self.tipo_paciente) if self.tipo_paciente else "💻"
        tipo_str = f", Tipo: {self.tipo_paciente}" if self.tipo_paciente else ""
        nombre_str = f", Nombre: {self.nombre_paciente}" if self.nombre_paciente else ""
        prioridad_str = f", Prioridad: {self.prioridad}"
        estado_str = f", Estado: {self.estado}" if self.completado or self.tiempo_inicio is not None else ""
        return f"{emoji} P{self.id} ({self.nombre_paciente}{tipo_str}) Llegada: {self.tiempo_llegada}, Ráfaga: {self.rafaga}{prioridad_str}{estado_str}"
    
    def __repr__(self):
        return self.__str__()
    
    def reiniciar(self):
        """Reinicia el proceso para una nueva simulación"""
        self.tiempo_restante = self.rafaga
        self.tiempo_inicio = None
        self.tiempo_finalizacion = None
        self.tiempo_espera = 0
        self.tiempo_retorno = 0
        self.completado = False
        self.estado = "Espera"
    
    def to_dict(self):
        """Convierte el proceso a diccionario para almacenamiento"""
        return {
            'id': self.id,
            'nombre_paciente': self.nombre_paciente,
            'tiempo_llegada': self.tiempo_llegada,
            'rafaga': self.rafaga,
            'prioridad': self.prioridad,
            'tipo_paciente': self.tipo_paciente,
            'tiempo_espera': self.tiempo_espera,
            'tiempo_retorno': self.tiempo_retorno,
            'tiempo_finalizacion': self.tiempo_finalizacion,
            'estado': self.estado,
            'completado': self.completado
        }
    
    def get_emoji(self):
        """Obtiene el emoji según el tipo de paciente"""
        return TipoPaciente.get_emoji(self.tipo_paciente) if self.tipo_paciente else "💻"
    
    def get_descripcion(self):
        """Obtiene la descripción del tipo de paciente"""
        return TipoPaciente.get_descripcion(self.tipo_paciente) if self.tipo_paciente else "Proceso normal"
    
    def get_tipo_prioridad(self):
        """Obtiene la prioridad del tipo de paciente"""
        return TipoPaciente.get_prioridad(self.tipo_paciente) if self.tipo_paciente else self.prioridad


# ============================================
# FUNCIONES DE UTILIDAD PARA CREAR PACIENTES
# ============================================

def crear_paciente_rojo(id_proceso, llegada, rafaga, nombre=None):
    """Crea un paciente ROJO (emergencia máxima)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.ROJO, nombre_paciente=nombre)


def crear_paciente_amarillo(id_proceso, llegada, rafaga, nombre=None):
    """Crea un paciente AMARILLO (urgencia)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.AMARILLO, nombre_paciente=nombre)


def crear_paciente_embarazada(id_proceso, llegada, rafaga, nombre=None):
    """Crea una paciente EMBARAZADA (prioridad especial)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.EMBARAZADA, nombre_paciente=nombre)


def crear_paciente_verde(id_proceso, llegada, rafaga, nombre=None):
    """Crea un paciente VERDE (atención normal)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.VERDE, nombre_paciente=nombre)


def crear_paciente_cita(id_proceso, llegada, rafaga, nombre=None):
    """Crea un paciente de CITA (programado)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.CITA, nombre_paciente=nombre)


def crear_paciente_seguimiento(id_proceso, llegada, rafaga, nombre=None):
    """Crea un paciente de SEGUIMIENTO"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.SEGUIMIENTO, nombre_paciente=nombre)


# ============================================
# FUNCIONES PARA CREAR PACIENTES DE EJEMPLO
# ============================================

def crear_pacientes_ejemplo_hospital():
    """
    Crea un conjunto de pacientes de ejemplo con tipos y nombres
    """
    return [
        crear_paciente_rojo(1, 0, 5, "Carlos Méndez"),
        crear_paciente_amarillo(2, 1, 3, "Laura Sánchez"),
        crear_paciente_rojo(3, 2, 8, "Ana Rodríguez"),
        crear_paciente_verde(4, 3, 6, "Miguel Ángel"),
        crear_paciente_embarazada(5, 4, 4, "Sofía Herrera"),
        crear_paciente_amarillo(6, 5, 7, "Pedro Jiménez"),
        crear_paciente_verde(7, 6, 5, "Paula Quirós"),
        crear_paciente_cita(8, 7, 3, "Mario Chacón"),
        crear_paciente_seguimiento(9, 8, 4, "Fernando Arroyo"),
        crear_paciente_rojo(10, 9, 6, "Jorge Ramírez"),
    ]


def crear_pacientes_prueba():
    """
    Crea un conjunto de pacientes de prueba (los mismos del PDF)
    """
    return [
        Proceso(1, 0, 5, 1),
        Proceso(2, 1, 3, 2),
        Proceso(3, 2, 8, 1),
        Proceso(4, 3, 6, 3),
        Proceso(5, 4, 4, 2),
        Proceso(6, 5, 7, 3),
    ]