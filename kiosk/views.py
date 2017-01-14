from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from kiosk.forms import SearchForm, ConfigurationForm, CheckinForm, DisableForm
from kiosk.models import *
from util.utils import *

@login_required
def home(request):
    searchForm = SearchForm()
    disableForm = DisableForm()
    kioskMode = request.session.get('kioskMode', False)
    config = Configuration.get_config_for_user(request.user)
    contextDict = {'form': searchForm, 'kioskMode': kioskMode,
            'disable': disableForm, 'config': config}
    return render(request, 'kiosk-index.html', contextDict)

@login_required
def search(request):
    if request.method == 'POST':
        searchForm = SearchForm(request.POST)
        if searchForm.is_valid():
            results = search_appointments(request,
                    first_name=searchForm.cleaned_data['first_name'],
                    last_name=searchForm.cleaned_data['last_name'])
    return redirect(reverse('kiosk:home'))
