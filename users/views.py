from django.shortcuts import render , redirect 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .helper import send_forgot_password_email
from .models import UserProfile
import uuid
import base64

# Validation Sections
def Required(value,field_name):
    if value == '':
        raise ValidationError(f'{field_name} is required')
# End Validation Sections


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            Required(username,'username')
            Required(password,'password')

            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, 'You are not super user')
        
            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('contact')
            else:
                pass
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'cms/login.html')

def logoutPage(request):
    logout(request)
    return redirect('admin_home')

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def homePage(request):
    username = request.user.username
    context = { 'username' : username }
    return render(request, 'cms/contact.html',context)

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def profilePage(request):
    current_user = request.user
    username = current_user.username
    email = current_user.email
    first_name = current_user.first_name
    last_name = current_user.last_name

    context = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    }
    return render(request, 'cms/profile.html',context)

@login_required(login_url='admin_login')
@user_passes_test(lambda user: user.is_superuser)
def changePassword(request):
    if request.method == 'POST':
        current_user = request.user
        current_password = request.POST.get('password')
        new_password = request.POST.get('newPassword')

        print(f"Current User: {current_user}")
        print(f"Current Password: {current_password}")
        print(f"New Password: {new_password}")

        if not current_user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        else:
            current_user.set_password(new_password)
            current_user.save()
            update_session_auth_hash(request, current_user)
            messages.success(request, 'Password successfully changed.')
            return redirect('admin_home')

    return render(request, 'cms/changePassword.html')


def reset_password(request, token_b64):
    try:
        # Decode the token from URL-safe base64 encoding
        token = base64.urlsafe_b64decode(token_b64).decode('utf-8')
        
        # Use the decoded token as the reset_token
        user_profile = UserProfile.objects.get(reset_token=token)
        user_obj = user_profile.user

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password == confirm_password:
                # Set the new password for the user
                user_obj.set_password(new_password)
                user_obj.save()

                # Clear the reset token in the user profile
                user_profile.reset_token = None
                user_profile.save()

                messages.success(request, 'Password reset successfully')
                return redirect('admin_login')
            else:
                messages.error(request, 'Passwords do not match')

    except UserProfile.DoesNotExist:
        messages.error(request, 'Invalid or expired token')
        return redirect('admin_login')
    except Exception as e:
        print(e)

    return render(request, 'cms/resetPassword.html')

def forgot_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).exists():
                messages.error(request, 'User not found with this username')
                return redirect('admin_login')

            user_obj = User.objects.get(username=username)

            user_profile, created = UserProfile.objects.get_or_create(user=user_obj)
            user_profile.reset_token = str(uuid.uuid4())
            user_profile.save()

            send_forgot_password_email(user_obj.email, user_profile.reset_token)
            messages.success(request, 'Email sent successfully')
            return redirect('admin_login')

    except Exception as e:
        print(e)
    return render(request, 'cms/forgotPassword.html')