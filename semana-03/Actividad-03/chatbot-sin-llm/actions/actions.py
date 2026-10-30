from typing import Any, Dict, List, Text
import unicodedata
import uuid

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


# ============================================================
# DATOS SIMULADOS DEL BANCO
# ============================================================

BANK_DATA = {
    "U001": {
        "nombre": "Ana López",
        "cuentas": {
            "debito": {
                "saldo": 20500.75,
                "estados_cuenta": {
                    "2026-09": {
                        "periodo": "Septiembre 2026",
                        "saldo_inicial": 16000.00,
                        "saldo_final": 20500.75,
                        "movimientos": [
                            {
                                "fecha": "2026-09-01",
                                "concepto": "Depósito de nómina",
                                "monto": 6000.00,
                            },
                            {
                                "fecha": "2026-09-08",
                                "concepto": "Supermercado",
                                "monto": -1250.25,
                            },
                            {
                                "fecha": "2026-09-15",
                                "concepto": "Transferencia SPEI",
                                "monto": -249.00,
                            },
                        ],
                    }
                },
            },
            "credito": {
                "saldo": 2850.50,
                "limite_credito": 30000.00,
                "estados_cuenta": {
                    "2026-09": {
                        "periodo": "Septiembre 2026",
                        "saldo_inicial": 3500.00,
                        "saldo_final": 2850.50,
                        "movimientos": [
                            {
                                "fecha": "2026-09-04",
                                "concepto": "Compra Amazon",
                                "monto": 1200.50,
                            },
                            {
                                "fecha": "2026-09-10",
                                "concepto": "Restaurante",
                                "monto": 650.00,
                            },
                            {
                                "fecha": "2026-09-20",
                                "concepto": "Pago tarjeta",
                                "monto": -2500.00,
                            },
                        ],
                    }
                },
            },
        },
    },

    "U002": {
        "nombre": "Carlos Martínez",
        "cuentas": {
            "debito": {
                "saldo": 16725.00,
                "estados_cuenta": {
                    "2026-09": {
                        "periodo": "Septiembre 2026",
                        "saldo_inicial": 9000.00,
                        "saldo_final": 16725.00,
                        "movimientos": [
                            {
                                "fecha": "2026-09-01",
                                "concepto": "Depósito",
                                "monto": 12000.00,
                            },
                            {
                                "fecha": "2026-09-06",
                                "concepto": "Pago de renta",
                                "monto": -3400.00,
                            },
                            {
                                "fecha": "2026-09-18",
                                "concepto": "Servicios",
                                "monto": -875.00,
                            },
                        ],
                    }
                },
            },
            "credito": {
                "saldo": 9550.00,
                "limite_credito": 45000.00,
                "estados_cuenta": {
                    "2026-09": {
                        "periodo": "Septiembre 2026",
                        "saldo_inicial": 10500.00,
                        "saldo_final": 9550.00,
                        "movimientos": [
                            {
                                "fecha": "2026-09-03",
                                "concepto": "Compra electrónica",
                                "monto": 3200.00,
                            },
                            {
                                "fecha": "2026-09-11",
                                "concepto": "Gasolina",
                                "monto": 850.00,
                            },
                            {
                                "fecha": "2026-09-25",
                                "concepto": "Pago tarjeta",
                                "monto": -5000.00,
                            },
                        ],
                    }
                },
            },
        },
    },

    "U003": {
        "nombre": "Mariana Torres",
        "cuentas": {
            "debito": {
                "saldo": 31100.00,
                "estados_cuenta": {
                    "2026-09": {
                        "periodo": "Septiembre 2026",
                        "saldo_inicial": 28000.00,
                        "saldo_final": 31100.00,
                        "movimientos": [
                            {
                                "fecha": "2026-09-02",
                                "concepto": "Transferencia recibida",
                                "monto": 7000.00,
                            },
                            {
                                "fecha": "2026-09-12",
                                "concepto": "Supermercado",
                                "monto": -1300.50,
                            },
                            {
                                "fecha": "2026-09-21",
                                "concepto": "Pago de servicios",
                                "monto": -2599.50,
                            },
                        ],
                    }
                },
            },
            "credito": {
                "saldo": 2500.00,
                "limite_credito": 20000.00,
                "estados_cuenta": {
                    "2026-09": {
                        "periodo": "Septiembre 2026",
                        "saldo_inicial": 0.00,
                        "saldo_final": 2500.00,
                        "movimientos": [
                            {
                                "fecha": "2026-09-05",
                                "concepto": "Tienda departamental",
                                "monto": 1500.00,
                            },
                            {
                                "fecha": "2026-09-14",
                                "concepto": "Compra en línea",
                                "monto": 2200.00,
                            },
                            {
                                "fecha": "2026-09-28",
                                "concepto": "Pago tarjeta",
                                "monto": -1200.00,
                            },
                        ],
                    }
                },
            },
        },
    },

    # Solo crédito
    "U004": {
        "nombre": "Roberto Hernández",
        "cuentas": {
            "credito": {
                "saldo": 4750.00,
                "limite_credito": 25000.00,
                "estados_cuenta": {
                    "2026-09": {
                        "periodo": "Septiembre 2026",
                        "saldo_inicial": 5500.00,
                        "saldo_final": 4750.00,
                        "movimientos": [
                            {
                                "fecha": "2026-09-07",
                                "concepto": "Compra supermercado",
                                "monto": 1800.00,
                            },
                            {
                                "fecha": "2026-09-16",
                                "concepto": "Restaurante",
                                "monto": 450.00,
                            },
                            {
                                "fecha": "2026-09-27",
                                "concepto": "Pago tarjeta",
                                "monto": -3000.00,
                            },
                        ],
                    }
                },
            }
        },
    },

    # Solo débito
    "U005": {
        "nombre": "Sofía Ramírez",
        "cuentas": {
            "debito": {
                "saldo": 17000.00,
                "estados_cuenta": {
                    "2026-09": {
                        "periodo": "Septiembre 2026",
                        "saldo_inicial": 10500.00,
                        "saldo_final": 17000.00,
                        "movimientos": [
                            {
                                "fecha": "2026-09-01",
                                "concepto": "Depósito de nómina",
                                "monto": 8500.00,
                            },
                            {
                                "fecha": "2026-09-09",
                                "concepto": "Supermercado",
                                "monto": -1420.00,
                            },
                            {
                                "fecha": "2026-09-19",
                                "concepto": "Telefonía e internet",
                                "monto": -580.00,
                            },
                        ],
                    }
                },
            }
        },
    },
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def normalize_text(value: str) -> str:
    """Convierte Nómina -> nomina, Débito -> debito, etc."""
    value = str(value).strip().lower()

    return "".join(
        char
        for char in unicodedata.normalize("NFD", value)
        if unicodedata.category(char) != "Mn"
    )


def normalize_user_id(value: str) -> str:
    return str(value).strip().upper()


def normalize_account_type(value: str) -> str:
    value = normalize_text(value)

    aliases = {
        "debito": "debito",
        "cuenta debito": "debito",
        "cuenta de debito": "debito",

        "credito": "credito",
        "cuenta credito": "credito",
        "cuenta de credito": "credito",
        "tarjeta de credito": "credito",
    }

    return aliases.get(value, value)


def normalize_period(value: str) -> str:
    """
    Convierte diferentes expresiones de septiembre 2026
    al formato interno 2026-09.
    """

    value = normalize_text(value)

    periods = {
        "septiembre": "2026-09",
        "septiembre 2026": "2026-09",
        "09/2026": "2026-09",
        "2026-09": "2026-09",
    }

    return periods.get(value, value)


# ============================================================
# VALIDACIÓN DEL FORMULARIO DE SALDO
# ============================================================

class ValidateSaldoForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_saldo_form"

    def validate_usuario_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        usuario_id = normalize_user_id(slot_value)

        if usuario_id not in BANK_DATA:
            dispatcher.utter_message(
                text=(
                    "El usuario indicado no existe. "
                    "Para esta demostración puedes utilizar "
                    "U001, U002, U003, U004 o U005."
                )
            )

            return {"usuario_id": None}

        return {"usuario_id": usuario_id}

    def validate_tipo_cuenta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        tipo_cuenta = normalize_account_type(slot_value)

        if tipo_cuenta not in ["debito", "credito"]:
            dispatcher.utter_message(
                text="El tipo de cuenta debe ser débito o crédito."
            )
            return {"tipo_cuenta": None}

        usuario_id = tracker.get_slot("usuario_id")

        if not usuario_id:
            return {"tipo_cuenta": tipo_cuenta}

        usuario_id = normalize_user_id(usuario_id)

        usuario = BANK_DATA.get(usuario_id)

        if not usuario:
            return {"tipo_cuenta": tipo_cuenta}

        if tipo_cuenta not in usuario["cuentas"]:
            cuentas = ", ".join(usuario["cuentas"].keys())

            dispatcher.utter_message(
                text=(
                    f"{usuario['nombre']} no tiene una cuenta de "
                    f"{tipo_cuenta}. Sus cuentas disponibles son: "
                    f"{cuentas}."
                )
            )

            return {"tipo_cuenta": None}

        return {"tipo_cuenta": tipo_cuenta}


# ============================================================
# ACTION: CONSULTAR SALDO
# ============================================================

class ActionConsultarSaldo(Action):

    def name(self) -> Text:
        return "action_consultar_saldo"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        usuario_id = tracker.get_slot("usuario_id")
        tipo_cuenta = tracker.get_slot("tipo_cuenta")

        if not usuario_id or not tipo_cuenta:
            dispatcher.utter_message(
                text="No tengo suficiente información para consultar el saldo."
            )
            return []

        usuario_id = normalize_user_id(usuario_id)
        tipo_cuenta = normalize_account_type(tipo_cuenta)

        usuario = BANK_DATA.get(usuario_id)

        if not usuario:
            dispatcher.utter_message(
                text="No encontré el usuario."
            )
            return []

        cuenta = usuario["cuentas"].get(tipo_cuenta)

        if not cuenta:
            dispatcher.utter_message(
                text=(
                    f"No encontré una cuenta de {tipo_cuenta} "
                    f"asociada a {usuario['nombre']}."
                )
            )
            return []

        # Cuenta de débito
        if tipo_cuenta == "debito":
            dispatcher.utter_message(
                text=(
                    f"{usuario['nombre']}, el saldo disponible de tu "
                    f"cuenta de débito es de "
                    f"${cuenta['saldo']:,.2f} MXN."
                )
            )

        # Cuenta de crédito
        elif tipo_cuenta == "credito":

            limite = cuenta["limite_credito"]
            saldo = cuenta["saldo"]
            disponible = limite - saldo

            dispatcher.utter_message(
                text=(
                    f"{usuario['nombre']}, el saldo actual de tu "
                    f"cuenta de crédito es de "
                    f"${saldo:,.2f} MXN. "
                    f"Tu crédito disponible es de "
                    f"${disponible:,.2f} MXN."
                )
            )

        return []


# ============================================================
# VALIDACIÓN ESTADO DE CUENTA
# ============================================================

class ValidateEstadoCuentaForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_estado_cuenta_form"

    def validate_usuario_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        usuario_id = normalize_user_id(slot_value)

        if usuario_id not in BANK_DATA:
            dispatcher.utter_message(
                text="No encontré ese usuario."
            )

            return {"usuario_id": None}

        return {"usuario_id": usuario_id}

    def validate_tipo_cuenta(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        tipo_cuenta = normalize_account_type(slot_value)

        if tipo_cuenta not in ["debito", "credito"]:
            dispatcher.utter_message(
                text="El tipo de cuenta debe ser débito o crédito."
            )

            return {"tipo_cuenta": None}

        usuario_id = tracker.get_slot("usuario_id")

        if usuario_id:
            usuario = BANK_DATA.get(
                normalize_user_id(usuario_id)
            )

            if (
                usuario
                and tipo_cuenta not in usuario["cuentas"]
            ):
                dispatcher.utter_message(
                    text=(
                        f"El usuario no tiene una cuenta "
                        f"de {tipo_cuenta}."
                    )
                )

                return {"tipo_cuenta": None}

        return {"tipo_cuenta": tipo_cuenta}

    def validate_fecha(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        periodo = normalize_period(slot_value)

        usuario_id = tracker.get_slot("usuario_id")
        tipo_cuenta = tracker.get_slot("tipo_cuenta")

        if not usuario_id or not tipo_cuenta:
            return {"fecha": periodo}

        usuario = BANK_DATA.get(
            normalize_user_id(usuario_id)
        )

        if not usuario:
            return {"fecha": None}

        cuenta = usuario["cuentas"].get(
            normalize_account_type(tipo_cuenta)
        )

        if not cuenta:
            return {"fecha": None}

        if periodo not in cuenta["estados_cuenta"]:
            dispatcher.utter_message(
                text=(
                    "No encontré un estado de cuenta para ese periodo. "
                    "En estos datos de prueba está disponible "
                    "Septiembre 2026."
                )
            )

            return {"fecha": None}

        return {"fecha": periodo}


# ============================================================
# ACTION: ESTADO DE CUENTA
# ============================================================

class ActionEstadoCuenta(Action):

    def name(self) -> Text:
        return "action_estado_cuenta"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        usuario_id = tracker.get_slot("usuario_id")
        tipo_cuenta = tracker.get_slot("tipo_cuenta")
        fecha = tracker.get_slot("fecha")

        if not usuario_id or not tipo_cuenta or not fecha:
            dispatcher.utter_message(
                text=(
                    "Necesito el usuario, tipo de cuenta y periodo "
                    "para consultar el estado de cuenta."
                )
            )
            return []

        usuario_id = normalize_user_id(usuario_id)
        tipo_cuenta = normalize_account_type(tipo_cuenta)
        periodo = normalize_period(fecha)

        usuario = BANK_DATA.get(usuario_id)

        if not usuario:
            dispatcher.utter_message(
                text="No encontré el usuario."
            )
            return []

        cuenta = usuario["cuentas"].get(tipo_cuenta)

        if not cuenta:
            dispatcher.utter_message(
                text=(
                    f"No encontré una cuenta de {tipo_cuenta} "
                    f"para {usuario['nombre']}."
                )
            )
            return []

        estado = cuenta["estados_cuenta"].get(periodo)

        if not estado:
            dispatcher.utter_message(
                text="No encontré el estado de cuenta solicitado."
            )
            return []

        movimientos = "\n".join(
            [
                (
                    f"• {movimiento['fecha']} - "
                    f"{movimiento['concepto']}: "
                    f"${movimiento['monto']:,.2f} MXN"
                )
                for movimiento in estado["movimientos"]
            ]
        )

        mensaje = (
            f"Estado de cuenta - {estado['periodo']}\n"
            f"Cliente: {usuario['nombre']}\n"
            f"Cuenta: {tipo_cuenta}\n\n"
            f"Saldo inicial: "
            f"${estado['saldo_inicial']:,.2f} MXN\n"
            f"Saldo final: "
            f"${estado['saldo_final']:,.2f} MXN\n\n"
            f"Movimientos:\n"
            f"{movimientos}"
        )

        dispatcher.utter_message(text=mensaje)

        return []

# ============================================================
# ACTION: PROCESAR SOPORTE
# ============================================================

class ActionProcesarSoporte(Action):

    def name(self) -> Text:
        return "action_procesar_soporte"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        tipo_solicitud = tracker.get_slot("tipo_solicitud")
        monto = tracker.get_slot("monto")

        folio = f"SOP-{uuid.uuid4().hex[:6].upper()}"

        mensaje = f"Registré tu reporte de soporte: {tipo_solicitud}."

        if monto:
            mensaje += f" Monto reportado: {monto}."

        mensaje += (
            f" Tu folio es {folio}. "
            f"Un asesor dará seguimiento a tu caso."
        )

        dispatcher.utter_message(text=mensaje)

        # Se limpian los slots para que un nuevo reporte vuelva a preguntar
        return [SlotSet("tipo_solicitud", None), SlotSet("monto", None)]