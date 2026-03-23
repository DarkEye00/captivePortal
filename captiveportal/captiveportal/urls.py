from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portal.urls')),
]
```

---

## Step 5 — Create Templates

Create this folder structure:
```
captive-portal/
└── templates/
    └── portal/
        ├── login.html
        └── success.html