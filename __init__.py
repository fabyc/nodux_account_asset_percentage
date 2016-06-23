# This file is part of Tryton.  The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.
from trytond.pool import Pool
from .asset import *

def register():
    Pool.register(
        Asset,
        module='nodux_account_asset_percentage', type_='model')
