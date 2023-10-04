{
    'name': "facturas",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base'],
    'author': "K22",
    'category': 'Trabajo',
    'description': """
    Espacio de trabajo
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/facturas_forms_views.xml',
        'views/facturas_trees_views.xml',
        'views/facturas_menus.xml',
        
    # data files containing optionally loaded demonstration data
        #'demo/demo_data.xml',
    ],
}