from django.shortcuts import render
from .models import SecurityTool

def list_security_tools(request):
    security_tools = SecurityTool.objects.all()
    return render(request, "security_tools/security_tools.html", {
        "security_tools": security_tools,
    })
