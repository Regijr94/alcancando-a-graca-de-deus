"""
Gerenciador de páginas e navegação
"""
import streamlit as st
from typing import Callable, Dict, Optional
from enum import Enum


class PageType(Enum):
    """Tipos de páginas da aplicação"""
    INTRO = "intro"
    GALLERY = "gallery"
    QUIZ = "quiz"
    PROPOSAL = "proposal"


class PageManager:
    """Gerenciador de navegação entre páginas"""
    
    def __init__(self):
        self.pages: Dict[PageType, Callable] = {}
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Inicializa variáveis de sessão"""
        if 'page' not in st.session_state:
            st.session_state.page = PageType.INTRO.value
        
        if 'page_transition' not in st.session_state:
            st.session_state.page_transition = False
        
        # Estados do quiz
        if 'quiz_current_question' not in st.session_state:
            st.session_state.quiz_current_question = 0
        
        if 'quiz_answers' not in st.session_state:
            st.session_state.quiz_answers = {}
        
        if 'quiz_show_result' not in st.session_state:
            st.session_state.quiz_show_result = False
        
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = False
        
        if 'popup_message' not in st.session_state:
            st.session_state.popup_message = ""
        
        if 'popup_type' not in st.session_state:
            st.session_state.popup_type = "success"
        
        # Estado da proposta
        if 'proposal_answer' not in st.session_state:
            st.session_state.proposal_answer = None
    
    def register_page(self, page_type: PageType, page_function: Callable):
        """
        Registra uma função de página
        
        Args:
            page_type: Tipo da página
            page_function: Função que renderiza a página
        """
        self.pages[page_type] = page_function
    
    def navigate_to(self, page_type: PageType, with_transition: bool = True):
        """
        Navega para uma página específica
        
        Args:
            page_type: Tipo da página de destino
            with_transition: Se deve usar transição suave
        """
        if with_transition:
            st.session_state.page_transition = True
        
        st.session_state.page = page_type.value
        st.rerun()
    
    def get_current_page(self) -> PageType:
        """Retorna o tipo da página atual"""
        page_value = st.session_state.get('page', PageType.INTRO.value)
        return PageType(page_value)
    
    def render_current_page(self):
        """Renderiza a página atual"""
        current_page = self.get_current_page()
        
        # Verificar query params para navegação externa
        self._check_query_params()
        
        # Renderizar transição se necessário
        if st.session_state.get('page_transition', False):
            self._render_transition()
            st.session_state.page_transition = False
        
        # Renderizar página
        page_function = self.pages.get(current_page)
        if page_function:
            page_function()
        else:
            st.error(f"Página não encontrada: {current_page}")
    
    def _check_query_params(self):
        """Verifica parâmetros de query para navegação"""
        try:
            query_params = st.query_params
            if 'page' in query_params:
                page_value = query_params['page']
                if page_value in [p.value for p in PageType]:
                    st.session_state.page = page_value
        except:
            try:
                query_params = st.experimental_get_query_params()
                if 'page' in query_params:
                    page_value = query_params['page'][0]
                    if page_value in [p.value for p in PageType]:
                        st.session_state.page = page_value
            except:
                pass
    
    def _render_transition(self):
        """Renderiza transição suave entre páginas"""
        transition_html = """
        <style>
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            .page-container {
                animation: fadeIn 0.5s ease-in;
            }
        </style>
        <div class="page-container"></div>
        """
        st.markdown(transition_html, unsafe_allow_html=True)
    
    def reset_quiz(self):
        """Reseta o estado do quiz"""
        st.session_state.quiz_current_question = 0
        st.session_state.quiz_answers = {}
        st.session_state.quiz_show_result = False
        st.session_state.show_popup = False
        st.session_state.popup_message = ""
        st.session_state.popup_type = "success"

