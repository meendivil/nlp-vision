# VoxCustomer

> **The voice of the customer, decoded.**
> A Streamlit + Plotly application that turns the raw text of support tickets
> into an operational, measurable signal — and shows students exactly where a
> traditional NLP pipeline ends and a transformer begins.

Built for the **Procesamiento de Lenguaje Natural y Visión Computacional**
course (TecMilenio, T2-2026), Week 4.

---

## What you get

### Page 1 · Executive Dashboard
Sentiment as a first-class production feature.

- Customer-health KPI bar (negative voice share, critical priority, CSAT, …)
- Voice-of-customer donut on the full ticket stream
- **Product Purchased × Predicted Sentiment** stacked bar, ranked by negative share
- **Ticket Priority vs. text negativity** violin distribution
- Predicted sentiment vs. real CSAT correlation
- Channel × sentiment heatmap and a most-negative-tickets drilldown
- Live filters by channel, status and priority

> *Master's lesson — text is not a string; it is an analytical dimension that
> drives business decisions and resource allocation.*

### Page 2 · Model Evaluation
A side-by-side, latency-aware shootout.

- **Playground** — type a ticket (or pick a sarcasm / negation / mixed preset)
  and watch both models score it in real time with full confidence bars.
- **Benchmark** — a curated, hand-labeled 50-example test set with confusion
  matrices, per-class precision / recall / F1, an inference-latency chart and
  a "where they disagree" table.
- **Theory** — short refresher on the $O(N)$ vs. self-attention $O(N^2 \cdot d)$
  trade-off, with a "when to pick which" rubric.

> *Master's lesson — production AI requires balancing accuracy against compute
> cost and latency.*

---

## Tech stack

| Layer            | Choice                                                  |
|------------------|---------------------------------------------------------|
| UI               | [Streamlit](https://streamlit.io) (multipage)            |
| Charts           | [Plotly](https://plotly.com/python/) (custom dark theme) |
| Traditional NLP  | scikit-learn `TfidfVectorizer` + `LogisticRegression`    |
| Deep NLP         | 🤗 Transformers · `cardiffnlp/twitter-roberta-base-sentiment-latest` |
| Data             | [Customer Support Ticket Dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset) |

---

## Project layout

```
voxcustomer/
├── app.py                       # Home page
├── pages/
│   ├── 1_Executive_Dashboard.py # Idea 1
│   └── 2_Model_Evaluation.py    # Idea 3
├── src/
│   ├── theme.py                 # CSS + Plotly template
│   ├── components.py            # KPI cards, sections, badges
│   ├── data_loader.py           # CSV ingest + cleaning
│   ├── models.py                # Traditional + transformer wrappers
│   └── corpus.py                # Bundled training / eval corpora
├── data/
│   └── customer_support_tickets.csv
├── .streamlit/config.toml       # Dark brand theme
├── requirements.txt
├── setup.sh                     # One-shot venv bootstrap (conda: see below)
└── README.md
```

---

## Getting started

### 1 · Create the Python environment

**Requirements:** Python **3.10 – 3.12** (3.11 recommended — `torch<2.5`
has no wheels for 3.13+). Pick **one** of the options below.

#### Option A · Conda (Anaconda / Miniconda)

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or
   [Anaconda](https://www.anaconda.com/download) if you don't have it, and
   check it works:

   ```bash
   conda --version
   ```

   > On **Windows**, use the *Anaconda Prompt* (or run `conda init powershell`
   > once and reopen PowerShell). On **macOS / Linux**, if `conda` is not
   > found, run `conda init zsh` (or `bash`) and open a new terminal.

2. Create and activate the environment:

   ```bash
   cd semana-04/voxcustomer
   conda create -n voxcustomer python=3.11 -y
   conda activate voxcustomer
   ```

3. Install the dependencies with `pip` **inside** the conda environment:

   ```bash
   python -m pip install --upgrade pip wheel setuptools
   python -m pip install -r requirements.txt
   ```

4. Check that the environment's Python is the one being used:

   ```bash
   python --version                        # Python 3.11.x
   python -c "import streamlit, torch; print(streamlit.__version__, torch.__version__)"
   ```

Useful conda commands:

```bash
conda env list                    # list your environments
conda deactivate                  # leave the environment
conda env remove -n voxcustomer   # delete it and start from scratch
```

#### Option B · venv (setup script)

The repo ships with a one-shot setup script (macOS / Linux) that creates a
local `.venv`, upgrades `pip`, and installs every dependency.

```bash
cd semana-04/voxcustomer
./setup.sh
```

> To use a specific interpreter: `PYTHON=python3.11 ./setup.sh`.

#### Option C · venv (by hand)

**macOS / Linux**

```bash
cd semana-04/voxcustomer
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
cd semana-04\voxcustomer
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

> The `transformers` + `torch` install is the heaviest part — expect a few
> hundred megabytes. On Apple Silicon, PyTorch ships an MPS backend that
> VoxCustomer picks up automatically.

### 2 · Verify the dataset

Place the Kaggle CSV at:

```
voxcustomer/data/customer_support_tickets.csv
```

The repo already ships with a copy; if it gets deleted, grab it again from
[Kaggle · suraj520/customer-support-ticket-dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset?select=customer_support_tickets.csv).

### 3 · Run the app

Activate the environment you created and launch Streamlit from the
`voxcustomer/` folder:

```bash
conda activate voxcustomer        # Option A (conda)
source .venv/bin/activate         # Options B / C (venv, macOS / Linux)
# .venv\Scripts\Activate.ps1      # Option C (venv, Windows PowerShell)

streamlit run app.py
```

Streamlit opens the home page at [http://localhost:8501](http://localhost:8501).
Use the sidebar to switch between the two views.

> The transformer is **lazy-loaded**. On Page 2, click **Load transformer**
> the first time you want a side-by-side comparison — the model is then
> cached for the rest of the session.

---

## What's bundled, and why

| File                | Content                                                            |
|---------------------|--------------------------------------------------------------------|
| `src/corpus.py`     | ~300 hand-written training examples (support-domain, 3 classes)    |
| `src/corpus.py`     | 50 hand-labeled evaluation examples with sarcasm / negation / mix  |
| `src/models.py`     | Identical `predict_one` / `predict_batch` interface for both models|
| `.streamlit/`       | Dark brand theme so the app looks like a real product              |

This means the app runs **fully offline** for the baseline model — only the
transformer download requires network access on first launch.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `FileNotFoundError: data/customer_support_tickets.csv` | Re-download the dataset from Kaggle and drop it in `voxcustomer/data/`. |
| Transformer fails to load with a network error | You're offline — Page 1 and the playground's TF-IDF column still work; retry the transformer load when online. |
| Slow first page load | Sentiment scoring runs once per dataset and is cached. Subsequent renders are instant. |
| Streamlit cannot find `src/...` | Always launch from the `voxcustomer/` folder (`streamlit run app.py`). |
| `streamlit: command not found` / `ModuleNotFoundError` | The environment isn't active. Run `conda activate voxcustomer` (or activate `.venv`) before launching. |
| `pip` can't find a matching `torch` version | Your Python is too new. Recreate the env with Python 3.11 (`conda create -n voxcustomer python=3.11 -y`). |

---

## Credits

- Dataset · [`suraj520/customer-support-ticket-dataset`](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)
- Transformer · [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
- Course · *Procesamiento de Lenguaje Natural y Visión Computacional* — TecMilenio, T2 2026
