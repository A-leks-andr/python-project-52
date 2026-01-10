from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

class UsersView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "users.html")
