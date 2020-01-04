from django.http import HttpResponse

from splitviewsmodels.models import TabelA, TabelB


def fitur_b_1(request):
    _ = TabelA.objects.all()
    _ = TabelB.objects.all()
    return HttpResponse('Fitur B #1')
