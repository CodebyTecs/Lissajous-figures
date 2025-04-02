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

# Глобальные переменные
current_window = None
fig = None
canvas = None
ax = None
animation = None
is_animation_running = False
is_3d_mode = True

def create_main_window():
    global current_window

    main_window = QMainWindow()
    main_window.setWindowTitle("Физические визуализации")
    main_window.setGeometry(200, 200, 800, 600)

    layout = QVBoxLayout()
    main_window.setStyleSheet("""
        QMainWindow { background-color: white; }
        QLabel { color: black; font-size: 18px; font-weight: bold; padding: 10px; }
        QPushButton { 
            background-color: white; color: black; font-size: 16px; 
            padding: 10px; border-radius: 5px; border: 2px solid black;
            min-width: 300px;
        }
        QPushButton:hover { background-color: black; color: white; }
        QLineEdit { 
            background-color: white; color: black; font-size: 14px; 
            padding: 5px; border-radius: 5px; border: 2px solid black;
        }
    """)

    label = QLabel("Выберите режим:")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label)

    buttons = [
        ("3D визуализация фигур Лиссажу", open_lissajous),
        ("Сложение двух волн - биение", open_beats)
    ]

    for text, handler in buttons:
        btn = QPushButton(text)
        btn.clicked.connect(handler)
        layout.addWidget(btn)

    container = QWidget()
    container.setLayout(layout)
    main_window.setCentralWidget(container)

    current_window = main_window
    return main_window

def open_lissajous_graph_in_new_window(a_input, b_input, delta_input):
    global new_window

    new_window = QMainWindow()
    new_window.setWindowTitle("График фигуры Лиссажу")
    new_window.setGeometry(200, 200, 1000, 800)

    layout = QVBoxLayout()
    fig_new = plt.figure(figsize=(10, 8), facecolor="white")
    canvas_new = FigureCanvas(fig_new)
    layout.addWidget(canvas_new)
    layout.addWidget(NavigationToolbar(canvas_new, new_window))

    ω1 = float(a_input.text())
    ω2 = float(b_input.text())
    φ = float(delta_input.text())

    t = np.linspace(0, 2 * np.pi, 1000)
    x = np.cos(ω1 * t)
    y = np.cos(ω2 * t + φ)

    fig_new.clear()
    if is_3d_mode:
        z = t / (2 * np.pi)
        ax = fig_new.add_subplot(111, projection="3d", facecolor="white")
        ax.plot(x, y, z, label="Фигура Лиссажу", color="black")
        ax.set_zlabel("ось Z")
    else:
        ax = fig_new.add_subplot(111, facecolor="white")
        ax.plot(x, y, label="Фигура Лиссажу", color="black")

    ax.set_xlabel("ось X")
    ax.set_ylabel("ось Y")
    ax.grid(True, which="major", linestyle="-", linewidth=0.75, color="black")
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, color="gray")
    ax.legend()
    canvas_new.draw()

    container = QWidget()
    container.setLayout(layout)
    new_window.setCentralWidget(container)
    new_window.show()

def open_beats_graph_in_new_window(a_input, b_input):
    global new_window

    new_window = QMainWindow()
    new_window.setWindowTitle("График биений")
    new_window.setGeometry(200, 200, 1000, 800)

    layout = QVBoxLayout()
    fig_new = plt.figure(figsize=(10, 8), facecolor="white")
    canvas_new = FigureCanvas(fig_new)
    layout.addWidget(canvas_new)
    layout.addWidget(NavigationToolbar(canvas_new, new_window))

    ω1 = float(a_input.text())
    ω2 = float(b_input.text())
    t = np.linspace(0, 2, 1000)
    y = 2 * np.cos(((ω1 - ω2) * t)/2) * np.cos(((ω1 + ω2) * t)/2)

    fig_new.clear()
    ax = fig_new.add_subplot(111, facecolor="white")
    ax.plot(t, y, label="Биение", color="black")
    ax.grid(True, which="major", linestyle="-", linewidth=0.75, color="black")
    ax.minorticks_on()
    ax.grid(True, which="minor", linestyle=":", linewidth=0.5, color="gray")
    ax.set_xlabel("ось X")
    ax.set_ylabel("ось Y")
    ax.legend()
    canvas_new.draw()

    container = QWidget()
    container.setLayout(layout)
    new_window.setCentralWidget(container)
    new_window.show()

def toggle_lissajous_mode(a_input, b_input, delta_input):
    global is_3d_mode
    is_3d_mode = not is_3d_mode
    plot_lissajous(a_input, b_input, delta_input)

