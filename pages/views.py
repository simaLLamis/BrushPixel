from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'No Subject')
        message = request.POST.get('message')

        # Send email
        try:
            send_mail(
                f"{subject} - From {name}",
                f"From: {name} <{email}>\n\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],  # Your email here
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f'Error sending message: {str(e)}')

        return redirect('contact')
    
    return render(request, 'your_template.html')
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
from listings.models import Artwork 
from .models import Testimonial
class IndexView(TemplateView):
    template_name = 'pages/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get trending artworks from the database
        context['trending_artworks'] = Artwork.objects.filter(is_trending=True)[:4]
        # Get latest testimonials
        context['testimonials'] = Testimonial.objects.order_by('-created_at')[:4]
        return context
class AboutView(TemplateView):
    template_name = 'pages/about.html'
class TermsView(TemplateView):
    template_name = 'pages/terms.html'

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
                from_email=settings.DEFAULT_FROM_EMAIL,  # Use Django's configured email
                recipient_list=['lami39564@gmail.com', 'lami39564@gmail.com'],
                fail_silently=False,
            )
            
            # Add success message
            messages.success(request, "Thank you for your message! We'll get back to you soon.")
            
        except Exception as e:
            # Add error message with details
            messages.error(request, f"Error sending message: {str(e)}")
            print(f"Email error: {str(e)}")  # Log the error for debugging
        
        # Redirect to index page with anchor to contact section
        return redirect('index')  # Optionally: return redirect('index') + '#contact'
    
    # If someone accesses this URL directly with GET, redirect to index
    return redirect('index')