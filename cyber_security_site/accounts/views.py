from django.shortcuts import render


# Добавить
# Формы:
#
# Login form (обычный + “лаб” с антипримером rate limiting/lockout).
#
# Change password form (проверка current password, сложность).
#
# Profile edit form (показать mass assignment и безопасный whitelist полей).
def accounts_view(request):
    return render(request, "accounts/accounts_view.html")
