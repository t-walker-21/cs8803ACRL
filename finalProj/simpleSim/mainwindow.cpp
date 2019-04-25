#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    scene = new QGraphicsScene(this);
    ui->graphicsView->setScene(scene);


    QBrush redBrush(Qt::red);
    QBrush blueBrush(Qt::blue);
    QPen blackPen(Qt::black);

    blackPen.setWidth(6);

    ellipse = scene->addEllipse(-250,-50,1,1,blackPen,redBrush);

    rect = scene->addRect(-800,0,50,10,blackPen,blueBrush);

    top = scene->addLine(-900,-400,100,-400);
    down = scene->addLine(-900,200,100,200);
    left = scene->addLine(-880,-400,-880,200);
    right = scene->addLine(90,-400,90,200);

    lidar = scene->addLine(-750,5,-700,5);

    ui->graphicsView->setFixedHeight(800);
    ui->graphicsView->setFixedWidth(1000);
    timer = new QTimer();
    timer->setInterval(100);
    connect(timer,SIGNAL(timeout()),this,SLOT(moveBot()));
    //connect(ui->pushButton,SIGNAL(clicked(bool)),this,SLOT(moveBot()));

    timer->start();

    x_in = -410;
    y_in = 10;
    theta_in = 0;

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::moveBot()
{

    applyMotionModel(x_in,y_in,theta_in,0.0,0.0,&x_out,&y_out,&theta_out);

   //qDebug() << "y_now: " << this->rect->y();
   //qDebug() << "x_now: " << this->rect->x();

    qDebug() << "rect: " << rect->mapFromScene(800,0) << endl;
    //qDebug() << "point: " << ellipse->scenePos() << endl;
    //qDebug() << rect->rotation() << endl;


    //ellipse->setPos(lidar->mapFromScene(-800,0));
    //ellipse->setY(lidar->scenePos().y());

    //this->rect->setX(x_out);
    //this->rect->setY(y_out);
    //this->rect->setX(-435);

    this->rect->moveBy(1,0);
    this->lidar->moveBy(1,0);

    //this->rect->setTransformOriginPoint(QPoint((-500+this->rect->x())+25,5));
    //this->rect->setRotation(this->rect->rotation() + 1);
    //x_in = x_out;
    //y_in = y_out;
    //theta_in = theta_out;
    //rect->rotate(this->rect->rotation()+1);
    //lidar->setRotation(this->rect->rotation()+1);

    //qDebug() << "x_out: " << x_out;

    //qDebug() << rect->collidesWithItem(ellipse);
    //qDebug() << ui->graphicsView->width();
    //qDebug() << ui->graphicsView->height();
    if (/*rect->collidesWithItem(ellipse) ||*/ rect->collidesWithItem(left) || rect->collidesWithItem(right) || rect->collidesWithItem(top) || rect->collidesWithItem(down))
    {
        resetBot();
    }


}

void MainWindow::resetBot()
{
    this->x_in = 0;
    this->y_in = 0;
    theta_in = 0;
    this->rect->setX(0);
    this->rect->setY(0);
    this->rect->setRotation(0);
    this->lidar->setY(0);
    this->lidar->setX(0);
    this->lidar->setRotation(0);
}



void MainWindow::applyMotionModel(float x_in, float y_in, float theta_in, float contLin, float contAng,float* x_out, float* y_out,float* theta_out)
{

    float d_theta_nom = contLin;
    float wb = 2.0;
    float l_radius = 0.25;
    float r_radius = 0.25;
    float d_theta_max_dev = 0.2;


    float r_dTheta = d_theta_nom + d_theta_max_dev*contAng;
    float l_dTheta = d_theta_nom - d_theta_max_dev*contAng;

    float R = r_radius * r_dTheta;
    float L = l_radius * l_dTheta;

    //qDebug() << "R trav: " << R;
    //qDebug() << "L trav: " << L;


    if (R == L)
    {
        *x_out = x_in + ((R+L) / 2) * cos(theta_in);
        *y_out = y_in + ((R+L) / 2) * sin(theta_in);

    }

    else
    {
        *x_out = x_in + wb/2 * (R+L)/(R-L) * (sin((R-L)/wb + theta_in) - sin(theta_in));
        *y_out = y_in - wb/2 * (R+L)/(R-L) * (cos((R-L)/wb + theta_in) - cos(theta_in));
    }

    *theta_out  = theta_in + (R-L)/wb;


}
