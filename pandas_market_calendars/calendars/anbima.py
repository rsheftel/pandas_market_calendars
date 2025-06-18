from datetime import time

from pandas import Timestamp
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    Day,
    Easter,
    GoodFriday,
    Holiday,
)
from zoneinfo import ZoneInfo

from pandas_market_calendars.market_calendar import FRIDAY, MarketCalendar

from pandas_market_calendars.holidays.br import (
    ConfraternizacaoUniversal,
    CarnavalSegunda,
    CarnavalTerca,
    PaixaoCristo,
    CorpusChristi,
    Tiradentes,
    DiaTrabalho,
    IndependenciaBrasil,
    NossaSenhoraAparecida,
    Finados,
    ProclamacaoRepublica,
    ConscienciaNegraNacional,
    Natal
)

class ANBIMAHolidayCalendar(MarketCalendar):
    """
    Calendário de feriados nacionais brasileiros segundo ANBIMA
    
    Baseado no arquivo "feriados_nacionais.xls" da ANBIMA que contém
    os feriados nacionais do Brasil de 2001 a 2099.
    
    Feriados regularmente observados:
    - Confraternização Universal (1º de Janeiro)
    - Carnaval (Segunda e Terça-feira, 48 e 47 dias antes da Páscoa)
    - Paixão de Cristo (Sexta-feira Santa, 2 dias antes da Páscoa)
    - Tiradentes (21 de Abril)
    - Dia do Trabalho (1º de Maio)
    - Corpus Christi (60 dias após a Páscoa)
    - Independência do Brasil (7 de Setembro)
    - Nossa Senhora Aparecida - Padroeira do Brasil (12 de Outubro)
    - Finados (2 de Novembro)
    - Proclamação da República (15 de Novembro)
    - Dia Nacional de Zumbi e da Consciência Negra (20 de Novembro, a partir de 2024)
    - Natal (25 de Dezembro)
    
    Notas importantes:
    1) A partir do ano 2000, a quinta-feira da Semana Santa foi considerada dia útil
    2) Esta lista não inclui feriados municipais, eleições e o último dia do ano
    3) O critério adotado foi indicar os feriados em que não há sensibilização das Reservas Bancárias
    """

    aliases = ["ANBIMA", "FERIADOS_NACIONAIS"]
    
    # Horários padrão do mercado financeiro brasileiro
    regular_market_times = {
        "market_open": ((None, time(10, 0)),),
        "market_close": ((None, time(18, 0)),),
    }

    @property
    def name(self):
        return "ANBIMA"

    @property
    def tz(self):
        return ZoneInfo("America/Sao_Paulo")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                ConfraternizacaoUniversal,
                CarnavalSegunda,
                CarnavalTerca,
                PaixaoCristo,
                Tiradentes,
                DiaTrabalho,
                CorpusChristi,
                IndependenciaBrasil,
                NossaSenhoraAparecida,
                Finados,
                ProclamacaoRepublica,
                ConscienciaNegraNacional,
                Natal,
            ]
        )

    @property
    def adhoc_holidays(self):
        # Feriados específicos que não seguem regra regular
        # Baseado nos dados do arquivo, todos os feriados seguem padrões regulares
        return []

    @property
    def special_opens(self):
        # Horários especiais de abertura
        # Não há horários especiais definidos no arquivo ANBIMA
        return []

    @property
    def special_closes(self):
        # Horários especiais de fechamento
        # Não há horários especiais definidos no arquivo ANBIMA
        return []