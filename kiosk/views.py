from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from kiosk.forms import SearchForm, ConfigurationForm, CheckinForm, DisableForm
from kiosk.models import *

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
        pass
    return redirect(reverse('kiosk:home'))
