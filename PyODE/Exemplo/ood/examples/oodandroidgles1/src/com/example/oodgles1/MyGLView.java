package com.example.oodgles1;

import android.content.Context;
import android.opengl.GLSurfaceView;

public class MyGLView extends GLSurfaceView {

    MyGLRenderer    m_renderer ;

    public MyGLView(Context context) {
        super(context);


        m_renderer = new MyGLRenderer() ;
        setRenderer(m_renderer) ;
    }
}
