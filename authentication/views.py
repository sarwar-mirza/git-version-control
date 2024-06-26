from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView
from .forms import SignUpUserCreationForm, LoginAuthenticationForm, ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Create Signup views here.
class SignUpTemplateView(TemplateView):
    template_name = 'authentication/signup.html'
    
    def get_context_data(self, **kwargs):    # create get function
        context = super().get_context_data(**kwargs)
        fm = SignUpUserCreationForm()
        context = {'form':fm}
        return context
    
    
    def post(self, request):     # create post function
        fm = SignUpUserCreationForm(request.POST)
        
        if fm.is_valid():       # check valid form
            fm.save()
            
            # messages framework
            messages.success(request, 'Congratulations!!! your account has been created successfully')
            fm = SignUpUserCreationForm()       # empty form
        return render(request, 'authentication/signup.html', {'form':fm})





# Create Login Function based view
def loginView(request):
    if request.method == 'POST':
        fm = LoginAuthenticationForm(request=request, data = request.POST)
        
        if fm.is_valid():
            un = fm.cleaned_data['username']
            pw = fm.cleaned_data['password']
            
            user = authenticate(username=un, password=pw)
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/accounts/dashboard/')
    else:
        fm = LoginAuthenticationForm()
    return render(request, 'authentication/login.html', {'form':fm})


# Dashboard
def dashboard(request):
    return render(request, 'authentication/dashboard.html')

# logout
def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/accounts/login/')
    else:
        return HttpResponseRedirect('/accounts/login/')

# change password
def changePasswordView(request):
    if request.method == 'POST':
        fm = ChangePasswordForm(user=request.user, data = request.POST)
        
        if fm.is_valid():
            fm.save()
            
            update_session_auth_hash(request, fm.user)      # change korar por jano dashboard thake 
            return HttpResponseRedirect('/accounts/dashboard/')
    else:
        fm = ChangePasswordForm(user=request.user)
    return render(request, 'authentication/changepassword.html', {'form':fm})


