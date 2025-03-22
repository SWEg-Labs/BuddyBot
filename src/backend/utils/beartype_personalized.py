from beartype import beartype
from unittest.mock import MagicMock, AsyncMock
from functools import wraps

def beartype_personalized(func):
    # Se il decoratore viene applicato a una classe, iteriamo sui suoi attributi.
    if isinstance(func, type):
        for attr_name in dir(func):
            # Saltiamo i metodi speciali non desiderati.
            if attr_name.startswith("__") and attr_name.endswith("__") and attr_name != "__init__":
                continue
            attr = getattr(func, attr_name)
            if callable(attr):
                # Applichiamo ricorsivamente il nostro decoratore ai metodi della classe.
                decorated = beartype_personalized(attr)
                setattr(func, attr_name, decorated)
        return func

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Se uno degli argomenti è un mock (o una funzione lambda), bypassa il controllo dei tipi.
        for arg in args:
            if isinstance(arg, MagicMock) or isinstance(arg, AsyncMock) or isinstance(arg, type(lambda: None)):
                print("Mock rilevato, bypassando il controllo dei tipi")
                return func(*args, **kwargs)
        # Altrimenti, applica beartype al momento della chiamata.
        return beartype(func)(*args, **kwargs)
    return wrapper
