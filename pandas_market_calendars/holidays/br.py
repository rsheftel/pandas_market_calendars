# BR Holidays - Brazil National Holidays
# Based on ANBIMA national holidays calendar

import pandas as pd
from pandas import DateOffset, Timestamp
from pandas.tseries.holiday import Holiday, Easter, GoodFriday, Day

from pandas_market_calendars.market_calendar import FRIDAY, MONDAY, TUESDAY

# Confraternização Universal (New Year's Day)
ConfraternizacaoUniversal = Holiday(
    "Confraternização Universal",
    month=1,
    day=1,
)

# Carnaval Monday (48 days before Easter)
CarnavalSegunda = Holiday(
    "Carnaval (Segunda-feira)",
    month=1,
    day=1,
    offset=[Easter(), Day(-48)]
)

# Carnaval Tuesday (47 days before Easter)
CarnavalTerca = Holiday(
    "Carnaval (Terça-feira)",
    month=1,
    day=1,
    offset=[Easter(), Day(-47)]
)

# Paixão de Cristo (Good Friday)
PaixaoCristo = GoodFriday

# Tiradentes
Tiradentes = Holiday(
    "Tiradentes",
    month=4,
    day=21,
)

# Dia do Trabalho (Labor Day)
DiaTrabalho = Holiday(
    "Dia do Trabalho",
    month=5,
    day=1,
)

# Corpus Christi (60 days after Easter)
CorpusChristi = Holiday(
    "Corpus Christi",
    month=1,
    day=1,
    offset=[Easter(), Day(60)]
)

# Independência do Brasil
IndependenciaBrasil = Holiday(
    "Independência do Brasil",
    month=9,
    day=7,
)

# Nossa Senhora Aparecida - Padroeira do Brasil
NossaSenhoraAparecida = Holiday(
    "Nossa Sr.a Aparecida - Padroeira do Brasil",
    month=10,
    day=12,
)

# Finados (All Souls' Day)
Finados = Holiday(
    "Finados",
    month=11,
    day=2,
)

# Proclamação da República
ProclamacaoRepublica = Holiday(
    "Proclamação da República",
    month=11,
    day=15,
)

# Dia Nacional de Zumbi e da Consciência Negra (National holiday starting 2024)
ConscienciaNegraNacional = Holiday(
    "Dia Nacional de Zumbi e da Consciência Negra",
    month=11,
    day=20,
    start_date=Timestamp("2024-01-01"),
)

# Natal (Christmas)
Natal = Holiday(
    "Natal",
    month=12,
    day=25,
)

# Regional/Local holidays that were occasionally observed nationally

# Aniversário de São Paulo (São Paulo City Anniversary - until 2021)
AniversarioSaoPaulo = Holiday(
    "Aniversário de São Paulo",
    month=1,
    day=25,
    end_date=Timestamp("2021-12-31")
)

# Revolução Constitucionalista (Constitutionalist Revolution - São Paulo state)
# Observed from 1997 to 2019, with some exceptions
RevConstitucionalista_1997_2019 = Holiday(
    "Revolução Constitucionalista",
    month=7,
    day=9,
    start_date=Timestamp("1997-01-01"),
    end_date=Timestamp("2019-12-31")
)

# Consciência Negra (Municipal holiday for São Paulo city from 2004 to 2019)
ConscienciaNegraMunicipal = Holiday(
    "Dia da Consciência Negra",
    month=11,
    day=20,
    start_date=Timestamp("2004-01-01"),
    end_date=Timestamp("2019-12-31")
)

# Véspera de Natal (Christmas Eve - sometimes observed)
VesperaNatal = Holiday(
    "Véspera de Natal",
    month=12,
    day=24,
)

# Véspera de Ano Novo (New Year's Eve - sometimes observed)
VesperaAnoNovo = Holiday(
    "Véspera de Ano Novo",
    month=12,
    day=31,
)