def open_lissajous():
    global current_window, fig, canvas, ax, animation, is_animation_running

    lissajous_window = QMainWindow()
    lissajous_window.setWindowTitle("3D Фигуры Лиссажу")
    lissajous_window.setGeometry(100, 100, 1000, 800)
    lissajous_window.setStyleSheet("""
        QMainWindow { background-color: white; }
        QLabel { color: black; font-size: 14px; padding: 5px; }
        QPushButton { 
            background-color: white; color: black; font-size: 14px; 
            padding: 8px; border-radius: 5px; border: 2px solid black;
            min-width: 200px;
        }
        QPushButton:hover { background-color: black; color: white; }
        QLineEdit { 
            background-color: white; color: black; font-size: 14px; 
            padding: 5px; border-radius: 5px; border: 2px solid black;
        }
    """)

    main_layout = QVBoxLayout()
    fig = plt.figure(figsize=(10, 8), facecolor="white")
    canvas = FigureCanvas(fig)
    main_layout.addWidget(canvas)
    main_layout.addWidget(NavigationToolbar(canvas, lissajous_window))

    # Параметры ввода
    param_layout = QHBoxLayout()
    inputs = [
        ("ω1:", "1"),
        ("ω2:", "1"),
        ("φ:", "3.14")
    ]
    input_widgets = []
    for label, default in inputs:
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(label))
        entry = QLineEdit(default)
        hbox.addWidget(entry)
        param_layout.addLayout(hbox)
        input_widgets.append(entry)
    main_layout.addLayout(param_layout)

    # Группировка кнопок по 2 в строке
    button_pairs = [
        ("Построить", lambda: plot_lissajous(*input_widgets)),
        ("Открыть график в новом окне", lambda: open_lissajous_graph_in_new_window(*input_widgets)),
        ("Переключить 2D/3D", lambda: toggle_lissajous_mode(*input_widgets)),
        ("Анимация", lambda: toggle_animation(*input_widgets)),
        ("Сохранить график", save_plot),
        ("На главный экран", lambda: return_to_main(lissajous_window))
    ]

    for i in range(0, len(button_pairs), 2):
        hbox = QHBoxLayout()
        if i < len(button_pairs):
            btn1 = QPushButton(button_pairs[i][0])
            btn1.clicked.connect(button_pairs[i][1])
            hbox.addWidget(btn1)
        if i+1 < len(button_pairs):
            btn2 = QPushButton(button_pairs[i+1][0])
            btn2.clicked.connect(button_pairs[i+1][1])
            hbox.addWidget(btn2)
        main_layout.addLayout(hbox)

    container = QWidget()
    container.setLayout(main_layout)
    lissajous_window.setCentralWidget(container)

    current_window.hide()
    lissajous_window.show()
    current_window = lissajous_window

def plot_lissajous(a_input, b_input, delta_input):
    global fig, ax, is_3d_mode

    try:
        ω1 = float(a_input.text())
        ω2 = float(b_input.text())
        φ = float(delta_input.text())

        t = np.linspace(0, 2 * np.pi, 1000)
        x = np.cos(ω1 * t)
        y = np.cos(ω2 * t + φ)

        fig.clear()
        if is_3d_mode:
            z = t / (2 * np.pi)
            ax = fig.add_subplot(111, projection="3d", facecolor="white")
            ax.plot(x, y, z, label="Фигура Лиссажу", color="black")
            ax.set_zlabel("ось Z")
        else:
            ax = fig.add_subplot(111, facecolor="white")
            ax.plot(x, y, label="Фигура Лиссажу", color="black")

        ax.set_xlabel("ось X")
        ax.set_ylabel("ось Y")
        ax.grid(True, which="major", linestyle="-", linewidth=0.75, color="black")
        ax.minorticks_on()
        ax.grid(True, which="minor", linestyle=":", linewidth=0.5, color="gray")
        ax.legend()
        canvas.draw()
    except ValueError:
        QMessageBox.warning(current_window, "Ошибка", "Пожалуйста, введите корректные числовые значения")


def toggle_animation(a_input, b_input, delta_input):
    global animation, is_animation_running

    if is_animation_running:
        animation.event_source.stop()
        is_animation_running = False
    else:
        try:
            ω1 = float(a_input.text())
            ω2 = float(b_input.text())
            initial_φ = float(delta_input.text())

            # Сохраняем начальное значение φ
            current_φ = initial_φ

            def update(frame):
                nonlocal current_φ

                # Увеличиваем фазу на каждом кадре
                current_φ += 0.01
                delta_input.setText(f"{current_φ:.2f}")

                # Пересчитываем данные с новым φ
                t = np.linspace(0, 2 * np.pi, 1000)
                x = np.cos(ω1 * t)
                y = np.cos(ω2 * t + current_φ)

                # Очищаем и перерисовываем график
                ax.clear()

                if is_3d_mode:
                    z = t / (2 * np.pi)
                    ax.plot(x, y, z, color="black")
                    ax.set_zlabel("ось Z")
                else:
                    ax.plot(x, y, color="black")

                ax.set_xlabel("ось X")
                ax.set_ylabel("ось Y")
                ax.grid(True, which="major", linestyle="-", linewidth=0.75, color="black")
                ax.minorticks_on()
                ax.grid(True, which="minor", linestyle=":", linewidth=0.5, color="gray")
                ax.legend()
                canvas.draw()

            # Запускаем анимацию с бесконечным числом кадров
            animation = FuncAnimation(fig, update, frames=None, interval=100)
            is_animation_running = True

        except ValueError:
            QMessageBox.warning(current_window, "Ошибка", "Пожалуйста, введите корректные числовые значения")

