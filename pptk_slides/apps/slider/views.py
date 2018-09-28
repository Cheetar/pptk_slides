from django.shortcuts import render


def get_demo_slides():
    """ Returns array of demo slides.
    """
    return ['slide1', 'slide2']


def demo(request):
    context = {'slides': get_demo_slides()}
    return render(request, 'slider/demo.html', context)
