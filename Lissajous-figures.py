import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import time


# Глобальные переменные
current_window = None
fig = None
canvas = None
ax = None
animation = None
is_animation_running = False  # Флаг для отслеживания состояния анимации
is_3d_mode = True  # Переменная для отслеживания режима


# Функция для создания главного окна
def create_main_window():
    global current_window

    # Создание главного окна
    main_window = QMainWindow()
    main_window.setWindowTitle("Физические визуализации")
    main_window.setGeometry(100, 100, 400, 300)

    # Основной макет
    layout = QVBoxLayout()

    # Настройка стилей для окна
    main_window.setStyleSheet(
        """
        QMainWindow {
            background-color: #2E3440;  /* Темный фон */
        }
        QLabel {
            color: #ECEFF4;  /* Белый текст */
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
        }
        QPushButton {
            background-color: #4C566A;  /* Серый фон */
            color: #ECEFF4;  /* Белый текст */
            font-size: 16px;
            padding: 10px;
            border-radius: 5px;  /* Закругленные углы */
            border: 2px solid #81A1C1;  /* Голубая рамка */
        }
        QPushButton:hover {
            background-color: #81A1C1;  /* Голубой фон при наведении */
            color: #2E3440;  /* Темный текст */
        }
        QLineEdit {
            background-color: #4C566A;  /* Серый фон */
            color: #ECEFF4;  /* Белый текст */
            font-size: 14px;
            padding: 5px;
            border-radius: 5px;  /* Закругленные углы */
            border: 2px solid #81A1C1;  /* Голубая рамка */
        }
    """
    )

    # Надпись для выбора режима
    label = QLabel("Выберите режим:")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)

    # Кнопка для открытия режима "3D визуализация фигур Лиссажу"
    lissajous_button = QPushButton("3D визуализация фигур Лиссажу")
    lissajous_button.clicked.connect(open_lissajous)
    layout.addWidget(lissajous_button)

    # Кнопка для открытия режима "Сложение двух волн - биение"
    beat_button = QPushButton("Сложение двух волн - биение")
    beat_button.clicked.connect(open_beats)
    layout.addWidget(beat_button)

    # Установка отступов и выравнивания
    layout.setSpacing(20)  # Расстояние между элементами
    layout.setContentsMargins(30, 30, 30, 30)  # Отступы от краев окна

    # Установка основного виджета
    container = QWidget()
    container.setLayout(layout)
    main_window.setCentralWidget(container)

    current_window = main_window
    return main_window


# Функция для переключения режима 2D/3D
def toggle_lissajous_mode(a_input, b_input, delta_input):
    global is_3d_mode
    is_3d_mode = not is_3d_mode  # Переключаем режим
    plot_lissajous(a_input, b_input, delta_input)  # Перерисовываем график


