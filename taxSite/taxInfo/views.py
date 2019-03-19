from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from random import randint
from django.views import generic

from .models import Tax, Names
from .forms import SearchForm

# Create your views here.
def index(request):
    template = loader.get_template('taxInfo/index.html')
    form = SearchForm(request.GET)
    context = {'form': form}
    return HttpResponse(template.render(context,request))

def getId(request):
    if request.method=='GET':
        form = SearchForm(request.GET)
        if form.isvalid():
            if form.cleaned_data['nameSearch']:
                taxon is Names.objects.get(altName = form.cleaned_data['nameSearch'])
                idNumber = taxon.idNumber
            else:
                idNumber = form.cleaned_data['idSearch']
            return HttpResponseRedirect(reverse('taxInfo:results', args = idNumber))
    return render(request, 'index.html', {'form' : form})

def results(request):
    if request.method=='GET':
        form = SearchForm(request.GET)
        if form.isvalid():
            if form.cleaned_data['nameSearch']:
                taxon is Names.objects.get(altName = form.cleaned_data['nameSearch'])
                idNumber = taxon.idNumber
            elif form.cleaned_data['idSearch']:
                idNumber = form.cleaned_data['idSearch']
            else:
                HttpResponseRedirect('/index/')

    template = loader.get_template('taxInfo/results.html')
    try:
        result = Tax.objects.get(idNumber = idNumber)
        current = result
        lineage = []
        while current.parent != 0 and current.parent !=  1:
            current = Tax.objects.get(idNumber = current.parent)
            if current.rank != "no rank":
                lineage.append("{}: {}".format(current.rank, current.sciName))
            else:
                lineage.append("{}".format(current.sciName))
    except:
        result = "Unidentified"

    context = {'result': result, 'lineage': lineage}
    return HttpResponse(template.render(context, request))

class ResultsView(generic.DetailView):
    model = Tax
