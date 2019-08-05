from __future__ import absolute_import, unicode_literals
from celery import task
from polls.models import Choice


@task()
def vote():
    choice = Choice.objects.get(id=7)
    choice.votes = choice.votes + 1
    choice.save()
    return 'voted!!'
