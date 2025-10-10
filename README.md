# 🎵 Galeria de Fotos com Música 🖼️

Uma aplicação Streamlit dockerizada que exibe fotos do diretório `pictures` e reproduz músicas enquanto exibe as fotos.

## 🚀 Funcionalidades

- **Exibição de Fotos**: Visualize fotos do diretório `pictures` em diferentes modos
- **Reprodução de Música**: Execute músicas em background enquanto visualiza as fotos
- **Slideshow Automático**: Reprodução automática de fotos com controle de velocidade
- **Múltiplos Modos de Visualização**: Sequencial, Aleatório e Manual
- **Interface Intuitiva**: Controles fáceis na sidebar
- **Dockerizado**: Fácil execução com Docker e Docker Compose

## 📁 Estrutura do Projeto

```
PedidoCasamento/
├── app.py                 # Aplicação principal Streamlit
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração do container
├── docker-compose.yml    # Orquestração com Docker Compose
├── README.md             # Este arquivo
├── pictures/             # Diretório para suas fotos
│   ├── foto1.jpg
│   ├── foto2.png
│   └── ...
└── music/                # Diretório para suas músicas
    ├── musica1.mp3
    ├── musica2.wav
    └── ...
```

## 🛠️ Instalação e Execução

### Pré-requisitos

- Docker
- Docker Compose
- Fotos no diretório `pictures/`
- Músicas no diretório `music/` (opcional)

### Formatos Suportados

**Imagens:**
- JPG/JPEG
- PNG
- GIF
- BMP
- WebP

**Músicas:**
- MP3
- WAV
- OGG
- M4A

### Execução com Docker Compose (Recomendado)

1. **Adicione suas fotos e músicas:**
   ```bash
   # Adicione suas fotos no diretório pictures/
   cp /caminho/para/suas/fotos/* pictures/
   
   # Adicione suas músicas no diretório music/
   cp /caminho/para/suas/musicas/* music/
   ```

2. **Execute a aplicação:**
   ```bash
   docker compose up --build
   ```

3. **Acesse a aplicação:**
   - Abra seu navegador em: http://localhost:8501

### Execução com Docker

1. **Construa a imagem:**
   ```bash
   docker build -t galeria-fotos .
   ```

2. **Execute o container:**
   ```bash
   docker run -p 8501:8501 \
     -v $(pwd)/pictures:/app/pictures:ro \
     -v $(pwd)/music:/app/music:ro \
     galeria-fotos
   ```

### Execução Local (Desenvolvimento)

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

## 🎛️ Como Usar

### Controles de Música

1. **Selecione uma música** no dropdown da sidebar
2. **Clique em "Play"** para iniciar a reprodução
3. **Clique em "Stop"** para parar a música
4. A música tocará em loop contínuo

### Modos de Visualização

1. **Manual**: Navegue pelas fotos usando os botões Anterior/Próxima
2. **Sequencial**: Visualize todas as fotos em ordem
3. **Aleatório**: Visualize as fotos em ordem aleatória

### Slideshow Automático

1. **Marque "Reprodução Automática"**
2. **Ajuste a duração** de cada slide (1-10 segundos)
3. **Clique em "Iniciar Slideshow"**
4. **Clique em "Parar Slideshow"** para interromper

### Filtros e Configurações

- **Mostrar nomes dos arquivos**: Exibe o nome de cada foto
- **Largura da imagem**: Ajusta o tamanho das imagens (200-1200px)

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

Você pode personalizar a aplicação através de variáveis de ambiente:

```bash
# Porta do servidor
STREAMLIT_SERVER_PORT=8501

# Endereço do servidor
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Modo headless
STREAMLIT_SERVER_HEADLESS=true

# CORS
STREAMLIT_SERVER_ENABLE_CORS=false

# Proteção XSRF
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
```

### Personalização do Docker

Para modificar a porta ou outras configurações, edite o arquivo `docker-compose.yml`:

```yaml
services:
  galeria-fotos:
    ports:
      - "8080:8501"  # Mude 8080 para a porta desejada
```

## 🐛 Solução de Problemas

### Problemas Comuns

1. **"Diretório 'pictures' não encontrado"**
   - Certifique-se de que o diretório `pictures/` existe
   - Adicione pelo menos uma foto no diretório

2. **"Nenhuma imagem encontrada"**
   - Verifique se os arquivos são de formatos suportados
   - Certifique-se de que os arquivos não estão corrompidos

3. **Música não toca**
   - Verifique se o arquivo de música é de formato suportado
   - Certifique-se de que o arquivo não está corrompido
   - No Docker, verifique se o diretório `music/` está montado corretamente

4. **Erro de permissão no Docker**
   - Certifique-se de que os diretórios `pictures/` e `music/` têm permissões de leitura

### Logs e Debug

Para ver os logs da aplicação:

```bash
docker compose logs -f galeria-fotos
```

## 📝 Notas Técnicas

- A aplicação usa **Pygame** para reprodução de áudio
- **Pillow** é usado para processamento de imagens
- O container inclui todas as dependências de sistema necessárias para áudio
- As imagens são carregadas dinamicamente do diretório montado
- A música é reproduzida em loop contínuo

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

**Desenvolvido com ❤️ usando Streamlit e Docker**
