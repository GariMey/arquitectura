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
    def listar_tipos(cls):
        """Lista todos los tipos de pacientes disponibles"""
        print("\n📋 TIPOS DE PACIENTES:")
        print("=" * 50)
        for tipo, descripcion in cls.DESCRIPCIONES.items():
            emoji = cls.EMOJIS.get(tipo, "")
            print(f"  {emoji} {tipo:<12} - {descripcion}")
        print("=" * 50)


class Proceso:
    """
    Clase que representa un proceso/paciente en el sistema
    Ahora incluye tipo de paciente para el contexto hospitalario
    """
    
    def __init__(self, id_proceso, tiempo_llegada, rafaga, prioridad=0, tipo_paciente=None):
        """
        Inicializa un nuevo proceso/paciente
        
        Args:
            id_proceso: Identificador único del proceso
            tiempo_llegada: Momento en que el proceso entra al sistema
            rafaga: Duración total de ejecución requerida
            prioridad: Nivel de prioridad (opcional, se calcula automáticamente si hay tipo)
            tipo_paciente: Tipo de paciente (Rojo, Amarillo, Embarazada, Verde, Cita, Seguimiento)
        """
        self.id = id_proceso
        self.tiempo_llegada = tiempo_llegada
        self.rafaga = rafaga
        
        # Si se especifica tipo de paciente, usar su prioridad
        if tipo_paciente:
            self.tipo_paciente = tipo_paciente
            self.prioridad = TipoPaciente.get_prioridad(tipo_paciente)
        else:
            self.tipo_paciente = None
            self.prioridad = prioridad if prioridad > 0 else 3  # Prioridad por defecto
        
        self.tiempo_restante = rafaga
        self.tiempo_inicio = None
        self.tiempo_finalizacion = None
        self.tiempo_espera = 0
        self.tiempo_retorno = 0
        self.completado = False
    
    def __str__(self):
        """Representación legible del proceso"""
        emoji = TipoPaciente.get_emoji(self.tipo_paciente) if self.tipo_paciente else "💻"
        tipo_str = f", Tipo: {self.tipo_paciente}" if self.tipo_paciente else ""
        prioridad_str = f", Prioridad: {self.prioridad}"
        return f"{emoji} P{self.id} (Llegada: {self.tiempo_llegada}, Ráfaga: {self.rafaga}{prioridad_str}{tipo_str})"
    
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
    
    def to_dict(self):
        """Convierte el proceso a diccionario para almacenamiento"""
        return {
            'id': self.id,
            'tiempo_llegada': self.tiempo_llegada,
            'rafaga': self.rafaga,
            'prioridad': self.prioridad,
            'tipo_paciente': self.tipo_paciente,
            'tiempo_espera': self.tiempo_espera,
            'tiempo_retorno': self.tiempo_retorno,
            'tiempo_finalizacion': self.tiempo_finalizacion
        }
    
    def get_emoji(self):
        """Obtiene el emoji según el tipo de paciente"""
        return TipoPaciente.get_emoji(self.tipo_paciente) if self.tipo_paciente else "💻"
    
    def get_descripcion(self):
        """Obtiene la descripción del tipo de paciente"""
        return TipoPaciente.get_descripcion(self.tipo_paciente) if self.tipo_paciente else "Proceso normal"


# Funciones de utilidad para crear pacientes
def crear_paciente_rojo(id_proceso, llegada, rafaga):
    """Crea un paciente ROJO (emergencia máxima)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.ROJO)

def crear_paciente_amarillo(id_proceso, llegada, rafaga):
    """Crea un paciente AMARILLO (urgencia)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.AMARILLO)

def crear_paciente_embarazada(id_proceso, llegada, rafaga):
    """Crea una paciente EMBARAZADA (prioridad especial)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.EMBARAZADA)

def crear_paciente_verde(id_proceso, llegada, rafaga):
    """Crea un paciente VERDE (atención normal)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.VERDE)

def crear_paciente_cita(id_proceso, llegada, rafaga):
    """Crea un paciente de CITA (programado)"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.CITA)

def crear_paciente_seguimiento(id_proceso, llegada, rafaga):
    """Crea un paciente de SEGUIMIENTO"""
    return Proceso(id_proceso, llegada, rafaga, tipo_paciente=TipoPaciente.SEGUIMIENTO)