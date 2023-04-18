from django.shortcuts import render
from AppCoder.models import Platillo, Profile, Mensaje
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def index(request):
    return render(request, "AppCoder/index.html")


class PlatilloList(ListView):
    model = Platillo
    context_object_name = "platillos"

class PlatilloMineList(PlatilloList):

    def get_queryset(self):
        return Platillo.objects.filter(propietario=self.request.user.id).all()


class PlatilloUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Platillo
    success_url = reverse_lazy("platillo-list")
    fields = '__all__'

    def test_func(self):
        user_id = self.request.user.id
        Platillo_id = self.kwargs.get("pk")
        return Platillo.objects.filter(propietario=user_id, id=Platillo_id).exists()


class PlatilloDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Platillo
    context_object_name = "platillo"
    success_url = reverse_lazy("platillo-list")

    def test_func(self):
        user_id = self.request.user.id
        Platillo_id = self.kwargs.get("pk")
        return Platillo.objects.filter(propietario=user_id, id=Platillo_id).exists()


class PlatilloCreate(LoginRequiredMixin, CreateView):
    model = Platillo
    success_url = reverse_lazy("platillo-list")
    fields = '__all__'



class PlatilloSearch(ListView):
    model = Platillo
    context_object_name = "platillos"

    def get_queryset(self):
        criterio = self.request.GET.get("criterio")
        result = Platillo.objects.filter(nombre=criterio).all()
        return result

class Login(LoginView):
    next_page = reverse_lazy("platillo-list")


class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('platillo-list')


class Logout(LogoutView):
    template_name = "registration/logout.html"

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    success_url = reverse_lazy("platillo-list")
    fields = ['avatar',]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = Profile
    success_url = reverse_lazy("platillo-list")
    fields = ['avatar',]

    def test_func(self):
        return Profile.objects.filter(user=self.request.user).exists()

#------------------------------------------------------------
class MensajeCreate(CreateView):
    model = Mensaje
    success_url = reverse_lazy('mensaje-create')
    fields = '__all__'


class MensajeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mensaje
    context_object_name = "mensaje"
    success_url = reverse_lazy("mensaje-list")

    def test_func(self):
        return Mensaje.objects.filter(destinatario=self.request.user).exists()
    

class MensajeList(LoginRequiredMixin, ListView):
    model = Mensaje
    context_object_name = "mensajes"

    def get_queryset(self):
        import pdb; pdb.set_trace
        return Mensaje.objects.filter(destinatario=self.request.user).all()