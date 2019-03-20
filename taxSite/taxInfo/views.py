from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.urls import reverse

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
        if request.GET:
            if request.GET['nameSearch']:
                try:
                    taxon = Names.objects.get(altName=request.GET['nameSearch'])
                    idNumber = taxon.idNumber
                    return HttpResponseRedirect(reverse('results', args=(idNumber,)))
                except:
                    return HttpResponse("Invalid query")
            elif request.GET['idSearch']:
                try:
                    idNumber = request.GET['idSearch']
                    taxon = Tax.objects.get(idNumber = idNumber)
                    return HttpResponseRedirect(reverse('results', args=(idNumber,)))
                except:
                    return HttpResponse("Invalid query")
            else:
                return HttpResponseRedirect('/taxInfo/')

def results(request, idNumber):
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
        lineage = []

    context = {'result': result, 'lineage': lineage}
    return HttpResponse(template.render(context, request))
