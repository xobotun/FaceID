/****************************************************************************
 *  webcam
 *
 *  Copyright (c) 2012 by Nikita Belov <null@deltaz.org>
 *
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************
*****************************************************************************/

#ifndef WEBCAM_H
#define WEBCAM_H

#include <QClipboard>
#include <QtMultimedia/QtMultimedia>
#include <QtMultimediaWidgets/QtMultimediaWidgets>
#include <QtWidgets/QtWidgets>

#include "ui_webcam.h"
#include "ui_webcamselect.h"

class webCam : public QWidget
{
	Q_OBJECT

public:
	webCam();
	~webCam();

	bool nativeEvent( QByteArray ba, void *message, long *result );

public slots:
	void cameraError( QCamera::Error value );
	void cameraStateChanged( QCamera::State state );
	void capture( bool checked = false );

protected:
	void mouseMoveEvent( QMouseEvent* event );
	void mousePressEvent( QMouseEvent* event );
	void paintEvent( QPaintEvent *event );
	void resizeEvent( QResizeEvent *event );

private:
	Ui::webCamClass ui;
	Ui::webCamSelectClass select_ui;

	QPoint m_drag_pos;

	static QByteArray m_defaultDevice;
	QDialog *m_selectDialog;

	QPointer< QCamera > m_camera;
	QPointer< QCameraImageCapture > m_imageCapture;

	QPixmap m_pixmap;

	QTimer *m_timer;

	int m_timerPaintState;
};

#endif // WEBCAM_H
