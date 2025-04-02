import subprocess
import webbrowser
import time

# Lancer Streamlit en arrière-plan sinon on peut plus acéder au terminal pour le main
process = subprocess.Popen(
    ["streamlit", "run", "src/streamlit_for_app.py"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

time.sleep(2)


