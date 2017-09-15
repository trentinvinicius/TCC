package com.example.oodgles1;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.MotionEvent;
import android.view.KeyEvent;
// import android.util.Log;
import android.util.FloatMath;
// import android.media.MediaPlayer;
import android.content.Context;
import android.view.Menu ;
import android.view.MenuItem ;
import java.io.File ;
import java.io.FileOutputStream ;
import java.io.IOException ;

import android.content.res.AssetManager ;

public class oodActivity extends Activity implements View.OnTouchListener
{

    private MyGLView                m_view ;

    private AssetManager            m_assets ;



    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {

        super.onCreate(savedInstanceState) ;



        m_view = new MyGLView(this) ;
        setContentView(m_view) ;

        m_view.setKeepScreenOn(true) ;

        m_view.setOnTouchListener(this) ;

        m_assets = getAssets() ;

        NativeLib.instance().onCreate( m_assets ) ;

    }


    @Override
    protected void onPause() {
        super.onPause() ;
        m_view.onPause() ;


        NativeLib.instance().onPause() ;
    }


    @Override
    protected void onResume() {
        super.onResume() ;
        m_view.onResume() ;


        NativeLib.instance().onResume() ;
    }


    @Override
    protected void onDestroy() {
        super.onDestroy() ;

        NativeLib.instance().onDestroy() ;
    }



    @Override
    public boolean onTouch(View v, MotionEvent event) {
        int n_points = event.getPointerCount() ;
        int action = event.getAction() & MotionEvent.ACTION_MASK ;

        if( (n_points == 1) ) {
            if( action == MotionEvent.ACTION_DOWN ) {
                NativeLib.instance().enqueueMouseButtonEvent(1, event.getX(0), event.getY(0), 1) ;

            } else if( action == MotionEvent.ACTION_UP ) {
                NativeLib.instance().enqueueMouseButtonEvent(1, event.getX(0), event.getY(0), 0) ;

            } else if( action == MotionEvent.ACTION_MOVE ) {
                NativeLib.instance().enqueueMotionEvent(event.getX(0), event.getY(0)) ;
            }
        }

        else if( (n_points == 2) ) {

            float   dx = event.getX(1) - event.getX(0) ;
            float   dy = event.getY(1) - event.getY(0) ;

            float   l = FloatMath.sqrt(dx*dx + dy*dy) ;




            if( action == 5 ) {
                NativeLib.instance().enqueueMouseButtonEvent(1, 0.0f, l, 0) ;
                NativeLib.instance().enqueueMouseButtonEvent(3, 0.0f, l, 1) ;

            } else if( action == 6 ) {
                NativeLib.instance().enqueueMouseButtonEvent(1, 0.0f, l, 0) ;
                NativeLib.instance().enqueueMouseButtonEvent(3, 0.0f, l, 0) ;

            } else if( action == MotionEvent.ACTION_MOVE ) {
                NativeLib.instance().enqueueMotionEvent(0.0f, l) ;
            }
        }

        return true ;
    }


    @Override
    public void onBackPressed() {

        if( true ) {
            super.onBackPressed() ;
            return ;
        }

//         NativeLib.instance().enqueueKeyboardEvent('q', 1) ;
    }





    @Override
    public boolean onCreateOptionsMenu(Menu menu) {


        try {
            String[]    file_list = m_assets.list("") ;


            for( String s: file_list ) {

                if( s.contains(".osgb") ) {
                    menu.add( s ) ;
                }
            }


            return true ;

        } catch( IOException e ) {
            return false ;
        }
    }




    @Override
    public boolean onOptionsItemSelected(MenuItem item)
    {
        String  title = item.getTitle().toString() ;


        NativeLib.instance().setSceneData( title ) ;

        return true ;
    }
}
