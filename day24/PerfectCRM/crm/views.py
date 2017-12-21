from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm.permissions.permission import check_permission_decorate


# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")


@check_permission_decorate
@login_required
def sales_index(request):
    return render(request, "sales/index.html")
