from django.shortcuts import render
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
