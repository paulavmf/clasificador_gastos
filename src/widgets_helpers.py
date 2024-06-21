import ipywidgets as widgets
from IPython.display import display, HTML

def on_category_change(change, df):
    from src.graphics import bar_plot_by_category_from_multy_sheets
    if change['type'] == 'change' and change['name'] == 'value':
        bar_plot_by_category_from_multy_sheets(df, change['new'])


def file_selector_from_filder(carpeta):
    from src.helpers import listar_archivos_en_carpeta

    archivos, archivos_paths = listar_archivos_en_carpeta(carpeta)

    # Crear el widget Dropdown
    dropdown_archivos = widgets.Dropdown(
        options=list(zip(archivos, archivos_paths)),
        description='Archivos:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='50%')
    )

    # Mostrar el widget Dropdown
    display(dropdown_archivos)
    return dropdown_archivos.value
