from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.template import loader
from django.contrib.auth.models import User
from django.db.models import F, Sum
from .models import *
from django.views import generic
from django.views.generic import TemplateView, DetailView, FormView
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db import transaction
from rest_framework import viewsets
from .serializers import PMuserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


class PMuserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = PMuser.objects.all()
    serializer_class = PMuserSerializer
    template_name = 'profile_list.html'



@login_required(login_url='/login/')
def dislike(request, pk):
    photo = get_object_or_404(Photo, id=pk)
    if Like.objects.filter(photo=photo, user=request.user):
        Like.objects.filter(photo=photo, user=request.user).delete()
        with transaction.atomic():
            Portfolio.objects.filter(user=request.user).update(likes=F("likes") - 1)
            album = Album.objects.filter(photo=photo.id)
            photo.likes -= 1
            photo.save()
            album.update(likes=F("likes") - 1)
            PMuser.objects.filter(album=album).update(likes=F("likes") - 1)
        data = {
            'likes': int(photo.likes),
            'url': reverse('like', args=[pk])
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


@login_required(login_url='/login/')
def like(request, pk):
    photo = get_object_or_404(Photo, id=pk)

    if not Like.objects.filter(photo=photo, user=request.user):
        with transaction.atomic():
            Portfolio.objects.filter(user=request.user).update(likes=F("likes") + 1)
            album = Album.objects.filter(photo=photo)
            Like.objects.create(photo=photo, user=request.user)
            photo.likes += 1
            photo.save()
            album.update(likes=F("likes") + 1)
            PMuser.objects.filter(id=request.user.id ).update(likes=F("likes") + 1)
        data = {
            'likes': int(photo.likes),
            'url': reverse('dislike', args=[pk])
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)



@login_required(login_url='/login/')
def deleteal(request, pk):
    album = Album.objects.get(id=pk)
    album.delete()
    return redirect('album')


@login_required(login_url='/login/')
def changeportfoliodescription(request):
    portfolio = request.user.portfolio
    portfolio.description = request.POST.get('changedescription')
    portfolio.save()
    return redirect('portfolio')

@login_required(login_url='/login/')
def changealbum(request, pk):
    album = Album.objects.get(id=pk)

    if request.method == 'POST':
        form = AlbumaddForm(request.POST, request.FILES, {'album_name': album.album_name,
                                                             'description': album.description})
        if 'save' in request.POST:
            if form.is_valid():
                album.description = form.cleaned_data['description']
                album.album_name = form.cleaned_data['album_name']
                album.save()

                image = request.FILES.getlist('photo')
                for img in image:
                    photo = Photo(image=img,
                                  photo_name=str(request.user.username) + str(len(img))
                                  )
                    photo.save()
                    album.photo.add(photo)
                    return redirect('photolist', pk)
        elif 'delete' in request.POST:
            album.delete()
            return redirect('album')
    else:

        form = AlbumaddForm({'album_name': album.album_name,
                            'description': album.description})

    return render(request, 'edit_album.html', {'form': form, 'pk': pk})


@login_required(login_url='/login/')
def addalbum(request):
    args = {}
    # instance = request.user.album if hasattr(request.user, "album") else None
    if request.method == 'POST':

        form = AlbumaddForm(request.POST, request.FILES)
        if form.is_valid():
            description = form.cleaned_data['description']
            album_name = form.cleaned_data['album_name']
            album = Album(description=description,
                          album_name=album_name)
            album.user = request.user
            album.save()
            image = request.FILES.getlist('photo')
            for img in image:
                photo = Photo(image=img,
                              photo_name=str(request.user.username) + str(len(img))
                              )

                photo.save()
                album.photo.add(photo)
            return redirect('album')
    else:

        form = AlbumaddForm()

    args['form'] = form
    return render(request, 'addalbum.html', {'form': form})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class Albumview(generic.DetailView):
    model = Album
    template_name = 'photo_in_album.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PortfolioAlbumAdd(generic.ListView):
    model = Album
    template_name = 'album_choice.html'

    def get_context_data(self, **kwargs):
        context = super(PortfolioAlbumAdd, self).get_context_data(**kwargs)
        context['album_list'] = Album.objects.filter(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        albums_id = request.POST.getlist('albumschoice')
        for id in albums_id:
            album = Album.objects.get(id=id)
            portfolio = Portfolio.objects.get(user=request.user)
            for photo in album.photo.all():
                addphoto = Photo.objects.get(image=photo.image)
                portfolio.Photo.add(addphoto)
        return redirect('portfolio')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PortfolioPhotoAdd(generic.ListView):
    model = Album
    template_name = 'photo_choice.html'

    def get_context_data(self, **kwargs):
        context = super(PortfolioPhotoAdd, self).get_context_data(**kwargs)
        context['album_list'] = Album.objects.filter(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        photo_id = request.POST.getlist('photochoice')
        portfolio = Portfolio.objects.get(user=request.user)
        if request.FILES:
            image = request.FILES.getlist('photo')
            for img in image:
                photo = Photo(image=img,
                              photo_name=str(request.user.username) + str(len(img))
                              )

                photo.save()
                portfolio.photo.add(photo)
        for id in photo_id:
            photo = Photo.objects.get(id=id)

            addphoto = Photo.objects.get(image=photo.image)
            portfolio.photo.add(addphoto)
        return redirect('portfolio', request.user.id)


def portfolio_photo_delete(request):
    photo_id = request.POST.getlist('photochoice')
    for id in photo_id:
        photo = Photo.objects.get(id=id)
        portfolio = Portfolio.objects.get(user=request.user)
        addphoto = Photo.objects.get(image=photo.image)
        portfolio.photo.remove(addphoto)

    return render(request, 'portfolio_photo_delete.html')


class AllProfiles(generic.ListView):
    model = PMuser
    template_name = 'Allprofiles.html'


class Profile(generic.DetailView):
    model = PMuser
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context['album_list'] = Album.objects.filter(user_id=self.kwargs['pk'])
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class Albums(generic.ListView):
    model = Album
    template_name = 'Albums.html'

    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(Albums, self).get_context_data(**kwargs)
        context['album_list'] = Album.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        album = Album.objects.get(id=self.kwargs['pk'])
        image = request.FILES.getlist('photo')
        for img in image:
            photo = Photo(image=img,
                          photo_name=str(request.user.username) + str(len(img))
                          )
            photo.save()
            album.photo.add(photo)
        return redirect('album')


class UserPortfolio (generic.DetailView):
    model = Portfolio
    template_name = "portfolio.html"
    def get_context_data(self, **kwargs):
        context = super(UserPortfolio, self).get_context_data(**kwargs)
        context['pmuser'] = PMuser.objects.get(id=self.kwargs['pk'])
        return context


@login_required(login_url='/login/')
def edit_portfolio(request):
    return render(request, 'edit_portfolio.html')


def logoutuser(request):
    logout(request)
    return redirect('/main/')


class Main(TemplateView):
    template_name = 'Main.html'


def registration(request):
    args = {}
    form = PMuserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = PMuser.objects.create_user(username=request.POST['username'],
                                              password=request.POST['password'],
                                              email=request.POST['email'],
                                              phone_number=request.POST['phone_number'])
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            portfolio = Portfolio(description='')
            portfolio.user = user
            portfolio.save()
            login(request, user)
            return HttpResponseRedirect('/profile/')
    else:
        form = PMuserForm()

    args['form'] = form
    return render(request, 'registration.html', {'form': form})


@login_required(login_url='/login/')
def photographregistration(request):
    args = {}
    instance = request.user.photograph if hasattr(request.user, "photograph") else None
    if request.method == 'POST':

        form = PhotographForm(request.POST, instance=instance)
        if form.is_valid():
            photograph = form.save(commit=False)
            photograph.user = request.user
            photograph.save()
    else:

        form = PhotographForm(instance=instance)

    args['form'] = form
    return render(request, 'photo_reg.html', {'form': form})


@login_required(login_url='/login/')
def modelregistration(request):
    args = {}
    instance = request.user.model if hasattr(request.user, "model") else None
    if request.method == 'POST':

        form = Modelform(request.POST, instance=instance)
        if form.is_valid():
            model = form.save(commit=False)
            model.user = request.user
            model.save()
    else:

        form = Modelform(instance=instance)

    args['form'] = form
    return render(request, 'model_reg.html', {'form': form})


@login_required(login_url='/login/')
def extendprofile(request):
    args = {}
    instance = request.user
    if request.method == 'POST':
        form = ExtendRegistrationForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()



    else:
        form = ExtendRegistrationForm(instance=instance)

    args['form'] = form
    return render(request, 'extend_profile.html', {'form': form})


def userlogin(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile', user.id)
            else:
                error = 'invalid'
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error': error})
