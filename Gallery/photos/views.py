from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .forms import RegForm, AuthForm, UploadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Images


class IndexView(generic.ListView):
    template_name = 'index.html'
    model = Images


class RegisterView(generic.FormView):
    form_class = RegForm
    template_name = 'register.html'


class AccountView(generic.ListView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = ''
    paginate_by = 50
    template_name = 'account.html'
    model = Images

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        context['upload_form'] = UploadForm
        context['object_list'] = Images.objects.filter(user_id=self.kwargs['id'])
        context['current_page_id'] = int(self.kwargs['id'])
        context['current_user_id'] = self.request.session['id']
        return context


def register(request):
    if(request.POST['password'] == request.POST['conf_password']):
        new_user = User(username=request.POST['username'])
        new_user.set_password(request.POST['password'])
        new_user.save()
        print(new_user.id)
        return HttpResponseRedirect(reverse('account', args=(new_user.id,)))
    else:
        return render(request, 'register.html', {'error_message': 'Passwords should be the same!'})


def upload_image(request, id):
    new_image = Images(image=request.FILES['image'], user_id=request.session['id'])
    new_image.save()
    return HttpResponseRedirect(reverse('account', args=(request.session['id'],)))


class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = AuthForm


def logging_in(request):
    try:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            request.session['id'] = user.id
            return HttpResponseRedirect(reverse_lazy('account', args=(user.id,)))
        else:
            return render(request, 'login.html', {'error_message': 'Wrong username or password!'})
    except:
        return render(request, 'login.html', {'error_message': 'Wrong username or password!'})


def logging_out(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))