# Функция для открытия режима "3D визуализация фигур Лиссажу"
def open_lissajous():
    global current_window, fig, canvas, ax, animation, is_animation_running

    # Создание окна для фигур Лиссажу
    lissajous_window = QMainWindow()
    lissajous_window.setWindowTitle("3D Фигуры Лиссажу")
    lissajous_window.setGeometry(100, 100, 800, 600)

    # Настройка стилей для окна
    lissajous_window.setStyleSheet(
        """
        QMainWindow {
            background-color: #2E3440;  /* Темный фон */
        }
        QLabel {
            color: #ECEFF4;  /* Белый текст */
            font-size: 14px;
            padding: 5px;
        }
        QPushButton {
            background-color: #4C566A;  /* Серый фон */
            color: #ECEFF4;  /* Белый текст */
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;  /* Закругленные углы */
            border: 2px solid #81A1C1;  /* Голубая рамка */
        }
        QPushButton:hover {
            background-color: #81A1C1;  /* Голубой фон при наведении */
            color: #2E3440;  /* Темный текст */
        }
        QLineEdit {
            background-color: #4C566A;  /* Серый фон */
            color: #ECEFF4;  /* Белый текст */
            font-size: 14px;
            padding: 5px;
            border-radius: 5px;  /* Закругленные углы */
            border: 2px solid #81A1C1;  /* Голубая рамка */
        }
    """
    )

    # Основной макет
    layout = QVBoxLayout()

    # Создание графика
    fig = plt.figure(facecolor="#2E3440")  # Темный фон для графика
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    toolbar = NavigationToolbar(canvas, lissajous_window)
    layout.addWidget(toolbar)

    # Макет для параметров
    param_layout = QHBoxLayout()

    # Поле для ввода параметра ω1
    a_label = QLabel("ω1:")
    a_input = QLineEdit("5")
    param_layout.addWidget(a_label)
    param_layout.addWidget(a_input)

    # Поле для ввода параметра ω2
    b_label = QLabel("ω2:")
    b_input = QLineEdit("4")
    param_layout.addWidget(b_label)
    param_layout.addWidget(b_input)

    # Поле для ввода параметра φ (фаза)
    delta_label = QLabel("φ:")
    delta_input = QLineEdit("0.5")
    param_layout.addWidget(delta_label)
    param_layout.addWidget(delta_input)

    layout.addLayout(param_layout)

    # Кнопка для построения графика
    update_button = QPushButton("Построить")
    update_button.clicked.connect(lambda: plot_lissajous(a_input, b_input, delta_input))
    layout.addWidget(update_button)

    # Кнопка для переключения 2D/3D
    mode_button = QPushButton("Переключить 2D/3D")
    mode_button.clicked.connect(
        lambda: toggle_lissajous_mode(a_input, b_input, delta_input)
    )
    layout.addWidget(mode_button)

    # Кнопка для запуска/остановки анимации
    animation_button = QPushButton("Анимация")
    animation_button.clicked.connect(
        lambda: toggle_animation(a_input, b_input, delta_input)
    )
    layout.addWidget(animation_button)

    # Кнопка для сохранения графика
    save_button = QPushButton("Сохранить график")
    save_button.clicked.connect(save_plot)
    layout.addWidget(save_button)

    # Кнопка для возврата на главный экран
    back_button = QPushButton("На главный экран")
    back_button.clicked.connect(lambda: return_to_main(lissajous_window))
    layout.addWidget(back_button)

    # Установка основного виджета
    container = QWidget()
    container.setLayout(layout)
    lissajous_window.setCentralWidget(container)

    current_window.hide()
    lissajous_window.show()
    current_window = lissajous_window


# Функция для построения фигур Лиссажу
def plot_lissajous(a_input, b_input, delta_input):
    global fig, ax, is_3d_mode

    # Получение параметров из полей ввода
    ω1 = float(a_input.text())
    ω2 = float(b_input.text())
    φ = float(delta_input.text())

    # Генерация данных для фигуры Лиссажу
    t = np.linspace(0, 2 * np.pi, 1000)
    x = np.sin(ω1 * t + φ)
    y = np.sin(ω2 * t)
    z = t / (2 * np.pi)

    # Очистка и построение графика
    fig.clear()
    if is_3d_mode:
        z = t / (2 * np.pi)
        ax = fig.add_subplot(111, projection="3d", facecolor="#2E3440")
        ax.plot(x, y, z, label="Фигура Лиссажу", color="#000000")
    else:
        ax = fig.add_subplot(111, facecolor="#2E3440")
        ax.plot(x, y, label="Фигура Лиссажу", color="#000000")

    ax.grid(True, which="major", linestyle="-", linewidth=0.75, color="#81A1C1")
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, color="#81A1C1")
    ax.legend()
    canvas.draw()


# Функция для запуска/остановки анимации
def toggle_animation(a_input, b_input, delta_input):
    global animation, is_animation_running

    if is_animation_running:
        # Остановка анимации
        animation.event_source.stop()
        is_animation_running = False
        print("Анимация остановлена")
    else:
        # Запуск анимации
        def update(frame):
            delta_input.setText(str(float(delta_input.text()) + 0.1))
            plot_lissajous(a_input, b_input, delta_input)

        animation = FuncAnimation(fig, update, frames=50, interval=100)
        is_animation_running = True
        print("Анимация запущена")


