# TestProject
Backend-пайплайн для обработки результатов опросника **UMUX-Lite**.

## Возможности

- Загрузка одной или нескольких CSV-выгрузок.
- Валидация и очистка данных.
- Удаление дубликатов.
- Нормализация категориальных полей.
- Логирование причин отбраковки записей.
- Расчет UMUX Score.
- Агрегация результатов по продуктам, версиям и времени.
- Генерация итоговых отчетов и визуализаций.
# Установка

## 1. Клонировать репозиторий

```bash
git clone https://github.com/<username>/<repository>.git

cd <repository>
```

---

## 2. Создать виртуальное окружение

Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Установить зависимости

### Через uv

```bash
uv sync
```
# Запуск пайплайна

Обработка одного файла

```bash
python main.py --input test.csv
```

или

```bash
uv run python main.py --input test.csv
```
```bash
python main.py \
    --input uploads/file1.csv uploads/file2.csv
```

# Результаты

После выполнения пайплайна формируются:

- очищенный датасет;
- лог отбраковки;
- агрегированная статистика;
- визуализации;
- итоговый отчет.

По умолчанию результаты сохраняются в директорию:

```
output/
```
