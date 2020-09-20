#include "bmsgui_mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    BMSGUI_MainWindow w;
    w.show();
    return a.exec();
}
