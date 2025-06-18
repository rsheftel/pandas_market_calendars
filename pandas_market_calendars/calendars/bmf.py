#
# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

# Import shared Brazil holiday definitions to avoid duplication
from pandas_market_calendars.holidays.br import (
    ConfraternizacaoUniversal as ConfUniversal,
    AniversarioSaoPaulo,
    CarnavalSegunda,
    CarnavalTerca,
    QuartaCinzas,
    PaixaoCristo as SextaPaixao,
    CorpusChristi,
    Tiradentes,
    DiaTrabalho,
    RevConstitucionalista_1997_2019 as Constitucionalista,
    IndependenciaBrasil as Independencia,
    NossaSeñoraAparecida as Aparecida,
    Finados,
    ProclamacaoRepublica,
    ConscienciaNegraMunicipal as ConscienciaNegra,
    ConscienciaNegraNacional,
    VesperaNatal,
    Natal,
    VesperaAnoNovo as AnoNovo,
    AnoNovoSabado,
    AnoNovoDomingo,
)


Constitucionalista2021 = Timestamp("2021-07-09", tz="UTC")
ConscienciaNegra2021 = Timestamp("2021-11-20", tz="UTC")


class BMFExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for BM&F BOVESPA

    Open Time: 10:00 AM, Brazil/Sao Paulo
    Close Time: 4:00 PM, Brazil/Sao Paulo

    Regularly-Observed Holidays:
    - Universal Confraternization (New year's day, Jan 1)
    - Sao Paulo City Anniversary (Jan 25 until 2021)
    - Carnaval Monday (48 days before Easter)
    - Carnaval Tuesday (47 days before Easter)
    - Passion of the Christ (Good Friday, 2 days before Easter)
    - Corpus Christi (60 days after Easter)
    - Tiradentes (April 21)
    - Labor day (May 1)
    - Constitutionalist Revolution (July 9 from 1997 until 2021, skipping 2020)
    - Independence Day (September 7)
    - Our Lady of Aparecida Feast (October 12)
    - All Souls' Day (November 2)
    - Proclamation of the Republic (November 15)
    - Day of Black Awareness, municipal holiday for the city of São Paulo (November 20 from 2004 until 2021, skipping 2020)
    - Day of Black Awareness, national holiday (November 20 starting in 2024)
    - Christmas (December 24 and 25)
    - Friday before New Year's Eve (December 30 or 29 if NYE falls on a Saturday or Sunday, respectively)
    - New Year's Eve (December 31)
    """

    aliases = ["BMF", "B3"]
    regular_market_times = {
        "market_open": ((None, time(10, 1)),),
        "market_close": ((None, time(16)),),
    }

    @property
    def name(self):
        return "BMF"

    @property
    def tz(self):
        return ZoneInfo("America/Sao_Paulo")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                ConfUniversal,
                AniversarioSaoPaulo,
                CarnavalSegunda,
                CarnavalTerca,
                SextaPaixao,
                CorpusChristi,
                Tiradentes,
                DiaTrabalho,
                Constitucionalista,
                Independencia,
                Aparecida,
                Finados,
                ProclamacaoRepublica,
                ConscienciaNegra,
                ConscienciaNegraNacional,
                VesperaNatal,
                Natal,
                AnoNovo,
                AnoNovoSabado,
                AnoNovoDomingo,
            ]
        )

    @property
    def adhoc_holidays(self):
        return [Constitucionalista2021, ConscienciaNegra2021]

    @property
    def special_opens(self):
        return [(time(13, 1), AbstractHolidayCalendar(rules=[QuartaCinzas]))]
