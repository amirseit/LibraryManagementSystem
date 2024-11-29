import logging
from library.library_management import Library

# --- Основная точка входа программы ---

if __name__ == "__main__":
    # Очистка существующих обработчиков логов
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Настройка конфигурации логирования
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,  # Логирование для уровней INFO и выше (WARNING, ERROR и т.д.)
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Создание экземпляра класса Library для управления операциями библиотеки
    library = Library()

    # Основной цикл программы для взаимодействия с пользователем
    while True:
        print("\nСистема управления библиотекой")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книг")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Введите ваш выбор (1-6): ").strip()

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.delete_book()
        elif choice == "3":
            library.search_books()
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            library.change_status()
        elif choice == "6":
            print("Выход из системы управления библиотекой. До свидания!")
            logging.shutdown()
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 6.")
            logging.warning(f"Invalid menu selection: '{choice}'")