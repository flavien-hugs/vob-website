# checkout.voucher.py


from django.conf import settings


from checkout.models import Voucher


class ApplyVoucher(object):

    def __init__(self, request):

        self.session = request.session
        self.id_voucher = self.session.get('id_voucher')

    @property
    def voucher(self):
        if self.id_voucher:
            return Voucher.objects.get(pk=self.id_voucher)
        return None

    def get_discount(self):
        if self.voucher:
            return (self.voucher.discount / int('100')) * int(self.book.price)
        return int('0')

    def get_total_cost_after_discount(self):
        return int(self.book.price) - self.get_discount()
