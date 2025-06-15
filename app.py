import streamlit as st
import time

st.set_page_config(page_title="Адаптивный тестирование", layout="centered")
st.title("Адаптивное тестирование по ОАиП")

# --- Данные вопросов ---
adaptive_test = [
    {
        "id": "Q1",
        "topic": "Алгоритмы и блок-схемы",
        "level": "🟢",
        "question": "Что такое алгоритм?",
        "options": ["Последовательность случайных действий",
                    "Набор команд, выполняемых по произвольному порядку",
                    "Последовательность действий, приводящая к решению задачи",
                    "Комментарии в коде"],
        "correct": 2,
        "next_if_correct": "Q2",
        "next_if_wrong": "Q3"
    },
    {
        "id": "Q2",
        "topic": "Состав языка C",
        "level": "🟡",
        "question": "Что делает директива `#define` в языке Си?",
        "options": ["Определяет переменную",
                    "Заменяет идентификатор на значение при препроцессинге",
                    "Удаляет переменные",
                    "Загружает библиотеки"],
        "correct": 1,
        "next_if_correct": "Q4",
        "next_if_wrong": "Q5"
    },
    {
        "id": "Q3",
        "topic": "Системы счисления",
        "level": "🟢",
        "question": "Чему равно двоичное число 1011 в десятичной системе?",
        "options": ["11", "9", "12", "13"],
        "correct": 0,
        "next_if_correct": "Q5",
        "next_if_wrong": "Q6"
    },
    {
        "id": "Q4",
        "topic": "Вещественные числа и архитектура",
        "level": "🔴",
        "question": "Что такое архитектура фон Неймана?",
        "options": ["Схема подключения к интернету",
                    "Модель, в которой данные и программы хранятся вместе",
                    "Тип памяти",
                    "Алгоритм сортировки"],
        "correct": 1,
        "next_if_correct": "Q7",
        "next_if_wrong": "Q6"
    },
    {
        "id": "Q5",
        "topic": "Циклы и условия",
        "level": "🟡",
        "question": "Какой из следующих операторов используется для цикла с предусловием в C?",
        "options": ["for", "repeat", "do", "while"],
        "correct": 3,
        "next_if_correct": "Q7",
        "next_if_wrong": "Q6"
    },
    {
        "id": "Q6",
        "topic": "Массивы",
        "level": "🟡",
        "question": "Как объявить массив из 10 целых чисел в C?",
        "options": ["int arr[10];", "int[10] arr;", "arr int[10];", "array<int> arr;"],
        "correct": 0,
        "next_if_correct": "Q8",
        "next_if_wrong": "Q8"
    },
    {
        "id": "Q7",
        "topic": "Шаблоны и сложность",
        "level": "🔴",
        "question": "Что означает запись O(n log n)?",
        "options": ["Время выполнения зависит от квадрата n",
                    "Время выполнения постоянно",
                    "Логарифмическая сложность",
                    "Оценка времени алгоритма в худшем случае"],
        "correct": 3,
        "next_if_correct": "Q9",
        "next_if_wrong": "Q8"
    },
    {
        "id": "Q8",
        "topic": "Строки",
        "level": "🟡",
        "question": "Как в C объявить строку 'hello'?",
        "options": ['char str[] = "hello";', "string str = 'hello';", "char str = hello;", "str = char['hello'];"],
        "correct": 0,
        "next_if_correct": "Q9",
        "next_if_wrong": "Q9"
    },
    {
        "id": "Q9",
        "topic": "Указатели",
        "level": "🔴",
        "question": "Что произойдёт при разыменовании нулевого указателя `int *p = NULL; *p;`?",
        "options": ["Вернётся значение 0", "Компилятор заменит на 0",
                    "Произойдёт ошибка выполнения (segmentation fault)", "Память будет очищена"],
        "correct": 2,
        "next_if_correct": None,
        "next_if_wrong": None
    }
]

