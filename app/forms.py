from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from datetime import date
from django import forms

class UsuarioCreateForm(UserCreationForm):
    # O campo precisa ser definido aqui para que possamos validá-lo
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'data_nascimento')

    def clean_data_nascimento(self):
        # Pega o valor da data de nascimento do formulário
        data_nascimento = self.cleaned_data.get('data_nascimento')
        
        if data_nascimento != None:
            hoje = date.today()
            
            if data_nascimento > hoje:
                raise forms.ValidationError("A data de nascimento não pode ser no futuro.", code='data_futura')
            
            # Calcula a idade do usuário de forma precisa
            idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
            
            if idade > 130:
                raise forms.ValidationError("A data de nascimento parece inválida.", code='data_invalida')
            
            elif idade < 10:
                raise forms.ValidationError("Você deve ter pelo menos 10 anos para se cadastrar.", code='idade_invalida')
            
        return data_nascimento