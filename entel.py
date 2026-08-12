from src.fabrica import construir_generador


def entel(base_dir, contexto):
    generador = construir_generador('Entel', base_dir)
    generador.ejecutar(contexto)
