"""
Componentes de estilo CSS centralizados
"""


class StyleComponents:
    """Componentes de estilo reutilizáveis"""
    
    @staticmethod
    def get_global_styles() -> str:
        """Retorna estilos globais da aplicação"""
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Dancing+Script:wght@400;700&family=Cinzel:wght@400;700&display=swap');
            
            /* Esconder elementos do Streamlit */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display: none;}
            [data-testid="stSidebar"] {display: none;}
            [data-testid="stHeader"] {display: none;}
            [data-testid="stToolbar"] {display: none;}
            [data-testid="manage-app"] {
                display: none !important;
                visibility: hidden !important;
            }
            [data-testid="stAppDeployButton"] {
                display: none !important;
                visibility: hidden !important;
            }
            .stAppDeployButton {
                display: none !important;
            }
            
            /* Estilos base */
            html, body, [data-testid="stAppViewContainer"] {
                overflow-x: hidden;
            }
            
            .stApp {
                overflow-x: hidden;
            }
            
            /* Animação de gradiente */
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
        </style>
        """
    
    @staticmethod
    def get_romantic_background() -> str:
        """Retorna CSS para fundo romântico animado"""
        return """
        <style>
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
        """
    
    @staticmethod
    def get_button_styles() -> str:
        """Retorna estilos para botões"""
        return """
        <style>
            div.stButton > button {
                width: 100%;
                background: linear-gradient(135deg, #ff6b6b, #ee5a6f);
                color: white;
                font-family: 'Dancing Script', cursive;
                font-size: 28px;
                font-weight: bold;
                border: none;
                border-radius: 50px;
                padding: 20px 40px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 8px 32px rgba(255, 105, 180, 0.4);
                animation: buttonPulse 2s ease-in-out infinite;
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
        """

