
from django.http import *
from appid_getter.models import CurAppid


def genReleaseAppid(**kwargs):
    return HttpResponse(CurAppid.objects.genAppid())
