from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from accounts.models import Activation


class UserInputPageView(LoginRequiredMixin, TemplateView):
    template_name = 'main/UserInputs.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                activation = Activation.objects.get(user=request.user)
                return redirect('chat')
            except Activation.DoesNotExist:
                pass
        return super().dispatch(request, *args, **kwargs)


class IndexPageView(TemplateView):
    template_name = 'main/index.html'


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
