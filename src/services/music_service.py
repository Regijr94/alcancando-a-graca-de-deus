"""
Serviço de gerenciamento de música
"""
from typing import Optional, List
from ..utils.file_utils import FileManager, ImageProcessor


class MusicService:
    """Serviço para gerenciar música da aplicação"""
    
    def __init__(self, music_directory: str = "music"):
        self.music_directory = music_directory
        self.file_manager = FileManager()
        self.processor = ImageProcessor()
    
    def get_music_for_page(self, page: str) -> Optional[str]:
        """
        Obtém música apropriada para a página
        
        Args:
            page: Nome da página ('intro', 'gallery', 'quiz', 'proposal')
            
        Returns:
            Base64 da música ou None
        """
        music_files = self.file_manager.get_music_files(self.music_directory)
        
        if not music_files:
            return None
        
        alceu_music = None
        roberta_music = None
        
        # Identificar músicas
        for music_file in music_files:
            if any(keyword in music_file for keyword in ["Alceu", "alceu", "Belle"]):
                alceu_music = self.processor.audio_to_base64(music_file)
            elif any(keyword in music_file for keyword in ["Roberta", "roberta", "Janeiro"]):
                roberta_music = self.processor.audio_to_base64(music_file)
        
        # Escolher música baseada na página
        if page == 'proposal':
            return roberta_music if roberta_music else alceu_music
        else:  # intro, quiz, gallery
            return alceu_music if alceu_music else roberta_music
    
    def generate_music_player_html(self, page: str) -> str:
        """
        Gera HTML do player de música para uma página específica
        
        Args:
            page: Nome da página
            
        Returns:
            HTML do player
        """
        music_base64 = self.get_music_for_page(page)
        
        if not music_base64:
            return ""
        
        return f"""
        <audio id="global-music-player" loop style="display: none;">
            <source src="data:audio/mpeg;base64,{music_base64}" type="audio/mpeg">
        </audio>
        <script>
            // Player de música persistente que não recarrega entre páginas
            (function() {{
                const audioPlayer = document.getElementById('global-music-player');
                const musicKey = 'music_playing_{page}';
                
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

