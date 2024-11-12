# listings/views.py
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.views.generic import CreateView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cuenta creada exitosamente. Por favor, inicia sesión.")
        return response

class CustomLoginView(View):
    form_class = EmailAuthenticationForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            login(request, user)
            messages.success(request, "Has iniciado sesión exitosamente.")
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, "Lo sentimos, el correo y/o contraseña no coinciden, intenta de nuevo.")
            return render(request, self.template_name, {'form': form})
        
@login_required
def perfil(request):
    return render(request, 'perfil.html', {'user': request.user})


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('perfil')
    else:
        form = CustomUserCreationForm(instance=request.user)
    
    return render(request, 'editar_perfil.html', {'form': form})

@login_required
def mis_inmuebles(request):
    # Puedes agregar lógica aquí para obtener los inmuebles del usuario si tienes un modelo de inmuebles
    return render(request, 'mis_inmuebles.html')