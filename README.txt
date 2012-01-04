
This package provides a module for the Tryton-ERP framework.

With this module you can quickly generate payments on invoices
based on credit notes.

Use case: when you create credit notes for a partial refund on
an invoice Tryton does not have an easy way to match the credit note
with the invoice. This module adds a wizard to the credit-note 
context that allows you to select an invoice and use the credit-note
to create a payment (refund) on the invoice.

Todo: 

- currently only accepts invoices with amounts larger than the 
credit_note. Being able to refund multiple smaller invoices with one
credit_note would be a nice to have.


License: GPLv3

Copyright: Paul J Stevens <paul@nfg.nl>, NFG Net Facilities Group BV, NL, 2012

