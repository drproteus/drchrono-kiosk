from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from kiosk.forms import SearchForm, ConfigurationForm, CheckinForm, DisableForm

@login_required
def home(request):
    searchForm = SearchForm()
    disableForm = DisableForm()
    kioskMode = request.session.get('kioskMode', False)
    contextDict = {'form': searchForm, 'kioskMode': kioskMode, 'disable': disableForm}
    return render(request, 'kiosk-index.html', contextDict)
