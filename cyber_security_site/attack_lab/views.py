from django.shortcuts import render


def attack_lab_view(request):
    return render(request, "attack_lab/attack_lab_view.html")
