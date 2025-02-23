import sys
import os

# Abilita pytest-asyncio per eseguire test asincroni
pytest_plugins = "pytest_asyncio"

# Imposta il percorso per importare i moduli dal backend
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, "..", "src", "backend"))
sys.path.insert(0, src_path)
