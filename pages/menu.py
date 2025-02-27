from django.shortcuts import render
from django.views import View

class MenuPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'menu.html')
