# This file is part of Tryton.  The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta
from trytond.modules.account_product import MissingFunction

__all__ = ['Template', 'Category']
__metaclass__ = PoolMeta


class Template:
    __name__ = 'product.template'

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()

        del cls.account_depreciation.domain[0]
        del cls.account_asset.domain[0]

class Category:
    __name__ = 'product.category'

    @classmethod
    def __setup__(cls):
        super(Category, cls).__setup__()

        del cls.account_depreciation.domain[0]
        del cls.account_asset.domain[0]
