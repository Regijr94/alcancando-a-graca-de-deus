"""
Utilitários para cálculos de data e tempo
"""
from datetime import datetime
from typing import Dict


class DateCalculator:
    """Calculadora de datas para o relacionamento"""
    
    @staticmethod
    def calculate_relationship_time(start_date: datetime = None) -> Dict[str, int]:
        """
        Calcula o tempo de relacionamento desde uma data específica
        
        Args:
            start_date: Data de início do relacionamento (default: 29/05/2021)
            
        Returns:
            Dicionário com anos, meses, dias, horas, minutos, segundos
        """
        if start_date is None:
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

