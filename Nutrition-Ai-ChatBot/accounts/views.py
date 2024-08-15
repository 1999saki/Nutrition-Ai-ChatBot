import json

from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.views.generic.base import TemplateView

from .food_chart import *
from .forms import (
    SignInViaUsernameForm, SignInViaEmailForm, SignInViaEmailOrUsernameForm, SignUpForm,
    RestorePasswordForm, RestorePasswordViaEmailOrUsernameForm, RemindUsernameForm,
    ResendActivationCodeForm, ResendActivationCodeViaEmailForm, ChangeProfileForm,
    ChangeEmailForm,
)
from .models import Activation
from .recipe_cleaner import *
from .gen_model import *
from .utils import (
    send_activation_email, send_reset_password_email, send_forgotten_username_email,
    send_activation_change_email,
)


class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().dispatch(request, *args, **kwargs)


class LogInView(GuestOnlyView, FormView):
    template_name = 'accounts/log_in.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME or settings.LOGIN_VIA_EMAIL:
            return SignInViaEmailForm

        if settings.LOGIN_VIA_EMAIL_OR_USERNAME:
            return SignInViaEmailOrUsernameForm

        return SignInViaUsernameForm

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        if url_is_safe:
            return redirect(redirect_to)

        return redirect(settings.LOGIN_REDIRECT_URL)


class SignUpView(GuestOnlyView, FormView):
    template_name = 'accounts/sign_up.html'
    form_class = SignUpForm

    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)

        if settings.DISABLE_USERNAME:
            # Set a temporary username
            user.username = get_random_string()
        else:
            user.username = form.cleaned_data['username']

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        # Create a user record
        user.save()

        # Change the username to the "user_ID" form
        if settings.DISABLE_USERNAME:
            user.username = f'user_{user.id}'
            user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.save()

            send_activation_email(request, user.email, code)

            messages.success(
                request, _('You are signed up. To activate the account, follow the link sent to the mail.'))
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            messages.success(request, _('You are successfully signed up!'))

        return redirect('index')


class ActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Activate profile
        user = act.user
        user.is_active = True
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully activated your account!'))

        return redirect('accounts:log_in')


class ResendActivationCodeView(GuestOnlyView, FormView):
    template_name = 'accounts/resend_activation_code.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.DISABLE_USERNAME:
            return ResendActivationCodeViaEmailForm

        return ResendActivationCodeForm

    def form_valid(self, form):
        user = form.user_cache

        activation = user.activation_set.first()
        activation.delete()

        code = get_random_string(20)

        act = Activation()
        act.code = code
        act.user = user
        act.save()

        send_activation_email(self.request, user.email, code)

        messages.success(self.request, _('A new activation code has been sent to your email address.'))

        return redirect('accounts:resend_activation_code')


class RestorePasswordView(GuestOnlyView, FormView):
    template_name = 'accounts/restore_password.html'

    @staticmethod
    def get_form_class(**kwargs):
        if settings.RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME:
            return RestorePasswordViaEmailOrUsernameForm

        return RestorePasswordForm

    def form_valid(self, form):
        user = form.user_cache
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        if isinstance(uid, bytes):
            uid = uid.decode()

        send_reset_password_email(self.request, user.email, token, uid)

        return redirect('accounts:restore_password_done')


class ChangeProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_profile.html'
    form_class = ChangeProfileForm

    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        return initial

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        messages.success(self.request, _('Profile data has been successfully updated.'))

        return redirect('accounts:change_profile')


class ChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, _('To complete the change of email address, click on the link sent to it.'))
        else:
            user.email = email
            user.save()

            messages.success(self.request, _('Email successfully changed.'))

        return redirect('accounts:change_email')


class ChangeEmailActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Change the email
        user = act.user
        user.email = act.email
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, _('You have successfully changed your email!'))

        return redirect('accounts:change_email')


class RemindUsernameView(GuestOnlyView, FormView):
    template_name = 'accounts/remind_username.html'
    form_class = RemindUsernameForm

    def form_valid(self, form):
        user = form.user_cache
        send_forgotten_username_email(user.email, user.username)

        messages.success(self.request, _('Your username has been successfully sent to your email.'))

        return redirect('accounts:remind_username')


class ChangePasswordView(BasePasswordChangeView):
    template_name = 'accounts/profile/change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, _('Your password was changed.'))

        return redirect('accounts:change_password')


class RestorePasswordConfirmView(BasePasswordResetConfirmView):
    template_name = 'accounts/restore_password_confirm.html'

    def form_valid(self, form):
        # Change the password
        form.save()

        messages.success(self.request, _('Your password has been set. You may go ahead and log in now.'))

        return redirect('accounts:log_in')


