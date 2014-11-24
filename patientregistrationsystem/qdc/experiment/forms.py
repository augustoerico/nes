# coding=utf-8
from experiment.models import Experiment, QuestionnaireConfiguration, QuestionnaireResponse, SubjectOfGroup, Group
from django.forms import ModelForm, TextInput, Textarea, Select, DateInput
# from datetimewidget.widgets import DateTimeWidget


class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment

        fields = ['title', 'description']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control',
                                      'required': "",
                                      'data-error': 'Título deve ser preenchido.'}),
            'description': Textarea(attrs={'class': 'form-control',
                                           'rows': '4', 'required': "",
                                           'data-error': 'Descrição deve ser preenchida.'}),
        }


class GroupForm(ModelForm):
    class Meta:

        model = Group

        fields = ['title', 'description', 'instruction']

        widgets = {
            'title': TextInput(attrs={'class': 'form-control',
                                      'required': "",
                                      'data-error': 'Título deve ser preenchido.'}),
            'description': Textarea(attrs={'class': 'form-control',
                                           'rows': '4', 'required': "",
                                           'data-error': 'Descrição deve ser preenchida.'}),
            'instruction': Textarea(attrs={'class': 'form-control',
                                           'rows': '4', 'required': "",
                                           'data-error': 'Descrição deve ser preenchida.'}),
        }


class QuestionnaireConfigurationForm(ModelForm):
    class Meta:
        model = QuestionnaireConfiguration
        fields = ['number_of_fills', 'interval_between_fills_value', 'interval_between_fills_unit']

        widgets = {
            'number_of_fills': TextInput(attrs={'class': 'form-control', 'required': "",
                                                'data-error': 'Quantidade deve ser preenchida.'}),
            'interval_between_fills_value': TextInput(attrs={'class': 'form-control', 'required': "",
                                                             'data-error': 'Intervalo deve ser preenchido.'}),
            'interval_between_fills_unit': Select(attrs={'class': 'form-control', 'required': "",
                                                         'data-error': "Unidade deve ser preenchida"}),
        }


class QuestionnaireResponseForm(ModelForm):
    class Meta:
        model = QuestionnaireResponse
        fields = [
            'date',
        ]

        widgets = {
            'date': DateInput(attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa', 'required': "",
                                     'data-error': "Data de preenchimento deve ser preenchida"}, )
        }


class FileForm(ModelForm):
    class Meta:
        model = SubjectOfGroup
        fields = ['consent_form']
