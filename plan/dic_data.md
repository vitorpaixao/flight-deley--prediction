# Dicionário de Dados - flights.csv (Flight Delays and Cancellations)

|  Coluna | Descrição | Tipo / Unidade  |
| --- | --- | --- |
|  YEAR | Ano do voo (ex.: 2015) | Inteiro  |
|  MONTH | Mês do voo (1 a 12) | Inteiro  |
|  DAY | Dia do mês do voo (1 a 31) | Inteiro  |
|  DAY_OF_WEEK | Dia da semana (1 = Segunda, 7 = Domingo) | Inteiro  |
|  AIRLINE | Código da companhia aérea (ex.: AA = American Airlines) | Categórica  |
|  FLIGHT_NUMBER | Número do voo | Inteiro  |
|  TAIL_NUMBER | Número de registro da aeronave | Texto  |
|  ORIGIN_AIRPORT | Código IATA do aeroporto de origem (ex.: ATL) | Categórica  |
|  DESTINATION_AIRPORT | Código IATA do aeroporto de destino | Categórica  |
|  SCHEDULED_DEPARTURE | Horário de partida programado (HHMM) | Inteiro  |
|  DEPARTURE_TIME | Horário real de partida (HHMM) | Inteiro  |
|  DEPARTURE_DELAY | Atraso na partida (em minutos) | Numérico  |
|  TAXI_OUT | Tempo gasto taxiando até a decolagem (em minutos) | Numérico  |
|  WHEELS_OFF | Horário em que o avião decolou (HHMM) | Inteiro  |
|  SCHEDULED_TIME | Tempo total programado de voo (em minutos) | Numérico  |
|  ELAPSED_TIME | Tempo total real de voo (em minutos) | Numérico  |
|  AIR_TIME | Tempo no ar (em minutos) | Numérico  |
|  DISTANCE | Distância entre origem e destino (em milhas) | Numérico  |
|  WHEELS_ON | Horário em que as rodas tocaram o solo (HHMM) | Inteiro  |
|  TAXI_IN | Tempo taxiando até o portão de desembarque (em minutos) | Numérico  |
|  SCHEDULED_ARRIVAL | Horário de chegada programado (HHMM) | Inteiro  |
|  ARRIVAL_TIME | Horário de chegada real (HHMM) | Inteiro  |
|  ARRIVAL_DELAY | Atraso na chegada (em minutos) | Numérico  |
|  DIVERTED | Indica se o voo foi desviado (1 = sim, 0 = não) | Binária  |
|  CANCELLED | Indica se o voo foi cancelado (1 = sim, 0 = não) | Binária  |
|  CANCELLATION_REASON | Motivo do cancelamento (A = Airline, B = Weather, C = NAS, D = Secuão) | Numérico  |
|  AIR_SYSTEM_DELAY | Atraso causado por controle de tráfego aéreo | Numérico  |
|  SECURITY_DELAY | Atraso causado por problemas de segurança | Numérico  |
|  AIRLINE_DELAY | Atraso causado pela companhia aérea | Numérico  |
|  LATE_AIRCRAFT_DELAY | Atraso causado por chegada tardia da aeronave | Numérico  |
|  WEATHER_DELAY | Atraso causado por condições meteorológicas | Numérico  |



