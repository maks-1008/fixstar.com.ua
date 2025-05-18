-- Фиксим структуру таблицы EmailNotificationSettings

-- 1. Создаем временную таблицу с правильной структурой
CREATE TABLE orders_emailnotificationsettings_new (
    id SERIAL PRIMARY KEY,
    email VARCHAR(254) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- 2. Копируем данные из старой таблицы с преобразованием полей
INSERT INTO orders_emailnotificationsettings_new (id, email, is_active, created_at, updated_at)
SELECT id, 
       CASE 
           WHEN email IS NULL OR email = '' THEN 'no-email@example.com' 
           ELSE SUBSTRING(email, 1, 254)
       END,
       is_active, 
       created_at, 
       updated_at
FROM orders_emailnotificationsettings;

-- 3. Удаляем старую таблицу и переименовываем новую
DROP TABLE orders_emailnotificationsettings;
ALTER TABLE orders_emailnotificationsettings_new RENAME TO orders_emailnotificationsettings;

-- 4. Восстанавливаем последовательность для ID
SELECT setval('orders_emailnotificationsettings_id_seq', 
             (SELECT MAX(id) FROM orders_emailnotificationsettings));

-- 5. Восстанавливаем индексы и ограничения
ALTER TABLE orders_emailnotificationsettings 
  ADD CONSTRAINT unique_active_email UNIQUE (email, is_active); 