from django.shortcuts import render


def portfolio(request):
    return render(request, 'portfolio/base.html')
