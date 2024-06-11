from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.contrib import messages
from .models import Student


def base(request):
    return render(request, "base.html")


# ------------------------------------------------------------------------------------------------------------------------------
# -------------------------------| Customer Registration Process |----------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------


def register1(request):
    return render(request, "auth/register.html")


def registration(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "auth/register.html", {
                'fname': fname,
                'lname': lname,
                'email': email
            })

        s = Student(fname=fname, lname=lname, email=email, password=password)
        s.save()

        messages.success(request, "Registration successful. Please login.")
        return redirect("/login1")
    else:
        return render(request, "auth/register.html")


# ------------------------------------------------------------------------------------------------------------------------------
# -------------------------------| Customer Register Data store |----------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------


def welcome(request):
    data = Student.objects.all()
    return render(request, 'auth/welcome.html', {'data': data})


def delete_stud(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('welcome')


def edit_stud(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.fname = request.POST['fname']
        student.lname = request.POST['lname']
        student.email = request.POST['email']
        student.password = request.POST['password']
        student.save()
        return redirect('welcome')
    return render(request, 'auth/edit.html', {'student': student})


# ------------------------------------------------------------------------------------------------------------------------------
# -------------------------------| Customer/Student Login Process |----------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------


def login1(request):
    return render(request, "auth/login.html")


def login_check(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(email=email, password=password)
            request.session['username'] = email
            messages.success(request, "Login successfully...")
            return redirect("/dashboard")
        except Student.DoesNotExist:
            messages.error(request, "Invalid Email or password please try again!")
            return redirect("/login1")  # Redirect back to login page on failure

    return render(request, 'auth/login1.html')


# def dashboard(request):
#     if 'username' in request.session:
#         return render(request, "dash_auth/dashboard.html")
#     else:
#         return redirect("/login1")


def logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect("/login1")


# ------------------------------------------------------------------------------------------------------------------------------
# -------------------------------| Forget Password Process (Pending)|----------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------


# views.py
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "auth/password_reset_email.html"
                c = {
                    'email': user.email,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'YourSite',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, "Password reset email sent.")
                return redirect(reverse('password_reset_done'))
        messages.error(request, "No user found with that email address.")
    return render(request, 'auth/password_reset.html')


def password_reset_done(request):
    return render(request=request, template_name="auth/password_reset_done.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST['password']
            user.set_password(password)
            user.save()
            return redirect(reverse('password_reset_complete'))
        return render(request=request, template_name='auth/password_reset_confirm.html')
    else:
        return render(request=request, template_name='auth/password_reset_invalid.html')


def password_reset_complete(request):
    return render(request=request, template_name="auth/password_reset_complete.html")


# ------------------------------------------------------------------------------------------------------------------------------
# -------------------| User Authentication || Admin Authentication |----------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------


# User Authentication
from django.contrib.auth import authenticate, login


def signup(request):
    return render(request, "user_auth/signup.html")


def user_register(request):
    if request.method == "POST":
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        job_title = request.POST['job_title']
        is_staff = request.POST.get('is_staff') == 'True'

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("/user_register/")  # Redirect back to signup page

        # Create a new User object
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = fname
        user.last_name = lname
        user.is_staff = is_staff  # Mark user as staff if the checkbox is checked
        user.save()

        # Log in the user
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)

        return redirect("/signin")
    else:
        return redirect("/signup")


def signin(request):
    if request.method == "POST":
        email = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('/')
        else:
            return render(request, "user_auth/signin.html", {"error": "Invalid email or password."})
    else:
        return render(request, "user_auth/signin.html")


# Admin Login

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('/admin/')
        else:
            error_message = "Invalid username or password, or you are not authorized to access the admin area."
            return render(request, "admin_auth/admin.html", {"error": error_message})
    else:
        return render(request, "admin_auth/admin.html")


def login_panel(request):
    return render(request, "admin_auth/registrations.html")


# ------------------------------------------------------------------------------------------------------------------------------
# -------------------------------| Bank Account Process |----------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------

from .models import BankAccount
from django.urls import reverse


def dashboard(request):
    if 'username' in request.session:
        # Retrieve the logged-in user's email
        user_email = request.session.get('username')

        # Retrieve the user's account, if it exists
        try:
            account = BankAccount.objects.get(student__email=user_email)
        except BankAccount.DoesNotExist:
            account = None

        return render(request, "dash_auth/dashboard.html", {'account': account})
    else:
        return redirect("/login1")


def create_account(request):
    if request.method == "POST":
        account_no = request.POST['account_no']
        branch_name = request.POST['branch_name']
        balance = request.POST['balance']
        account_type = request.POST['account_type']

        # Retrieve the current logged-in user
        user_email = request.session.get('username')

        # Check if the user already has an existing account
        existing_account = BankAccount.objects.filter(student__email=user_email).exists()
        if existing_account:
            messages.error(request, "You already have an existing account.")
            return redirect('dashboard')  # Redirect back to dashboard

        # If the user doesn't have an existing account, proceed with account creation
        student = get_object_or_404(Student, email=user_email)
        new_account = BankAccount.objects.create(
            student=student,
            account_no=account_no,
            branch_name=branch_name,
            balance=balance,
            account_type=account_type
        )
        messages.success(request, "Bank account created successfully.")
        return redirect('account_details', account_id=new_account.id)  # Redirect to account details with account ID
    return render(request, 'dash_auth/create_account.html')


def account_details(request, account_id):
    account = get_object_or_404(BankAccount, pk=account_id)
    return render(request, 'dash_auth/account_details.html', {'account': account})


# ------------------------------------------------------------------------------------------------------------------------------
# -------------------------------| Account Process Operations |----------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
def deposit1(request, account_id):
    account = get_object_or_404(BankAccount, pk=account_id)
    return render(request, 'dash_auth/acc_auth/deposit.html', {'account': account})


from decimal import Decimal


def deposit_money(request, account_id):
    account = get_object_or_404(BankAccount, pk=account_id)

    if request.method == "POST":
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount <= Decimal('0'):
                messages.error(request, "Please enter a valid positive amount.")
                return redirect('deposit_money', account_id=account_id)
            account.balance += amount
            account.save()
            messages.success(request, f"${amount} deposited successfully.")
            return redirect('account_details', account_id=account_id)
        except ValueError:
            messages.error(request, "Please enter a valid numeric amount.")
            return redirect('deposit_money', account_id=account_id)

    return render(request, 'dash_auth/deposit.html')


def withdraw_money(request, account_id):
    account = get_object_or_404(BankAccount, pk=account_id)

    if request.method == "POST":
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount <= Decimal('0'):
                messages.error(request, "Please enter a valid positive amount.")
                return redirect('withdraw_money', account_id=account_id)
            if amount > account.balance:
                messages.error(request, "Insufficient balance.")
                return redirect('withdraw_money', account_id=account_id)
            account.balance -= amount
            account.save()
            messages.success(request, f"${amount} withdrawn successfully.")
            return redirect('withdraw_money', account_id=account_id)
        except ValueError:
            messages.error(request, "Please enter a valid numeric amount.")
            return redirect('withdraw_money', account_id=account_id)

    return render(request, 'dash_auth/withdraw.html')


def transfer_money(request, account_id):
    sender_account = get_object_or_404(BankAccount, pk=account_id)

    if request.method == "POST":
        receiver_account_no = request.POST.get('receiver_account_no')
        try:
            receiver_account = BankAccount.objects.get(account_no=receiver_account_no)
        except BankAccount.DoesNotExist:
            raise Http404("Receiver account does not exist")

        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount <= Decimal('0'):
                messages.error(request, "Please enter a valid positive amount.")
            elif amount > sender_account.balance:
                messages.error(request, "Insufficient balance.")
            else:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
                # Include receiver's account number in the success message
                messages.success(request, f"${amount} transferred successfully to account number {receiver_account_no}.")
                return redirect('transfer_money', account_id=sender_account.id)
        except ValueError:
            messages.error(request, "Please enter a valid numeric amount.")

    return render(request, 'dash_auth/acc_auth/transfer.html')