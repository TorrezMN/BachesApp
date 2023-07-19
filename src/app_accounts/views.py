from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from app_db.models import User_Profile
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from .forms import New_User_Form
from .forms import Login_Users_Form
from .forms import Update_Profile_Form
from .forms import Update_User_Form_Admin


from django.urls import reverse_lazy


# HELPER FUNCTIONS
def get_user_profile(id):
    return User_Profile.objects.get(profile_user=id)


class Ingresar(TemplateView):
    """View that controls the access to the platform."""

    template_name = "accounts_ingresar.html"

    def get(self, request):
        cont = {
            "form": Login_Users_Form(),
            "head_title": "Ingresar",
        }
        return render(request, self.template_name, cont)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("../admin")
            else:
                return redirect("../contributor")
        else:
            return redirect("../cuentas/ingresar")


class Registrarse(TemplateView):
    template_name = "accounts_registrarse.html"

    def get(self, request):
        cont = {
            "form": New_User_Form(),
            "head_title": "Registrarse",
        }
        return render(request, self.template_name, cont)

    def post(self, request):
        form = New_User_Form(request.POST)
        c = {
            "form": New_User_Form(),
            "title": "Registrarse",
        }
        if form.is_valid():
            # print("----------------> Formulario Valido")
            # form.save(commit=False)
            # form.save()
            # print("->>>>>> SE GUARDO EL REGISTRO!")
            try:
                form.save(commit=False)
                form.save()
                messages.success(
                    request, "Se ha registrado correctamente. <a href='/'>volver.</a>"
                )
                return render(request, self.template_name, c)
            except IntegrityError as e:
                messages.error(
                    request, "Lo sentimos, el email ya se encuentra registrado."
                )
                return render(request, self.template_name, c)
        # else:
        #     print("---------------------> Formulario NO VALIDO")
        #     print("--------------------->", form.errors.get_json_data())
        else:
            # Found in: https://docs.djangoproject.com/en/3.0/ref/forms/api/
            # get_json_data()
            # Returns the errors as a dictionary suitable for serializing to JSON. Form.errors.as_json() returns serialized JSON,
            # while this returns the error data before it’s serialized. They are stored in the "error" variable.
            error = form.errors.get_json_data()
            # An empty string type variable is declared.
            msg = ""
            # With error.keys () all the keys of the dictionary are extracted to be able to go through
            # them one by one.The dictionary contains a list of errors where each field has its
            # place on the list. The number of keys is equal to the number of fields with errors.
            for i in error.keys():
                for j in error[i]:
                    # Each of the dictionary error messages is added to the variable "msg"
                    # regardless of its size. In this way the final message is constructed.
                    msg += "\n" + j["message"]
            # Once the message is built, it is added to the "messages" instance of the session.
            messages.error(request, msg)
            return render(request, self.template_name, c)


class Logout(TemplateView):
    def get(self, request):
        logout(request)
        return redirect("../")


class Detalle_Usuario(DetailView):
    # template_name = 'accounts_detalle_usuario.html'
    template_name = ""

    model = User_Profile
    context_object_name = "user_profile"
    queryset = User_Profile.objects.all()
    extra_context = {
        "head_title": "Detalle Usuario",
    }

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Set template for extension.
        if self.request.user.is_superuser:
            self.template_name = "accounts_detalle_usuario_admin.html"
            # context['user_profile'] = get_user_profile(self.kwargs['pk'])
            context["user_profile"] = get_user_profile(self.request.user.id)
            context["user_profile_data"] = get_user_profile(self.kwargs["pk"])

        else:
            self.template_name = "accounts_detalle_usuario_contributor.html"
            #  context['user_profile'] = get_user_profile(self.kwargs['pk'])
            context["user_profile"] = get_user_profile(self.request.user.id)

        return context


class Delete_Usuario(DeleteView):
    template_name = "accounts_delete_user.html"
    model = User_Profile
    extra_context = {
        "head_title": " Eliminar Usuario",
    }
    success_url = reverse_lazy("admin_listado_usuarios")

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context["user_profile"] = get_user_profile(self.request.user.id)
        return context


class Editar_Usuario(UpdateView):
    template_name = ""
    form = Update_User_Form_Admin()
    model = User_Profile
    form_class = Update_User_Form_Admin
    success_message = "El perfil de usuario fue actualizado correctamente."
    extra_context = {
        "head_title": " Editar Usuario",
    }

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Set template for extension.
        if self.request.user.is_superuser:
            self.template_name = "accounts_edit_user_admin.html"
            context["user_profile"] = get_user_profile(self.request.user.id)
            context["user_profile_data"] = get_user_profile(self.kwargs["pk"])

        else:
            self.template_name = "accounts_edit_user_contributor.html"
            context["user_profile"] = get_user_profile(self.kwargs["pk"])

        return context

    def get_success_url(self, **kwargs):
        if self.request.user.is_superuser:
            return reverse("admin_home")
        else:
            return reverse("contrib_home")


class Editar_Perfil(UpdateView):
    template_name = ""
    form = Update_Profile_Form()
    model = User_Profile
    form_class = Update_Profile_Form
    success_message = "El perfil de usuario fue actualizado correctamente."
    extra_context = {
        "head_title": " Editar Perfil",
    }

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Set template for extension.
        if self.request.user.is_superuser:
            self.template_name = "accounts_edit_profile_admin.html"
            context["user_profile"] = get_user_profile(self.request.user.id)
            # context['user_profile_data'] = get_user_profile(self.kwargs['pk'])

        else:
            self.template_name = "accounts_edit_profile_contributor.html"
            context["user_profile"] = get_user_profile(self.request.user.id)
            # context['user_profile'] = get_user_profile(self.kwargs['pk'])
        return context

    def get_success_url(self, **kwargs):
        if self.request.user.is_superuser:
            return reverse("admin_home")
        else:
            return reverse("contrib_home")
