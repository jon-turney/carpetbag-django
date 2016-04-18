from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
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
     if r.log:
       r.log = os.path.basename(r.log)
     if r.buildlog:
       r.buildlog = os.path.basename(r.buildlog)

  return render(request, "builds/builds.html", {"rows" : rows })


def detail(request, id):
  job = get_object_or_404(Jobs.objects.using('builds'), pk=id)

  if job.end_timestamp:
    job.duration = job.end_timestamp - job.start_timestamp

  # jobs which have completed processing and did not get successfully built are retryable
  if (job.status in ['processed', 'exception', 'cancelled']) and (job.built != True):
    job.retry_disable = ""
  else:
    job.retry_disable = "disabled"

  # jobs which are pending (but not in-progress) are cancellable
  if job.status in ['pending']:
    job.cancel_disable = ""
  else:
    job.cancel_disable = "disabled"

  return render(request, "builds/detail.html", {"job" : job })


def action(request, id):
  job = get_object_or_404(Jobs.objects.using('builds'), pk=id)

  print(request.POST)

  if 'retry' in request.POST:
    # reset status to 'pending' and clear build data
    job.status = 'pending'
    job.log = ''
    job.buildlog = ''
    job.built = None
    job.verify = None
    job.start_timestamp = None
    job.end_timestamp = None
    job.save()
  elif 'cancel' in request.POST:
    job.status = 'cancelled'
    job.save()

  return HttpResponseRedirect('/builds')

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
