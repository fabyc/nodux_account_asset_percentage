# This file is part of Tryton.  The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.
import datetime
import calendar
from decimal import Decimal, ROUND_HALF_EVEN
from dateutil import relativedelta
from dateutil import rrule

from trytond.model import Workflow, ModelSQL, ModelView, fields
from trytond.pyson import Eval, Bool, If
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond.tools import grouped_slice


__all__ = ['Asset']

__metaclass__ = PoolMeta

def date2datetime(date):
    return datetime.datetime.combine(date, datetime.time())

class Asset():
    'Asset'
    __name__ = 'account.asset'
    _rec_name = 'reference'

    #campo para obtener el valor residual de acuerdo al porcentaje que sea ingresado
    porcentaje = fields.Numeric('Porcentaje de valor residual',
        states={
            'readonly': (Eval('lines', [0]) | (Eval('state') != 'draft') | (~Eval('value', Decimal(0.0)))),
            },
        depends=['currency_digits', 'state'],
        required=True,
        digits=(16, Eval('currency_digits', 2)))

    @classmethod
    def __setup__(cls):
        super(Asset, cls).__setup__()
        cls.residual_value.states['readonly'] |= Eval('active', True)

    @staticmethod
    def default_frequency():
        return 'yearly'

    #metodo para calcular el valor residual
    @fields.depends('value', 'porcentaje', 'residual_value', 'company')
    def on_change_porcentaje(self):
        res = {}
        if self.porcentaje:
            porcentaje =self.porcentaje / 100
            if self.value and self.company:
                residual=(self.value * porcentaje)
                residual =  self.company.currency.round(residual)
                res['residual_value'] = residual
        return res

    #metodo para cambiar porcentaje cuando cambia value
    @fields.depends('value', 'porcentaje', 'residual_value', 'company')
    def on_change_value(self):
        res = {}
        res['porcentaje'] = None
        res['residual_value'] = None
        return res
