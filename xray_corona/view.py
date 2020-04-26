from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template


def terms_and_condition(request):
    return render(request, "terms_and_cond.html")


def privacy_policy(request):
    return render(request, "Privacy_Policy.html")
