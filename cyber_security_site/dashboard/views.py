from django.shortcuts import render

from .models import UserProgress


def dashboard_view(request):
    # Django делает один SQL запрос:
    # SELECT *
    # FROM userprogress
    # JOIN user
    # ON userprogress.user_id = user.id
    users = UserProgress.objects.select_related("user")
    return render(
        request,
        "dashboard/dashboard_view.html",
        {
            "users": users,
        },
    )
