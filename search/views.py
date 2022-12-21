from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
import datetime
from django.db.models import Q
import numpy as np
import json
from customers.models import *


	

def ac_search(request, query, slug):
	perusahaan = get_object_or_404(Perusahaan, slug=slug)

	if query != "NONE":		
		customer = DataCustomers.objects.filter(perusahaan=perusahaan)

		all_ac = list(reversed(DataAC.objects.filter(ac_id__icontains=query, customer__in=customer).order_by('ac_id')))
		state = 'RESULT'
	else:
		all_ac = []
		state = 'BEGIN'

	context = {
		'all_ac': all_ac,
		'state': state,
		'query': query,
		'perusahaan': perusahaan
	}
	return render(request, 'search/ac_search.html', context)

