from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def index(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))
