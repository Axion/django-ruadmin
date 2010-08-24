# -*- coding: utf-8 -*-

import traceback
import sys
import re

from django.db import models
from django.contrib import messages
from django.contrib.admin import ModelAdmin

class verbose_name_field_cases:
    """
    Extended verbose_name for field, capable of using different case for sorting in admin
    """
    def __init__(self, verbose_name, **kwargs):
        self._verbose_name = verbose_name
	self._sort_name = kwargs.get("sort", verbose_name)

    @property
    def sort(self):
        return self._sort_name
        
    def __str__(self):
        return self._verbose_name

    def __unicode__(self):
        return self._verbose_name
        
class verbose_name_cases:
    def __init__(self, verbose_name, plural_forms, **kwargs):
        self._verbose_name = verbose_name
        self._change_name = kwargs.get("change", verbose_name)
        self._add_name = kwargs.get("add", verbose_name)
        self._delete_name = kwargs.get("delete", verbose_name)
        self._plural = plural_forms
        self._gender = kwargs.get("gender", 1)

        if self._gender == 0:
            """
            Monkey-patch Django's ModelAdmin function with our custom message handler
            """
            def msg(self, request, message):
                msg_re = re.compile(u"(.*?) \"(.*?)\" был успешно добавлен")

                if msg_re.match(message):
                    grp = msg_re.search(message).groups(1)
 
                    message = message.replace(u"был",u"была").replace(u"добавлен",u"добавлена")
                    message = message.replace(u"один "+grp[0],u"одну "+self.VerboseNameCaseReplace[grp[0]])

		message = message.replace(u"Ниже вы можете снова его отредактировать", u"Ниже вы можете снова её отредактировать")
		
		msg_addmore_re = re.compile(u"(.*?)Ниже вы можете добавить еще один (.*?)\.")
		
		if msg_addmore_re.match(message):
                    grp = msg_addmore_re.search(message).groups(1)
		    message = message.replace(u"Ниже вы можете добавить еще один %s." % grp[1], u"Ниже вы можете добавить еще одну %s." % self.VerboseNameCaseReplace[grp[1]])
		
		msg_save_re = re.compile(u"(.*?) \"(.*?)\" был успешно изменён")
		if msg_save_re.match(message):
		    message = message.replace(u"был",u"была").replace(u"изменён",u"изменена")

                messages.info(request, message)
            ModelAdmin.message_user = msg
            
        if not hasattr(ModelAdmin, "VerboseNameCaseReplace"):
            ModelAdmin.VerboseNameCaseReplace = {}
            
        ModelAdmin.VerboseNameCaseReplace[self._verbose_name] = self._change_name

    @property
    def plural(self):
        return self._plural[1]

    @property
    def plural_forms_amount(self):
        return [self._plural[1],self._plural[2]]

    @property
    def plural_forms(self):
        return unicode(",".join(self._plural))

    @property
    def add(self):
        return self._add_name    

    def __str__(self):
        return self._verbose_name

    def __unicode__(self):
        """
        Inspect stack 3 levels up, this is potentialy very bad thing as any change in i18n calls will break this, so
        TODO: inspect whole stack
        """        
        if "Select %s to change" in traceback.extract_stack()[-3][3]: # Edit entries
            return self._change_name
        elif "Add %s" in traceback.extract_stack()[-3][3]: # Add new entry
            return self._add_name
        elif "Change %s" in traceback.extract_stack()[-3][3]: # Edit entry
            return self._change_name
        elif "delete_view" == traceback.extract_stack()[-3][2]: # Confirm deletion
            return self._delete_name
        else:        
            return self._verbose_name   
