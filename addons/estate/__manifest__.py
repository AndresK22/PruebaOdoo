{
    'name': "estate",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'author': "K22",
    'category': 'Ejemplo',
    'description': """
    Ejemplo de modulo nuevo
    """,
    # data files always loaded at installation
    'data': [
        'data/ir.model.access.csv',
        'views/estate_menus_views.xml',
        'views/estate_trees_views.xml',
        'views/estate_views.xml',
        'views/res_users_views.xml'
        
    # data files containing optionally loaded demonstration data
        #'demo/demo_data.xml',
    ],
}