# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage

import sys
sys.path.append("../../")
from Chinese_segment_augment.find_new_words import find_new_words

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.shortcuts import render

from .forms import ContactForm, FilesForm, ContactFormSet

from subprocess import Popen,PIPE
import os

import config

# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, "dummy.txt")


class HomePageView(TemplateView):
    template_name = "sensi_web/home.html"


class DefaultFormsetView(FormView):
    template_name = "sensi_web/formset.html"
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = "sensi_web/form.html"
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = "sensi_web/form_by_field.html"
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = "sensi_web/form_horizontal.html"
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = "sensi_web/form_inline.html"
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = "sensi_web/form_with_files.html"
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", "vertical")
        return context

    def get_initial(self):
        return {"file4": fieldfile}


class PaginationView(TemplateView):
    template_name = "sensi_web/pagination.html"

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append("Line %s" % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get("page")
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context["lines"] = show_lines
        return context


class MiscView(TemplateView):
    template_name = "sensi_web/misc.html"


class CheckView(TemplateView):
    template_name = "sensi_web/check.html"

    def get_context_data(self, **kwargs):
        context = super(CheckView, self).get_context_data(**kwargs)
        a = [1,2,3,4]
        context['a'] = a
        return context
    
def result(request):
    if request.method=="POST":
        #if request.POST.has_key('update'):
        #    f = open('data/politic_words','w+')
        #    for word in request.post.getlist():
        #        f.write(word+'\n')
        
        if 'keywords' in request.POST:
            keywords = request.POST['keywords']
            key_file = open('../../YQ_spider/YQ_spider/keywords.txt','w')
            for word in keywords:
                key_file.write(word)
            key_file.close()
            os.system('cd ../../YQ_spider/YQ_spider ; scrapy crawl weibo ; cd ../../data/ ; python extract_content.py ; cd ../sensitive_web_sys/sensi_web')
            print('finish spider')
            return render(request,'sensi_web/search.html')
        else:
            print("fail")
            return HttpResponse("fail")
    else:
        a = [1,2,3,4]
        return render(request,'sensi_web/result.html',{'a':a})


def search(request):
    if request.method=="POST":
        root_path = "../../data/extra_data/root.pkl"
        dict_path = '../../data/extra_data/dict.txt'
        filename = '../../data/content_data/contents'
        new_dict_path = '../../data/extra_data/new_dict'
        stopword_path = '../../data/extra_data/stopword.txt'
        newwords = find_new_words(root_path,dict_path,filename,new_dict_path,stopword_path)
        return render(request,'sensi_web/result.html',{'newwords': newwords.keys()})
    
    
def submit(request):
    if request.method=="POST":
        check_box_list = request.POST.getlist('check_box_list')
        if check_box_list:
            new_dict_path = '../../data/extra_data/new_dict'
            new_dict = open(new_dict_path,'w+')
            jieba_dict = open(config.jieba_dict,'w+')
            for box in check_box_list:
                print(box)
                jieba_dict.write(box + '\n')
                new_dict.write(box + '\n')
            return HttpResponse("ok")
        else:
            print("fail")
            return HttpResponse("fail")
    else:
        a = [1,2,3,4]
        return render(request,'result.html',{'a':a})