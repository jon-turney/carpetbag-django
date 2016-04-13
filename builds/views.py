from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse

from builds.models import Jobs

import os

def index(request):
  all_rows = Jobs.objects.using('builds').all().order_by('-id')
  paginator = Paginator(all_rows, 25)

  page = request.GET.get('page')
  try:
     rows = paginator.page(page)
  except PageNotAnInteger:
     rows = paginator.page(1)
  except EmptyPAge:
     rows = paginator.page(paginator.num_pages)

  return render(request, "builds/template.html", {"rows" : rows })

def log(request, fn):
  fn = os.path.join('/var/log/carpetbag/', os.path.basename(fn))

  with open(fn) as f:
    content = f.read()

  response = HttpResponse(content, content_type='text/plain')

  return response
