#include "bmsgui_mainwindow.h"
#include "ui_bmsgui_mainwindow.h"

BMSGUI_MainWindow::BMSGUI_MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::BMSGUI_MainWindow)
{
    ui->setupUi(this);
}

BMSGUI_MainWindow::~BMSGUI_MainWindow()
{
    delete ui;
}

