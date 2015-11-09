# -*- coding:utf-8 -*-
import sys, traceback

from django.shortcuts import Http404



class ExceptionPrinter(object):

    def process_exception(self, request, exception):
        if type(exception) != Http404:
            print "__traceback__"
            traceback.print_exc(file=sys.stdout)

