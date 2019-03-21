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
                    taxon = Names.objects.get(altName__iexact=request.GET['nameSearch'])
                    idNumber = taxon.idNumber
                    return HttpResponseRedirect(reverse('results', args=(idNumber,)))
                except:
                    return HttpResponseRedirect("invalid")
            elif request.GET['idSearch']:
                try:
                    idNumber = request.GET['idSearch']
                    taxon = Tax.objects.get(idNumber = idNumber)
                    return HttpResponseRedirect(reverse('results', args=(idNumber,)))
                except:
                    return HttpResponseRedirect("invalid")
            else:
                return HttpResponseRedirect('/taxInfo/')

def invalid(request):
    template = loader.get_template('taxInfo/invalid.html')
    context = {}
    return HttpResponse(template.render(context,request))

def results(request, idNumber):
    template = loader.get_template('taxInfo/results.html')
    try:
        result = Tax.objects.get(idNumber = idNumber)
        current = result
        lineageS = []
        lineageL = []
        while current.parent != 0 and current.parent !=  1:
            current = Tax.objects.get(idNumber = current.parent)
            if current.rank != "no rank":
                lineageS.append("{}: {}".format(current.rank, current.sciName))
                lineageL.append("{}: {}".format(current.rank, current.sciName))
            else:
                lineageL.append("{}".format(current.sciName))
    except:
        result = "Unidentified"
        lineageL = []
        lineageS = []

    context = {'result': result, 'lineageL': lineageL, 'lineageS': lineageS}
    return HttpResponse(template.render(context, request))
