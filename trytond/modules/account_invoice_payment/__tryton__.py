#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name': 'Reconcile credit-notes with invoices',
    'name_nl_NL': 'Credit notas wegboeken als deel-betalingen op facturen',
    'version': '2.2.1',
    'author': 'NFG',
    'email': 'info@nfg.nl',
    'website': 'https://github.com/pjstevns/trytond_account_invoice_payment',
    'description': '''Use credit-notes as partial payments on open invoices.
''',
    'xml': [
        'invoice.xml',
    ],
    'depends': [
        'account',
        'account_invoice',
        'company',
        'party',
        'currency',
    ],
}
