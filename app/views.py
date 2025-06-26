from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View
from .models import *
import google.generativeai as genai
from decouple import config
from django.shortcuts import get_object_or_404, redirect


class IndexView(View):
    def get(self, request, *args, **kwargs):
        filosofo = Filosofo.objects.order_by('?').first()
        # Nova linha: buscando os 3 últimos dilemas
        ultimos_dilemas = Dilema.objects.order_by('-data_criacao')[:3]
        
        context = {
            'filosofo': filosofo,
            'ultimos_dilemas': ultimos_dilemas,
        }
        return render(request, 'index.html', context)

class ComoFuncionaView(TemplateView):
    template_name = 'como_funciona.html'

class DilemaCreateView(TemplateView):
    template_name = 'dilema_create.html'

class DilemaListView(ListView):
    model = Dilema
    template_name = 'dilema_list.html'
    context_object_name = 'dilemas'

def get_gemini_response(prompt):
    genai.configure(api_key=config('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text

class DilemaDetailView(View):
    def get(self, request, *args, **kwargs):
        dilema = get_object_or_404(Dilema, pk=self.kwargs['pk'])
        sessao, created = SessaoReflexao.objects.get_or_create(
            usuario=request.user,
            dilema=dilema
        )
        mensagens = sessao.mensagens.all()
        context = {
            'dilema': dilema,
            'sessao': sessao,
            'mensagens': mensagens
        }
        return render(request, 'dilema_detail.html', context)

    def post(self, request, *args, **kwargs):
        dilema = get_object_or_404(Dilema, pk=self.kwargs['pk'])
        sessao = get_object_or_404(SessaoReflexao, usuario=request.user, dilema=dilema)
        
        # Salva a mensagem do usuário
        conteudo_usuario = request.POST.get('mensagem')
        Mensagem.objects.create(sessao=sessao, remetente='USUARIO', conteudo=conteudo_usuario)

        # Prepara o prompt para a IA
        prompt = f"Analise o seguinte dilema ético: '{dilema.titulo}: {dilema.descricao}'. Meu pensamento sobre isso é: '{conteudo_usuario}'. Aja como um filósofo socrático e me faça uma pergunta curta e provocativa para aprofundar minha reflexão, sem me dar a resposta."
        
        # Obtém e salva a resposta da IA
        resposta_ia = get_gemini_response(prompt)
        Mensagem.objects.create(sessao=sessao, remetente='IA', conteudo=resposta_ia)

        return redirect('dilema_detail', pk=dilema.pk)

class TesteFilosoficoView(TemplateView):
    template_name = 'teste_filosofico.html'

class TeoriaFilosoficaListView(ListView):
    model = TeoriaFilosofica
    template_name = 'teoria_list.html'
    context_object_name = 'teorias'

class TeoriaFilosoficaDetailView(DetailView):
    model = TeoriaFilosofica
    template_name = 'teoria_detail.html'

class DiarioView(ListView):
    model = SessaoReflexao
    template_name = 'diario.html'
    context_object_name = 'sessoes'

class CalculadoraEticaView(TemplateView):
    template_name = 'calculadora_etica.html'