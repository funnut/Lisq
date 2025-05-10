def wykonaj_komende(komenda):
    try:
        if komenda == "start":
            print("Uruchamiam...")
        elif komenda == "stop":
            print("Zatrzymuję...")
        else:
            raise ValueError(f"Nieznana komenda: {komenda}")
    except Exception as e:
        print(f"Błąd: {e}")

# Test:
wykonaj_komende("start")
wykonaj_komende("foo")
