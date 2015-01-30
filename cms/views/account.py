from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.query import Q

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser

NOT_ADMIN_CHOICES = ((3, 'Company'),)

@login_required
def list(request):
    # ログインしているユーザー所有のアカウントをすべて取得する。
    if request.user.acc_type_id == 1:
        acc_list = UserProfile.objects.filter(
            Q(identifier=request.user.identifier) |
            Q(parent_admin_id__exact=request.user.user_id)
        )
    elif request.user.acc_type_id == 2:
        acc_list = UserProfile.objects.filter(
            Q(identifier=request.user.identifier) |
            Q(parent_agency_id__exact=request.user.user_id)
        )
    elif request.user.acc_type_id == 3:
        acc_list = UserProfile.objects.filter(identifier=request.user.identifier)

    return render(request, 'account_list.html', {'acc_list': acc_list})

@login_required
def new(request):
    if request.user.acc_type_id != 3:
        if request.POST:
            form = UserProfileForm(request.POST)
            if form.is_valid():
                acc_type_id = form.cleaned_data['acc_type_id']
                enterprise = form.cleaned_data['enterprise']
                person = form.cleaned_data['person']
                address = form.cleaned_data['address']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']

                if request.user.acc_type_id == 1:
                    parent_admin_id = request.user.parent_admin_id
                    parent_agency_id = None
                elif request.user.acc_type_id == 2:
                    parent_admin_id = request.user.parent_admin_id
                    parent_agency_id = request.user.user_id

                new_account = UserProfile.objects.create_user(
                                acc_type_id=acc_type_id,
                                parent_admin_id=parent_admin_id,
                                parent_agency_id=parent_agency_id,
                                enterprise=enterprise, person=person,
                                address=address, email=email,
                                phone_number=phone_number,
                                password=password)
                return redirect('/account/list')
            else:
                return render(request, 'account_new.html', {'form': form})
        else:
            form = UserProfileForm()
            if request.user.acc_type_id != 1:
                form.fields.get('acc_type_id').choices = NOT_ADMIN_CHOICES
        return render(request, 'account_new.html', {'form': form})
    else:
        # Companyは新規作成はできない。
        return redirect('/account/list')

@login_required
def edit(request, acctypeid, userid):
    if request.POST:
        i = UserProfile.objects.get(acc_type_id=acctypeid,
                                    user_id=userid)
        form = UserProfileForm(request.POST, instance=i)
        if form.is_valid():
            acc_type_id = form.cleaned_data['acc_type_id']
            enterprise = form.cleaned_data['enterprise']
            person = form.cleaned_data['person']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            #password = form.cleaned_data['password']

            if request.user.acc_type_id == 1:
                parent_admin_id = request.user.parent_admin_id
                parent_agency_id = None
            elif request.user.acc_type_id == 2:
                parent_admin_id = request.user.parent_admin_id
                parent_agency_id = request.user.user_id
            elif request.user.acc_type_id == 3:
                parent_admin_id = request.user.parent_admin_id
                parent_agency_id = request.user.user_id

            #edit_account = UserProfile(id=id,
            #                          acc_type_id=acc_type_id,
            #                          user_id=userid,
            #                          parent_admin_id=parent_admin_id,
            #                          parent_agency_id=parent_agency_id,
            #                          enterprise=enterprise, person=person,
            #                          address=address, email=email,
            #                          phone_number=phone_number,
            #)
            #edit_account.save()
            form.save()
            return redirect('/account/list')
        else:
            return render(request, 'account_edit.html',
                {'form': form, 'acctypeid': acctypeid, 'userid': userid})
    else:
        form = UserProfileForm(
            instance=UserProfile.objects.get(acc_type_id=acctypeid,
                                             user_id=userid)
        )
        if request.user.acc_type_id != 1:
            form.fields.get('acc_type_id').choices = NOT_ADMIN_CHOICES
    return render(request, 'account_edit.html',
                {'form': form, 'acctypeid': acctypeid, 'userid': userid})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('acc_type_id', 'enterprise', 'person', 'address',
                  'email','phone_number', 'password',)

