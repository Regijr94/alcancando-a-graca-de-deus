"""
Aplicação de Pedido de Casamento - Versão Modularizada
Aplicando princípios de Engenharia de Software e Clean Code
"""
import streamlit as st
import streamlit.components.v1 as components
import time
from src.services.page_manager import PageManager, PageType
from src.services.music_service import MusicService
from src.services.quiz_service import QuizService
from src.utils.file_utils import FileManager, ImageProcessor
from src.utils.date_utils import DateCalculator
from src.components.styles import StyleComponents


# ============================================================================
# CONFIGURAÇÃO DA APLICAÇÃO
# ============================================================================

class WeddingProposalApp:
    """Aplicação principal de pedido de casamento"""
    
    def __init__(self):
        self.configure_page()
        self.page_manager = PageManager()
        self.music_service = MusicService()
        self.quiz_service = QuizService()
        self.file_manager = FileManager()
        self.image_processor = ImageProcessor()
        self.date_calculator = DateCalculator()
        self.styles = StyleComponents()
        
        # Registrar páginas
        self._register_pages()
    
    def configure_page(self):
        """Configura página do Streamlit"""
        st.set_page_config(
            page_title="Reginaldo e Beatriz - Uma história de amor",
            page_icon="💕",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    def _register_pages(self):
        """Registra todas as páginas da aplicação"""
        self.page_manager.register_page(PageType.INTRO, self.show_intro_page)
        self.page_manager.register_page(PageType.GALLERY, self.show_gallery_page)
        self.page_manager.register_page(PageType.QUIZ, self.show_quiz_page)
        self.page_manager.register_page(PageType.PROPOSAL, self.show_proposal_page)
    
    def run(self):
        """Executa a aplicação"""
        # Aplicar estilos globais
        st.markdown(self.styles.get_global_styles(), unsafe_allow_html=True)
        
        # Adicionar música
        current_page = self.page_manager.get_current_page()
        music_html = self.music_service.generate_music_player_html(current_page.value)
        if music_html:
            st.markdown(music_html, unsafe_allow_html=True)
        
        # Renderizar página atual
        self.page_manager.render_current_page()
    
    # ========================================================================
    # PÁGINAS
    # ========================================================================
    
    def show_intro_page(self):
        """Página de introdução com mensagem animada"""
        # Carregar imagens para mosaico
        image_files = self.file_manager.get_image_files("pictures")
        
        # Criar mosaico de fundo
        import random
        selected_images = random.sample(image_files, min(20, len(image_files))) if image_files else []
        images_base64 = []
        
        for img_path in selected_images:
            img_b64 = self.image_processor.image_to_base64(img_path, max_width=800)
            if img_b64:
                images_base64.append(img_b64)
        
        # Gerar CSS do mosaico
        if images_base64:
            mosaic_images = ', '.join([f'url({img})' for img in images_base64[:16]])
            mosaic_style = f"""
            <style>
                .stApp {{
                    background-image: {mosaic_images};
                    background-size: 25% 25%;
                    background-position: 
                        0% 0%, 25% 0%, 50% 0%, 75% 0%,
                        0% 25%, 25% 25%, 50% 25%, 75% 25%,
                        0% 50%, 25% 50%, 50% 50%, 75% 50%,
                        0% 75%, 25% 75%, 50% 75%, 75% 75%;
                    background-repeat: no-repeat;
                }}
            </style>
            """
        else:
            mosaic_style = """
            <style>
                .stApp {
                    background: linear-gradient(135deg, #ffecd2, #fcb69f, #ff9a9e, #fecfef);
                }
            </style>
            """
        
        st.markdown(mosaic_style, unsafe_allow_html=True)
        
        # HTML da página de introdução
        intro_html = self._generate_intro_html(images_base64)
        components.html(intro_html, height=700, scrolling=False)
        
        # Auto-avançar após 19 segundos
        time.sleep(19)
        self.page_manager.navigate_to(PageType.GALLERY)
    
    def _generate_intro_html(self, images_base64: list) -> str:
        """Gera HTML da página de introdução"""
        # Preparar fundo
        if images_base64:
            mosaic_images = ', '.join([f'url({img})' for img in images_base64[:16]])
            body_background = f"""
                background-image: {mosaic_images};
                background-size: 25% 25%;
                background-position: 
                    0% 0%, 25% 0%, 50% 0%, 75% 0%,
                    0% 25%, 25% 25%, 50% 25%, 75% 25%,
                    0% 50%, 25% 50%, 50% 50%, 75% 50%,
                    0% 75%, 25% 75%, 50% 75%, 75% 75%;
                background-repeat: no-repeat;
            """
        else:
            body_background = """
                background: linear-gradient(135deg, #ffecd2, #fcb69f, #ff9a9e, #fecfef);
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Dancing+Script:wght@400;700&display=swap" rel="stylesheet">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    {body_background}
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    overflow: hidden;
                    font-family: 'Dancing Script', cursive;
                }}
                
                #intro-container {{
                    text-align: center;
                    z-index: 10;
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(20px);
                    padding: 60px;
                    border-radius: 30px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    border: 3px solid rgba(255, 255, 255, 0.4);
                    max-width: 90%;
                    margin: 20px;
                }}
                
                #typed-text {{
                    font-size: 48px;
                    color: #fff;
                    text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.6);
                    min-height: 200px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                }}
                
                #infinity-symbol {{
                    font-size: 100px;
                    color: #fff;
                    text-shadow: 4px 4px 12px rgba(0, 0, 0, 0.6);
                    animation: pulse 2s infinite;
                    margin: 30px 0;
                }}
                
                #infinity-text {{
                    font-family: 'Great Vibes', cursive;
                    font-size: 56px;
                    color: #fff;
                    text-shadow: 3px 3px 8px rgba(0, 0, 0, 0.6);
                    margin-top: 20px;
                }}
                
                #skip-btn {{
                    display: none;
                    margin-top: 30px;
                    padding: 15px 40px;
                    font-size: 24px;
                    font-family: 'Dancing Script', cursive;
                    background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
                    color: white;
                    border: none;
                    border-radius: 50px;
                    cursor: pointer;
                    transition: all 0.3s;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                }}
                
                #skip-btn:hover {{
                    transform: scale(1.05);
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
                }}
                
                @keyframes pulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.1); }}
                }}
                
                /* Responsividade */
                @media (max-width: 768px) {{
                    #intro-container {{
                        padding: 30px 20px;
                        max-width: 95%;
                    }}
                    #typed-text {{
                        font-size: 28px;
                        min-height: 150px;
                    }}
                    #infinity-symbol {{
                        font-size: 60px;
                    }}
                    #infinity-text {{
                        font-size: 36px;
                    }}
                    #skip-btn {{
                        font-size: 18px;
                        padding: 12px 30px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div id="intro-container">
                <div id="typed-text"></div>
                <div id="infinity-symbol">∞</div>
                <div id="infinity-text">Para sempre</div>
                <button id="skip-btn" onclick="window.parent.postMessage('skip', '*')">Pular ⏭️</button>
            </div>
            
            <script>
                const text = "Olá meu amor, prepare-se para uma experiência inesquecível...";
                const typingSpeed = 80;
                let charIndex = 0;
                
                function typeText() {{
                    const typedTextElement = document.getElementById('typed-text');
                    if (charIndex < text.length) {{
                        typedTextElement.textContent += text.charAt(charIndex);
                        charIndex++;
                        setTimeout(typeText, typingSpeed);
                    }}
                }}
                
                // Mostrar botão pular após 5 segundos
                setTimeout(() => {{
                    document.getElementById('skip-btn').style.display = 'inline-block';
                }}, 5000);
                
                // Iniciar digitação
                setTimeout(typeText, 500);
            </script>
        </body>
        </html>
        """
    
    def show_gallery_page(self):
        """Página da galeria de fotos/vídeos"""
        # Implementação similar à original, mas usando os serviços
        st.markdown(self.styles.get_romantic_background(), unsafe_allow_html=True)
        
        # TODO: Implementar galeria usando componentes modularizados
        st.info("🎨 Galeria em desenvolvimento na versão modular...")
        
        if st.button("Ir para Quiz"):
            self.page_manager.navigate_to(PageType.QUIZ)
    
    def show_quiz_page(self):
        """Página do quiz"""
        st.markdown(self.styles.get_romantic_background(), unsafe_allow_html=True)
        
        # TODO: Implementar quiz usando QuizService
        st.info("📝 Quiz em desenvolvimento na versão modular...")
        
        if st.button("Ir para Pedido"):
            self.page_manager.navigate_to(PageType.PROPOSAL)
    
    def show_proposal_page(self):
        """Página do pedido de casamento"""
        st.markdown(self.styles.get_romantic_background(), unsafe_allow_html=True)
        
        # TODO: Implementar pedido usando componentes modularizados
        st.info("💍 Pedido de casamento em desenvolvimento na versão modular...")


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    app = WeddingProposalApp()
    app.run()

