#ifndef BMSGUI_MAINWINDOW_H
#define BMSGUI_MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class BMSGUI_MainWindow; }
QT_END_NAMESPACE

class BMSGUI_MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    BMSGUI_MainWindow(QWidget *parent = nullptr);
    ~BMSGUI_MainWindow();

private:
    Ui::BMSGUI_MainWindow *ui;
};
#endif // BMSGUI_MAINWINDOW_H
