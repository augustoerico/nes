# coding=utf-8

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, Select, PasswordInput, CheckboxSelectMultiple, CharField
from django.utils.translation import ugettext as _

from .models import Person, Institution

from patient.quiz_widget import SelectBoxCountries


class PersonRegisterForm(ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'institution']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'required': ""}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': ""}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': ""}),
            'institution': Select(attrs={'class': 'form-control'}),
        }


class UserPersonForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'groups']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'required': "", 'disabled': 'disabled',
                                         'placeholder': _('Type a new username')}),
            'password': PasswordInput(attrs={'id': 'id_new_password1', 'required': "", 'class': 'form-control',
                                             'onkeyup': "passwordForce(); if(beginCheckPassword1)checkPassExt();"}),
            'groups': CheckboxSelectMultiple(),
        }

        def clean_password(self):
            return make_password(self.cleaned_data['password'])


class UserPersonPasswordForm(UserPersonForm):
    password = CharField(required=False,
                         widget=PasswordInput(attrs={'id': 'id_new_password1', 'class': 'form-control',
                                                     'placeholder': _('Type password'), 'onkeyup': "passwordForce();"
                                                     "if(beginCheckPassword1) checkPassExt();"}))

    def clean_password(self):
        if self.cleaned_data['password']:
            return make_password(self.cleaned_data['password'])
        else:
            return self.instance.password


class InstitutionRegisterForm(ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'acronym', 'country', 'parent']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'required': "", 'autofocus': ''}),
            'acronym': TextInput(attrs={'class': 'form-control'}),
            'country': SelectBoxCountries(attrs={'data-flags': 'true'}),
            'parent': Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(InstitutionRegisterForm, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            parent_list = Institution.objects.all()
            parents_to_exclude = get_institutions_recursively(instance)
            for parent in parents_to_exclude:
                parent_list = parent_list.exclude(id=parent.id)
            self.fields['parent'].queryset = parent_list


def get_institutions_recursively(institution):
    institution_list = [institution]
    output_list = set(institution_list)
    children = Institution.objects.filter(parent=institution)
    for child in children:
        if child not in output_list:
            output_list |= get_institutions_recursively(child)
    return output_list
