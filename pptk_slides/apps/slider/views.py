from random import sample

from django.shortcuts import render

from .models import Slide, SlidePacket


def get_demo_slides():
    all_slide_packets = list(SlidePacket.objects.all().exclude(description__startswith="test"))
    # Get a random slide_packet
    slide_packet = sample(all_slide_packets, 1)[0]
    slides = Slide.objects.filter(slide_packet=slide_packet)
    return slides


def demo(request):
    context = {'slides': get_demo_slides()}
    return render(request, 'slider/demo.html', context)
