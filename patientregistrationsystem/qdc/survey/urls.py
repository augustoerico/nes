from django.conf.urls import patterns, url

urlpatterns = patterns(
    'survey.views',
    url(r'^list/$', 'survey_list', name='survey_list'),
    url(r'^(?P<survey_id>\d+)/$', 'survey_view', name='survey_view'),
    url(r'^new/$', 'survey_create', name='survey_create'),
    url(r'^edit/(?P<survey_id>\d+)/$', 'survey_update', name='survey_edit'),
    url(r'^edit/(?P<survey_id>\d+)/sensitive_questions/$',
        'survey_update_sensitive_questions',
        name='survey_edit_sensitive_questions'),
)
