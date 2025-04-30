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
        context['trending_artworks'] = Artwork.objects.filter(is_trending=True)[:4]
        context['testimonials'] = Testimonial.objects.order_by('-created_at')[:4]
        return context
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
                recipient_list=['lami39564@gmail.com', 'lamis16553@cotigz.com'],  # Replace with your email
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