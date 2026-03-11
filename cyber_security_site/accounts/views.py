from django.shortcuts import render


def accounts_view(request):
    return render(request, "accounts/accounts_view.html")
