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

class SearchQuery(generic.DetailView):
    def getId(request, searchQuery):
        pass

def getId(request):
    if request.method=='GET':
        if request.GET:
            if request.GET['nameSearch']:
                taxon = Names.objects.get(altName=request.GET['nameSearch'])
                idNumber = taxon.idNumber
            elif request.GET['idSearch']:
                idNumber = request.GET['idSearch']
            return HttpResponseRedirect(reverse('results', args=(idNumber,)))
        else:
            return HttpResponseRedirect('')


    '''
    if request.method=='GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            return form.cleaned_data
            if form.cleaned_data['nameSearch']:
                taxon = Names.objects.get(altName = form.cleaned_data['nameSearch'])
                idNumber = taxon.idNumber
            elif form.cleaned_data['idSearch']:
                idNumber = form.cleaned_data['idSearch']
            else:
                return render(request, 'index.html', {'form' : form})
            return render()
            #reverse('taxInfo:results', args = idNumber))
    '''


def results(request, idNumber):
    #if request.method=='GET':
    #    form = SearchForm(request.GET)
    #    return HttpResponseRedirect('')
    #    if form.isvalid():
    #        if form.cleaned_data['nameSearch']:
    #            taxon = Names.objects.get(altName = form.cleaned_data['nameSearch'])
    #            idNumber = taxon.idNumber
    #        elif form.cleaned_data['idSearch']:
    #            idNumber = form.cleaned_data['idSearch']
    #        else:
    #            return HttpResponseRedirect('/index/')

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

#class ResultsView(generic.DetailView):
#    model = Tax
