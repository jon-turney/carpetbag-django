from django.shortcuts import render
from django.http import HttpResponse

from builds.models import Jobs

import os

def index(request):
  rows = Jobs.objects.using('builds').all().order_by('-id')
  return render(request, "builds/template.html", {"rows" : rows })

def log(request, fn):
  fn = os.path.join('/var/log/carpetbag/', os.path.basename(fn))

  with open(fn) as f:
    content = f.read()

  response = HttpResponse(content, content_type='text/plain')

  return response
