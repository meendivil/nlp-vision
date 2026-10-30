# Chatbot bancario sin LLM (Rasa)

> **Solo Windows** (PowerShell). Requiere **Python 3.10**.

## 1. Crear y activar el entorno

```powershell
# Desde la carpeta raíz del repositorio nlp-vision
cd semana-03\Actividad-03\chatbot-sin-llm
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la activación: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 2. Actualizar pip

```powershell
python -m pip install --upgrade pip setuptools wheel
```

## 3. Instalar dependencias (incluye Rasa)

```powershell
pip install -r requirements.txt
rasa --version
```

## 4. Validar y entrenar

```powershell
rasa data validate
rasa train
```

## 5. Ejecutar

**Terminal 1 — servidor de acciones**

```powershell
.\.venv\Scripts\Activate.ps1
rasa run actions
```

**Terminal 2 — chat**

```powershell
.\.venv\Scripts\Activate.ps1
rasa shell
```

Para salir del chat: `/stop`
