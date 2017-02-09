#include "mainwindow.h"
#include <QApplication>
#include "webcam.h"

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    webCam wc;
    wc.show();

    return a.exec();
}
