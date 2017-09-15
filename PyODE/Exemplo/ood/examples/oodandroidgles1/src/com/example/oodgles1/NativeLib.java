package com.example.oodgles1;

import android.content.res.AssetManager ;

public class NativeLib {


    private static final NativeLib  m_instance = new NativeLib() ;

    private NativeLib() {
        super() ;
    }

    public native void      onCreate( AssetManager mgr ) ;
    public native void      onPause() ;
    public native void      onResume() ;
    public native void      onDestroy() ;
    public native void      onSurfaceCreated() ;
    public native void      onSurfaceChanged(float w, float h) ;
    public native void      onDrawFrame(float t) ;
    public native void      enqueueMouseButtonEvent(int button, float x, float y, int pressed) ;
    public native void      enqueueKeyboardEvent(int key, int pressed) ;
    public native void      enqueueMotionEvent(float x, float y) ;
    public native void      enqueueFrameEvent(float time) ;
    public native void      setSceneData( String asset_name ) ;


    public static NativeLib instance() {
        return m_instance ;
    }



    static {
        System.loadLibrary("oodgles1-native") ;
    }

}
