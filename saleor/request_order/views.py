from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from .forms import RequestOrderForm


# Create your views here.
@login_required
def request_order(request):
    if not request.user.is_industry:
        return HttpResponseRedirect(reverse('home'))
    form = RequestOrderForm(request.POST or None)
    if form.is_valid():
        request_order = form.save(commit=False)
        request_order.slug = slugify(request_order.name)
        request_order.user = request.user
        request_order.save()
        return HttpResponseRedirect(reverse('home'))
    ctx = {'form': form}
    return TemplateResponse(request, 'request_order/index.html', ctx)
