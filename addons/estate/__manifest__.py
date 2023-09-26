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
        'security/ir.model.access.csv',
        'views/estate_menus_views.xml',
        'views/estate_trees_views.xml',
        'views/estate_views.xml',
        
    # data files containing optionally loaded demonstration data
        #'demo/demo_data.xml',
    ],
}