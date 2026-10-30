# Chatbot bancario con LLM (Rasa + Ollama)

> **Solo Windows** (PowerShell). Requiere **Python 3.10** y **Ollama**.

## 1. Instalar Ollama y descargar el modelo

1. Descarga e instala `OllamaSetup.exe` desde [ollama.com/download](https://ollama.com/download).
2. Cierra y vuelve a abrir PowerShell.
3. Verifica la instalación y descarga el modelo:

```powershell
ollama --version
ollama pull llama3.2
Invoke-RestMethod http://localhost:11434/api/tags
```

> Ollama queda corriendo en segundo plano (ícono de llama en la bandeja del sistema).

## 2. Crear y activar el entorno

```powershell
# Desde la carpeta raíz del repositorio nlp-vision
cd semana-03\Actividad-03\chatbot-con-llm
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la activación: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## 3. Actualizar pip

```powershell
python -m pip install --upgrade pip setuptools wheel
```

## 4. Instalar dependencias (Rasa, Rasa SDK y requests)

```powershell
pip install -r requirements.txt
rasa --version
```

## 5. Validar y entrenar

```powershell
rasa data validate
rasa train
```

## 6. Ejecutar

**Terminal 1 — servidor de acciones**

```powershell
.\.venv\Scripts\Activate.ps1
$env:OLLAMA_URL = "http://127.0.0.1:11434/api/generate"   # opcional: evita ~2 s de espera por llamada en Windows
rasa run actions
```

**Terminal 2 — chat**

```powershell
.\.venv\Scripts\Activate.ps1
$env:RASA_SHELL_STREAM_READING_TIMEOUT_IN_SECONDS = "60"
rasa shell
```

Para salir del chat: `/stop`
