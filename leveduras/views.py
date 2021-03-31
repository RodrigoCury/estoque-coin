from datetime import date, timedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from .forms import FermentativeProfileCreateForm, TodoForm, YeastCreateForm, BrandCreateForm
from .helpers import *
from .models import ActivityLog, Yeast, Brand, FermentativeProfile, Todo


class AuthenticatedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated


class HomeView(AuthenticatedMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        yeasts = Yeast.objects.all().order_by(
            'next_reinnoculation_limit_date')
        context['leveduras'] = yeasts[:4]
        context['activities'] = ActivityLog.objects.all()
        context['brands'] = model_shares(Brand)
        context['profiles'] = model_shares(FermentativeProfile)
        context['todo_form'] = TodoForm
        context['todo_list'] = self.request.user.todo_set.all()
        return context


def todoDelete(request, id):
    obj = Todo.objects.get(pk=id)
    obj.delete()
    return HttpResponse("OK")


@require_POST
def todoAdd(request):
    form = TodoForm(request.POST)

    if form.is_valid():
        obj = Todo(activity=request.POST['activity'], user=request.user)
        obj.save()
    return JsonResponse({'id': obj.id})


def todoComplete(request, id):
    obj = Todo.objects.get(pk=id)
    if obj.complete == True:
        obj.complete = False
    else:
        obj.complete = True
    obj.save()
    return HttpResponse("OK")


class SearchView(AuthenticatedMixin, TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        query = request.GET.get("search")

        if query is not None:
            query = (Q(name__icontains=query))
            context['results'] = True
            context['yeast'] = Yeast.objects.filter(query).order_by('name')
            context['brand'] = Brand.objects.filter(query).order_by('name')
            context['profile'] = FermentativeProfile.objects.filter(query).order_by(
                'name')
            return context
        context['results'] = None
        return context


class YeastListView(AuthenticatedMixin, ListView):
    model = Yeast
    template_name = 'bank/yeasts/yeast_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        obj = yeast_order_by(self.request, context['object_list'])
        paginator = Paginator(obj, 8)
        page = self.request.GET.get('page')

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['object_list'] = objects
        context['page_obj'] = paginator.get_page(page)
        return context


class YeastDetailView(AuthenticatedMixin, DetailView):
    model = Yeast
    template_name = 'bank/yeasts/yeast_detail.html'


class YeastCreateView(AuthenticatedMixin,  CreateView):
    model = Yeast
    form_class = YeastCreateForm
    template_name = 'bank/yeasts/yeast_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.name = obj.name.title().strip()
        obj.user = self.request.user
        obj.slug = slugify(obj.name)
        obj.next_reinnoculation_limit_date = obj.last_reinnoculation + \
            timedelta(days=180)
        obj.save()
        creation_log(Yeast, obj, self.request.user)
        return super().form_valid(form)


@login_required(login_url='/login')
def reinnoculate(request, slug):
    try:
        obj = Yeast.objects.get(slug=slug)
        obj.reinnoculation_count += 1
        obj.last_reinnoculation = date.today()
        obj.next_reinnoculation_limit_date = date.today() + \
            timedelta(weeks=24)
        obj.save()
    except Exception:
        raise Http404("Levedura não existe")
    reinnoculation_log(obj, request.user)
    return HttpResponseRedirect(reverse('yeast_detail', args=[slug]))


@login_required(login_url='/login')
def delete_yeast_from_bank(request, slug):
    try:
        obj = Yeast.objects.get(slug=slug)
        obj.delete()
    except Exception:
        raise Http404("Levedura não encontrada")
    deletion_log(Yeast, obj, request.user)
    return HttpResponseRedirect(reverse('home'))

# Brand Views


class BrandListView(AuthenticatedMixin, ListView):
    model = Brand
    paginate_by = 10
    template_name = 'bank/brand/brand_list.html'


class BrandCreateView(AuthenticatedMixin, CreateView):
    model = Brand
    form_class = BrandCreateForm
    template_name = 'bank/brand/brand_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.name = obj.name.title().strip()
        obj.slug = slugify(obj.name)
        obj.save()
        creation_log(Brand, obj, self.request.user)
        return super().form_valid(form)


class BrandDetailView(AuthenticatedMixin, DetailView):
    model = Brand
    template_name = 'bank/brand/brand_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        obj = yeast_order_by(self.request, context['object'].yeast_set)
        paginator = Paginator(obj, 8)
        page = self.request.GET.get('page')

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['leveduras'] = objects
        context['page_obj'] = paginator.get_page(page)
        return context


@login_required(login_url='/login')
def delete_brand_from_bank(request, slug):
    try:
        obj = Brand.objects.get(slug=slug)
        obj.delete()
    except Exception as err:
        raise Http404("Marca não encontrada")
    deletion_log(Brand, obj, request.user)
    return HttpResponseRedirect(reverse('brand_list'))

# Fermentative Profile


class FermentativeProfileListView(AuthenticatedMixin, ListView):
    model = FermentativeProfile
    paginate_by = 10
    template_name = 'bank/profile/profile_list.html'


class FermentativeProfileCreateView(AuthenticatedMixin, CreateView):
    model = FermentativeProfile
    form_class = FermentativeProfileCreateForm
    template_name = 'bank/profile/profile_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.name = obj.name.title().strip()
        obj.slug = slugify(obj.name)
        obj.save()
        creation_log(FermentativeProfile, obj, self.request.user)
        return super().form_valid(form)


class FermentativeProfileDetailView(AuthenticatedMixin, DetailView):
    model = FermentativeProfile
    template_name = 'bank/profile/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        obj = yeast_order_by(self.request, context['object'].yeast_set)
        paginator = Paginator(obj, 8)
        page = self.request.GET.get('page')

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context['leveduras'] = objects
        context['page_obj'] = paginator.get_page(page)
        return context


@login_required(login_url='/login')
def delete_profile_from_bank(request, slug):
    try:
        obj = FermentativeProfile.objects.get(slug=slug)
        obj.delete()
    except Exception:
        raise Http404("Perfil não encontrada")
    deletion_log(FermentativeProfile, obj, request.user)
    return HttpResponseRedirect(reverse('profile_list'))
