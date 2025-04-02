import subprocess
import webbrowser
import time

# Lancer Streamlit en arrière-plan
process = subprocess.Popen(
    ["streamlit", "run", "src/streamlit_for_app.py"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

# Attendre un peu que Streamlit démarre
time.sleep(2)

# Ouvrir le navigateur automatiquement

