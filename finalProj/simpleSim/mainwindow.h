#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsScene>
#include <QGraphicsEllipseItem>
#include <QGraphicsLineItem>
#include<QDebug>
#include<QTimer>
#include<math.h>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    QGraphicsScene* scene;
    QGraphicsEllipseItem *ellipse;
    QGraphicsRectItem* rect;
    QGraphicsLineItem* top;
    QGraphicsLineItem* down;
    QGraphicsLineItem* left;
    QGraphicsLineItem* right;
    void applyMotionModel(float x_in,float y_in, float theta_in,float contLin, float contAng,float* x_out, float* y_out,float* theta_out);
    float x_in,x_out,y_in,y_out,theta_in,theta_out;
    void resetBot();
    QTimer* timer;


private slots:
    void moveBot();
};

#endif // MAINWINDOW_H
