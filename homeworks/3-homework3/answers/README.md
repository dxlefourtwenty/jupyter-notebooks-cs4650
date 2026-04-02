# Homework 3 Analysis Files

Each homework part now has its own Python file:

- `analysis/question1.py`
- `analysis/question2.py`
- `analysis/question3.py`
- `analysis/question4.py`

Shared code lives in:

- `analysis/common.py`

You can run them one at a time:

```bash
MPLCONFIGDIR=/tmp/mpl venv/bin/python analysis/question1.py
MPLCONFIGDIR=/tmp/mpl venv/bin/python analysis/question2.py
MPLCONFIGDIR=/tmp/mpl venv/bin/python analysis/question3.py
MPLCONFIGDIR=/tmp/mpl venv/bin/python analysis/question4.py
```

Or run everything:

```bash
MPLCONFIGDIR=/tmp/mpl venv/bin/python analysis/run_logistic_analysis.py
```
