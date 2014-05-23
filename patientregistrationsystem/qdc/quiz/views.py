# coding=utf-8
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import RequestContext, loader
from django import forms
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from datetime import date

from models import Patient, SocialDemographicData, FleshToneOption, MaritalStatusOption, SchoolingOption, PaymentOption, ReligionOption, GenderOption
from forms import PatientForm, SocialDemographicDataForm, SocialHistoryDataForm


@login_required
def pg_home(request):
    flesh_tone_options = FleshToneOption.objects.all()
    marital_status_options = MaritalStatusOption.objects.all()
    gender_options = GenderOption.objects.all()
    schooling_options = SchoolingOption.objects.all()
    payment_options = PaymentOption.objects.all()
    religion_options = ReligionOption.objects.all()
    new_patient = None
    new_personal_data = None
    new_social_demographic_data = None
    new_social_history_data = None
    if request.method == "POST":
        patient_form = PatientForm(request.POST)
        social_demographic_form = SocialDemographicDataForm(request.POST)
        social_history_form = SocialHistoryDataForm(request.POST)
        if patient_form.is_valid():
            new_patient = patient_form.save(commit=False)
            new_patient.gender_opt = GenderOption.objects.filter(gender_txt=request.POST['gender_opt'])[0]
            new_patient.marital_status_opt = MaritalStatusOption.objects.filter(marital_status_txt=request.POST['marital_status_opt'])[0]
            new_patient.save()
            if social_demographic_form.is_valid():
                new_social_demographic_data = social_demographic_form.save(commit=False)
                new_social_demographic_data.id_patient = new_patient
                new_social_demographic_data.religion_opt = ReligionOption.objects.filter(religion_txt=request.POST['religion_opt'])[0]
                new_social_demographic_data.payment_opt = PaymentOption.objects.filter(payment_txt=request.POST['payment_opt'])[0]
                new_social_demographic_data.flesh_tone_opt = FleshToneOption.objects.filter(flesh_tone_txt=request.POST['flesh_tone_opt'])[0]
                new_social_demographic_data.schooling_opt = SchoolingOption.objects.filter(schooling_txt=request.POST['schooling_opt'])[0]
                new_social_demographic_data.save()
                new_social_demographic_data = None
            if social_history_form.is_valid() and False:
                new_social_history_data = social_history_form.save(commit=False)
                new_social_history_data.id_patient = new_patient
                new_social_history_data.save()
                new_social_history_data = None
    context = {'gender_options': gender_options, 'new_social_history_data': new_social_history_data,
               'new_social_demographic_data': new_social_demographic_data, 'flesh_tone_options': flesh_tone_options,
               'marital_status_options': marital_status_options, 'schooling_options': schooling_options,
               'payment_options': payment_options, 'religion_options': religion_options, 'new_patient': new_patient,
               'new_personal_data': new_personal_data}
    return render(request, 'quiz/pg_home.html', context)


def patients(request):
    language = 'en-us'
    session_language = 'en-us'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']

    if 'lang' in request.session:
        session_language = request.session['lang']

    args = {}
    args.update(csrf(request))

    args['patients'] = Patient.objects.all()
    args['language'] = language
    args['session_language'] = session_language

    return render_to_response('pg_home.html', args)


def patient(request, patient_id):
    flesh_tone_options = FleshToneOption.objects.all()
    marital_status_options = MaritalStatusOption.objects.all()
    gender_options = GenderOption.objects.all()
    schooling_options = SchoolingOption.objects.all()
    payment_options = PaymentOption.objects.all()
    religion_options = ReligionOption.objects.all()

    p = Patient.objects.get(nr_record=patient_id)
    if p.dt_birth_txt:
        dt_birth = str(p.dt_birth_txt.day) + "/" + str(p.dt_birth_txt.month) + "/" + str(p.dt_birth_txt.year)
    else:
        dt_birth = ""
    marital_status_searched = p.marital_status_opt_id
    gender_searched = p.gender_opt_id

    try:
        p_social_demo = SocialDemographicData.objects.get(id_patient_id=patient_id)
    except SocialDemographicData.DoesNotExist:
        p_social_demo = ""
    if p_social_demo:
        occupation_searched = p_social_demo.occupation_txt
        profession_searched = p_social_demo.profession_txt
        religion_searched = p_social_demo.religion_opt_id
        benefit_gov_searched = p_social_demo.benefit_gov_bool
        payment_opt_searched = p_social_demo.payment_opt_id
        flesh_tone_opt_searched = p_social_demo.flesh_tone_opt_id
        schooling_opt_searched = p_social_demo.schooling_opt_id
        tv_opt_searched = p_social_demo.tv_opt
        dvd_opt_searched = p_social_demo.dvd_opt
        radio_opt_searched = p_social_demo.radio_opt
        bath_opt_searched = p_social_demo.bath_opt
        automobile_opt_searched = p_social_demo.automobile_opt
        wash_machine_opt_searched = p_social_demo.wash_machine_opt
        refrigerator_opt_searched = p_social_demo.refrigerator_opt
        freezer_opt_searched = p_social_demo.freezer_opt
        house_maid_opt_searched = p_social_demo.house_maid_opt
        social_class_opt_searched = p_social_demo.social_class_opt


    context = {'name': p.name_txt, 'cpf': p.cpf_id, 'rg': p.rg_id, 'place_of_birth': p.natural_of_txt,
               'citizenship': p.citizenship_txt, 'street': p.street_txt, 'zipcode': p.zipcode_number,
               'country': p.country_txt, 'state': p.state_txt, 'city': p.city_txt, 'phone': p.phone_number,
               'cellphone': p.cellphone_number, 'email': p.email_txt, 'medical_record': p.medical_record_number,
               'dt_birth': dt_birth,
               'flesh_tone_options': flesh_tone_options, 'marital_status_options': marital_status_options,
               'gender_options': gender_options, 'schooling_options': schooling_options,
               'payment_options': payment_options, 'religion_options': religion_options,
               'gender_searched': gender_searched, 'marital_status_searched': marital_status_searched,
               'religion_searched': religion_searched, 'profession_searched': profession_searched,
               'occupation_searched': occupation_searched, 'benefit_gov_searched': benefit_gov_searched,
               'payment_opt_searched': payment_opt_searched, 'flesh_tone_opt_searched': flesh_tone_opt_searched,
               'schooling_opt_searched': schooling_opt_searched, 'tv_opt_searched': tv_opt_searched,
               'dvd_opt_searched': dvd_opt_searched, 'radio_opt_searched': radio_opt_searched,
               'bath_opt_searched': bath_opt_searched, 'automobile_opt_searched': automobile_opt_searched,
               'wash_machine_opt_searched': wash_machine_opt_searched, 'refrigerator_opt_searched': refrigerator_opt_searched,
               'freezer_opt_searched': freezer_opt_searched, 'house_maid_opt_searched': house_maid_opt_searched,
               'social_class_opt_searched': social_class_opt_searched,
               }
    return render(request, 'quiz/pg_home.html', context)


def search_patients(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
        if search_text:
            patients = Patient.objects.filter(name_txt__icontains=search_text)
        else:
            #patients = False
            patients = ''
    else:
        search_text = ''

    #patients = Patient.objects.filter(name_txt__contains=search_text)

    return render_to_response('quiz/ajax_search.html', {'patients': patients})
