from django.shortcuts import render


def logs_analysis_view(request):
    return render(request, "logs_analysis/logs_analysis.html")
