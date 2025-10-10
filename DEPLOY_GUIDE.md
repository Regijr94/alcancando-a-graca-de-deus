# 🚀 Guia de Deploy - Pedido de Casamento

## ✅ Opção 1: Streamlit Cloud (RECOMENDADO - GRATUITO E PRIVADO)

### Passo 1: Criar Repositório PRIVADO no GitHub

1. Acesse: https://github.com
2. Faça login (ou crie uma conta)
3. Clique em **"New repository"** (botão verde)
4. Preencha:
   - **Repository name:** `pedido-casamento` (ou outro nome)
   - **Description:** "Aplicação especial para pedido de casamento"
   - ⚠️ **MARQUE: "Private"** (para manter privado)
   - ✅ **NÃO marque** "Add a README file"
5. Clique em **"Create repository"**

### Passo 2: Subir o Código para o GitHub

No terminal (WSL), execute os comandos que o GitHub mostrar:

```bash
cd /home/reginaldojr/PedidoCasamento

# Inicializar git
git init

# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Aplicação de pedido de casamento - inicial"

# Conectar ao GitHub (substitua SEU_USUARIO pelo seu usuário do GitHub)
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/pedido-casamento.git

# Enviar para o GitHub
git push -u origin main
```

**Nota:** O GitHub vai pedir seu usuário e senha (ou token de acesso pessoal)

### Passo 3: Criar Arquivo .gitignore (para não subir arquivos desnecessários)

O arquivo já existe, mas verifique se tem:
```
venv/
__pycache__/
*.pyc
.env
```

### Passo 4: Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io
2. Clique em **"Sign up"** ou **"Sign in"**
3. **Conecte sua conta do GitHub**
4. Clique em **"New app"**
5. Preencha:
   - **Repository:** `seu-usuario/pedido-casamento`
   - **Branch:** `main`
   - **Main file path:** `app.py`
6. Clique em **"Deploy!"**

⏳ Aguarde 2-5 minutos para o deploy completar!

### Passo 5: Obter o Link da Aplicação

Após o deploy, você receberá um link tipo:
```
https://seu-app.streamlit.app
```

💡 **Envie este link para sua namorada!**

---

## ✅ Opção 2: ngrok (Link Temporário - SEM GITHUB)

### Passo 1: Instalar ngrok

```bash
# Baixar ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok
```

### Passo 2: Criar conta no ngrok

1. Acesse: https://dashboard.ngrok.com/signup
2. Copie seu **token de autenticação**
3. Configure no terminal:

```bash
ngrok config add-authtoken SEU_TOKEN_AQUI
```

### Passo 3: Rodar a aplicação

```bash
# Terminal 1: Rodar o Streamlit
cd /home/reginaldojr/PedidoCasamento
source venv/bin/activate
streamlit run app.py --server.port=8502

# Terminal 2: Criar túnel ngrok
ngrok http 8502
```

Você receberá um link tipo:
```
https://abc123.ngrok-free.app
```

⚠️ **ATENÇÃO:** Este link expira quando você fecha o terminal!

---

## ✅ Opção 3: Heroku (Pago/Gratuito com limitações)

### Passo 1: Criar arquivo de configuração

Crie `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Passo 2: Criar Procfile

Crie `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

### Passo 3: Deploy no Heroku

```bash
# Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Criar app
heroku create nome-do-seu-app

# Deploy
git push heroku main
```

---

## 📊 Comparação de Opções

| Opção | Gratuito | Privacidade | Permanente | Facilidade |
|-------|----------|-------------|------------|------------|
| **Streamlit Cloud** | ✅ Sim | ⭐⭐⭐ Alta | ✅ Sim | ⭐⭐⭐ Fácil |
| **ngrok** | ✅ Sim | ⭐⭐ Média | ❌ Não | ⭐⭐ Médio |
| **Heroku** | ⚠️ Limitado | ⭐⭐ Média | ✅ Sim | ⭐ Difícil |

---

## 🔒 Segurança e Privacidade

### Para Streamlit Cloud com Repositório Privado:

1. ✅ **Código fica privado** no GitHub
2. ✅ **App fica público** (qualquer um com o link acessa)
3. 💡 **Dica:** Não compartilhe o link publicamente

### Para adicionar autenticação simples:

Adicione no início do `app.py`:

```python
import streamlit as st

# Senha simples
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    senha = st.text_input("Digite a senha para continuar:", type="password")
    if st.button("Entrar"):
        if senha == "SENHA_SECRETA_AQUI":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Senha incorreta!")
    st.stop()
```

---

## ❓ Dúvidas Comuns

**P: O Streamlit Cloud é realmente gratuito?**
R: Sim! Totalmente gratuito para apps públicos.

**P: As fotos ficarão visíveis no GitHub?**
R: Sim, se o repositório for público. Use repositório PRIVADO!

**P: Posso deletar o app depois?**
R: Sim, você pode deletar a qualquer momento no dashboard do Streamlit Cloud.

**P: O link expira?**
R: No Streamlit Cloud, o link é permanente. No ngrok, expira ao fechar.

---

## 🎯 Próximos Passos

Escolha sua opção e siga o passo a passo!

**Recomendação:** Use Streamlit Cloud com repositório privado! 💕

