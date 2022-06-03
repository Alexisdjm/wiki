from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util

import random

import markdown2
from markdown2 import Markdown, markdown

def index(request):
    return render(request, "encyclopediaTP/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    entries = util.list_entries()
    if str(entry).lower() in str(entries).lower():
        content = util.get_entry(entry)
        HTML_format = markdown2.markdown(content)
        return render(request, "encyclopediaTP/entrypage.html", {
            "title":entry,
            "content":HTML_format
        })
    else:
        return HttpResponseRedirect("/error")

def error(request):
    return render(request, "encyclopediaTP/ErrorPage.html")

def search(request):
    if request.method == "GET":
        query = request.GET.get("q")
        if query.lower() == "" or query.lower() is None:
            return HttpResponseRedirect(reverse("index"))
    else:
         return HttpResponseRedirect(reverse("index"))
    if util.get_entry(query) is not None:
        return redirect(wiki, query)

    entries = util.list_entries()
    resultado = []
    for e in entries:
        if str(query).lower() in e.lower() or e.lower() in str(query).lower():
            resultado.append(e)

    return render(request, "encyclopediaTP/search.html", {
        "query": query,
        "resultado": resultado,
        "encontrado": len(resultado) > 0
    })



def newpage(request):
    return render(request, "encyclopediaTP/newpage.html")

def save(request):
    if request.method == "POST":
        newtitle = request.POST['input']
        newcontent = request.POST['textarea']
        mybool = util.get_entry(newtitle)

        if mybool is not None:
            return HttpResponse("Ya existe")
        else:
            guardar = open(f'C:/Users/Alexis Jimenez/Desktop/Proyectos django/wiki project/Entries//{newtitle}.md', 'w+')
            guardar.write(newcontent)
            guardar.close()
            return render(request, "encyclopediaTP/index.html", {
                "entries": util.list_entries()
            })

def random_page(request):
    entries=util.list_entries()
    random_entry = random.choice(entries)
    return redirect(wiki, random_entry)

def edit(request, entry):
    content = util.get_entry(entry)
    if request.method=="POST":
        new_content = request.POST.get("content")
        util.save_entry(title=entry, content=new_content)
        return redirect(wiki, entry)

    if content:
        return render(request, "encyclopediaTP/PageEdit.html",{
        "title": entry,
        "content" : util.get_entry(entry)
    })
    else:
        return HttpResponseRedirect(reverse('index'))



