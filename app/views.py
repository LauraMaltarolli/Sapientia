from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
import google.generativeai as genai
from decouple import config
from django.shortcuts import get_object_or_404, redirect
from .forms import *
from django.urls import reverse_lazy
from collections import Counter

class IndexView(View):
    def get(self, request, *args, **kwargs):
        filosofo = Filosofo.objects.order_by('?').first()
        ultimos_dilemas = Dilema.objects.order_by('-data_criacao')[:3]
        
        context = {
            'filosofo': filosofo,
            'ultimos_dilemas': ultimos_dilemas,
        }
        return render(request, 'index.html', context)


class ComoFuncionaView(TemplateView):
    template_name = 'como_funciona.html'


class DilemaCriadoForm(forms.ModelForm):
    class Meta:
        model = DilemaCriado
        # Excluímos 'usuario_criador' pois ele será definido automaticamente
        exclude = ('usuario_criador',)

class DilemaCreateView(LoginRequiredMixin, CreateView):
    model = DilemaCriado
    form_class = DilemaCriadoForm
    template_name = 'dilema_create.html'
    success_url = reverse_lazy('dilema_list') # Redireciona para a lista após sucesso

    def form_valid(self, form):
        # Associa o usuário logado ao dilema antes de salvar
        form.instance.usuario_criador = self.request.user
        return super().form_valid(form)


class DilemaListView(ListView):
    model = Dilema
    template_name = 'dilema_list.html'
    context_object_name = 'dilemas'

def get_gemini_response(prompt):
    genai.configure(api_key=config('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(prompt)
    return response.text


class DilemaDetailView(LoginRequiredMixin, View):
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


class TesteFilosoficoView(LoginRequiredMixin, View):
    template_name = 'teste_filosofico.html'

    def get(self, request, *args, **kwargs):
        teste = TesteFilosofico.objects.first()
        context = {
            'teste': teste,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teste = TesteFilosofico.objects.first()
        respostas = []
        
        for i, pergunta_data in enumerate(teste.perguntas):
            resposta = request.POST.get(f'pergunta_{i}')
            if resposta:
                respostas.append(resposta)

        if not respostas:
            resultado_final = "Indeterminado"
        else:
            contagem = Counter(respostas)
            resultado_final = contagem.most_common(1)[0][0]

        ResultadoTeste.objects.create(
            usuario=request.user,
            teste=teste,
            resultado=resultado_final
        )

        context = {
            'teste': teste,
            'resultado': resultado_final,
        }
        return render(request, self.template_name, context)


class TeoriaFilosoficaListView(ListView):
    model = TeoriaFilosofica
    template_name = 'teoria_list.html'
    context_object_name = 'teorias'


class TeoriaFilosoficaDetailView(DetailView):
    model = TeoriaFilosofica
    template_name = 'teoria_detail.html'


class DiarioView(LoginRequiredMixin, ListView):
    model = SessaoReflexao
    template_name = 'diario.html'
    context_object_name = 'sessoes'

    def get_queryset(self):
        return SessaoReflexao.objects.filter(usuario=self.request.user).order_by('-data_inicio')


class CalculadoraEticaView(TemplateView):
    template_name = 'calculadora_etica.html'


class CadastroView(CreateView):
    form_class = UsuarioCreateForm
    template_name = 'cadastro.html'
    success_url = reverse_lazy('index')