from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.shortcuts import redirect
from hashlib import sha256

def login(request):
    if request.session.get('usuario'):
        return redirect('/livro/home')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status':status})

def cadastro(request):
    if request.session.get('usuario'):
        return redirect('/livro/home')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status':status})

def valida_cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario.objects.filter(email=email)

        if len(nome.strip()) == 0 or len(email.strip()) == 0:
            return redirect('/auth/cadastro/?status=1')

        if len(senha.strip()) < 8:
            return redirect('/auth/cadastro/?status=2')

        if len(usuario) > 0:
            return redirect('/auth/cadastro/?status=3')
        else:
            try:
                senha = sha256(senha.encode()).hexdigest()
                usuario = Usuario(nome=nome, email=email, senha=senha)
                usuario.save()
                return redirect('/auth/cadastro/?status=0')
            except:
                return redirect('/auth/cadastro/?stauts=4')

def valida_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario.objects.filter(email=email).filter(senha=senha)
        if usuario.exists():
            request.session['usuario'] = usuario[0].id
            return redirect(f"/livro/home/?id_usuario={request.session['usuario']}")
        else:
            return redirect('/auth/login/?status=1')

def logout(request):
    request.session.flush()
    return redirect('/auth/login/')
