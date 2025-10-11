import streamlit as st
import streamlit.components.v1 as components
import os
import time
from PIL import Image
from pathlib import Path
import base64
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Reginaldo e Beatriz - Um história de amor",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado - Esconder TODOS os elementos do Streamlit
st.markdown("""
<style>
    /* Esconder menu, footer e header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Esconder toolbar/header preto do topo */
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Esconder header container */
    [data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Esconder botão de deploy/menu */
    button[kind="header"] {
        display: none !important;
    }
    
    /* Esconder barra de status */
    [data-testid="stStatusWidget"] {
        display: none !important;
    }
    
    /* Esconder decoração do header */
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Esconder sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Esconder janela "Manage App" no canto inferior direito */
    [data-testid="manage-app"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Esconder botão de gerenciar app */
    [data-testid="stAppDeployButton"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Esconder qualquer elemento no canto inferior direito */
    .stAppDeployButton {
        display: none !important;
    }
    
    /* Ajustar padding */
    .main > div {
        padding-top: 0rem;
    }
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem;
    }
</style>
""", unsafe_allow_html=True)

# Player de música global - toca músicas específicas por página
def add_global_music():
    """Adiciona player de música que funciona em todas as páginas"""
    # Detectar página atual
    current_page = st.session_state.get('page', 'intro')
    
    # Selecionar música baseada na página
    music_dir = "music"
    music_files = get_music_files(music_dir)
    
    if music_files:
        try:
            # Separar músicas por nome
            alceu_music = None
            roberta_music = None
            
            for music_file in music_files:
                if "Alceu" in music_file or "alceu" in music_file or "Belle" in music_file:
                    with open(music_file, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        alceu_music = base64.b64encode(audio_bytes).decode()
                elif "Roberta" in music_file or "roberta" in music_file or "Janeiro" in music_file:
                    with open(music_file, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                        roberta_music = base64.b64encode(audio_bytes).decode()
            
            # Escolher música baseada na página
            if current_page == 'proposal':
                selected_music = roberta_music if roberta_music else alceu_music
                music_name = "Roberta Campos - De Janeiro a Janeiro"
            else:  # intro, quiz, gallery
                selected_music = alceu_music if alceu_music else roberta_music
                music_name = "Alceu Valença - La Belle de Jour"
            
            if selected_music:
                # HTML com player de música persistente usando localStorage
                music_html = f"""
                <audio id="global-music-player" loop style="display: none;">
                    <source src="data:audio/mpeg;base64,{selected_music}" type="audio/mpeg">
                </audio>
                <script>
                    // Player de música persistente que não recarrega entre páginas
                    (function() {{
                        const audioPlayer = document.getElementById('global-music-player');
                        const musicKey = 'music_playing_{current_page}';
                        
                        // Verificar se a música já está tocando
                        const isMusicPlaying = localStorage.getItem('music_is_playing') === 'true';
                        const currentTime = parseFloat(localStorage.getItem('music_current_time') || '0');
                        
                        if (audioPlayer) {{
                            // Restaurar tempo se for a mesma música
                            if (isMusicPlaying && currentTime > 0) {{
                                audioPlayer.currentTime = currentTime;
                            }}
                            
                            // Função para iniciar música
                            const startMusic = () => {{
                                audioPlayer.play().then(() => {{
                                    localStorage.setItem('music_is_playing', 'true');
                                    console.log('Música iniciada com sucesso!');
                                    
                                    // Salvar progresso da música periodicamente
                                    setInterval(() => {{
                                        if (!audioPlayer.paused) {{
                                            localStorage.setItem('music_current_time', audioPlayer.currentTime.toString());
                                        }}
                                    }}, 1000);
                                }}).catch(e => {{
                                    console.log('Aguardando interação do usuário...');
                                }});
                            }};
                            
                            // Tentar tocar imediatamente
                            startMusic();
                            
                            // Tentar novamente após pequeno delay
                            setTimeout(startMusic, 100);
                            setTimeout(startMusic, 500);
                            
                            // Adicionar listeners para múltiplos eventos
                            const events = ['click', 'touchstart', 'keydown', 'scroll', 'mousemove'];
                            const playOnInteraction = () => {{
                                if (audioPlayer.paused) {{
                                    startMusic();
                                }}
                                // Remover listeners após primeiro sucesso
                                events.forEach(event => {{
                                    document.removeEventListener(event, playOnInteraction);
                                }});
                            }};
                            
                            events.forEach(event => {{
                                document.addEventListener(event, playOnInteraction, {{ once: true }});
                            }});
                        }}
                    }})();
                </script>
                """
                st.markdown(music_html, unsafe_allow_html=True)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")

def get_image_files(directory):
    """Obtém lista de arquivos de imagem do diretório"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_files = []
    
    if os.path.exists(directory):
        for file in sorted(os.listdir(directory)):
            if Path(file).suffix.lower() in image_extensions:
                full_path = os.path.join(directory, file)
                if not file.endswith(':Zone.Identifier'):  # Ignorar arquivos do Windows
                    image_files.append(full_path)
    
    return image_files

def get_media_files(directory):
    """Obtém lista de arquivos de mídia (imagens e vídeos) do diretório"""
    media_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.mp4', '.avi', '.mov', '.mkv', '.webm'}
    media_files = []
    
    if os.path.exists(directory):
        for file in sorted(os.listdir(directory)):
            if Path(file).suffix.lower() in media_extensions:
                full_path = os.path.join(directory, file)
                if not file.endswith(':Zone.Identifier'):  # Ignorar arquivos do Windows
                    media_files.append(full_path)
    
    return media_files

def is_video_file(file_path):
    """Verifica se o arquivo é um vídeo"""
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
    return Path(file_path).suffix.lower() in video_extensions

def get_music_files(directory):
    """Obtém lista de arquivos de música do diretório"""
    music_extensions = {'.mp3', '.wav', '.ogg', '.m4a'}
    music_files = []
    
    if os.path.exists(directory):
        for file in sorted(os.listdir(directory)):
            if Path(file).suffix.lower() in music_extensions:
                full_path = os.path.join(directory, file)
                if not file.endswith(':Zone.Identifier'):  # Ignorar arquivos do Windows
                    music_files.append(full_path)
    
    return music_files

def calculate_relationship_time():
    """Calcula o tempo de relacionamento desde 29/05/2021"""
    start_date = datetime(2021, 5, 29)
    current_date = datetime.now()
    time_diff = current_date - start_date
    
    years = time_diff.days // 365
    months = (time_diff.days % 365) // 30
    days = (time_diff.days % 365) % 30
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    seconds = time_diff.seconds % 60
    
    return {
        'years': years,
        'months': months,
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'total_days': time_diff.days
    }

def image_to_base64(image_path, max_width=1920):
    """Converte imagem para base64 com otimização"""
    try:
        img = Image.open(image_path)
        
        # Redimensionar se muito grande
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Converter para RGB se necessário
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Salvar em buffer
        from io import BytesIO
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85, optimize=True)
        img_bytes = buffer.getvalue()
        
        # Converter para base64
        img_base64 = base64.b64encode(img_bytes).decode()
        return f"data:image/jpeg;base64,{img_base64}"
    except Exception as e:
        print(f"Erro ao processar {image_path}: {e}")
        return None

def main():
    # Adicionar música global que toca em todas as páginas
    add_global_music()
    
    # Botão flutuante de controle de música
    st.markdown("""
    <style>
        #music-control {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        #music-control:hover {
            background: rgba(255, 255, 255, 0.5);
            transform: scale(1.1);
        }
        
        #music-control-icon {
            font-size: 24px;
        }
    </style>
    
    <div id="music-control" onclick="toggleMusic()">
        <span id="music-control-icon">🎵</span>
    </div>
    
    <script>
        function toggleMusic() {
            const audioPlayer = document.getElementById('global-music-player');
            const icon = document.getElementById('music-control-icon');
            
            if (audioPlayer) {
                if (audioPlayer.paused) {
                    audioPlayer.play().then(() => {
                        icon.textContent = '🎵';
                        localStorage.setItem('music_is_playing', 'true');
                    });
                } else {
                    audioPlayer.pause();
                    icon.textContent = '🔇';
                    localStorage.setItem('music_is_playing', 'false');
                }
            }
        }
        
        // Atualizar ícone baseado no estado atual
        setInterval(() => {
            const audioPlayer = document.getElementById('global-music-player');
            const icon = document.getElementById('music-control-icon');
            if (audioPlayer && icon) {
                icon.textContent = audioPlayer.paused ? '🔇' : '🎵';
            }
        }, 500);
    </script>
    """, unsafe_allow_html=True)
    
    # Verificar query params para mudança de página (compatível com versões antigas)
    try:
        # Tentar nova API primeiro
        query_params = st.query_params
        if 'page' in query_params and query_params['page'] == 'gallery':
            st.session_state.page = 'gallery'
        elif 'page' in query_params and query_params['page'] == 'quiz':
            st.session_state.page = 'quiz'
    except:
        try:
            # Fallback para API antiga
            query_params = st.experimental_get_query_params()
            if 'page' in query_params and query_params['page'][0] == 'gallery':
                st.session_state.page = 'gallery'
            elif 'page' in query_params and query_params['page'][0] == 'quiz':
                st.session_state.page = 'quiz'
        except:
            pass
    
    # Inicializar estado da página
    if 'page' not in st.session_state:
        st.session_state.page = 'intro'
    
    # Página de introdução
    if st.session_state.page == 'intro':
        show_intro_page()
        return
    
    # Página do quiz
    if st.session_state.page == 'quiz':
        show_quiz_page()
        return
    
    # Página da galeria
    if st.session_state.page == 'gallery':
        show_gallery_page()
        return
    
    # Página do pedido de casamento
    if st.session_state.page == 'proposal':
        show_proposal_page()
        return

def show_intro_page():
    """Página de introdução com mensagem animada e tema romântico"""
    
    # Carregar fotos do diretório pictures para o mosaico
    pictures_dir = "pictures"
    image_files = get_image_files(pictures_dir)
    
    # Converter até 20 fotos aleatórias para base64 (para não sobrecarregar)
    import random
    selected_images = random.sample(image_files, min(20, len(image_files))) if image_files else []
    images_base64 = []
    
    for img_path in selected_images:
        img_b64 = image_to_base64(img_path, max_width=400)  # Menor resolução para mosaico
        if img_b64:
            images_base64.append(img_b64)
    
    # Criar CSS do mosaico de fotos
    mosaic_style = ""
    if images_base64:
        mosaic_images = ", ".join([f"url('{img}')" for img in images_base64[:12]])  # Usar até 12 fotos
        mosaic_style = f"""
        /* Mosaico de fotos de fundo */
        .stApp {{
            background: 
                linear-gradient(rgba(255, 154, 158, 0.85), rgba(252, 182, 159, 0.85)),
                {mosaic_images};
            background-size: 
                cover,
                {'25% 25%, ' * 12};
            background-position: 
                center,
                0% 0%, 25% 0%, 50% 0%, 75% 0%,
                0% 33%, 25% 33%, 50% 33%, 75% 33%,
                0% 66%, 25% 66%, 50% 66%, 75% 66%;
            background-repeat: no-repeat;
            animation: mosaicShift 30s ease infinite !important;
        }}
        
        @keyframes mosaicShift {{
            0%, 100% {{ filter: brightness(1) saturate(1.2); }}
            50% {{ filter: brightness(1.1) saturate(1.3); }}
        }}
        """
    else:
        # Fallback para gradiente se não houver fotos
        mosaic_style = """
        .stApp {
            background: linear-gradient(135deg, 
                #ff9a9e 0%, 
                #fecfef 20%, 
                #ffecd2 40%, 
                #fcb69f 60%, 
                #ff9a9e 80%, 
                #fecfef 100%
            ) !important;
            background-size: 400% 400% !important;
            animation: gradientShift 25s ease infinite !important;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        """
    
    # CSS para o fundo romântico - aplicado globalmente no Streamlit
    st.markdown(f"""
    <style>
        /* Remover padding padrão do Streamlit */
        .main .block-container {{
            padding: 0 !important;
            max-width: 100% !important;
        }}
        
        {mosaic_style}
        
        /* Overlay romântico */
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(255, 182, 193, 0.2) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 105, 180, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(255, 192, 203, 0.2) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Obter música para tocar - Alceu Valença na página inicial
    music_dir = "music"
    music_files = get_music_files(music_dir)
    music_base64 = None
    
    if music_files:
        try:
            # Procurar especificamente pela música do Alceu Valença
            alceu_music_file = None
            for music_file in music_files:
                if "Alceu" in music_file or "alceu" in music_file or "Belle" in music_file:
                    alceu_music_file = music_file
                    break
            
            # Se não encontrar Alceu, usar a primeira música
            music_to_load = alceu_music_file if alceu_music_file else music_files[0]
            
            with open(music_to_load, "rb") as audio_file:
                audio_bytes = audio_file.read()
                music_base64 = base64.b64encode(audio_bytes).decode()
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
    
    # Criar CSS do body com mosaico
    body_background = ""
    if images_base64:
        mosaic_images_html = ", ".join([f"url('{img}')" for img in images_base64[:12]])
        body_background = f"""
                background: 
                    linear-gradient(rgba(255, 154, 158, 0.85), rgba(252, 182, 159, 0.85)),
                    {mosaic_images_html};
                background-size: 
                    cover,
                    {'25% 25%, ' * 12};
                background-position: 
                    center,
                    0% 0%, 25% 0%, 50% 0%, 75% 0%,
                    0% 33%, 25% 33%, 50% 33%, 75% 33%,
                    0% 66%, 25% 66%, 50% 66%, 75% 66%;
                background-repeat: no-repeat;
                animation: mosaicShift 30s ease infinite;
        """
    else:
        body_background = """
                background: linear-gradient(135deg, 
                    #ff9a9e 0%, 
                    #fecfef 20%, 
                    #ffecd2 40%, 
                    #fcb69f 60%, 
                    #ff9a9e 80%, 
                    #fecfef 100%
                );
                background-size: 400% 400%;
                animation: gradientShift 25s ease infinite;
        """
    
    intro_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Great+Vibes&family=Pacifico&family=Crimson+Text:ital@1&display=swap" rel="stylesheet">
        <style>
            * {{{{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}}}
            
            body {{{{
                margin: 0;
                padding: 0;
                {body_background}
                height: 100vh;
                width: 100vw;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                position: relative;
            }}}}
            
            /* Overlay romântico */
            body::before {{{{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 20% 50%, rgba(255, 182, 193, 0.2) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255, 105, 180, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 40% 20%, rgba(255, 192, 203, 0.2) 0%, transparent 50%);
                pointer-events: none;
                z-index: 1;
            }}}}
            
            @keyframes gradientShift {{{{
                0% {{{{ background-position: 0% 50%; }}}}
                50% {{{{ background-position: 100% 50%; }}}}
                100% {{{{ background-position: 0% 50%; }}}}
            }}}}
            
            @keyframes mosaicShift {{{{
                0%, 100% {{{{ filter: brightness(1) saturate(1.2); }}}}
                50% {{{{ filter: brightness(1.1) saturate(1.3); }}}}
            }}}}
            /* Corações flutuantes de fundo - mais suaves e românticos */
            .heart {{{{
                position: absolute;
                font-size: 30px;
                opacity: 0;
                animation: floatHearts 18s ease-in-out infinite;
                pointer-events: none;
                z-index: 2;
                filter: drop-shadow(0 0 10px rgba(255, 105, 180, 0.6));
            }}}}
            
            .heart:nth-child(1) {{{{ left: 5%; font-size: 28px; animation-delay: 0s; }}}}
            .heart:nth-child(2) {{{{ left: 15%; font-size: 36px; animation-delay: 2.5s; }}}}
            .heart:nth-child(3) {{{{ left: 25%; font-size: 32px; animation-delay: 5s; }}}}
            .heart:nth-child(4) {{{{ left: 35%; font-size: 30px; animation-delay: 1.5s; }}}}
            .heart:nth-child(5) {{{{ left: 45%; font-size: 34px; animation-delay: 3.5s; }}}}
            .heart:nth-child(6) {{{{ left: 55%; font-size: 42px; animation-delay: 6s; }}}}
            .heart:nth-child(7) {{{{ left: 65%; font-size: 26px; animation-delay: 7.5s; }}}}
            .heart:nth-child(8) {{{{ left: 75%; font-size: 38px; animation-delay: 4s; }}}}
            .heart:nth-child(9) {{{{ left: 85%; font-size: 31px; animation-delay: 8.5s; }}}}
            .heart:nth-child(10) {{{{ left: 95%; font-size: 35px; animation-delay: 10s; }}}}
            .heart:nth-child(21) {{{{ left: 10%; font-size: 24px; animation-delay: 11s; }}}}
            .heart:nth-child(22) {{{{ left: 20%; font-size: 40px; animation-delay: 12s; }}}}
            .heart:nth-child(23) {{{{ left: 30%; font-size: 29px; animation-delay: 13s; }}}}
            .heart:nth-child(24) {{{{ left: 40%; font-size: 33px; animation-delay: 14s; }}}}
            .heart:nth-child(25) {{{{ left: 50%; font-size: 27px; animation-delay: 15s; }}}}
            
            @keyframes floatHearts {{{{
                0% {{{{ 
                    transform: translateY(110vh) translateX(0) rotate(-15deg) scale(0.3); 
                    opacity: 0; 
                }}}}
                5% {{{{ 
                    opacity: 0.6; 
                }}}}
                15% {{{{ 
                    opacity: 0.9; 
                    transform: translateY(85vh) translateX(20px) rotate(15deg) scale(0.9);
                }}}}
                30% {{{{ 
                    opacity: 1; 
                    transform: translateY(70vh) translateX(-10px) rotate(-20deg) scale(1.1);
                }}}}
                45% {{{{ 
                    opacity: 0.95; 
                    transform: translateY(55vh) translateX(15px) rotate(25deg) scale(1);
                }}}}
                60% {{{{ 
                    opacity: 0.9; 
                    transform: translateY(40vh) translateX(-20px) rotate(-30deg) scale(1.15);
                }}}}
                75% {{{{ 
                    opacity: 0.8; 
                    transform: translateY(25vh) translateX(10px) rotate(20deg) scale(0.95);
                }}}}
                90% {{{{ 
                    opacity: 0.5; 
                    transform: translateY(10vh) translateX(-15px) rotate(-25deg) scale(0.8);
                }}}}
                100% {{{{ 
                    transform: translateY(-10vh) translateX(0) rotate(0deg) scale(0.4); 
                    opacity: 0; 
                }}}}
            }}}}
            .intro-container {{{{
                text-align: center;
                color: white;
                padding: 40px;
                max-width: 1000px;
                position: relative;
                z-index: 10;
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                border-radius: 30px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                box-shadow: 
                    0 8px 32px rgba(255, 105, 180, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.1);
            }}}}
            
            #typed-text {{{{
                font-family: 'Allura', cursive;
                font-size: 38px;
                line-height: 1.5;
                min-height: 350px;
                text-shadow: 
                    3px 3px 6px rgba(0,0,0,0.4),
                    0 0 30px rgba(255, 182, 193, 0.8),
                    0 0 60px rgba(255, 105, 180, 0.6);
                color: #fff;
                font-weight: 700;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 30px;
            }}}}
            .cursor {{{{
                display: inline-block;
                width: 4px;
                background-color: white;
                margin-left: 3px;
                animation: blink 0.7s infinite;
            }}}}
            #infinity-container {{{{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                opacity: 0;
                z-index: 1000;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}}}
            #infinity {{{{
                font-size: 120px;
                animation: pulse 1.5s infinite;
                color: #fff;
                text-shadow: 
                    0 0 40px rgba(255,255,255,1),
                    0 0 80px rgba(255,107,107,0.8),
                    0 0 120px rgba(255,182,193,0.6);
                margin: 0;
                padding: 0;
                font-weight: 900;
                line-height: 1;
            }}}}
            #infinity-text {{{{
                font-family: 'Allura', cursive;
                font-size: 32px;
                color: #fff;
                text-shadow: 
                    3px 3px 6px rgba(0,0,0,0.5),
                    0 0 30px rgba(255, 182, 193, 0.8);
                font-weight: bold;
                text-align: center;
                margin-top: 50px;
                padding: 0 20px;
                max-width: 90%;
                line-height: 1.4;
            }}}}
            @keyframes pulse {{{{
                0%, 100% {{{{ 
                    opacity: 0.4; 
                    transform: scale(1) rotate(0deg);
                }}}}
                50% {{{{ 
                    opacity: 1; 
                    transform: scale(1.15) rotate(8deg);
                }}}}
            }}}}
            @keyframes blink {{{{
                0%, 50% {{{{ opacity: 1; }}}}
                51%, 100% {{{{ opacity: 0; }}}}
            }}}}
            @keyframes fallAndDisappear {{{{
                0% {{{{ 
                    transform: translateY(0) scale(1) rotate(0deg);
                    opacity: 1;
                }}}}
                50% {{{{
                    transform: translateY(150px) scale(0.9) rotate(-5deg);
                    opacity: 0.5;
                }}}}
                100% {{{{ 
                    transform: translateY(300px) scale(0.5) rotate(-10deg);
                    opacity: 0;
                }}}}
            }}}}
            .fall-and-disappear {{{{
                animation: fallAndDisappear 1.5s ease-in forwards;
            }}}}
            @keyframes fadeInInfinity {{{{
                from {{{{ 
                    opacity: 0;
                    transform: scale(0.5);
                }}}}
                to {{{{ 
                    opacity: 1;
                    transform: scale(1);
                }}}}
            }}}}
            @keyframes fadeInText {{{{
                from {{{{ opacity: 0; }}}}
                to {{{{ opacity: 1; }}}}
            }}}}
            
            /* Otimização para celular e tablets */
            @media (max-width: 768px) {{{{
                #typed-text {{{{
                    font-size: 28px;
                    min-height: 250px;
                    padding: 20px;
                }}}}
                #infinity {{{{
                    font-size: 80px;
                }}}}
                #infinity-text {{{{
                    font-size: 24px;
                    padding: 0 15px;
                }}}}
                .intro-container {{{{
                    padding: 20px;
                    max-width: 95%;
                }}}}
            }}}}
            
            @media (max-width: 480px) {{{{
                #typed-text {{{{
                    font-size: 22px;
                    min-height: 200px;
                    padding: 15px;
                }}}}
                #infinity {{{{
                    font-size: 60px;
                }}}}
                #infinity-text {{{{
                    font-size: 20px;
                    padding: 0 10px;
                }}}}
                .intro-container {{{{
                    padding: 15px;
                }}}}
            }}}}
            
            @keyframes fadeOut {{{{
                from {{{{ opacity: 1; }}}}
                to {{{{ opacity: 0; }}}}
            }}}}
            .fade-in-infinity {{{{
                animation: fadeInInfinity 1.5s forwards;
            }}}}
            .fade-out {{{{
                animation: fadeOut 2s forwards;
            }}}}
            
            /* Estrelas piscando */
            .star {{{{
                position: absolute;
                color: white;
                font-size: 20px;
                opacity: 0;
                animation: twinkle 3s infinite;
                pointer-events: none;
                z-index: 2;
            }}}}
            .star:nth-child(11) {{{{ top: 10%; left: 20%; animation-delay: 0s; }}}}
            .star:nth-child(12) {{{{ top: 20%; left: 80%; animation-delay: 1s; }}}}
            .star:nth-child(13) {{{{ top: 30%; left: 10%; animation-delay: 2s; }}}}
            .star:nth-child(14) {{{{ top: 40%; left: 90%; animation-delay: 0.5s; }}}}
            .star:nth-child(15) {{{{ top: 60%; left: 15%; animation-delay: 1.5s; }}}}
            .star:nth-child(16) {{{{ top: 70%; left: 85%; animation-delay: 2.5s; }}}}
            .star:nth-child(17) {{{{ top: 80%; left: 30%; animation-delay: 0.8s; }}}}
            .star:nth-child(18) {{{{ top: 15%; left: 60%; animation-delay: 1.8s; }}}}
            
            @keyframes twinkle {{{{
                0%, 100% {{{{ opacity: 0; transform: scale(0.5); }}}}
                50% {{{{ opacity: 1; transform: scale(1.2); }}}}
            }}}}
        </style>
    </head>
    <body>
        <!-- Corações flutuantes - mais românticos -->
        <div class="heart">❤️</div>
        <div class="heart">💕</div>
        <div class="heart">💖</div>
        <div class="heart">💝</div>
        <div class="heart">💗</div>
        <div class="heart">💘</div>
        <div class="heart">💓</div>
        <div class="heart">💞</div>
        <div class="heart">💟</div>
        <div class="heart">💜</div>
        <div class="heart">❤️</div>
        <div class="heart">💕</div>
        <div class="heart">💖</div>
        <div class="heart">💝</div>
        <div class="heart">💗</div>
        
        <!-- Estrelas piscando -->
        <div class="star">✨</div>
        <div class="star">⭐</div>
        <div class="star">✨</div>
        <div class="star">⭐</div>
        <div class="star">✨</div>
        <div class="star">⭐</div>
        <div class="star">✨</div>
        <div class="star">⭐</div>
        
        <div class="intro-container">
            <div id="typed-text"></div>
            <div id="infinity-container">
                <div id="infinity">∞</div>
                <div id="infinity-text">Nosso amor é como o infinito</div>
            </div>
        </div>
        
        <!-- Player de música automático -->
        """ + (f'''<audio id="intro-music" loop style="display: none;">
            <source src="data:audio/mpeg;base64,{music_base64}" type="audio/mpeg">
        </audio>
        <script>
            // Garantir que a música comece a tocar
            (function() {{
                const audioPlayer = document.getElementById('intro-music');
                if (audioPlayer) {{
                    // Função para tentar tocar
                    const tryPlay = () => {{
                        audioPlayer.play().then(() => {{
                            console.log('Música do Alceu Valença iniciada!');
                            localStorage.setItem('music_is_playing', 'true');
                        }}).catch(e => {{
                            console.log('Aguardando interação: ', e);
                        }});
                    }};
                    
                    // Tentar tocar imediatamente
                    tryPlay();
                    
                    // Tentar novamente com delays
                    setTimeout(tryPlay, 100);
                    setTimeout(tryPlay, 300);
                    setTimeout(tryPlay, 500);
                    
                    // Adicionar listeners para garantir que toque ao interagir
                    const events = ['click', 'touchstart', 'keydown', 'mousemove'];
                    events.forEach(event => {{
                        document.addEventListener(event, function handler() {{
                            if (audioPlayer.paused) {{
                                tryPlay();
                            }}
                            events.forEach(e => document.removeEventListener(e, handler));
                        }}, {{ once: true }});
                    }});
                }}
            }})();
        </script>''' if music_base64 else '') + """
        
        <script>
            const text1 = "Meu amor, sou grato a Deus por ter conhecido você!";
            const text2 = "O nosso amor seja puro, lindo e inigualável!";
            const typedTextElement = document.getElementById('typed-text');
            const infinityContainer = document.getElementById('infinity-container');
            let index = 0;
            
            async function typeText() {
                // PRIMEIRA FRASE: Digitar letra por letra
                while (index < text1.length) {
                    typedTextElement.textContent = text1.substring(0, index + 1);
                    
                    // Adicionar cursor piscando
                    const cursor = document.createElement('span');
                    cursor.className = 'cursor';
                    cursor.innerHTML = '&nbsp;';
                    typedTextElement.appendChild(cursor);
                    
                    index++;
                    
                    // Velocidade de digitação (em ms)
                    await new Promise(resolve => setTimeout(resolve, 80));
                }
                
                // Remover cursor da primeira frase
                let cursor = typedTextElement.querySelector('.cursor');
                if (cursor) cursor.remove();
                
                // Aguardar 1.5 segundos antes de trocar
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                // Fade out da primeira frase
                typedTextElement.style.animation = 'fadeOut 0.8s forwards';
                await new Promise(resolve => setTimeout(resolve, 800));
                
                // Reset para segunda frase
                typedTextElement.style.animation = 'none';
                typedTextElement.style.opacity = '1';
                typedTextElement.textContent = '';
                index = 0;
                
                // SEGUNDA FRASE: Digitar letra por letra
                while (index < text2.length) {
                    typedTextElement.textContent = text2.substring(0, index + 1);
                    
                    // Adicionar cursor piscando
                    const cursor = document.createElement('span');
                    cursor.className = 'cursor';
                    cursor.innerHTML = '&nbsp;';
                    typedTextElement.appendChild(cursor);
                    
                    index++;
                    
                    // Velocidade de digitação (em ms)
                    await new Promise(resolve => setTimeout(resolve, 80));
                }
                
                // Remover cursor da segunda frase
                cursor = typedTextElement.querySelector('.cursor');
                if (cursor) cursor.remove();
                
                // Aguardar 2 segundos para ler o texto
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Animação: texto cai e desaparece
                typedTextElement.classList.add('fall-and-disappear');
                
                // Aguardar animação de queda completar
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                // Mostrar símbolo do infinito no centro com animação
                infinityContainer.style.display = 'block';
                infinityContainer.classList.add('fade-in-infinity');
                infinityContainer.style.opacity = '1';
                
                // Aguardar 5 segundos com infinito piscando
                await new Promise(resolve => setTimeout(resolve, 5000));
                
                // Fade out suave
                document.body.classList.add('fade-out');
                
                // Aguardar fade out completar
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Mudar para a galeria SEM recarregar (navegação suave)
                window.location.href = '?page=quiz';
            }
            
            // Iniciar animação
            typeText();
        </script>
    </body>
    </html>
    """
    
    # Adicionar corações flutuantes diretamente no Streamlit
    st.markdown("""
    <style>
        /* Corações flutuantes */
        .floating-heart {
            position: fixed;
            font-size: 30px;
            opacity: 0;
            animation: floatUp 18s ease-in-out infinite;
            pointer-events: none;
            z-index: 9999;
            filter: drop-shadow(0 0 10px rgba(255, 105, 180, 0.6));
        }
        
        .floating-heart:nth-child(1) { left: 5%; animation-delay: 0s; font-size: 28px; }
        .floating-heart:nth-child(2) { left: 15%; animation-delay: 2.5s; font-size: 36px; }
        .floating-heart:nth-child(3) { left: 25%; animation-delay: 5s; font-size: 32px; }
        .floating-heart:nth-child(4) { left: 35%; animation-delay: 1.5s; font-size: 30px; }
        .floating-heart:nth-child(5) { left: 45%; animation-delay: 3.5s; font-size: 34px; }
        .floating-heart:nth-child(6) { left: 55%; animation-delay: 6s; font-size: 42px; }
        .floating-heart:nth-child(7) { left: 65%; animation-delay: 7.5s; font-size: 26px; }
        .floating-heart:nth-child(8) { left: 75%; animation-delay: 4s; font-size: 38px; }
        .floating-heart:nth-child(9) { left: 85%; animation-delay: 8.5s; font-size: 31px; }
        .floating-heart:nth-child(10) { left: 95%; animation-delay: 10s; font-size: 35px; }
        .floating-heart:nth-child(11) { left: 10%; animation-delay: 11s; font-size: 24px; }
        .floating-heart:nth-child(12) { left: 20%; animation-delay: 12s; font-size: 40px; }
        .floating-heart:nth-child(13) { left: 30%; animation-delay: 13s; font-size: 29px; }
        .floating-heart:nth-child(14) { left: 40%; animation-delay: 14s; font-size: 33px; }
        .floating-heart:nth-child(15) { left: 50%; animation-delay: 15s; font-size: 27px; }
        
        @keyframes floatUp {
            0% { 
                transform: translateY(110vh) translateX(0) rotate(-15deg) scale(0.3); 
                opacity: 0; 
            }
            5% { opacity: 0.6; }
            15% { 
                opacity: 0.9; 
                transform: translateY(85vh) translateX(20px) rotate(15deg) scale(0.9);
            }
            30% { 
                opacity: 1; 
                transform: translateY(70vh) translateX(-10px) rotate(-20deg) scale(1.1);
            }
            45% { 
                opacity: 0.95; 
                transform: translateY(55vh) translateX(15px) rotate(25deg) scale(1);
            }
            60% { 
                opacity: 0.9; 
                transform: translateY(40vh) translateX(-20px) rotate(-30deg) scale(1.15);
            }
            75% { 
                opacity: 0.8; 
                transform: translateY(25vh) translateX(10px) rotate(20deg) scale(0.95);
            }
            90% { 
                opacity: 0.5; 
                transform: translateY(10vh) translateX(-15px) rotate(-25deg) scale(0.8);
            }
            100% { 
                transform: translateY(-10vh) translateX(0) rotate(0deg) scale(0.4); 
                opacity: 0; 
            }
        }
        
        /* Estrelas piscando */
        .floating-star {
            position: fixed;
            color: white;
            font-size: 20px;
            opacity: 0;
            animation: twinkle 3s infinite;
            pointer-events: none;
            z-index: 9999;
        }
        
        .star-1 { top: 10%; left: 20%; animation-delay: 0s; }
        .star-2 { top: 20%; left: 80%; animation-delay: 1s; }
        .star-3 { top: 30%; left: 10%; animation-delay: 2s; }
        .star-4 { top: 40%; left: 90%; animation-delay: 0.5s; }
        .star-5 { top: 60%; left: 15%; animation-delay: 1.5s; }
        .star-6 { top: 70%; left: 85%; animation-delay: 2.5s; }
        .star-7 { top: 80%; left: 30%; animation-delay: 0.8s; }
        .star-8 { top: 15%; left: 60%; animation-delay: 1.8s; }
        
        @keyframes twinkle {
            0%, 100% { opacity: 0; transform: scale(0.5); }
            50% { opacity: 1; transform: scale(1.2); }
        }
    </style>
    
    <div class="floating-heart">❤️</div>
    <div class="floating-heart">💕</div>
    <div class="floating-heart">💖</div>
    <div class="floating-heart">💝</div>
    <div class="floating-heart">💗</div>
    <div class="floating-heart">💘</div>
    <div class="floating-heart">💓</div>
    <div class="floating-heart">💞</div>
    <div class="floating-heart">💟</div>
    <div class="floating-heart">💜</div>
    <div class="floating-heart">❤️</div>
    <div class="floating-heart">💕</div>
    <div class="floating-heart">💖</div>
    <div class="floating-heart">💝</div>
    <div class="floating-heart">💗</div>
    
    <div class="floating-star star-1">✨</div>
    <div class="floating-star star-2">⭐</div>
    <div class="floating-star star-3">✨</div>
    <div class="floating-star star-4">⭐</div>
    <div class="floating-star star-5">✨</div>
    <div class="floating-star star-6">⭐</div>
    <div class="floating-star star-7">✨</div>
    <div class="floating-star star-8">⭐</div>
    """, unsafe_allow_html=True)
    
    # Criar HTML com JavaScript para animação
    typing_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }
            
            #intro-container {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                border-radius: 30px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                box-shadow: 
                    0 8px 32px rgba(255, 105, 180, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.1);
                padding: 60px;
                max-width: 1000px;
                text-align: center;
            }
            
            #typed-text {
                font-family: 'Allura', cursive;
                font-size: 72px;
                line-height: 1.5;
                text-shadow: 
                    3px 3px 6px rgba(0,0,0,0.4),
                    0 0 30px rgba(255, 182, 193, 0.8),
                    0 0 60px rgba(255, 105, 180, 0.6);
                color: #fff;
                font-weight: 700;
                min-height: 350px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 20px;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            
            /* Responsividade para celular */
            @media (max-width: 768px) {
                #intro-container {
                    padding: 30px 20px;
                    max-width: 95%;
                }
                
                #typed-text {
                    font-size: 36px;
                    min-height: 200px;
                    padding: 15px;
                }
                
                #infinity-symbol {
                    font-size: 120px;
                    margin: 30px 0 20px 0;
                }
                
                #infinity-text {
                    font-size: 28px;
                }
            }
            
            @media (max-width: 480px) {
                #intro-container {
                    padding: 20px 15px;
                }
                
                #typed-text {
                    font-size: 28px;
                    min-height: 180px;
                    padding: 10px;
                }
                
                #infinity-symbol {
                    font-size: 100px;
                }
                
                #infinity-text {
                    font-size: 24px;
                }
            }
            
            #infinity-container {
                display: none;
                opacity: 0;
            }
            
            #infinity-symbol {
                font-size: 220px;
                color: #fff;
                text-shadow: 
                    0 0 40px rgba(255,255,255,1),
                    0 0 80px rgba(255,107,107,0.8),
                    0 0 120px rgba(255,182,193,0.6);
                margin: 60px 0 40px 0;
                font-weight: 900;
                animation: pulse 1.5s infinite;
            }
            
            #infinity-text {
                font-family: 'Allura', cursive;
                font-size: 52px;
                color: #fff;
                text-shadow: 
                    3px 3px 6px rgba(0,0,0,0.5),
                    0 0 30px rgba(255, 182, 193, 0.8);
                font-weight: bold;
                margin: 0;
            }
            
            @keyframes pulse {
                0%, 100% { 
                    opacity: 0.4; 
                    transform: scale(1) rotate(0deg);
                }
                50% { 
                    opacity: 1; 
                    transform: scale(1.15) rotate(8deg);
                }
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: scale(0.8);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            @keyframes fadeOut {
                from {
                    opacity: 1;
                    transform: translateY(0);
                }
                to {
                    opacity: 0;
                    transform: translateY(30px);
                }
            }
            
            .cursor {
                display: inline-block;
                width: 3px;
                height: 1em;
                background-color: white;
                margin-left: 5px;
                animation: blink 0.7s infinite;
            }
            
            @keyframes blink {
                0%, 50% { opacity: 1; }
                51%, 100% { opacity: 0; }
            }
        </style>
    </head>
    <body>
        <div id="intro-container">
            <h1 id="typed-text"></h1>
            
            <div id="infinity-container">
                <div id="infinity-symbol">∞</div>
                <p id="infinity-text">Que o nosso amor seja como o infinito</p>
            </div>
        </div>
        
        <script>
            const text1 = "Sou grato, e agradeço a Deus por ter você em minha vida <3";
            const text2 = "Fiz essa aplicação para comemorar nossas conquistas e nosso amor.";
            const typedTextElement = document.getElementById('typed-text');
            const infinityContainer = document.getElementById('infinity-container');
            let index = 0;
            let currentPhase = 1; // Fase 1: primeira frase, Fase 2: segunda frase
            
            function typeText() {
                const currentText = currentPhase === 1 ? text1 : text2;
                
                if (index < currentText.length) {
                    typedTextElement.textContent = currentText.substring(0, index + 1);
                    
                    // Adicionar cursor piscando
                    const cursor = document.createElement('span');
                    cursor.className = 'cursor';
                    typedTextElement.appendChild(cursor);
                    
                    index++;
                    setTimeout(typeText, 80);
                } else {
                    // Remover cursor
                    const cursor = typedTextElement.querySelector('.cursor');
                    if (cursor) cursor.remove();
                    
                    if (currentPhase === 1) {
                        // Primeira frase completa, aguardar 1.5s e iniciar segunda frase
                        setTimeout(() => {
                            // Fade out da primeira frase
                            typedTextElement.style.animation = 'fadeOut 0.8s forwards';
                            
                            setTimeout(() => {
                                // Reset para segunda frase
                                typedTextElement.style.animation = 'none';
                                typedTextElement.style.opacity = '1';
                                typedTextElement.textContent = '';
                                index = 0;
                                currentPhase = 2;
                                
                                // Fade in e começar segunda frase
                                setTimeout(() => {
                                    typeText();
                                }, 100);
                            }, 800);
                        }, 1500);
                    } else {
                        // Segunda frase completa, aguardar e mostrar infinito
                        setTimeout(() => {
                            // Fade out da segunda frase
                            typedTextElement.style.animation = 'fadeOut 1s forwards';
                            
                            setTimeout(() => {
                                // Esconder texto e mostrar infinito
                                typedTextElement.style.display = 'none';
                                infinityContainer.style.display = 'block';
                                infinityContainer.style.animation = 'fadeIn 1.5s forwards';
                            }, 1000);
                        }, 2000);
                    }
                }
            }
            
            // Iniciar digitação da primeira frase
            typeText();
            
            // Botão "Pular" que aparece após 5 segundos
            setTimeout(() => {{
                const skipButton = document.getElementById('skip-button');
                if (skipButton) {{
                    skipButton.style.opacity = '1';
                    skipButton.style.pointerEvents = 'auto';
                }}
            }}, 5000);
        </script>
        
        <!-- Botão Pular -->
        <a id="skip-button" href="?page=gallery" style="
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(10px);
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-family: 'Dancing Script', cursive;
            font-size: 20px;
            font-weight: bold;
            border: 2px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            opacity: 0;
            pointer-events: none;
            transition: all 0.5s ease;
            z-index: 1000;
        " onmouseover="this.style.background='rgba(255, 255, 255, 0.4)'; this.style.transform='scale(1.05)';" 
           onmouseout="this.style.background='rgba(255, 255, 255, 0.25)'; this.style.transform='scale(1)';">
            Pular ⏭️
        </a>
    </body>
    </html>
    """
    
    # Renderizar com components.html
    components.html(typing_html, height=700, scrolling=False)
    
    # Auto-avançar após tempo suficiente para todas as animações
    # Digitação (~8s) + pausa (2s) + fade out (1s) + infinito (8s) = ~19s
    import time
    time.sleep(19)
    st.session_state.page = 'gallery'
    st.rerun()

