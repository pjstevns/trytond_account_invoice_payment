
import os
import logging

from z3c.rml import pagetemplate
from trytond.model import ModelView, fields
from trytond.report import Report
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.wizard import Wizard
from trytond.pyson import Eval

log = logging.getLogger(__name__)

class ReconcileCreditNoteInit(ModelView):
    'Reconcile Credit Note Init'
    _name = 'account.invoice.reconcile_creditnote.init'
    _description = __doc__

    party = fields.Many2One('party.party', 'Party', required=True, readonly=True)
    invoice = fields.Many2One('account.invoice', 'Invoice', required=True,
                              domain=[
                                  ('type','=','out_invoice'),
                                  ('state', '=','open'),
                                  ('party','=',Eval('party'))
                              ])

    def default_party(self):
        active_id = Transaction().context.get('active_ids')[0]
        invoice_obj = Pool().get('account.invoice')
        invoice = invoice_obj.browse(active_id)
        return invoice.party.id

ReconcileCreditNoteInit()

class ReconcileCreditNote(Wizard):
    '(Partially) reconcile credit note'
    _name = 'account.invoice.reconcile_creditnote'

    states = {
        'init': {
            'actions': ['_init'],
            'result': {
                'type': 'form',
                'object': 'account.invoice.reconcile_creditnote.init',
                'state': [
                    ('end', 'Cancel', 'tryton-cancel'),
                    ('next', 'Next', 'tryton-ok'),
                ],
            },
        },
        'next': {
            'result': {
                'type': 'action',
                'action': '_reconcile',
                'state': 'end',
            },
        },
    }

    def __init__(self):
        super(ReconcileCreditNote,self).__init__()
        self._error_messages.update({
            'invoice_type': 'You can only mark credit notes as payment of' \
                'open invoices',
        })

    def _init(self, data):
        invoice_obj = Pool().get('account.invoice')
        invoice = invoice_obj.browse(data['id'])
        if invoice.type != 'out_credit_note':
            self.raise_user_error('invoice_type')
        return {}

    def _reconcile(self, data):
        log.debug(data)
        return {}

ReconcileCreditNote()

