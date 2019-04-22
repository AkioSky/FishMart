from django import forms
from django.utils.translation import pgettext, pgettext_lazy
from .models import RequestOrder


class RequestOrderForm(forms.ModelForm):
    class Meta:
        model = RequestOrder
        fields = ('name', 'phone', 'fish_name', 'detail')
        labels = {
            'name': pgettext_lazy('Nama', 'masukan Nama'),
            'phone': pgettext_lazy('Nomer Hp/telp', 'Masukan nomer'),
            'fish_name': pgettext_lazy('Nama Ikan', 'Masukan Nama Ikan'),
            'detail': pgettext_lazy('Detail Request', 'masukan berapa kg yang ingin di beli')
        }
