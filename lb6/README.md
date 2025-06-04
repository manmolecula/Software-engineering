## Лабараторная работа №6
**Предмет: Программная инженерия**<br>
**Выполнил: Кучев Антон Алексеевич, М80-109СВ-24**  <br><br>
1. Реализуйте для добавления одной из сущностей вашего задания паттерн CQRS:
a. сервис вместо записи в базу данных должен сохранять сообщение в topic
kafka (допускается одновременное сохранение сущности в кеш Redis –
шаблон сквозная-запись)
b. реализуйте отдельный контейнер, который считывает сообщения из
topic kafka и сохраняет их в базу данных
2. Актуализируйте модель архитектуры в Structurizr DSL
3. Ваши сервисы должны запускаться через docker-compose командой dockercompose up (создайте Docker файлы для каждого сервиса)

Рекомендации по C++
- Используйте фреймворк Poco https://docs.pocoproject.org/current/
- Используйте библиотеки
o https://github.com/edenhill/librdkafka
o https://github.com/mfontanini/cppkafka
- Пример по работе с Kafka
https://github.com/DVDemon/hl_mai_10_kafka

Рекомендации по Python:
- Используйте FastAPI для построения интерфейсов
- Простой пример применения confluent_kafka
https://github.com/DVDemon/architecture_python/tree/main/10_kafka
