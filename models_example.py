# -*- coding: utf-8 -*-

import traceback
import sys
import re

from django.db import models
from django.contrib import messages
from django.contrib.admin import ModelAdmin

from pyadmin import verbose_name_cases, verbose_name_field_cases

class TestCase(models.Model):
    name = models.CharField(max_length = 512, blank = False, verbose_name = verbose_name_field_cases(u'Имя', sort = u"имени"))

    class Meta:
        verbose_name = verbose_name_cases(u"проверка", (u"проверка", u"проверки", u"проверок"), gender = 0, change = u"проверку", delete = u"проверку", add = u"проверку")
        verbose_name_plural = verbose_name.plural  
         
    def __unicode__(self):
        return u'%s' % (self.name)   
    
    
    
class TestCaseOld(models.Model):
    name = models.CharField(max_length = 512, blank = False, verbose_name = u'Имя')

    class Meta:
        verbose_name = u"старая проверка"
        verbose_name_plural = u"старые проверки"
         
    def __unicode__(self):
        return u'%s' % (self.name)       
    
