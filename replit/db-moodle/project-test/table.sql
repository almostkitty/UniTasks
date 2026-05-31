-- Таблица для сотрудников
CREATE TABLE IF NOT EXISTS `Сотрудник` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `last_name` VARCHAR(255) NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `middle_name` VARCHAR(255) NOT NULL,
  `birthday` DATE NOT NULL,
  `position` INT NOT NULL,
  `rank` INT NOT NULL,
  FOREIGN KEY (`position`) REFERENCES `Должность` (`id`),
  FOREIGN KEY (`rank`) REFERENCES `Звание` (`id`)
);

-- Таблица для должностей
CREATE TABLE IF NOT EXISTS `Должность` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `group` VARCHAR(255) NOT NULL
);

-- Таблица для званий
CREATE TABLE IF NOT EXISTS `Звание` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(255) NOT NULL
);

-- Таблица для аттестаций
CREATE TABLE IF NOT EXISTS `Аттестации` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `employee_id` INT NOT NULL,
  `type` INT NOT NULL,
  `status` BOOLEAN NOT NULL,
  `no_attestation_reason` VARCHAR(255),
  `date` DATE NOT NULL,
  FOREIGN KEY (`employee_id`) REFERENCES `Сотрудник` (`id`),
  FOREIGN KEY (`type`) REFERENCES `Виды аттестации` (`id`)
);

-- Таблица для видов аттестаций
CREATE TABLE IF NOT EXISTS `Виды аттестации` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(255) NOT NULL
);

-- Таблица для занятий
CREATE TABLE IF NOT EXISTS `Занятия` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `employee_id` INT NOT NULL,
  `exercise_type` INT NOT NULL,
  `date` DATE NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  FOREIGN KEY (`employee_id`) REFERENCES `Сотрудник` (`id`),
  FOREIGN KEY (`exercise_type`) REFERENCES `Виды занятий` (`id`)
);

-- Таблица для видов занятий
CREATE TABLE IF NOT EXISTS `Виды занятий` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` VARCHAR(255) NOT NULL
);

-- Таблица для отчетов по занятиям
CREATE TABLE IF NOT EXISTS `Отчет по занятиям` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `start_date` DATE NOT NULL,
  `finish_date` DATE NOT NULL,
  `count_plan` SMALLINT NOT NULL,
  `count_actual` SMALLINT NOT NULL,
  `count_reason` VARCHAR(255) NOT NULL,
  `comment` TEXT,
  FOREIGN KEY (`id`) REFERENCES `Занятия` (`id`)
);


-- Таблица для транспорта
CREATE TABLE IF NOT EXISTS `Транспорт`(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  'number' VARCHAR(255) NOT NULL,
  'model' VARCHAR(255) NOT NULL,
  'manufacture_year' SMALLINT NOT NULL,
  'start_year' SMALLINT NOT NULL
);

-- Таблица для выездов
CREATE TABLE IF NOT EXISTS `Выезды`(
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `number` VARCHAR(255) NOT NULL,
  `duration` INTEGER NOT NULL,
  `lead_employee_id` INTEGER NOT NULL,
  `rescued_count` INTEGER NOT NULL,
  `evacuated_count` INTEGER NOT NULL,
  `work_date` DATE NOT NULL,
  `work_type` VARCHAR(255) NOT NULL,
  `work_address` VARCHAR(255) NOT NULL,
  `fire_rank` INTEGER NOT NULL,
  FOREIGN KEY (`lead_employee_id`) REFERENCES `Сотрудник` (`id`)
);