def show_quiz_page():
    """Página do quiz romântico sobre o relacionamento"""
    
    # Carregar fotos do diretório pictures para o mosaico
    pictures_dir = "pictures"
    image_files = get_image_files(pictures_dir)
    
    # Converter até 20 fotos aleatórias para base64
    import random
    selected_images = random.sample(image_files, min(20, len(image_files))) if image_files else []
    images_base64 = []
    
    for img_path in selected_images:
        img_b64 = image_to_base64(img_path, max_width=400)
        if img_b64:
            images_base64.append(img_b64)
    
    # Criar CSS do mosaico de fotos
    mosaic_style = ""
    if images_base64:
        mosaic_images = ", ".join([f"url('{img}')" for img in images_base64[:12]])
        mosaic_style = f"""
        .stApp {{
            background: 
                linear-gradient(rgba(255, 236, 210, 0.90), rgba(252, 182, 159, 0.90)),
                {mosaic_images};
            background-size: 
                cover,
                {'25% 25%, ' * 12};
            background-position: 
                center,
                0% 0%, 25% 0%, 50% 0%, 75% 0%,
                0% 33%, 25% 33%, 50% 33%, 75% 33%,
                0% 66%, 25% 66%, 50% 66%, 75% 66%;
            background-repeat: no-repeat;
            animation: mosaicShift 30s ease infinite !important;
        }}
        
        @keyframes mosaicShift {{
            0%, 100% {{ filter: brightness(1.05) saturate(1.1); }}
            50% {{ filter: brightness(1.1) saturate(1.2); }}
        }}
        """
    else:
        mosaic_style = """
        .stApp {
            background: linear-gradient(135deg, 
                #ffecd2 0%, 
                #fcb69f 25%, 
                #ff9a9e 50%, 
                #fecfef 75%, 
                #ffecd2 100%
            ) !important;
            background-size: 400% 400% !important;
            animation: gradientShift 25s ease infinite !important;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        """
    
    # CSS para fundo romântico com mosaico
    st.markdown(f"""
    <style>
        /* Fundo romântico para o quiz com mosaico */
        {mosaic_style}
    </style>
    """, unsafe_allow_html=True)
    
    # Inicializar estado do quiz
    if 'quiz_current_question' not in st.session_state:
        st.session_state.quiz_current_question = 0
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_show_result' not in st.session_state:
        st.session_state.quiz_show_result = False
    
    # Perguntas e respostas
    questions = [
        {
            'num': 1,
            'question': 'Qual foi o primeiro lugar que te convidei para sair?',
            'options': ['Habbibs', 'Assistir Netflix', 'Minha Casa', 'Cinema', 'Hiper BomPreço'],
            'correct': 4,
            'key': 'q1'
        },
        {
            'num': 2,
            'question': 'Onde foi nosso primeiro beijo?',
            'options': ['No golzera', 'No sunshine', 'Lá na mimosa', 'No cinema'],
            'correct': 0,
            'key': 'q2'
        },
        {
            'num': 3,
            'question': 'Qual foi nossa primeira viagem?',
            'options': ['Canoa Quebrada', 'Cumbuco', 'Icaraí', 'Morro Branco'],
            'correct': 1,
            'key': 'q3'
        },
        {
            'num': 4,
            'question': 'Qual a data do nosso primeiro beijo?',
            'options': ['16/03/2020', '16/04/2020', '16/03/2021', '16/04/2021', '14/05/2021'],
            'correct': 2,
            'key': 'q4'
        },
        {
            'num': 5,
            'question': 'Qual local mais gostamos de sair ?',
            'options': ['Praia', 'Shopping', 'Comer', 'Academia', 'Cinema'],
            'correct': 2,
            'key': 'q5'
        },
        {
            'num': 6,
            'question': 'Qual música representa nosso relacionamento?',
            'options': ['SomeWhere Only We Know', 'Golzinho', 'Na hora de amar', 
                       'Todas as músicas românticas me lembra você', 'Não tem uma específica'],
            'correct': 3,
            'key': 'q6'
        },
        {
            'num': 7,
            'question': 'Qual o motivo da nossa primeira briga?',
            'options': ['Stella', 'Sorvete', 'Viagem', 'Sol quente'],
            'correct': 0,
            'key': 'q7'
        },
        {
            'num': 8,
            'question': 'O que eu gosto mais em você?',
            'options': ['Cabeça e Topete', 'Sorriso e Sinal no canto da boca', 
                       'Olhar e bico', 'Quando fica manhosa', 'Todas as respostas anteriores'],
            'correct': 4,
            'key': 'q8'
        },
        {
            'num': 9,
            'question': 'Qual comida eu não costumava comer muito e passei a comer mais depois que te conheci?',
            'options': ['Sushi', 'Kebbab', 'Pizza', 'Hamburguer'],
            'correct': 1,
            'key': 'q9'
        },
        {
            'num': 10,
            'question': 'Qual foi o primeiro presente que te dei?',
            'options': ['Squeeze', 'Bolsa', 'Viagem', 'Calça', 'Perfume'],
            'correct': -1,  # Resposta especial
            'key': 'q10'
        }
    ]
    
    # Mostrar resultado final se terminado
    if st.session_state.quiz_show_result:
        # Calcular acertos
        correct_count = 0
        for q in questions[:9]:  # Excluir pergunta 10
            if st.session_state.quiz_answers.get(q['key']) == q['correct']:
                correct_count += 1
        
        total = 9
        percentage = (correct_count / total) * 100
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(255, 105, 180, 0.4), rgba(255, 182, 193, 0.4));
            backdrop-filter: blur(15px);
            border-radius: 30px;
            border: 3px solid rgba(255, 255, 255, 0.5);
            padding: 40px;
            margin: 40px 0;
            text-align: center;
            box-shadow: 0 15px 50px rgba(255, 105, 180, 0.4);
        ">
            <h2 style="
                font-family: 'Great Vibes', cursive;
                font-size: 56px;
                color: #fff;
                text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
                margin-bottom: 20px;
            ">
                💖 Resultado Final 💖
            </h2>
            <p style="
                font-family: 'Dancing Script', cursive;
                font-size: 40px;
                color: #fff;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                margin: 20px 0;
            ">
                Você acertou {correct_count} de {total} perguntas!
            </p>
            <p style="
                font-family: 'Dancing Script', cursive;
                font-size: 36px;
                color: #fff;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                margin: 20px 0;
            ">
                Nota: {percentage:.0f}%
            </p>
            <p style="
                font-family: 'Great Vibes', cursive;
                font-size: 48px;
                color: #fff;
                text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
                margin-top: 30px;
                line-height: 1.4;
            ">
                Você é meu top picks,<br>minha preda bijú! 💕✨
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Adicionar espaço
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Botão centralizado para ir ao pedido
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # CSS para o botão
            st.markdown("""
            <style>
                div.stButton > button {
                    width: 100%;
                    height: 80px;
                    font-size: 36px;
                    font-weight: bold;
                    font-family: 'Dancing Script', cursive;
                    background: linear-gradient(135deg, #ff6b9d, #c06c84);
                    color: white;
                    border: 4px solid white;
                    border-radius: 25px;
                    box-shadow: 0 8px 32px rgba(255, 105, 180, 0.5);
                    animation: buttonPulse 2s ease-in-out infinite;
                    transition: all 0.3s ease;
                }
                
                div.stButton > button:hover {
                    transform: scale(1.05);
                    box-shadow: 0 12px 48px rgba(255, 105, 180, 0.7);
                }
                
                @keyframes buttonPulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                }
            </style>
            """, unsafe_allow_html=True)
            
            if st.button("💕 Clique Aqui 💕", key="go_to_proposal_btn", use_container_width=True):
                st.session_state.page = 'proposal'
                st.rerun()
        
        return
    
    # Mostrar pergunta atual
    current_q = questions[st.session_state.quiz_current_question]
    total_questions = len(questions)
    
    # Título do quiz com progresso
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <h1 style="
            font-family: 'Great Vibes', cursive;
            font-size: 64px;
            color: #2c3e50;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
            margin-bottom: 10px;
            font-weight: bold;
        ">
            💕 Quiz do Nosso Amor 💕
        </h1>
        <p style="
            font-family: 'Dancing Script', cursive;
            font-size: 32px;
            color: #34495e;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.7);
            font-weight: bold;
        ">
            Pergunta {st.session_state.quiz_current_question + 1} de {total_questions}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container da pergunta atual
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        border: 3px solid rgba(255, 255, 255, 0.6);
        padding: 50px;
        margin: 40px auto;
        max-width: 950px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    ">
        <h3 style="
            font-family: 'Dancing Script', cursive;
            font-size: 44px;
            color: #000000;
            text-shadow: 1px 1px 3px rgba(255,255,255,0.8);
            margin-bottom: 30px;
            text-align: center;
            line-height: 1.6;
            font-weight: bold;
        ">
            {current_q['num']}. {current_q['question']}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # CSS para estilizar os radio buttons
    st.markdown("""
    <style>
        /* Aumentar e centralizar opções de resposta */
        div[data-testid="stRadio"] {
            max-width: 900px;
            margin: 40px auto;
        }
        
        div[data-testid="stRadio"] > label {
            font-family: 'Dancing Script', cursive !important;
            font-size: 36px !important;
            color: #000000 !important;
            text-shadow: 1px 1px 3px rgba(255,255,255,0.8) !important;
            margin-bottom: 25px !important;
            text-align: center !important;
            display: block !important;
            font-weight: bold !important;
        }
        
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }
        
        div[data-testid="stRadio"] label[data-baseweb="radio"] {
            background: rgba(255, 255, 255, 0.50) !important;
            backdrop-filter: blur(12px) !important;
            border-radius: 18px !important;
            padding: 25px 40px !important;
            border: 3px solid rgba(255, 182, 193, 0.5) !important;
            transition: all 0.3s ease !important;
            min-width: 650px !important;
            cursor: pointer !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        }
        
        div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
            background: rgba(255, 255, 255, 0.75) !important;
            border-color: rgba(255, 105, 180, 0.7) !important;
            transform: scale(1.03) !important;
            box-shadow: 0 6px 20px rgba(255, 105, 180, 0.3) !important;
        }
        
        div[data-testid="stRadio"] label[data-baseweb="radio"] span {
            font-family: 'Dancing Script', cursive !important;
            font-size: 28px !important;
            color: #000000 !important;
            text-shadow: 0.5px 0.5px 2px rgba(255,255,255,0.8) !important;
            font-weight: bold !important;
            line-height: 1.4 !important;
        }
        
        /* Forçar cor preta em todos os elementos de texto dentro do radio */
        div[data-testid="stRadio"] label[data-baseweb="radio"] span,
        div[data-testid="stRadio"] label[data-baseweb="radio"] div,
        div[data-testid="stRadio"] label[data-baseweb="radio"] p,
        div[data-testid="stRadio"] label[data-baseweb="radio"] * {
            color: #000000 !important;
        }
        
        /* Responsivo para celular */
        @media (max-width: 768px) {
            div[data-testid="stRadio"] label[data-baseweb="radio"] {
                min-width: 85% !important;
                padding: 20px 30px !important;
            }
            
            div[data-testid="stRadio"] label[data-baseweb="radio"] span {
                font-size: 22px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # CSS adicional para label "Escolha sua resposta"
    st.markdown("""
    <style>
        /* Label "Escolha sua resposta" com mesmo estilo da pergunta */
        div[data-testid="stRadio"] > label > div > p {
            font-family: 'Dancing Script', cursive !important;
            font-size: 36px !important;
            color: #000000 !important;
            text-shadow: 1px 1px 3px rgba(255,255,255,0.8) !important;
            font-weight: bold !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Radio buttons para as opções
    answer = st.radio(
        "Escolha sua resposta:",
        options=list(range(len(current_q['options']))),
        format_func=lambda x: f"{chr(97+x)}) {current_q['options'][x]}",
        key=f"current_{current_q['key']}"
    )
    
    # Inicializar estado do popup
    if 'show_popup' not in st.session_state:
        st.session_state.show_popup = False
    if 'popup_message' not in st.session_state:
        st.session_state.popup_message = ""
    if 'popup_type' not in st.session_state:
        st.session_state.popup_type = "success"
    
    # Mostrar popup se ativo
    if st.session_state.show_popup:
        # Cores mais escuras e com melhor contraste
        if st.session_state.popup_type == "success":
            popup_color = "#27ae60"  # Verde escuro
            bg_gradient = "linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(209, 242, 209, 0.98))"
        elif st.session_state.popup_type == "special":
            popup_color = "#e74c3c"  # Rosa/vermelho escuro
            bg_gradient = "linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 209, 220, 0.98))"
        else:
            popup_color = "#c0392b"  # Vermelho escuro
            bg_gradient = "linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(255, 200, 200, 0.98))"
        
        st.markdown(f"""
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 9999;
            background: {bg_gradient};
            backdrop-filter: blur(20px);
            border-radius: 35px;
            border: 4px solid {popup_color};
            padding: 70px;
            min-width: 550px;
            text-align: center;
            box-shadow: 0 25px 70px rgba(0,0,0,0.5);
            animation: popupBounce 0.5s ease-out;
        ">
            <p style="
                font-family: 'Great Vibes', cursive;
                font-size: 52px;
                color: {popup_color};
                text-shadow: 2px 2px 6px rgba(255,255,255,0.8);
                margin: 0;
                line-height: 1.5;
                font-weight: bold;
            ">
                {st.session_state.popup_message}
            </p>
        </div>
        
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: 9998;
        "></div>
        
        <style>
            @keyframes popupBounce {{
                0% {{ transform: translate(-50%, -50%) scale(0.3); opacity: 0; }}
                50% {{ transform: translate(-50%, -50%) scale(1.05); }}
                100% {{ transform: translate(-50%, -50%) scale(1); opacity: 1; }}
            }}
        </style>
        """, unsafe_allow_html=True)
    
    # Botão para próxima pergunta
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💕 Próxima Pergunta 💕" if st.session_state.quiz_current_question < total_questions - 1 else "💕 Ver Resultado 💕", 
                    key="next_btn", use_container_width=True):
            # Guardar resposta
            st.session_state.quiz_answers[current_q['key']] = answer
            
            # Definir mensagem do popup
            if current_q['num'] == 10:
                st.session_state.popup_message = "💖 A resposta é:<br>EU NA SUA VIDA, BEBÊ!!!! 💖"
                st.session_state.popup_type = "special"
            elif answer == current_q['correct']:
                st.session_state.popup_message = "✅ Ai sim bebê,<br>você é o amor da<br>minha vida ❤️"
                st.session_state.popup_type = "success"
            else:
                st.session_state.popup_message = "❌ Ai não bebê!"
                st.session_state.popup_type = "error"
            
            # Mostrar popup
            st.session_state.show_popup = True
            st.rerun()
    
    # Auto-avançar se popup está ativo
    if st.session_state.show_popup:
        import time
        time.sleep(2)
        st.session_state.show_popup = False
        
        # Avançar para próxima pergunta ou resultado
        if st.session_state.quiz_current_question < total_questions - 1:
            st.session_state.quiz_current_question += 1
            st.rerun()
        else:
            st.session_state.quiz_show_result = True
            st.rerun()

def show_proposal_page():
    """Página do pedido de casamento"""
    
    # Nota: A música é controlada pelo player global (add_global_music)
    # que já toca "Roberta Campos - De Janeiro a Janeiro" nesta página
    
    # Carregar foto 37 como fundo
    background_image = None
    background_path = "pictures/37.jpeg"
    try:
        background_image = image_to_base64(background_path)
    except Exception as e:
        print(f"Erro ao carregar foto de fundo: {e}")
    
    # CSS para fundo com foto
    background_css = f"""
    <style>
        .stApp {{
            background: 
                linear-gradient(rgba(255, 154, 158, 0.6), rgba(252, 182, 159, 0.6)),
                url('{background_image}') !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
    </style>
    """ if background_image else """
    <style>
        .stApp {
            background: linear-gradient(135deg, 
                #ff9a9e 0%, 
                #fecfef 20%, 
                #ffecd2 40%, 
                #fcb69f 60%, 
                #ff9a9e 80%, 
                #fecfef 100%
            ) !important;
            background-size: 400% 400% !important;
            animation: gradientShift 25s ease infinite !important;
        }
    </style>
    """
    
    st.markdown(background_css, unsafe_allow_html=True)
    
    # Nota: Player de música já gerenciado pelo global (add_global_music)
    
    proposal_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Allura&family=Cinzel:wght@700&family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, 
                    #ff9a9e 0%, 
                    #fecfef 20%, 
                    #ffecd2 40%, 
                    #fcb69f 60%, 
                    #ff9a9e 80%, 
                    #fecfef 100%
                );
                background-size: 400% 400%;
                animation: gradientShift 25s ease infinite;
                height: 100vh;
                width: 100vw;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                position: relative;
            }
            
            @keyframes gradientShift {
                0%% { background-position: 0%% 50%%; }
                50%% { background-position: 100%% 50%%; }
                100%% { background-position: 0%% 50%%; }
            }
            
            /* Corações flutuantes */
            .heart {
                position: absolute;
                font-size: 40px;
                opacity: 0;
                animation: floatHearts 15s ease-in-out infinite;
                pointer-events: none;
                filter: drop-shadow(0 0 10px rgba(255, 105, 180, 0.6));
            }
            
            .heart:nth-child(1) { left: 10%; animation-delay: 0s; }
            .heart:nth-child(2) { left: 20%; animation-delay: 2s; }
            .heart:nth-child(3) { left: 30%; animation-delay: 4s; }
            .heart:nth-child(4) { left: 40%; animation-delay: 1s; }
            .heart:nth-child(5) { left: 50%; animation-delay: 3s; }
            .heart:nth-child(6) { left: 60%; animation-delay: 5s; }
            .heart:nth-child(7) { left: 70%; animation-delay: 2.5s; }
            .heart:nth-child(8) { left: 80%; animation-delay: 4.5s; }
            .heart:nth-child(9) { left: 90%; animation-delay: 1.5s; }
            .heart:nth-child(10) { left: 15%; animation-delay: 6s; }
            
            @keyframes floatHearts {
                0%% { transform: translateY(110vh) scale(0.5); opacity: 0; }
                10%% { opacity: 0.8; }
                90%% { opacity: 0.8; }
                100%% { transform: translateY(-10vh) scale(1.2); opacity: 0; }
            }
            
            #proposal-container {
                text-align: center;
                color: white;
                padding: 60px;
                max-width: 900px;
                position: relative;
                z-index: 10;
                background: 
                    linear-gradient(rgba(255, 105, 180, 0.75), rgba(255, 182, 193, 0.75)),
                    url('""" + (background_image if background_image else '') + """');
                background-size: cover;
                background-position: center;
                backdrop-filter: blur(8px);
                border-radius: 40px;
                border: 3px solid rgba(255, 255, 255, 0.6);
                box-shadow: 
                    0 15px 60px rgba(0, 0, 0, 0.3),
                    inset 0 0 30px rgba(255, 255, 255, 0.1);
                opacity: 0;
                animation: fadeInProposal 2s forwards;
            }
            
            @keyframes fadeInProposal {
                from {
                    opacity: 0;
                    transform: scale(0.8);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            #message {
                font-family: 'Cinzel', serif;
                font-size: 52px;
                line-height: 1.6;
                text-shadow: 
                    3px 3px 8px rgba(0,0,0,0.5),
                    0 0 40px rgba(255, 182, 193, 0.8);
                color: #fff;
                font-weight: 700;
                margin-bottom: 40px;
                animation: textGlow 3s ease-in-out infinite;
            }
            
            @keyframes textGlow {
                0%%, 100%% { text-shadow: 3px 3px 8px rgba(0,0,0,0.5), 0 0 40px rgba(255, 182, 193, 0.8); }
                50%% { text-shadow: 3px 3px 8px rgba(0,0,0,0.5), 0 0 60px rgba(255, 105, 180, 1); }
            }
            
            #ring {
                font-size: 120px;
                margin: 30px 0;
                animation: ringBounce 2s ease-in-out infinite;
                display: inline-block;
            }
            
            @keyframes ringBounce {
                0%%, 100%% { transform: translateY(0) rotate(0deg); }
                25%% { transform: translateY(-20px) rotate(-10deg); }
                75%% { transform: translateY(-10px) rotate(10deg); }
            }
            
            #question {
                font-family: 'Cinzel', serif;
                font-size: 68px;
                font-weight: 700;
                color: #fff;
                text-shadow: 
                    4px 4px 10px rgba(0,0,0,0.6),
                    0 0 50px rgba(255, 182, 193, 1);
                margin: 40px 0;
                animation: pulse 2s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%%, 100%% { transform: scale(1); }
                50%% { transform: scale(1.1); }
            }
            
            .sparkle {
                position: absolute;
                width: 4px;
                height: 4px;
                background: white;
                border-radius: 50%;
                box-shadow: 0 0 10px white;
                animation: sparkleAnim 2s ease-in-out infinite;
            }
            
            @keyframes sparkleAnim {
                0%%, 100%% { opacity: 0; transform: scale(0); }
                50%% { opacity: 1; transform: scale(1); }
            }
            
            /* Responvidade */
            @media (max-width: 768px) {
                #proposal-container {
                    padding: 40px 30px;
                    max-width: 95%;
                }
                #message {
                    font-size: 36px;
                }
                #ring {
                    font-size: 80px;
                }
                #question {
                    font-size: 48px;
                }
            }
            
            @media (max-width: 480px) {
                #message {
                    font-size: 28px;
                }
                #ring {
                    font-size: 60px;
                }
                #question {
                    font-size: 38px;
                }
            }
        </style>
    </head>
    <body>
        <!-- Corações flutuantes -->
        <div class="heart">💕</div>
        <div class="heart">❤️</div>
        <div class="heart">💖</div>
        <div class="heart">💗</div>
        <div class="heart">💕</div>
        <div class="heart">❤️</div>
        <div class="heart">💖</div>
        <div class="heart">💗</div>
        <div class="heart">💕</div>
        <div class="heart">❤️</div>
        
        <div id="proposal-container">
            <p id="message">
                Beatriz, meu amor,<br>
                Você ilumina minha vida todos os dias.<br>
                Esses anos ao seu lado foram os melhores da minha vida.
            </p>
            
            <div id="ring">💍</div>
            
            <h1 id="question">QUER CASAR COMIGO?</h1>
        </div>
        
        <!-- Sparkles -->
        <div class="sparkle" style="top: 20%; left: 15%;"></div>
        <div class="sparkle" style="top: 40%; right: 20%; animation-delay: 0.5s;"></div>
        <div class="sparkle" style="bottom: 30%; left: 25%; animation-delay: 1s;"></div>
        <div class="sparkle" style="top: 60%; right: 30%; animation-delay: 1.5s;"></div>
        
        <script>
            // Adicionar mais sparkles aleatoriamente
            for (let i = 0; i < 20; i++) {
                const sparkle = document.createElement('div');
                sparkle.className = 'sparkle';
                sparkle.style.top = Math.random() * 100 + '%';
                sparkle.style.left = Math.random() * 100 + '%';
                sparkle.style.animationDelay = Math.random() * 2 + 's';
                document.body.appendChild(sparkle);
            }
        </script>
    </body>
    </html>
    """
    
    # Renderizar página do pedido
    components.html(proposal_html, height=800, scrolling=False)
    
    # Botões de resposta
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <style>
            div.stButton > button {
                width: 100%;
                height: 80px;
                font-size: 32px;
                font-weight: bold;
                font-family: 'Montserrat', sans-serif;
                border-radius: 20px;
                margin: 10px 0;
            }
            div.stButton > button:first-child {
                background: linear-gradient(135deg, #ff6b9d, #c06c84);
                color: white;
                border: 3px solid #fff;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("💕 SIM! EU ACEITO! 💕", key="yes_btn", use_container_width=True):
            st.session_state.proposal_answer = 'yes'
            
            # Múltiplos efeitos de comemoração
            st.balloons()
            st.snow()
            
            # Mensagem de celebração com emojis
            celebration_html = """
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 99999;
                background: linear-gradient(135deg, rgba(255, 215, 0, 0.95), rgba(255, 105, 180, 0.95));
                backdrop-filter: blur(20px);
                border-radius: 40px;
                border: 5px solid white;
                padding: 80px;
                text-align: center;
                box-shadow: 0 30px 90px rgba(0,0,0,0.5);
                animation: celebrationPop 0.6s ease-out;
            ">
                <h1 style="
                    font-family: 'Cinzel', serif;
                    font-size: 72px;
                    color: white;
                    text-shadow: 4px 4px 8px rgba(0,0,0,0.5);
                    margin: 20px 0;
                    animation: textBounce 1s ease-in-out infinite;
                ">
                    🎉 ELA DISSE SIM! 🎉
                </h1>
                <div style="
                    font-size: 80px;
                    margin: 30px 0;
                    animation: emojiSpin 2s linear infinite;
                ">
                    💍 💕 🎊 ✨ 🥳 🎆 💖 🎈
                </div>
                <p style="
                    font-family: 'Dancing Script', cursive;
                    font-size: 48px;
                    color: white;
                    text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
                    margin: 20px 0;
                ">
                    UUUUUUHUUUUUUUUULLLLLLLL QUE FELICIDADE!<br>
                    VAMOS CASAR! 💍💕✨
                </p>
            </div>
            
            <style>
                @keyframes celebrationPop {
                    0%% { 
                        transform: translate(-50%, -50%) scale(0.3); 
                        opacity: 0; 
                    }
                    50%% { 
                        transform: translate(-50%, -50%) scale(1.1); 
                    }
                    100%% { 
                        transform: translate(-50%, -50%) scale(1); 
                        opacity: 1; 
                    }
                }
                
                @keyframes textBounce {
                    0%%, 100%% { transform: translateY(0); }
                    50%% { transform: translateY(-10px); }
                }
                
                @keyframes emojiSpin {
                    0%% { transform: rotate(0deg); }
                    100%% { transform: rotate(360deg); }
                }
            </style>
            """
            
            st.markdown(celebration_html, unsafe_allow_html=True)
            time.sleep(5)
            st.rerun()

def show_gallery_page():
    """Página principal com galeria e contador"""
    
    # CSS para fundo romântico da galeria
    st.markdown("""
    <style>
        /* Fundo romântico para a galeria */
        .stApp {
            background: linear-gradient(135deg, 
                #ffecd2 0%, 
                #fcb69f 25%, 
                #ff9a9e 50%, 
                #fecfef 75%, 
                #ffecd2 100%
            ) !important;
            background-size: 400% 400% !important;
            animation: gradientShift 25s ease infinite !important;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Diretórios
    pictures_dir = "pictures"
    music_dir = "music"
    
    # Obter arquivos (imagens e vídeos)
    media_files = get_media_files(pictures_dir)
    music_files = get_music_files(music_dir)
    
    if not media_files:
        st.error("❌ Nenhuma foto ou vídeo encontrado no diretório 'pictures'!")
        return
    
    # Separar imagens e vídeos
    image_files = [f for f in media_files if not is_video_file(f)]
    video_files = [f for f in media_files if is_video_file(f)]
    
    # Título
    st.markdown("""
    <h1 style='text-align: center; color: #ff6b6b; font-size: 3em;'>
        💕 Reginaldo e Beatriz 💕
    </h1>
    """, unsafe_allow_html=True)
    
    # Contador de tempo com JavaScript assíncrono usando st.components
    rel_time = calculate_relationship_time()
    
    counter_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
            }}
            .counter-container {{
                text-align: center;
                background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
                padding: 20px;
                border-radius: 10px;
                color: white;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }}
            h2 {{
                margin: 0;
                color: white;
                font-size: 24px;
            }}
            .subtitle {{
                margin: 10px 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            #time-display {{
                margin: 15px 0;
                font-size: 22px;
                font-weight: bold;
                transition: color 0.3s;
            }}
            
            /* Responsivo para celular */
            @media (max-width: 768px) {{
                h2 {{
                    font-size: 18px;
                }}
                .subtitle {{
                    font-size: 12px;
                }}
                #time-display {{
                    font-size: 16px;
                }}
                .counter-container {{
                    padding: 15px 10px;
                }}
            }}
            
            @media (max-width: 480px) {{
                h2 {{
                    font-size: 16px;
                }}
                .subtitle {{
                    font-size: 11px;
                }}
                #time-display {{
                    font-size: 14px;
                }}
                .counter-container {{
                    padding: 12px 8px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="counter-container">
            <h2>⏰ Tempo de Relacionamento</h2>
            <p class="subtitle">Desde 29 de maio de 2021 • {rel_time['total_days']} dias juntos ❤️</p>
            <div id="time-display">Carregando...</div>
        </div>
        
        <script>
            // Cronômetro assíncrono em tempo real
            const startDate = new Date('2021-05-29T00:00:00');
            
            async function updateTime() {{
                while(true) {{
                    const now = new Date();
                    const diff = now - startDate;
                    const totalSeconds = Math.floor(diff / 1000);
                    
                    // Calcular componentes
                    const years = Math.floor(totalSeconds / (365.25 * 24 * 60 * 60));
                    const remainingAfterYears = totalSeconds - (years * 365.25 * 24 * 60 * 60);
                    
                    const months = Math.floor(remainingAfterYears / (30.44 * 24 * 60 * 60));
                    const remainingAfterMonths = remainingAfterYears - (months * 30.44 * 24 * 60 * 60);
                    
                    const days = Math.floor(remainingAfterMonths / (24 * 60 * 60));
                    const remainingAfterDays = remainingAfterMonths - (days * 24 * 60 * 60);
                    
                    const hours = Math.floor(remainingAfterDays / (60 * 60));
                    const remainingAfterHours = remainingAfterDays - (hours * 60 * 60);
                    
                    const minutes = Math.floor(remainingAfterHours / 60);
                    const seconds = Math.floor(remainingAfterHours % 60);
                    
                    // Atualizar display
                    const display = document.getElementById('time-display');
                    if (display) {{
                        const timeText = years + ' anos, ' + months + ' meses, ' + days + ' dias, ' +
                                       hours + ' horas, ' + minutes + ' minutos e ' + seconds + ' segundos';
                        display.textContent = timeText;
                        
                        // Efeito visual
                        display.style.color = '#4ecdc4';
                        setTimeout(() => {{ display.style.color = 'white'; }}, 200);
                    }}
                    
                    // Aguardar 1 segundo de forma assíncrona
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }}
            }}
            
            // Iniciar cronômetro assíncrono
            updateTime();
        </script>
    </body>
    </html>
    """
    
    components.html(counter_html, height=150)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Poesia romântica para as fotos
    poesia_versos = [
        "No teu olhar encontrei meu lar",
        "Em cada sorriso, um novo amanhecer",
        "Nossos sonhos entrelaçados como estrelas",
        "Tua mão na minha, eternidade em um toque",
        "Cada momento contigo é poesia",
        "Amor que cresce como flor na primavera",
        "Teus olhos são meu céu preferido",
        "Contigo, o tempo não passa, dança",
        "Nossa história escrita em cada abraço",
        "Sorrisos que iluminam minha alma",
        "Caminhando juntos rumo ao infinito",
        "Teu amor é minha canção favorita",
        "Em teus braços encontro paz",
        "Cada dia ao teu lado é presente",
        "Nosso amor desafia a gravidade",
        "Você é meu sol em dias nublados",
        "Juntos construímos nosso paraíso",
        "Tua felicidade é minha missão",
        "Amor que transborda em cada olhar",
        "Contigo aprendi o significado de amar",
        "Nossos corações batem em sincronia",
        "Você é a resposta que eu buscava",
        "Cada foto, uma memória eterna",
        "Nosso amor é aventura sem fim",
        "Teu sorriso é meu maior tesouro",
        "Juntos somos invencíveis",
        "Amor que aquece até nos dias frios",
        "Você é meu para sempre",
        "Nossa cumplicidade é mágica",
        "Contigo descobri o amor verdadeiro",
        "Cada momento é único e especial",
        "Teu carinho é meu refúgio",
        "Nosso amor é obra de arte",
        "Você completa minha vida",
        "Juntos escrevemos nossa história",
        "Amor que só cresce a cada dia",
        "Tua presença é meu maior presente",
        "Nossos sonhos se tornaram realidade",
        "Você é meu amor eterno",
        "Contigo, tudo faz sentido",
        "Nossa jornada apenas começou",
        "Amor que transcende o tempo",
        "Você é meu destino",
        "Juntos para sempre, amor infinito",
        "Nosso amor é lindo e verdadeiro",
        "Você é minha pessoa favorita",
        "Cada dia juntos é uma bênção",
        "Nosso amor é inspiração",
        "Você é o amor da minha vida",
        "Para sempre ao teu lado, meu amor"
    ]
    
    # Converter mídias para base64 (limitando para não sobrecarregar)
    total_media = len(media_files)
    
    # Criar lista de mídias com tipo e conteúdo base64
    media_list = []
    for media_path in media_files[:50]:  # Limitar a 50 arquivos
        try:
            if is_video_file(media_path):
                # Processar vídeo
                with open(media_path, "rb") as video_file:
                    video_bytes = video_file.read()
                    video_base64 = base64.b64encode(video_bytes).decode()
                    video_ext = Path(media_path).suffix.lower()
                    mime_type = 'video/mp4' if video_ext == '.mp4' else f'video/{video_ext[1:]}'
                    media_list.append({
                        'type': 'video',
                        'data': f"data:{mime_type};base64,{video_base64}",
                        'mime': mime_type
                    })
            else:
                # Processar imagem
                img_b64 = image_to_base64(media_path)
                if img_b64:
                    media_list.append({
                        'type': 'image',
                        'data': img_b64,
                        'mime': 'image/jpeg'
                    })
        except Exception as e:
            print(f"Erro ao processar {media_path}: {e}")
    
    # Manter compatibilidade (para legendas)
    images_base64 = [m['data'] for m in media_list]
    
    # Música em base64
    music_base64 = None
    if music_files:
        try:
            with open(music_files[0], "rb") as audio_file:
                audio_bytes = audio_file.read()
                music_base64 = base64.b64encode(audio_bytes).decode()
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
    
    # Criar carrossel com HTML/JS
    slide_duration = 6  # segundos
    
    carousel_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: linear-gradient(135deg, 
                    #ffecd2 0%, 
                    #fcb69f 25%, 
                    #ff9a9e 50%, 
                    #fecfef 75%, 
                    #ffecd2 100%
                );
                background-size: 400% 400%;
                animation: gradientShift 25s ease infinite;
            }}
            
            @keyframes gradientShift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            #carousel-container {{
                position: relative;
                width: 100vw;
                height: 80vh;
                overflow: hidden;
            }}
            .carousel-image, .carousel-video {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: contain;
                opacity: 0;
                transition: opacity 1s ease-in-out;
            }}
            .carousel-image.active, .carousel-video.active {{
                opacity: 1;
            }}
            #controls {{
                position: absolute;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 10px;
                z-index: 100;
            }}
            .dot {{
                width: 15px;
                height: 15px;
                border-radius: 50%;
                background: rgba(255,255,255,0.5);
                cursor: pointer;
                transition: all 0.3s;
            }}
            .dot.active {{
                background: white;
                transform: scale(1.3);
            }}
            #info {{
                position: absolute;
                bottom: 80px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0,0,0,0.9);
                color: white;
                padding: 20px 30px;
                border-radius: 15px;
                z-index: 100;
                text-align: center;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255,255,255,0.3);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                max-width: 80%;
            }}
            #verse {{
                font-size: 24px;
                font-style: italic;
                color: #4ecdc4;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                font-family: 'Georgia', serif;
            }}
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
            }}
            #music-player {{
                position: absolute;
                top: 20px;
                right: 200px;
                z-index: 100;
            }}
        </style>
    </head>
    <body>
        <div id="carousel-container">
            {''.join([
                f'<video class="carousel-video" id="media-{i}" controls muted loop><source src="{m["data"]}" type="{m["mime"]}"></video>' 
                if m['type'] == 'video' 
                else f'<img class="carousel-image" id="media-{i}" src="{m["data"]}" />'
                for i, m in enumerate(media_list)
            ])}
        </div>
        
        <div id="info">
            <div id="verse">{poesia_versos[0] if poesia_versos else ""}</div>
            <div id="counter">1 / {len(media_list)}</div>
        </div>
        <div id="controls">
            {''.join([f'<div class="dot" onclick="goTo({i})"></div>' for i in range(len(media_list))])}
        </div>
        
        {f'<audio id="music-player" autoplay loop><source src="data:audio/mpeg;base64,{music_base64}" type="audio/mpeg"></audio>' if music_base64 else ''}
        
        <script>
            let current = 0;
            let total = {len(media_list)};
            const verses = {poesia_versos};
            let viewedPhotos = 0;
            
            function show(index) {{
                // Pausar todos os vídeos e remover classe active
                document.querySelectorAll('.carousel-image, .carousel-video').forEach(media => {{
                    media.classList.remove('active');
                    if (media.tagName === 'VIDEO') {{
                        media.pause();
                        media.currentTime = 0;
                    }}
                }});
                document.querySelectorAll('.dot').forEach(dot => dot.classList.remove('active'));
                
                // Ativar mídia atual
                const currentMedia = document.getElementById('media-' + index);
                currentMedia.classList.add('active');
                
                // Se for vídeo, tocar
                if (currentMedia.tagName === 'VIDEO') {{
                    currentMedia.play();
                }}
                
                document.querySelectorAll('.dot')[index].classList.add('active');
                document.getElementById('counter').textContent = (index + 1) + ' / ' + total;
                
                // Atualizar verso da poesia
                const verseElement = document.getElementById('verse');
                if (verseElement && verses[index]) {{
                    verseElement.textContent = verses[index];
                    verseElement.style.animation = 'fadeIn 1s';
                }}
                
                current = index;
                
                // Incrementar fotos vistas
                if (index > viewedPhotos) {{
                    viewedPhotos = index;
                }}
                
                // Se chegou na última foto, redirecionar para o quiz após 3 segundos
                if (index === total - 1 && viewedPhotos === total - 1) {{
                    setTimeout(() => {{
                        window.location.href = '?page=quiz';
                    }}, 3000);
                }}
            }}
            
            function next() {{
                show((current + 1) % total);
            }}
            
            function goTo(index) {{
                show(index);
            }}
            
            // Controles de teclado
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowLeft') show((current - 1 + total) % total);
                if (e.key === 'ArrowRight') show((current + 1) % total);
            }});
            
            // Adicionar animação fadeIn
            const style = document.createElement('style');
            style.textContent = `
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(10px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
            `;
            document.head.appendChild(style);
            
            // Iniciar carrossel
            show(0);
            setInterval(next, {slide_duration * 1000});
        </script>
    </body>
    </html>
    """
    
    # Renderizar carrossel
    components.html(carousel_html, height=800, scrolling=False)

if __name__ == "__main__":
    main()
