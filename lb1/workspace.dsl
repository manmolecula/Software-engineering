workspace {
    title "Система управления проектами"
    !identifiers hierarchical

    model {
        // Типы пользователей системы
        systemAdmin = Person "System Administrator" "Управляет системой, настройками и правами доступа"
        regularUser = Person "Regular User" "Основной пользователь, работает с проектами и задачами"
        visitor = Person "Visitor" "Имеет доступ только к публичной информации"

        // Основные компоненты системы
        pms = softwareSystem "Project Management Platform" {
            // Сервисы системы
            authModule = container "Auth Module" {
                techStack "FastAPI (Python)"
                purpose "Обработка аутентификации и управления сессиями"
                component "AuthHandler" {
                    techStack "FastAPI"
                    responsibility "Валидация учетных данных"
                }
            }

            userModule = container "User Module" {
                techStack "FastAPI (Python)"
                purpose "Управление учетными записями пользователей"
                component "UserManager" {
                    techStack "FastAPI"
                    responsibility "Обработка операций с пользователями"
                }
                component "UserStorage" {
                    techStack "PostgreSQL"
                    responsibility "Хранение информации о пользователях"
                }
            }

            projectModule = container "Project Module" {
                techStack "FastAPI (Python)"
                purpose "Управление жизненным циклом проектов"
                component "ProjectManager" {
                    techStack "FastAPI"
                    responsibility "Обработка операций с проектами"
                }
                component "ProjectStorage" {
                    techStack "PostgreSQL"
                    responsibility "Хранение данных проектов"
                }
            }

            taskModule = container "Task Module" {
                techStack "FastAPI (Python)"
                purpose "Управление задачами в проектах"
                component "TaskProcessor" {
                    techStack "FastAPI"
                    responsibility "Обработка операций с задачами"
                }
                component "TaskDatabase" {
                    techStack "PostgreSQL"
                    responsibility "Хранение информации о задачах"
                }
            }

            notifications = container "Notification Module" {
                techStack "FastAPI (Python)"
                purpose "Рассылка уведомлений пользователям"
                component "NotificationHandler" {
                    techStack "FastAPI"
                    responsibility "Обработка запросов на уведомления"
                }
                component "MessagingService" {
                    techStack "aiogram"
                    responsibility "Интеграция с Telegram ботом"
                }
            }

            webInterface = container "Web Client" {
                techStack "HTML5, CSS3, JavaScript"
                purpose "Пользовательский интерфейс системы"
                component "AuthUI" {
                    -> authModule "Проверка учетных данных" "REST API"
                }
                component "MainUI" {
                    -> projectModule "Загрузка проектов" "REST API"
                    -> taskModule "Загрузка задач" "REST API"
                }
                component "ProjectUI" {
                    -> projectModule "Получение информации о проекте" "REST API"
                    -> taskModule "Получение связанных задач" "REST API"
                }
            }

            // Связи между компонентами
            authModule -> userModule "Запрос информации о пользователе" "REST API"
            userModule -> projectModule "Инициализация нового проекта" "REST API"
            userModule -> taskModule "Создание новой задачи" "REST API"
            projectModule -> taskModule "Получение задач проекта" "REST API"
            taskModule -> notifications "Триггер уведомлений" "REST API"
        }

        // Взаимодействие пользователей
        systemAdmin -> pms.userModule "Администрирование пользователей" "REST API"
        regularUser -> pms.authModule "Авторизация в системе" "REST API"
        regularUser -> pms.webInterface "Работа через веб-интерфейс" "HTTPS"
        visitor -> pms.webInterface "Просмотр доступной информации" "HTTPS"

        deploymentEnvironment "Production" {
            deploymentNode "Web Server" {
                infrastructure "Nginx"
                containerInstance pms.webInterface
            }

            deploymentNode "App Server" {
                infrastructure "Gunicorn"
                containerInstance pms.authModule
                containerInstance pms.userModule
                containerInstance pms.projectModule
                containerInstance pms.taskModule
                containerInstance pms.notifications
            }

            deploymentNode "DB Server" {
                infrastructure "PostgreSQL Cluster"
                containerInstance pms.userModule
                containerInstance pms.projectModule
                containerInstance pms.taskModule
            }
        }
    }

    views {
        theme default

        systemContext pms "Общая архитектура" {
            include *
            autoLayout leftToRight
        }

        container pms "Компоненты системы" {
            include *
            autoLayout
        }

        dynamic pms "Процесс создания проекта" {
            regularUser -> pms.webInterface "Вход в систему" "HTTPS"
            pms.webInterface -> pms.authModule "Проверка авторизации" "REST API"
            pms.authModule -> pms.userModule "Получение профиля" "REST API"
            regularUser -> pms.webInterface "Инициация проекта" "HTTPS"
            pms.webInterface -> pms.projectModule "Создание проекта" "REST API"
            regularUser -> pms.webInterface "Добавление задачи" "HTTPS"
            pms.webInterface -> pms.taskModule "Создание задачи" "REST API"
            pms.taskModule -> pms.notifications "Уведомление о задаче" "REST API"
            autoLayout leftToRight
        }
    }
}