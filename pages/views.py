from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'pages/index.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class TermsView(TemplateView):
    template_name = 'pages/terms.html'

class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'
    
    
    
    # views.py
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject') or "New Contact Form Submission"
        message = request.POST.get('message')
        
        # Prepare email content
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        
        try:
            # Send email
            send_mail(
                subject=subject,
                message=email_message,
                from_email=email,
                recipient_list=['yahialinus21alg@gmail.com', 'yihak16553@cotigz.com'],  # Replace with your email
                fail_silently=False,
            )
            
            # Add success message
            messages.success(request, "Thank you for your message! We'll get back to you soon.")
            return redirect('index')  # Redirect to the same page after submission
            
        except Exception as e:
            # Handle any errors that occur during email sending
            messages.error(request, f"Sorry, there was an error sending your message. Please try again later.")
            
    # For GET requests, just render the contact page
    return redirect(request, 'index')  # Assuming your template is named contact.html