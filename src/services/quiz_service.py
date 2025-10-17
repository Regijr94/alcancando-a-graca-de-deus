"""
Serviço de gerenciamento do quiz
"""
from typing import Dict, List, Tuple
import random


class QuizService:
    """Serviço para gerenciar lógica do quiz"""
    
    @staticmethod
    def get_questions() -> List[Dict]:
        """Retorna lista de perguntas do quiz"""
        return [
            {
                'num': 1,
                'question': 'Onde nos conhecemos?',
                'options': ['Tinder', 'Instagram', 'Badoo', 'Amigos em comum'],
                'correct': 0,
                'key': 'q1'
            },
            {
                'num': 2,
                'question': 'Qual foi nosso primeiro encontro?',
                'options': ['Cinema', 'Restaurante', 'Parque', 'Shopping'],
                'correct': 1,
                'key': 'q2'
            },
            {
                'num': 3,
                'question': 'Qual foi o apelido carinhoso que te dei primeiro?',
                'options': ['Meu amor', 'Bebê', 'Linda', 'Princesa'],
                'correct': 1,
                'key': 'q3'
            },
            {
                'num': 4,
                'question': 'Qual é a nossa música?',
                'options': ['Ed Sheeran - Perfect', 'John Legend - All of Me', 
                           'Bruno Mars - Just The Way You Are', 'Alceu Valença - La Belle de Jour'],
                'correct': 3,
                'key': 'q4'
            },
            {
                'num': 5,
                'question': 'Qual foi nossa primeira viagem juntos?',
                'options': ['Praia', 'Montanha', 'Campo', 'Cidade histórica'],
                'correct': 0,
                'key': 'q5'
            },
            {
                'num': 6,
                'question': 'O que eu mais admiro em você?',
                'options': ['Inteligência', 'Carinho', 'Determinação', 'Todas as anteriores'],
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
    
    @staticmethod
    def get_success_message() -> str:
        """Retorna mensagem aleatória de acerto"""
        messages = [
            "✅ Ai sim bebê,<br>você é o amor da<br>minha vida ❤️",
            "💕 Acertou meu amor!<br>Você me conhece<br>tão bem! 💕",
            "🌟 Isso aí bebê!<br>Você é demais! 🌟",
            "💖 Perfeito!<br>Meu coração é seu! 💖",
            "✨ Maravilhosa!<br>Como sempre! ✨",
            "❤️ Acertou meu bem!<br>Te amo demais! ❤️"
        ]
        return random.choice(messages)
    
    @staticmethod
    def get_error_message(correct_answer: str) -> str:
        """Retorna mensagem aleatória de erro com a resposta correta"""
        messages = [
            f"❌ Ops bebê!<br>A resposta certa é:<br><b>{correct_answer}</b>",
            f"💔 Errou meu amor!<br>Mas tudo bem...<br>Era: <b>{correct_answer}</b>",
            f"😅 Quase lá bebê!<br>A correta era:<br><b>{correct_answer}</b>",
            f"🤔 Não foi dessa vez!<br>A certa é:<br><b>{correct_answer}</b>"
        ]
        return random.choice(messages)
    
    @staticmethod
    def calculate_statistics(answers: Dict[str, int], questions: List[Dict]) -> Dict:
        """
        Calcula estatísticas do quiz
        
        Args:
            answers: Dicionário de respostas do usuário
            questions: Lista de perguntas
            
        Returns:
            Dicionário com estatísticas
        """
        correct_count = 0
        wrong_questions = []
        
        for q in questions[:9]:  # Excluir pergunta 10
            if answers.get(q['key']) == q['correct']:
                correct_count += 1
            else:
                wrong_questions.append(q['num'])
        
        total = 9
        percentage = (correct_count / total) * 100
        wrong_count = total - correct_count
        
        # Mensagem personalizada baseada na performance
        if percentage == 100:
            performance_msg = "PERFEIÇÃO ABSOLUTA! 🏆<br>Você me conhece melhor<br>que eu mesma! 💖"
            emoji = "🌟"
        elif percentage >= 80:
            performance_msg = "INCRÍVEL! 🎉<br>Você realmente presta<br>atenção em tudo! 💕"
            emoji = "⭐"
        elif percentage >= 60:
            performance_msg = "MUITO BOM! 😊<br>Você me conhece<br>bastante! ❤️"
            emoji = "💫"
        elif percentage >= 40:
            performance_msg = "BOM COMEÇO! 😅<br>Mas ainda tem<br>muito pra aprender! 💗"
            emoji = "✨"
        else:
            performance_msg = "VAMOS ESTUDAR<br>MAIS BEBÊ! 📚<br>Ainda temos tempo! 💝"
            emoji = "💕"
        
        return {
            'correct_count': correct_count,
            'wrong_count': wrong_count,
            'total': total,
            'percentage': percentage,
            'performance_msg': performance_msg,
            'emoji': emoji,
            'wrong_questions': wrong_questions
        }

