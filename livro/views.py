from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from usuarios.models import Usuario
from .models import Livros, Categoria, Emprestimo
from .forms import LivrosForm, CategoriaLivro
from datetime import datetime
from django.db.models import Q

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id=request.session['usuario'])
        status_categoria = request.GET.get('cadastro_categoria')
        status_emprestimo = request.GET.get('cadastro_emprestimo')
        livros = Livros.objects.filter(usuario=usuario)
        tot_livros = Livros.objects.all().count()
        form = LivrosForm()
        form_categoria = CategoriaLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
        usuarios = Usuario.objects.all()
        livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)
        livros_emprestados = Livros.objects.filter(usuario = usuario).filter(emprestado = True)

        return render(request, 'home.html', {'livros':livros, 'usuario_logado':request.session.get('usuario'), 'form':form, 'categoria_form':form_categoria, 'status_categoria':status_categoria, 'usuarios':usuarios, 'status_emprestimo':status_emprestimo, 'livros_emprestar':livros_emprestar, 'total_livros':tot_livros, 'livros_emprestados':livros_emprestados})
    else:
        return redirect('/auth/login/?status=2')

def ver_livro(request, id):
    if request.session.get('usuario'):
        livro = Livros.objects.get(id=id)
        if request.session.get('usuario') == livro.usuario.id:
            usuario = Usuario.objects.get(id=request.session['usuario'])
            categorias = Categoria.objects.filter(usuario_id = request.session.get('usuario'))
            emprestimos = Emprestimo.objects.filter(livro = livro)
            form = LivrosForm()
            form_categoria = CategoriaLivro()
            form.fields['usuario'].initial = request.session['usuario']
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)
            usuarios = Usuario.objects.all()
            livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)
            livros_emprestados = Livros.objects.filter(usuario = usuario).filter(emprestado = True)
            return render(request, 'ver_livro.html', {'livro':livro, 'categorias':categorias, 'emprestimos':emprestimos, 
            'usuario_logado':request.session.get('usuario'), 'form':form, 'categoria_form':form_categoria, 'usuarios':usuarios, 'livros_emprestar':livros_emprestar, 'livros_emprestados':livros_emprestados})
        else:
            return HttpResponse('Esse livro não te pertence')
    else:
        return redirect('/auth/login/?status=2')

def cadastrar_livro(request):
    if request.method == 'POST':
        form = LivrosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/livro/home?status=3')
        else:
            usuario = Usuario.objects.get(id=request.session['usuario'])
            livros = Livros.objects.filter(usuario=usuario)
            form = LivrosForm()
            return render(request, 'home.html', {'livros':livros, 'usuario_logado':request.session.get('usuario'), 'form':form})
    else:
        return redirect('/livro/home?status=4')

def excluir_livro(request, id):
    livro = Livros.objects.get(id=id)
    if livro:
        livro.delete()
        return redirect('/livro/home/')
    else:
        return HttpResponse('Erro em excluir esse livro')

def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)
    nome = form.data['nome']
    descricao = form.data['descricao']
    id_usuario = request.POST.get('usuario')
    if int(request.session.get('usuario')) == int(id_usuario):
        user = Usuario.objects.get(id=id_usuario)
        categoria = Categoria(nome=nome, descricao=descricao, usuario = user)
        categoria.save()
        return redirect('/livro/home/?cadastro_categoria=1')
    else:
        return HttpResponse('Pare de tentar enganar meu SISTEMAAA !!!')

def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado = request.POST.get('livro_emprestado')
        if nome_emprestado_anonimo:
            emprestimo = Emprestimo(nome_emprestado_anonimo=nome_emprestado_anonimo, livro_id=livro_emprestado)
        else:
            emprestimo = Emprestimo(nome_emprestado_id=nome_emprestado, livro_id=livro_emprestado)
        emprestimo.save()

        livro = Livros.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()
        return redirect('/livro/home/?cadastro_emprestimo=1')
    else:
        return HttpResponse('Você pensa que é esperto mas eu sou mais. KKKK')

def devolver_livro(request):
    id = request.POST.get('id_livro_devolucao')
    livro_devolucao = Livros.objects.get(id=id)
    emprestimo_devolucao = Emprestimo.objects.get(Q(livro = livro_devolucao) & Q(data_devolucao = None))
    emprestimo_devolucao.data_devolucao = datetime.now()
    emprestimo_devolucao.save()
    livro_devolucao.emprestado = False
    livro_devolucao.save()
    return redirect('/livro/home/?status_devolucao=1')

def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')
    co_autor_livro = request.POST.get('co_autor_livro')
    autor_livro = request.POST.get('autor_livro')
    categoria_id = request.POST.get('categoria')
    categoria = Categoria.objects.get(id=categoria_id)
    livro = Livros.objects.get(id = livro_id)
    if livro.usuario.id == request.session['usuario']:
        livro.nome = nome_livro
        livro.co_autor = co_autor_livro
        livro.autor = autor_livro
        livro.categoria = categoria
        livro.save()
        return redirect(f'/livro/ver_livro/{livro_id}')
    else:
        return HttpResponse('Erro, eu fui mais esperto outra vez KKKK')

def seus_emprestimos(request):
    usuario = Usuario.objects.get(id=request.session['usuario'])
    emprestimos = Emprestimo.objects.filter(nome_emprestado=usuario)
    return render(request, 'seus_emprestimos.html', {'usuario_logado': request.session['usuario'], 'emprestimos':emprestimos})

def avaliacao_emprestimo(request):
    if request.method == 'POST':
        id_livro_avaliacao = request.POST.get('id_livro_avaliacao')
        opcoes_avaliacao = request.POST.get('opcoes_avaliacao')
        
    else:
        return HttpResponse('Se quiser acessar usa o fomulario espertinho KKK')