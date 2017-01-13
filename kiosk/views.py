from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from kiosk.forms import SearchForm, ConfigurationForm, DemographicsForm

@login_required
def home(request):
    searchForm = SearchForm()
    kioskMode = request.session.get('kioskMode', False)
    contextDict = {'form': searchForm, 'kioskMode': kioskMode}
    return render(request, 'kiosk-index.html', contextDict)
