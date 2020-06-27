from django.shortcuts import render
from .models import Subscriber
from .forms import NewsLetterSignUpForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



def newsletter_signup(request):
    if request.method == "POST":
        form = NewsLetterSignUpForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            if Subscriber.objects.filter(email=save_form.email).exists():
                messages.info(request, "Your email already exists", "alert alert-info alert-dismissible fade show")
            else:
                save_form.save()
                messages.success(request, "Thank you for subscribing to my newsletter", "alert alert-success alert-dismissible fade show")
                subject = "Thank you for Signing up to our newsletter"
                from_email = settings.EMAIL_HOST_USER
                to_email = [save_form.email]
                message = f"Hello {to_email} welcome to our news letter"
                send_mail(subject, message, from_email, to_email)

    else:
        form = NewsLetterSignUpForm()
    return render(request, 'subscribe.html', {'form':form})



def newsletter_unsubscribe(request):
    if request.method == "POST":
        form = NewsLetterSignUpForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if Subscriber.objects.filter(email=instance.email).exists():
                Subscriber.objects.get(email=instance.email).delete()
                messages.success(request, "You have successfully unsubscribed", "alert alert-success alert-dismissible fade show")
                subject = "Successfully unsubscribed"
                from_email = settings.EMAIL_HOST_USER
                to_email = [save_form.email]
                message = f"Dear {to_email} we are sorry to see you go"
                send_mail(subject, message, from_email, to_email)

            else:
                messages.warning(request, "You are not a subscriber", "alert alert-warning alert-dismissible fade show")

    else:
        form = NewsLetterSignUpForm()
    return render(request, 'unsubscribe.html', {'form':form})


