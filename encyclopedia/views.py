from django.shortcuts import render
from django.shortcuts import redirect
from markdown2 import Markdown
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
import re
from django import forms
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "navlink1": "active"
    })

def display(request, title):
    entry_items = util.list_entries()
    entries = []
    for entry_item in entry_items:
        case_insestive = entry_item.lower()
        entries.append(case_insestive)
    if title.lower() in entries:
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "entry" : markdowner.convert(util.get_entry(title)),
            "title" : title,
            "navlink3" : "active"
        })

    else:
        message = "Sorry! Page doesn't exist"
        code = 400
        return util.errorMessage(request, code, message)

def search(request):
    value = request.GET['q']
    entry_items = util.list_entries()
    results = []
    entries = []
    for entry_item in entry_items:
        case_insestive = entry_item.lower()
        entries.append(case_insestive)

    if value.lower() in entries:
        return HttpResponseRedirect(reverse("display", kwargs={'title': value }))

    else:
        for entry in entries:
            if value.lower() in entry:
                results.append(entry)
        if len(results) == 0:
            message = "Sorry! Page doesn't exist"
            code = 400
            return util.errorMessage(request, code, message)
        else:
            return render(request, "encyclopedia/searchResult.html", {
            "results": results,
            "navlink1": "activate"
        })

def create(request):
    if request.method == "POST":
        title = request.POST['create']
        text = request.POST['text']
        entry_items = util.list_entries()
        entries = []
        for entry_item in entry_items:
            case_insestive = entry_item.lower()
            entries.append(case_insestive)
        if title.lower() in entries:
            message = "Sorry! Page already exists"
            code = 400
            return util.errorMessage(request, code, message)
        else:
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("display", kwargs={'title': title }))
    else:
        return render(request, "encyclopedia/newPage.html", {
            "navlink2": "active"
        })

def edit(request, title):
    if request.method == 'POST':
        updated_text = request.POST['edit']
        updated_text = updated_text.replace('\n', "")
        updated_text = updated_text.replace('\t', "")
        util.save_entry(title, updated_text)
        return HttpResponseRedirect(reverse("display", kwargs={'title': title }))

    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/editPage.html", {
            "content": content,
            "title": title
        })

def randomPage(request):
    entries = util.list_entries()

    random_imdx = random.randrange(len(entries))
    random_entry = entries[random_imdx]
    return HttpResponseRedirect(reverse("display", kwargs={'title': random_entry }))





         



