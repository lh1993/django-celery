# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery_once import QueueOnce
from ScheduleTasks.tasksfile.ops_test import exec_ops_test


@shared_task(base=QueueOnce, once={'graceful': True})
def ops_test(**kwargs):
    res = exec_ops_test(**kwargs)
    return res