class RestorePasswordDoneView(BasePasswordResetDoneView):
    template_name = 'accounts/restore_password_done.html'


class LogOutConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/log_out_confirm.html'


class LogOutView(LoginRequiredMixin, BaseLogoutView):
    template_name = 'accounts/log_out.html'


data = {'age': None, 'veg_non_veg': None, 'weight': None, 'height': None}

#
# def update_and_check_data(input_dict=None):
#     if input_dict is None:
#         input_dict = {}
#     global data
#
#     # Update the data dictionary with values from the input dictionary
#     for key in data.keys():
#         if key in input_dict and input_dict[key] is not None:
#             data[key] = input_dict[key]
#
#     # Check for missing values
#     missing_values = {key: value for key, value in data.items() if value is None}
#
#     if missing_values:
#         # Construct a message for the missing values
#         missing_fields = ', '.join(missing_values.keys())
#         return False, f"Please provide the following values in valid format: {missing_fields}"
#
#     return True, "All values are present."

###############################################################################

from keras.models import load_model
import random
import pickle
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
# from .recipe_cleaner import get_recipe
from os.path import dirname, abspath, join

nltk.download('wordnet')

BASE_DIR = dirname(dirname(abspath(__file__)))
CONTENT_DIR = join(BASE_DIR, 'content/static')

lemmatizer = WordNetLemmatizer()


def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    words = pickle.load(open(join(CONTENT_DIR, 'words.pkl'), "rb"))
    classes = pickle.load(open(join(CONTENT_DIR, 'classes.pkl'), "rb"))

    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def chatbot_response(user_message):
    model = load_model(join(CONTENT_DIR, 'chatbot_model.h5'))

    # Load and process the intents JSON file
    data_file = open(join(CONTENT_DIR, 'intents.json')).read()
    intents = json.loads(data_file)

    # Rest of your existing code
    if user_message.startswith('my name is'):
        name = user_message[11:]
        ints = predict_class(user_message, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}", name)
    elif user_message.startswith('hi my name is'):
        name = user_message[14:]
        ints = predict_class(user_message, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}", name)
    else:
        ints = predict_class(user_message, model)
        res = getResponse(ints, intents)
    return res


@csrf_exempt
def chat_handler(request, data=None):
    activation_record = get_object_or_404(Activation, user=request.user)

    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message")
        user_message = user_message.lower()

        if "hello" in user_message:
            response = "Hello!"
        elif "how are you" in user_message:
            response = "I am fine! How are you?"
        elif "bye" in user_message:
            response = "Bye Have a nice day ;)"
        elif "ok" in user_message or "okay" in user_message:
            response = "Believe in yourself! Every step counts, no matter how small."
        elif "/generate_recipe" in user_message:
            try:
                food_items = user_message.split('/generate_recipe')[-1].split(',')
                response = generate_recipe(food_items)
            except:
                response = "There is some issue in the passed food items."

        elif "/food_chart" in user_message:
            daily_calories, macros, diet_chart = calculate_tdee_and_macros_and_generate_diet_chart(
                activation_record.gender, int(activation_record.weight),
                int(activation_record.height), int(activation_record.age),
                activation_record.activity_level,
                activation_record.goal, activation_record.food_options)
            response = format_diet_chart_html(diet_chart, daily_calories, activation_record.food_options)
            return JsonResponse({'response': response, 'render': True})
        else:
            response = generate_response([user_message])

        # res, message = update_and_check_data()
        # if not res:
        #     return JsonResponse({'response': message})
        # # user_input = data.get('message', '')
        #
        # # Determine which function to call based on user input
        # if 'weight gain' in user_message.lower():
        #     response = Weight_Gain()
        # elif 'weight loss' in user_message.lower():
        #     response = Weight_Loss()
        # elif 'healthy' in user_message.lower():
        #     response = Healthy()
        # else:
        #     response = "I don't understand. Can you please clarify?"

        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        goal = data.get('goal')
        gender = data.get('gender')
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        activity_level = data.get('activity_level')
        food_options = data.get('food_options')

        user, created = User.objects.get_or_create(username=name)

        activation, created = Activation.objects.get_or_create(user=user)
        activation.email = user.email
        activation.age = age
        activation.height = height
        activation.goal = goal
        activation.weight = weight
        activation.gender = gender
        activation.activity_level = activity_level
        activation.food_options = food_options
        activation.save()

        return redirect('chat')

    return JsonResponse({'status': 'fail'}, status=400)
