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
    page_title="Reginaldo e Beatriz - Galeria de Amor",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado
st.markdown("""
<style>
    .main > div {
        padding-top: 0rem;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

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
    
    # Página principal (galeria)
    show_gallery_page()

def show_intro_page():
    """Página de introdução com mensagem animada e tema romântico"""
    
    # CSS para o fundo romântico - aplicado globalmente no Streamlit
    st.markdown("""
    <style>
        /* Remover padding padrão do Streamlit */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Fundo romântico animado */
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
        
        /* Overlay romântico */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(255, 182, 193, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 105, 180, 0.2) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(255, 192, 203, 0.3) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Obter música para tocar
    music_dir = "music"
    music_files = get_music_files(music_dir)
    music_base64 = None
    
    if music_files:
        try:
            with open(music_files[0], "rb") as audio_file:
                audio_bytes = audio_file.read()
                music_base64 = base64.b64encode(audio_bytes).decode()
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
    
    intro_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Great+Vibes&family=Pacifico&family=Crimson+Text:ital@1&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
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
            }}
            
            /* Overlay romântico */
            body::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 20% 50%, rgba(255, 182, 193, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 80%, rgba(255, 105, 180, 0.2) 0%, transparent 50%),
                    radial-gradient(circle at 40% 20%, rgba(255, 192, 203, 0.3) 0%, transparent 50%);
                pointer-events: none;
                z-index: 1;
            }}
            
            @keyframes gradientShift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            /* Corações flutuantes de fundo - mais suaves e românticos */
            .heart {{
                position: absolute;
                font-size: 30px;
                opacity: 0;
                animation: floatHearts 18s ease-in-out infinite;
                pointer-events: none;
                z-index: 2;
                filter: drop-shadow(0 0 10px rgba(255, 105, 180, 0.6));
            }}
            
            .heart:nth-child(1) {{ left: 5%; font-size: 28px; animation-delay: 0s; }}
            .heart:nth-child(2) {{ left: 15%; font-size: 36px; animation-delay: 2.5s; }}
            .heart:nth-child(3) {{ left: 25%; font-size: 32px; animation-delay: 5s; }}
            .heart:nth-child(4) {{ left: 35%; font-size: 30px; animation-delay: 1.5s; }}
            .heart:nth-child(5) {{ left: 45%; font-size: 34px; animation-delay: 3.5s; }}
            .heart:nth-child(6) {{ left: 55%; font-size: 42px; animation-delay: 6s; }}
            .heart:nth-child(7) {{ left: 65%; font-size: 26px; animation-delay: 7.5s; }}
            .heart:nth-child(8) {{ left: 75%; font-size: 38px; animation-delay: 4s; }}
            .heart:nth-child(9) {{ left: 85%; font-size: 31px; animation-delay: 8.5s; }}
            .heart:nth-child(10) {{ left: 95%; font-size: 35px; animation-delay: 10s; }}
            .heart:nth-child(21) {{ left: 10%; font-size: 24px; animation-delay: 11s; }}
            .heart:nth-child(22) {{ left: 20%; font-size: 40px; animation-delay: 12s; }}
            .heart:nth-child(23) {{ left: 30%; font-size: 29px; animation-delay: 13s; }}
            .heart:nth-child(24) {{ left: 40%; font-size: 33px; animation-delay: 14s; }}
            .heart:nth-child(25) {{ left: 50%; font-size: 27px; animation-delay: 15s; }}
            
            @keyframes floatHearts {{
                0% {{ 
                    transform: translateY(110vh) translateX(0) rotate(-15deg) scale(0.3); 
                    opacity: 0; 
                }}
                5% {{ 
                    opacity: 0.6; 
                }}
                15% {{ 
                    opacity: 0.9; 
                    transform: translateY(85vh) translateX(20px) rotate(15deg) scale(0.9);
                }}
                30% {{ 
                    opacity: 1; 
                    transform: translateY(70vh) translateX(-10px) rotate(-20deg) scale(1.1);
                }}
                45% {{ 
                    opacity: 0.95; 
                    transform: translateY(55vh) translateX(15px) rotate(25deg) scale(1);
                }}
                60% {{ 
                    opacity: 0.9; 
                    transform: translateY(40vh) translateX(-20px) rotate(-30deg) scale(1.15);
                }}
                75% {{ 
                    opacity: 0.8; 
                    transform: translateY(25vh) translateX(10px) rotate(20deg) scale(0.95);
                }}
                90% {{ 
                    opacity: 0.5; 
                    transform: translateY(10vh) translateX(-15px) rotate(-25deg) scale(0.8);
                }}
                100% {{ 
                    transform: translateY(-10vh) translateX(0) rotate(0deg) scale(0.4); 
                    opacity: 0; 
                }}
            }}
            .intro-container {{
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
            }}
            
            #typed-text {{
                font-family: 'Great Vibes', cursive;
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
            }}
            .cursor {{
                display: inline-block;
                width: 4px;
                background-color: white;
                margin-left: 3px;
                animation: blink 0.7s infinite;
            }}
            #infinity-container {{
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
            }}
            #infinity {{
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
            }}
            #infinity-text {{
                font-family: 'Great Vibes', cursive;
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
            }}
            @keyframes pulse {{
                0%, 100% {{ 
                    opacity: 0.4; 
                    transform: scale(1) rotate(0deg);
                }}
                50% {{ 
                    opacity: 1; 
                    transform: scale(1.15) rotate(8deg);
                }}
            }}
            @keyframes blink {{
                0%, 50% {{ opacity: 1; }}
                51%, 100% {{ opacity: 0; }}
            }}
            @keyframes fallAndDisappear {{
                0% {{ 
                    transform: translateY(0) scale(1) rotate(0deg);
                    opacity: 1;
                }}
                50% {{
                    transform: translateY(150px) scale(0.9) rotate(-5deg);
                    opacity: 0.5;
                }}
                100% {{ 
                    transform: translateY(300px) scale(0.5) rotate(-10deg);
                    opacity: 0;
                }}
            }}
            .fall-and-disappear {{
                animation: fallAndDisappear 1.5s ease-in forwards;
            }}
            @keyframes fadeInInfinity {{
                from {{ 
                    opacity: 0;
                    transform: scale(0.5);
                }}
                to {{ 
                    opacity: 1;
                    transform: scale(1);
                }}
            }}
            @keyframes fadeInText {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            
            /* Otimização para celular e tablets */
            @media (max-width: 768px) {{
                #typed-text {{
                    font-size: 28px;
                    min-height: 250px;
                    padding: 20px;
                }}
                #infinity {{
                    font-size: 80px;
                }}
                #infinity-text {{
                    font-size: 24px;
                    padding: 0 15px;
                }}
                .intro-container {{
                    padding: 20px;
                    max-width: 95%;
                }}
            }}
            
            @media (max-width: 480px) {{
                #typed-text {{
                    font-size: 22px;
                    min-height: 200px;
                    padding: 15px;
                }}
                #infinity {{
                    font-size: 60px;
                }}
                #infinity-text {{
                    font-size: 20px;
                    padding: 0 10px;
                }}
                .intro-container {{
                    padding: 15px;
                }}
            }}
            
            @keyframes fadeOut {{
                from {{ opacity: 1; }}
                to {{ opacity: 0; }}
            }}
            .fade-in-infinity {{
                animation: fadeInInfinity 1.5s forwards;
            }}
            .fade-out {{
                animation: fadeOut 2s forwards;
            }}
            
            /* Estrelas piscando */
            .star {{
                position: absolute;
                color: white;
                font-size: 20px;
                opacity: 0;
                animation: twinkle 3s infinite;
                pointer-events: none;
                z-index: 2;
            }}
            .star:nth-child(11) {{ top: 10%; left: 20%; animation-delay: 0s; }}
            .star:nth-child(12) {{ top: 20%; left: 80%; animation-delay: 1s; }}
            .star:nth-child(13) {{ top: 30%; left: 10%; animation-delay: 2s; }}
            .star:nth-child(14) {{ top: 40%; left: 90%; animation-delay: 0.5s; }}
            .star:nth-child(15) {{ top: 60%; left: 15%; animation-delay: 1.5s; }}
            .star:nth-child(16) {{ top: 70%; left: 85%; animation-delay: 2.5s; }}
            .star:nth-child(17) {{ top: 80%; left: 30%; animation-delay: 0.8s; }}
            .star:nth-child(18) {{ top: 15%; left: 60%; animation-delay: 1.8s; }}
            
            @keyframes twinkle {{
                0%, 100% {{ opacity: 0; transform: scale(0.5); }}
                50% {{ opacity: 1; transform: scale(1.2); }}
            }}
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
        """ + (f'<audio id="intro-music" autoplay loop style="display: none;"><source src="data:audio/mpeg;base64,{music_base64}" type="audio/mpeg"></audio>' if music_base64 else '') + """
        
        <script>
            const text = "Meu amor, agora construí minha própria aplicação para te dizer o quanto te amo, e sou feliz por ter você.";
            const typedTextElement = document.getElementById('typed-text');
            const infinityContainer = document.getElementById('infinity-container');
            let index = 0;
            
            async function typeText() {
                // Digitar texto letra por letra
                while (index < text.length) {
                    typedTextElement.textContent = text.substring(0, index + 1);
                    
                    // Adicionar cursor piscando
                    const cursor = document.createElement('span');
                    cursor.className = 'cursor';
                    cursor.innerHTML = '&nbsp;';
                    typedTextElement.appendChild(cursor);
                    
                    index++;
                    
                    // Velocidade de digitação (em ms)
                    await new Promise(resolve => setTimeout(resolve, 80));
                }
                
                // Remover cursor
                const cursor = typedTextElement.querySelector('.cursor');
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
                
                // Mudar para a galeria
                window.location.href = '?page=gallery';
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
                font-family: 'Great Vibes', cursive;
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
                font-family: 'Great Vibes', cursive;
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
            const text = "Meu amor, agora construí minha própria aplicação para te dizer o quanto te amo, e sou feliz por ter você.";
            const typedTextElement = document.getElementById('typed-text');
            const infinityContainer = document.getElementById('infinity-container');
            let index = 0;
            
            function typeText() {
                if (index < text.length) {
                    typedTextElement.textContent = text.substring(0, index + 1);
                    
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
                    
                    // Aguardar 2 segundos
                    setTimeout(() => {
                        // Fade out do texto
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
            
            // Iniciar digitação
            typeText();
        </script>
    </body>
    </html>
    """
    
    # Renderizar com components.html
    components.html(typing_html, height=700, scrolling=False)
    
    # Player de música
    if music_base64:
        st.markdown(f'''
        <audio autoplay loop style="display: none;">
            <source src="data:audio/mpeg;base64,{music_base64}" type="audio/mpeg">
        </audio>
        ''', unsafe_allow_html=True)
    
    # Botão manual para avançar
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💕 Continuar para a Galeria 💕", key="continue_btn", use_container_width=True):
            st.session_state.page = 'gallery'
            st.rerun()
    
    # Auto-avançar após tempo suficiente para todas as animações
    # Digitação (~8s) + pausa (2s) + fade out (1s) + infinito (8s) = ~19s
    import time
    time.sleep(19)
    st.session_state.page = 'quiz'
    st.rerun()

def show_quiz_page():
    """Página do quiz romântico sobre o relacionamento"""
    
    # CSS para fundo romântico
    st.markdown("""
    <style>
        /* Fundo romântico para o quiz */
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
        
        # Auto-avançar para galeria após 5 segundos
        import time
        time.sleep(5)
        st.session_state.page = 'gallery'
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
            color: #fff;
            text-shadow: 
                3px 3px 6px rgba(0,0,0,0.4),
                0 0 30px rgba(255, 182, 193, 0.8),
                0 0 60px rgba(255, 105, 180, 0.6);
            margin-bottom: 10px;
        ">
            💕 Quiz do Nosso Amor 💕
        </h1>
        <p style="
            font-family: 'Dancing Script', cursive;
            font-size: 28px;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        ">
            Pergunta {st.session_state.quiz_current_question + 1} de {total_questions}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Container da pergunta atual
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.4);
        padding: 40px;
        margin: 40px auto;
        max-width: 900px;
        box-shadow: 0 8px 32px rgba(255, 105, 180, 0.2);
    ">
        <h3 style="
            font-family: 'Dancing Script', cursive;
            font-size: 42px;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 30px;
            text-align: center;
            line-height: 1.5;
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
            max-width: 800px;
            margin: 40px auto;
        }
        
        div[data-testid="stRadio"] > label {
            font-family: 'Dancing Script', cursive !important;
            font-size: 28px !important;
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
            margin-bottom: 20px !important;
            text-align: center !important;
            display: block !important;
        }
        
        div[data-testid="stRadio"] > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }
        
        div[data-testid="stRadio"] label[data-baseweb="radio"] {
            background: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 15px !important;
            padding: 20px 30px !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            transition: all 0.3s ease !important;
            min-width: 600px !important;
            cursor: pointer !important;
        }
        
        div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
            background: rgba(255, 255, 255, 0.25) !important;
            border-color: rgba(255, 182, 193, 0.6) !important;
            transform: scale(1.02) !important;
        }
        
        div[data-testid="stRadio"] label[data-baseweb="radio"] span {
            font-family: 'Dancing Script', cursive !important;
            font-size: 24px !important;
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
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
        popup_color = "#90ee90" if st.session_state.popup_type == "success" else "#ff6b9d" if st.session_state.popup_type == "special" else "#ff6347"
        st.markdown(f"""
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 9999;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 182, 193, 0.95));
            backdrop-filter: blur(20px);
            border-radius: 30px;
            border: 3px solid {popup_color};
            padding: 60px;
            min-width: 500px;
            text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            animation: popupBounce 0.5s ease-out;
        ">
            <p style="
                font-family: 'Great Vibes', cursive;
                font-size: 48px;
                color: {popup_color};
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                margin: 0;
                line-height: 1.4;
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
            background: rgba(0, 0, 0, 0.5);
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

def show_gallery_page():
    """Página principal com galeria e contador"""
    # Diretórios
    pictures_dir = "pictures"
    music_dir = "music"
    
    # Obter arquivos
    image_files = get_image_files(pictures_dir)
    music_files = get_music_files(music_dir)
    
    if not image_files:
        st.error("❌ Nenhuma foto encontrada no diretório 'pictures'!")
        return
    
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
    
    # Converter imagens para base64 (limitando para não sobrecarregar)
    st.info(f"📸 Carregando {len(image_files)} fotos...")
    images_base64 = []
    for img_path in image_files[:50]:  # Limitar a 50 fotos
        img_b64 = image_to_base64(img_path)
        if img_b64:
            images_base64.append(img_b64)
    
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
                background: #000;
            }}
            #carousel-container {{
                position: relative;
                width: 100vw;
                height: 80vh;
                overflow: hidden;
            }}
            .carousel-image {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: contain;
                opacity: 0;
                transition: opacity 1s ease-in-out;
            }}
            .carousel-image.active {{
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
            {''.join([f'<img class="carousel-image" id="img-{i}" src="{img}" />' for i, img in enumerate(images_base64)])}
        </div>
        
        <div id="info">
            <div id="verse">{poesia_versos[0] if poesia_versos else ""}</div>
            <div id="counter">1 / {len(images_base64)}</div>
        </div>
        <div id="controls">
            {''.join([f'<div class="dot" onclick="goTo({i})"></div>' for i in range(len(images_base64))])}
        </div>
        
        {f'<audio id="music-player" autoplay loop><source src="data:audio/mpeg;base64,{music_base64}" type="audio/mpeg"></audio>' if music_base64 else ''}
        
        <script>
            let current = 0;
            let total = {len(images_base64)};
            const verses = {poesia_versos};
            
            function show(index) {{
                document.querySelectorAll('.carousel-image').forEach(img => img.classList.remove('active'));
                document.querySelectorAll('.dot').forEach(dot => dot.classList.remove('active'));
                
                document.getElementById('img-' + index).classList.add('active');
                document.querySelectorAll('.dot')[index].classList.add('active');
                document.getElementById('counter').textContent = (index + 1) + ' / ' + total;
                
                // Atualizar verso da poesia
                const verseElement = document.getElementById('verse');
                if (verseElement && verses[index]) {{
                    verseElement.textContent = verses[index];
                    verseElement.style.animation = 'fadeIn 1s';
                }}
                
                current = index;
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
