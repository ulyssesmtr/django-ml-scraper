from django.shortcuts import render
from .forms import NameForm
from . import ml_scrap


def index(request):
    return render(request, 'index.html')

def result(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data['url_search']
            df = ml_scrap.process(form)
    return render(request, 'result.html',{'df': df})
