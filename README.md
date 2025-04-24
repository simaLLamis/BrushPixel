this is my django project structure 
```
artwork_gallery/
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── artwork_gallery/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── listings/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── media/
├── pages/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── img/
│   └── js/
│       └── main.js
├── staticfiles/
├── templates/
│   ├── registrations/
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── settings.html
│   ├── base.html
│   ├── listings/
│   │   ├── artwork-detail.html
│   │   ├── checkout.html
│   │   └── gallery.html
│   ├── pages/
│   │   ├── about.html
│   │   └── index.html
│   └── partials/
│       ├── _footer.html
│       └── _navbar.html
└── manage.py
```

now i will give your the dashboard.html theme page and try to figure out the base template and the partials




NOTE: don't add any context object just keep the previous HTML as it is i only want it in blocks (content , title , extra_css, extra_js) and extending the base template
now the dashboard page but for the extra css block just add static link to the css file



https://poe.com/s/WcyTMxpmRZP51kbTtIJ7