# New Year's Eve when it falls on Saturday (Friday becomes holiday)
AnoNovoSabado = Holiday(
    "Véspera Ano Novo (Sábado)",
    month=12,
    day=30,
    days_of_week=(FRIDAY,),
)

# New Year's Eve when it falls on Sunday (Friday becomes holiday)
AnoNovoDomingo = Holiday(
    "Véspera Ano Novo (Domingo)",
    month=12,
    day=29,
    days_of_week=(FRIDAY,),
)

# Quarta-feira de Cinzas (Ash Wednesday - sometimes half day)
QuartaCinzas = Holiday(
    "Quarta-feira de Cinzas",
    month=1,
    day=1,
    offset=[Easter(), Day(-46)]
)

# One-off holidays and special dates

UniqueCloses = []

# World Cup Finals when Brazil played at home or won
UniqueCloses.append(pd.Timestamp("1970-06-21", tz="UTC"))  # Brazil wins World Cup (Mexico)
UniqueCloses.append(pd.Timestamp("1994-07-17", tz="UTC"))  # Brazil wins World Cup (USA)
UniqueCloses.append(pd.Timestamp("2002-06-30", tz="UTC"))  # Brazil wins World Cup (Korea/Japan)

# Pope visits
UniqueCloses.append(pd.Timestamp("1980-07-02", tz="UTC"))  # Pope John Paul II visit
UniqueCloses.append(pd.Timestamp("1997-10-04", tz="UTC"))  # Pope John Paul II visit
UniqueCloses.append(pd.Timestamp("2007-05-13", tz="UTC"))  # Pope Benedict XVI visit
UniqueCloses.append(pd.Timestamp("2013-07-28", tz="UTC"))  # Pope Francis visit (World Youth Day)

# Special commemorative dates
UniqueCloses.append(pd.Timestamp("2000-04-22", tz="UTC"))  # 500 years of Brazil discovery
UniqueCloses.append(pd.Timestamp("2022-09-07", tz="UTC"))  # 200 years of Independence (Bicentennial)

# Major sporting events in Brazil
UniqueCloses.append(pd.Timestamp("2014-07-13", tz="UTC"))  # World Cup Final (Brazil hosting)
UniqueCloses.append(pd.Timestamp("2016-08-21", tz="UTC"))  # Olympics Final Day (Rio 2016)

# Elections (second round runoffs - typically Sundays but can affect Friday trading)
# Presidential elections that historically affected markets
UniqueCloses.append(pd.Timestamp("1989-12-17", tz="UTC"))  # First direct presidential election
UniqueCloses.append(pd.Timestamp("2018-10-28", tz="UTC"))  # Bolsonaro election
UniqueCloses.append(pd.Timestamp("2022-10-30", tz="UTC"))  # Lula re-election

# Special financial market closures
UniqueCloses.append(pd.Timestamp("1999-01-15", tz="UTC"))  # Real devaluation crisis
UniqueCloses.append(pd.Timestamp("2008-10-10", tz="UTC"))  # Global financial crisis
UniqueCloses.append(pd.Timestamp("2020-03-18", tz="UTC"))  # COVID-19 circuit breaker

# Deaths of important figures
UniqueCloses.append(pd.Timestamp("1985-04-21", tz="UTC"))  # Death of Tancredo Neves
UniqueCloses.append(pd.Timestamp("1994-08-12", tz="UTC"))  # Death of Ayrton Senna (observed later)

# Additional specific holidays for 2021 (COVID-19 related adjustments)
CovidAdjustments2021 = []
CovidAdjustments2021.append(pd.Timestamp("2021-07-09", tz="UTC"))  # Constitutionalist Revolution (one-off return)
CovidAdjustments2021.append(pd.Timestamp("2021-11-20", tz="UTC"))  # Black Awareness Day (one-off return)

# Extend unique closes with COVID adjustments
UniqueCloses.extend(CovidAdjustments2021)