def open_beats():
    global current_window, fig, canvas, ax, animation, is_animation_running

    beats_window = QMainWindow()
    beats_window.setWindowTitle("Сложение двух волн - биение")
    beats_window.setGeometry(100, 100, 1000, 800)
    beats_window.setStyleSheet("""
        QMainWindow { background-color: white; }
        QLabel { color: black; font-size: 14px; padding: 5px; }
        QPushButton { 
            background-color: white; color: black; font-size: 14px; 
            padding: 8px; border-radius: 5px; border: 2px solid black;
            min-width: 200px;
        }
        QPushButton:hover { background-color: black; color: white; }
        QLineEdit { 
            background-color: white; color: black; font-size: 14px; 
            padding: 5px; border-radius: 5px; border: 2px solid black;
        }
    """)

    main_layout = QVBoxLayout()
    fig = plt.figure(figsize=(10, 8), facecolor="white")
    canvas = FigureCanvas(fig)
    main_layout.addWidget(canvas)
    main_layout.addWidget(NavigationToolbar(canvas, beats_window))

    # Параметры ввода
    param_layout = QHBoxLayout()
    inputs = [
        ("ω1:", "1"),
        ("ω2:", "1.1")
    ]
    input_widgets = []
    for label, default in inputs:
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(label))
        entry = QLineEdit(default)
        hbox.addWidget(entry)
        param_layout.addLayout(hbox)
        input_widgets.append(entry)
    main_layout.addLayout(param_layout)

    # Группировка кнопок по 2 в строке
    button_pairs = [
        ("Построить", lambda: plot_beats(*input_widgets)),
        ("Открыть график в новом окне", lambda: open_beats_graph_in_new_window(*input_widgets)),
        ("Анимация", lambda: toggle_beats_animation(*input_widgets)),
        ("Сохранить график", save_plot),
        ("На главный экран", lambda: return_to_main(beats_window))
    ]

    for i in range(0, len(button_pairs), 2):
        hbox = QHBoxLayout()
        if i < len(button_pairs):
            btn1 = QPushButton(button_pairs[i][0])
            btn1.clicked.connect(button_pairs[i][1])
            hbox.addWidget(btn1)
        if i+1 < len(button_pairs):
            btn2 = QPushButton(button_pairs[i+1][0])
            btn2.clicked.connect(button_pairs[i+1][1])
            hbox.addWidget(btn2)
        main_layout.addLayout(hbox)

    container = QWidget()
    container.setLayout(main_layout)
    beats_window.setCentralWidget(container)

    current_window.hide()
    beats_window.show()
    current_window = beats_window

def plot_beats(f1_input, f2_input):
    global fig, ax

    try:
        ω1 = float(f1_input.text())
        ω2 = float(f2_input.text())

        t = np.linspace(0, 2, 1000)
        y = 2 * np.cos(((ω1 - ω2) * t)/2) * np.cos(((ω1 + ω2) * t)/2)

        fig.clear()
        ax = fig.add_subplot(111, facecolor="white")
        ax.plot(t, y, label="Биение", color="black")
        ax.grid(True, which="major", linestyle="-", linewidth=0.75, color="black")
        ax.minorticks_on()
        ax.grid(True, which="minor", linestyle=":", linewidth=0.5, color="gray")
        ax.set_xlabel("ось X")
        ax.set_ylabel("ось Y")
        ax.legend()
        canvas.draw()
    except ValueError:
        QMessageBox.warning(current_window, "Ошибка", "Пожалуйста, введите корректные числовые значения")

def toggle_beats_animation(ω1_input, ω2_input):
    global animation, is_animation_running

    if is_animation_running:
        animation.event_source.stop()
        is_animation_running = False
    else:
        def update(frame):
            try:
                ω1_input.setText(str(float(ω1_input.text()) + 0.05))
                plot_beats(ω1_input, ω2_input)
            except ValueError:
                animation.event_source.stop()
                is_animation_running = False
                QMessageBox.warning(current_window, "Ошибка", "Некорректное значение частоты")

        animation = FuncAnimation(fig, update, frames=50, interval=100)
        is_animation_running = True

def save_plot():
    filename = "graph.png"
    fig.savefig(filename)
    QMessageBox.information(current_window, "Сохранено", f"График сохранен как {filename}")

def return_to_main(window):
    global current_window
    window.hide()
    current_window = create_main_window()
    current_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = create_main_window()
    main_window.show()
    sys.exit(app.exec_())
