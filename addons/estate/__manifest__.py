{
    'name': "estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "K22",
    'category': 'Ejemplo',
    'description': """
    Ejemplo de modulo nuevo
    """,
    # data files always loaded at installation
    'data': [
        'data/ir.estate.access.csv',
        'views/estate_views.xml',
    ]
    # data files containing optionally loaded demonstration data
    #    'demo/demo_data.xml',
    #],
}