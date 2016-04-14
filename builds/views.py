from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from builds.models import Jobs

import os
from ansi2html import Ansi2HTMLConverter


def index(request):
  all_rows = Jobs.objects.using('builds').all().order_by('-id')
  paginator = Paginator(all_rows, 25)

  page = request.GET.get('page')
  try:
     rows = paginator.page(page)
  except PageNotAnInteger:
     rows = paginator.page(1)
  except EmptyPage:
     rows = paginator.page(paginator.num_pages)

  for r in rows:
     r.log = os.path.basename(r.log)
     r.buildlog = os.path.basename(r.buildlog)

  return render(request, "builds/builds.html", {"rows" : rows })


def rawlog(request, fn):
  afn = os.path.join('/var/log/carpetbag/', os.path.basename(fn))

  with open(afn) as f:
    content = f.read()

  response = HttpResponse(content, content_type='text/plain')

  return response


def log(request, fn):
  afn = os.path.join('/var/log/carpetbag/', os.path.basename(fn))

  with open(afn) as f:
    content = f.read()

  content = content.decode('utf-8')

  conv = Ansi2HTMLConverter()

  style = mark_safe(conv.produce_headers())
  content = mark_safe(conv.convert(content, full=False))

  return render(request, "builds/logs.html", {"style" : style, "content" : content, "log" : fn})