# Функция для открытия режима "Сложение двух волн - биение"
def open_beats():
    global current_window, fig, canvas, ax, animation, is_animation_running

    # Создание окна для биений
    beats_window = QMainWindow()
    beats_window.setWindowTitle("Сложение двух волн - биение")
    beats_window.setGeometry(100, 100, 800, 600)

    # Настройка стилей для окна
    beats_window.setStyleSheet(
        """
        QMainWindow {
            background-color: #2E3440;  /* Темный фон */
        }
        QLabel {
            color: #ECEFF4;  /* Белый текст */
            font-size: 14px;
            padding: 5px;
        }
        QPushButton {
            background-color: #4C566A;  /* Серый фон */
            color: #ECEFF4;  /* Белый текст */
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;  /* Закругленные углы */
            border: 2px solid #81A1C1;  /* Голубая рамка */
        }
        QPushButton:hover {
            background-color: #81A1C1;  /* Голубой фон при наведении */
            color: #2E3440;  /* Темный текст */
        }
        QLineEdit {
            background-color: #4C566A;  /* Серый фон */
            color: #ECEFF4;  /* Белый текст */
            font-size: 14px;
            padding: 5px;
            border-radius: 5px;  /* Закругленные углы */
            border: 2px solid #81A1C1;  /* Голубая рамка */
        }
    """
    )

    # Основной макет
    layout = QVBoxLayout()

    # Создание графика
    fig = plt.figure(facecolor="#2E3440")  # Темный фон для графика
    canvas = FigureCanvas(fig)
    layout.addWidget(canvas)
    toolbar = NavigationToolbar(canvas, beats_window)
    layout.addWidget(toolbar)

    # Макет для параметров
    param_layout = QHBoxLayout()

    # Поле для ввода частоты f1
    f1_label = QLabel("f1:")
    f1_input = QLineEdit("5")
    param_layout.addWidget(f1_label)
    param_layout.addWidget(f1_input)

    # Поле для ввода частоты f2
    f2_label = QLabel("f2:")
    f2_input = QLineEdit("6")
    param_layout.addWidget(f2_label)
    param_layout.addWidget(f2_input)

    layout.addLayout(param_layout)

    # Кнопка для построения графика
    update_button = QPushButton("Построить")
    update_button.clicked.connect(lambda: plot_beats(f1_input, f2_input))
    layout.addWidget(update_button)

    # Кнопка для запуска/остановки анимации
    animation_button = QPushButton("Анимация")
    animation_button.clicked.connect(lambda: toggle_beats_animation(f1_input, f2_input))
    layout.addWidget(animation_button)

    # Кнопка для сохранения графика
    save_button = QPushButton("Сохранить график")
    save_button.clicked.connect(save_plot)
    layout.addWidget(save_button)

    # Кнопка для возврата на главный экран
    back_button = QPushButton("На главный экран")
    back_button.clicked.connect(lambda: return_to_main(beats_window))
    layout.addWidget(back_button)

    # Установка основного виджета
    container = QWidget()
    container.setLayout(layout)
    beats_window.setCentralWidget(container)

    current_window.hide()
    beats_window.show()
    current_window = beats_window


# Функция для построения биений
def plot_beats(f1_input, f2_input):
    global fig, ax

    # Получение параметров из полей ввода
    f1 = float(f1_input.text())
    f2 = float(f2_input.text())

    # Генерация данных для биений
    t = np.linspace(0, 1, 1000)
    y = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)

    # Очистка и построение графика
    fig.clear()
    ax = fig.add_subplot(111, facecolor="#2E3440")  # Темный фон для графика
    ax.plot(t, y, label="Биение", color="#000000")  # Голубой цвет линии\
    ax.grid(
        True, which="major", linestyle="-", linewidth=0.75, color="#81A1C1"
    )  # Основные линии
    ax.minorticks_on()
    ax.grid(
        True, which="minor", linestyle=":", linewidth=0.5, color="#81A1C1"
    )  # Вспомогательные линии
    ax.legend()
    canvas.draw()


# Функция для запуска/остановки анимации биений
def toggle_beats_animation(f1_input, f2_input):
    global animation, is_animation_running

    if is_animation_running:
        # Остановка анимации
        animation.event_source.stop()
        is_animation_running = False
        print("Анимация остановлена")
    else:
        # Запуск анимации
        def update(frame):
            f1_input.setText(str(float(f1_input.text()) + 0.1))
            plot_beats(f1_input, f2_input)

        animation = FuncAnimation(fig, update, frames=50, interval=100)
        is_animation_running = True
        print("Анимация запущена")


# Функция для сохранения графика
def save_plot():
    filename = "graph.png"
    fig.savefig(filename)
    QMessageBox.information(
        current_window, "Сохранено", f"График сохранен как {filename}"
    )


# Функция для возврата на главный экран
def return_to_main(window):
    global current_window
    window.hide()
    current_window = create_main_window()
    current_window.show()


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = create_main_window()
    main_window.show()
    sys.exit(app.exec_())
