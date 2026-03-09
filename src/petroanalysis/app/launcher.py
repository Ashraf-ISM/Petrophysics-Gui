import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from .main_window import MainWindow
from ..utils.paths import image_path


def create_app() -> QApplication:
    return QApplication(sys.argv)


def show_splash() -> QSplashScreen:
    splash_pix = QPixmap(str(image_path("app.webp")))
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.FramelessWindowHint)
    splash.show()
    return splash


def main() -> int:
    app = create_app()
    splash = show_splash()

    QTimer.singleShot(3000, splash.close)

    window = MainWindow()
    QTimer.singleShot(3000, window.show)

    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
