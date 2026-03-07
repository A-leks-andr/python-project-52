def get_client_ip(request):
    """
    Универсальная функция для получения IP-адреса пользователя.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        # Берем первый адрес в списке (реальный IP клиента)
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        # Берем адрес напрямую
        ip = request.META.get("REMOTE_ADDR")
    return ip