if "started" not in st.session_state:
    st.session_state.started = False
if "current_id" not in st.session_state:
    st.session_state.current_id = "Q1"
    st.session_state.score = 0
    st.session_state.knowledge = {}
    st.session_state.just_answered = False
    st.session_state.start_time = 0


# --- Функция отображения вопроса ---
def show_question(q):
    #st.markdown(f"### Тема: {q['topic']} | Уровень: {q['level']}")

    col1, col2 = st.columns([4, 1])  # Широкий блок с вопросом и узкий — для таймера

    with col1:
        st.markdown(f"### Тема: {q['topic']} | Уровень: {q['level']}")
        st.write(q["question"])
    
    with col2:
        elapsed = int(time.time() - st.session_state.start_time)
        minutes, seconds = divmod(elapsed, 60)
        st.markdown(f"⏱ **{minutes:02d}:{seconds:02d}**")

    # Уникальный ключ для хранения выбранного варианта
    answer_key = f"answer_{q['id']}"

    # Проверяем, был ли уже дан ответ
    already_answered = st.session_state.get("just_answered", False)

    # Если студент еще не ответил, radio активно
    selected = st.radio(
        "Выберите вариант:",
        q["options"],
        key=answer_key,
        disabled=already_answered
    )

    if not already_answered and st.button("Ответить", key="btn_" + q["id"]):
        correct = (q["options"].index(selected) == q["correct"])
        st.session_state.knowledge[q["topic"]] = "✅" if correct else "❌"
        st.session_state.last_answer_correct = correct
        st.session_state.just_answered = True
        if correct:
            st.session_state.score += 1

        # Сохраняем текущий ID вопроса для показа результата
        st.session_state.last_question_id = q["id"]
        st.rerun()  # Обновим страницу, чтобы скрыть кнопку и зафиксировать ответ

    # После ответа — показываем результат
    if already_answered and st.session_state.get("last_question_id") == q["id"]:
        if st.session_state.last_answer_correct:
            st.success("✅ Верно!")
        else:
            st.error("❌ Неверно.")
        if st.button("Продолжить ➡️"):
            st.session_state.current_id = (
                q["next_if_correct"] if st.session_state.last_answer_correct
                else q["next_if_wrong"]
            )
            st.session_state.just_answered = False
            st.session_state.last_question_id = None
            st.rerun()

# --- Основной цикл ---
question_map = {q["id"]: q for q in adaptive_test}
if not st.session_state.started:
    st.markdown("## 🧪 Адаптивное тестирование по программированию")
    st.write("""
    Добро пожаловать в систему адаптивного тестирования!

    **Цель:** определить уровень ваших знаний в области алгоритмизации, языка C и базовых структур данных.

    Вопросы подбираются автоматически на основе ваших ответов. Вы получите обратную связь и итоговый результат.

    ⚠️ Отвечать можно **только один раз** на каждый вопрос. Внимательно читайте формулировки.

    ⏱ Время тестирования будет зафиксировано.
    """)
    if st.button("Начать тест"):
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.rerun()
elif st.session_state.current_id:
    show_question(question_map[st.session_state.current_id])
else:
    st.markdown("## 🧾 Результаты")
    for topic, result in st.session_state.knowledge.items():
        st.write(f"**{topic}**: {result}")
    st.write(f"**Итог**: {st.session_state.score} правильных ответов из {len(st.session_state.knowledge)}")
    elapsed_time = int(time.time() - st.session_state.start_time)
    minutes, seconds = divmod(elapsed_time, 60)
    st.write(f"⏱ Время прохождения: {minutes} мин {seconds} сек")

    if st.button("Начать заново"):
        st.session_state.current_id = "Q1"
        st.session_state.score = 0
        st.session_state.knowledge = {}
        st.session_state.just_answered = False
        st.session_state.start_time = time.time()  # обновляем старт
        st.rerun()
