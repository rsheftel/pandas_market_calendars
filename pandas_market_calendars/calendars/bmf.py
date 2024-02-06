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
from pytz import timezone

from pandas_market_calendars.market_calendar import FRIDAY, MarketCalendar

# Universal Confraternization (new years day)
ConfUniversal = Holiday(
    "Dia da Confraternizacao Universal",
    month=1,
    day=1,
)
# Sao Paulo city birthday
AniversarioSaoPaulo = Holiday(
    "Aniversario de Sao Paulo", month=1, day=25, end_date="2021-12-31"
)
# Carnival Monday
CarnavalSegunda = Holiday(
    "Carnaval Segunda", month=1, day=1, offset=[Easter(), Day(-48)]
)
# Carnival Tuesday
CarnavalTerca = Holiday("Carnaval Terca", month=1, day=1, offset=[Easter(), Day(-47)])
# Ash Wednesday (short day)
QuartaCinzas = Holiday("Quarta Cinzas", month=1, day=1, offset=[Easter(), Day(-46)])
# Good Friday
SextaPaixao = GoodFriday
# Feast of the Most Holy Body of Christ
CorpusChristi = Holiday("Corpus Christi", month=1, day=1, offset=[Easter(), Day(60)])
# Tiradentes Memorial
Tiradentes = Holiday(
    "Tiradentes",
    month=4,
    day=21,
)
# Labor Day
DiaTrabalho = Holiday(
    "Dia Trabalho",
    month=5,
    day=1,
)
# Constitutionalist Revolution
Constitucionalista = Holiday(
    "Constitucionalista", month=7, day=9, start_date="1997-01-01", end_date="2019-12-31"
)
# Independence Day
Independencia = Holiday(
    "Independencia",
    month=9,
    day=7,
)
# Our Lady of Aparecida
Aparecida = Holiday(
    "Nossa Senhora de Aparecida",
    month=10,
    day=12,
)
# All Souls' Day
Finados = Holiday(
    "Dia dos Finados",
    month=11,
    day=2,
)
# Proclamation of the Republic
ProclamacaoRepublica = Holiday(
    "Proclamacao da Republica",
    month=11,
    day=15,
)
# Day of Black Awareness (municipal holiday for the city of São Paulo)
ConscienciaNegra = Holiday(
    "Dia da Consciencia Negra",
    month=11,
    day=20,
    start_date="2004-01-01",
    end_date="2019-12-31",
)
# Day of Black Awareness (national holiday)
ConscienciaNegraNacional = Holiday(
    "Dia da Consciencia Negra",
    month=11,
    day=20,
    start_date="2023-12-22",
)
# Christmas Eve
VesperaNatal = Holiday(
    "Vespera Natal",
    month=12,
    day=24,
)
# Christmas
Natal = Holiday(
    "Natal",
    month=12,
    day=25,
)
# New Year's Eve
AnoNovo = Holiday(
    "Ano Novo",
    month=12,
    day=31,
)
# New Year's Eve falls on Saturday
AnoNovoSabado = Holiday(
    "Ano Novo Sabado",
    month=12,
    day=30,
    days_of_week=(FRIDAY,),
)
# New Year's Eve falls on Sunday
AnoNovoDomingo = Holiday(
    "Ano Novo Domingo",
    month=12,
    day=29,
    days_of_week=(FRIDAY,),
)

##########################
# Non-recurring holidays
##########################

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
        return timezone("America/Sao_Paulo")

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
