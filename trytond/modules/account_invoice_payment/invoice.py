
import logging

from decimal import Decimal
from trytond.model import ModelView, fields
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
                'action': '_create_move',
                'state': 'end',
            },
        },
    }

    def __init__(self):
        super(ReconcileCreditNote,self).__init__()
        self._error_messages.update({
            'invoice_type': 'You can only mark credit notes as payment of' \
                'open invoices',
            'invoice_state': 'You can only reconcile opened credit notes',
            'amount_greater_invoice_amount_to_pay': 'Amount (%s) greater than '\
                                'the amount to pay of invoice!',


        })

    def _init(self, data):
        invoice_obj = Pool().get('account.invoice')
        invoice = invoice_obj.browse(data['id'])
        if invoice.type != 'out_credit_note':
            self.raise_user_error('invoice_type')
        if invoice.state != 'open':
            self.raise_user_error('invoice_state')
        

        return {}

    def _create_move(self, data):
        invoice_id = data['form'].get('invoice','')
        if invoice_id == '':
            return {}

        pool = Pool()
        move_obj = pool.get('account.move')
        invoice_obj = pool.get('account.invoice')
        currency_obj = pool.get('currency.currency')

        invoice = invoice_obj.browse(invoice_id)
        creditnote = invoice_obj.browse(data.get('id'))

        if invoice.amount_to_pay < creditnote.amount_to_pay:
            self.raise_user_error('amount_greater_invoice_amount_to_pay',
                                                          error_args=(creditnote.amount_to_pay,))
        reconcile_lines = invoice_obj.get_reconcile_lines_for_amount(invoice,
                                                                     creditnote.amount_to_pay)
        amount = creditnote.amount_to_pay
        move = move_obj.browse(creditnote.move.id)
        for move_line in move.lines:
            if move_line.account.id == invoice.account.id:
                line_id = move_line.id
                invoice_obj.write(invoice.id, {
                    'payment_lines': [('add', line_id)],
                })
                amount -= move_line.credit

        if amount == Decimal('0.0'):
            log.debug("amount: %d" % amount)
            invoice_obj.write(creditnote.id, {
                'state': 'paid',
            })

        return {}

ReconcileCreditNote()

