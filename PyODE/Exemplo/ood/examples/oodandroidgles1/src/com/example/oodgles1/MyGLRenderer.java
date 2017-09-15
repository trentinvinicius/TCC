package com.example.oodgles1;

import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;

import android.opengl.GLSurfaceView;

import android.app.Activity;
// import android.util.Log;
import java.io.File ;
import java.io.FileInputStream ;
import java.io.FileOutputStream ;

public class MyGLRenderer implements GLSurfaceView.Renderer {


    private long    m_start_millis = -1 ;
    private long    m_last_millis = -1 ;



    public void onDrawFrame(GL10 gl) {


        if( m_start_millis < 0 ) {
            m_start_millis = System.currentTimeMillis() ;
            m_last_millis = m_start_millis ;
        }


        long    cur_millis = System.currentTimeMillis() ;
        long    millis = cur_millis - m_start_millis ;
        float   cur_time = (float)millis / 1000.0f ;

        m_last_millis = cur_millis ;



        NativeLib.instance().enqueueFrameEvent(cur_time) ;
        NativeLib.instance().onDrawFrame(cur_time);
    }





    public void onSurfaceChanged(GL10 gl, int w, int h) {
        NativeLib.instance().onSurfaceChanged(w,  h) ;
    }



    public void onSurfaceCreated(GL10 gl, EGLConfig conf) {
        NativeLib.instance().onSurfaceCreated() ;
    }
}