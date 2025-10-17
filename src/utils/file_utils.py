"""
Utilitários para manipulação de arquivos (imagens, vídeos, músicas)
"""
import os
import base64
from pathlib import Path
from typing import List, Optional
from PIL import Image
from io import BytesIO


class FileManager:
    """Gerenciador de arquivos para a aplicação"""
    
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
    MUSIC_EXTENSIONS = {'.mp3', '.wav', '.ogg', '.m4a'}
    
    @staticmethod
    def get_files_by_extension(directory: str, extensions: set) -> List[str]:
        """
        Obtém lista de arquivos com extensões específicas
        
        Args:
            directory: Diretório para buscar arquivos
            extensions: Set de extensões permitidas
            
        Returns:
            Lista de caminhos completos dos arquivos
        """
        files = []
        
        if not os.path.exists(directory):
            return files
            
        for file in sorted(os.listdir(directory)):
            if Path(file).suffix.lower() in extensions:
                full_path = os.path.join(directory, file)
                if not file.endswith(':Zone.Identifier'):
                    files.append(full_path)
        
        return files
    
    @classmethod
    def get_image_files(cls, directory: str) -> List[str]:
        """Obtém lista de arquivos de imagem"""
        return cls.get_files_by_extension(directory, cls.IMAGE_EXTENSIONS)
    
    @classmethod
    def get_video_files(cls, directory: str) -> List[str]:
        """Obtém lista de arquivos de vídeo"""
        return cls.get_files_by_extension(directory, cls.VIDEO_EXTENSIONS)
    
    @classmethod
    def get_music_files(cls, directory: str) -> List[str]:
        """Obtém lista de arquivos de música"""
        return cls.get_files_by_extension(directory, cls.MUSIC_EXTENSIONS)
    
    @classmethod
    def get_media_files(cls, directory: str) -> List[str]:
        """Obtém lista de arquivos de mídia (imagens e vídeos)"""
        all_extensions = cls.IMAGE_EXTENSIONS | cls.VIDEO_EXTENSIONS
        return cls.get_files_by_extension(directory, all_extensions)
    
    @staticmethod
    def is_video_file(file_path: str) -> bool:
        """Verifica se o arquivo é um vídeo"""
        return Path(file_path).suffix.lower() in FileManager.VIDEO_EXTENSIONS


class ImageProcessor:
    """Processador de imagens com otimização"""
    
    @staticmethod
    def image_to_base64(image_path: str, max_width: int = 1920) -> Optional[str]:
        """
        Converte imagem para base64 com otimização
        
        Args:
            image_path: Caminho da imagem
            max_width: Largura máxima para redimensionamento
            
        Returns:
            String base64 da imagem ou None se houver erro
        """
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
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85, optimize=True)
            img_bytes = buffer.getvalue()
            
            # Converter para base64
            img_base64 = base64.b64encode(img_bytes).decode()
            return f"data:image/jpeg;base64,{img_base64}"
        except Exception as e:
            print(f"Erro ao processar {image_path}: {e}")
            return None
    
    @staticmethod
    def video_to_base64(video_path: str) -> Optional[str]:
        """Converte vídeo para base64"""
        try:
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
                video_base64 = base64.b64encode(video_bytes).decode()
                
                # Determinar mime type baseado na extensão
                ext = Path(video_path).suffix.lower()
                mime_types = {
                    '.mp4': 'video/mp4',
                    '.webm': 'video/webm',
                    '.avi': 'video/x-msvideo',
                    '.mov': 'video/quicktime',
                    '.mkv': 'video/x-matroska'
                }
                mime_type = mime_types.get(ext, 'video/mp4')
                
                return f"data:{mime_type};base64,{video_base64}"
        except Exception as e:
            print(f"Erro ao processar vídeo {video_path}: {e}")
            return None
    
    @staticmethod
    def audio_to_base64(audio_path: str) -> Optional[str]:
        """Converte áudio para base64"""
        try:
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                return base64.b64encode(audio_bytes).decode()
        except Exception as e:
            print(f"Erro ao processar áudio {audio_path}: {e}")
            return None

