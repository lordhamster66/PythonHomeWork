from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")


@login_required
def sales_index(request):
    return render(request, "sales/index.html")

