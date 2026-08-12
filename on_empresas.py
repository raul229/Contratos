from src.fabrica import construir_generador


def on_empresas(base_dir, contexto):
    generador = construir_generador('On Empresas', base_dir)
    generador.ejecutar(contexto)
