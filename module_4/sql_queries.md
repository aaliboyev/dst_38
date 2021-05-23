## Проект 4. Авиарейсы без потерь
На этом файле приведены ответы на вопросы итогового проекта по работе с базами данных.


## Задание 4.2

---
### Вопрос 1. Таблица рейсов содержит всю информацию о прошлых, текущих и запланированных рейсах. Сколько всего статусов для рейсов определено в таблице?
```sql
SELECT count(distinct status) 
FROM dst_project.flights; 
# Ответ: 6
```

### Вопрос 2. Какое количество самолетов находятся в воздухе на момент среза в базе (статус рейса «самолёт уже вылетел и находится в воздухе»).
```sql
SELECT count(flight_id) FROM dst_project.flights
WHERE status = 'Departed'; 
# Ответ: 58
```

### Вопрос 3. Места определяют схему салона каждой модели. Сколько мест имеет самолет модели  (Boeing 777-300)?
```sql
SELECT count(seat_no) FROM dst_project.seats
WHERE aircraft_code = '773'; 
# Ответ: 402
```

### Вопрос 4. Сколько состоявшихся (фактических) рейсов было совершено между 1 апреля 2017 года и 1 сентября 2017 года?
```sql
SELECT count(flight_id) FROM dst_project.flights
WHERE actual_arrival BETWEEN '04-01-2017' AND '09-01-2017' AND status = 'Arrived'; 
# Ответ: 74227
```

## Задание 4.3

---
### Вопрос 1. Сколько всего рейсов было отменено по данным базы?
```sql
SELECT count(flight_id) FROM dst_project.flights
WHERE status = 'Cancelled';
# Ответ: 437
```
### Вопрос 2. Сколько самолетов моделей типа Boeing, Sukhoi Superjet, Airbus находится в базе авиаперевозок?
```sql
SELECT count(aircraft_code) FROM dst_project.aircrafts
WHERE model LIKE 'Boeing%'
# Ответ: 3
SELECT count(aircraft_code) FROM dst_project.aircrafts
WHERE model LIKE 'Sukhoi Superjet%'
# Ответ: 1
SELECT count(aircraft_code) FROM dst_project.aircrafts
WHERE model LIKE 'Airbus%'
# Ответ: 3
```
### Вопрос 3. В какой части (частях) света находится больше аэропортов?
```sql
select timezone from dst_project.airports
# Ответ: Europe, Asia
```
### Вопрос 4. У какого рейса была самая большая задержка прибытия за все время сбора данных? Введите id рейса (flight_id).
```sql
SELECT max(actual_arrival - scheduled_arrival) AS delay, flight_id FROM dst_project.flights
WHERE actual_arrival IS NOT NULL
GROUP BY flight_id
ORDER BY delay DESC
LIMIT 1
# Ответ: 157571
```

## Задание 4.4

---
### Вопрос 1. Когда был запланирован самый первый вылет, сохраненный в базе данных?
```sql
SELECT scheduled_departure FROM dst_project.flights
ORDER BY scheduled_departure
LIMIT 1
# Ответ: 14.08.2016

```
### Вопрос 2. Сколько минут составляет запланированное время полета в самом длительном рейсе?
```sql
SELECT extract(EPOCH FROM (scheduled_arrival - scheduled_departure)) / 60 AS planned_time FROM dst_project.flights
WHERE actual_arrival IS NOT NULL
GROUP BY flight_id
ORDER BY planned_time DESC
LIMIT 1
# Ответ: 530
```
### Вопрос 3. Между какими аэропортами пролегает самый длительный по времени запланированный рейс?
```sql
SELECT  arrival_airport, departure_airport, max(extract(EPOCH from (scheduled_arrival - scheduled_departure))) / 60 AS planned_time FROM dst_project.flights
WHERE actual_arrival IS NOT NULL
GROUP BY flight_id
ORDER BY planned_time DESC
LIMIT 1
# Ответ: DME - UUS
```
### Вопрос 4. Сколько составляет средняя дальность полета среди всех самолетов в минутах? Секунды округляются в меньшую сторону (отбрасываются до минут).
```sql
SELECT avg(extract(EPOCH from (scheduled_arrival - scheduled_departure))) / 60 as planned_time FROM dst_project.flights
# Ответ: 128.36
```

## Задание 4.5

---
### Вопрос 1. Мест какого класса у SU9 больше всего?
```sql
SELECT fare_conditions FROM dst_project.seats
WHERE aircraft_code = 'SU9'
GROUP BY fare_conditions
ORDER BY count(seat_no) DESC
LIMIT 1
# Ответ: Economy
```

### Вопрос 2. Какую самую минимальную стоимость составило бронирование за всю историю?
```sql
SELECT min(total_amount) FROM dst_project.bookings
# Ответ: 3400
```

### Вопрос 3. Какой номер места был у пассажира с id = 4313 788533?
```sql
SELECT seat_no FROM dst_project.boarding_passes
WHERE ticket_no = (
    SELECT ticket_no FROM dst_project.tickets
    WHERE passenger_id = '4313 788533'
)
# Ответ: 2A
```

## Задание 5.1

---
### Вопрос 1. Анапа — курортный город на юге России. Сколько рейсов прибыло в Анапу за 2017 год?
```sql
SELECT count(flight_id) FROM dst_project.flights
WHERE actual_arrival BETWEEN '01-01-2017' AND '01-01-2018' AND arrival_airport IN (
    SELECT airport_code FROM dst_project.airports
    WHERE city = 'Anapa'
)
# Ответ: 486
```
### Вопрос 2. Сколько рейсов из Анапы вылетело зимой 2017 года?
```sql
SELECT count(flight_id) FROM dst_project.flights
WHERE (
        actual_departure BETWEEN '01-01-2017' AND '03-01-2017'
        OR actual_departure BETWEEN '12-01-2017' AND '01-01-2018' 
    ) 
    AND 
    departure_airport IN (
        SELECT airport_code FROM dst_project.airports
        WHERE city = 'Anapa'
    )
# Ответ: 127
```
### Вопрос 3. Посчитайте количество отмененных рейсов из Анапы за все время.
```sql
SELECT count(flight_id) FROM dst_project.flights
WHERE status = 'Cancelled' AND departure_airport IN (
    SELECT airport_code FROM dst_project.airports
    WHERE city = 'Anapa'
)
# Ответ: 1
```
### Вопрос 4. Сколько рейсов из Анапы не летают в Москву?
```sql
SELECT count(flight_id) FROM dst_project.flights
WHERE departure_airport IN (
        SELECT airport_code FROM dst_project.airports
        WHERE city = 'Anapa'
    )
    AND
    arrival_airport NOT IN (
        SELECT airport_code FROM dst_project.airports
        WHERE city = 'Moscow'
    )
# Ответ: 453
```
### Вопрос 5. Какая модель самолета летящего на рейсах из Анапы имеет больше всего мест?
```sql
SELECT a.model FROM dst_project.seats s
JOIN dst_project.flights f ON f.aircraft_code = s.aircraft_code
JOIN dst_project.aircrafts a ON a.aircraft_code = s.aircraft_code
WHERE f.departure_airport IN (
        SELECT airport_code FROM dst_project.airports
        WHERE city = 'Anapa'
    )
GROUP BY a.model
ORDER BY count(a.model) desc
LIMIT 1
# Ответ: Boeing 737-300
```
