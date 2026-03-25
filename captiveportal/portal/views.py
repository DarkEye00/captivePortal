import msal
import requests as http_requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse


def get_msal_app():
    return msal.ConfidentialClientApplication(
        settings.CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{settings.TENANT_ID}",
        client_credential=settings.CLIENT_SECRET,
    )


def login(request):
    msal_app = get_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=["User.Read"],
        redirect_uri=settings.REDIRECT_URI,
    )
    return render(request, 'portal/login.html', {'auth_url': auth_url})


def callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Authentication failed — no code received.", status=400)

    msal_app = get_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=["User.Read"],
        redirect_uri=settings.REDIRECT_URI,
    )

    if "error" in result:
        return HttpResponse(
            f"Authentication failed: {result.get('error_description')}",
            status=400
        )

    access_token = result.get("access_token")
    user_info = http_requests.get(
        "https://graph.microsoft.com/v1.0/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    request.session['user'] = {
        'name': user_info.get('displayName', 'User'),
        'email': user_info.get('mail') or user_info.get('userPrincipalName', ''),
    }

    return redirect('/success')


def success(request):
    user = request.session.get('user')
    if not user:
        return redirect('/')
    return render(request, 'portal/success.html', {'user': user})


def logout(request):
    request.session.flush()
    return redirect('/')