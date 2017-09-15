/*!
 * @file oodgles1-native.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2016 by Rocco Martino                                   *
 *   martinorocco@gmail.com                                                *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

/* ======================================================================= */
/* ....................................................................... */
#include <jni.h>
#include <android/asset_manager.h>
#include <android/asset_manager_jni.h>

#include <ood/Notify>

#include <sstream>

#include <osg/Notify>

#include <osgViewer/Viewer>

#include <osgDB/Registry>
#include <osgDB/FileUtils>
#include <osgDB/FileNameUtils>

#include <osgGA/TrackballManipulator>
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
USE_OSGPLUGIN(osg2) ;

USE_SERIALIZER_WRAPPER_LIBRARY(osg) ;
USE_SERIALIZER_WRAPPER_LIBRARY(ood) ;

USE_SERIALIZER_WRAPPER(DefaultUserDataContainer) ;
USE_SERIALIZER_WRAPPER(BoolValueObject) ;

/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
#define FN( FNAME ) Java_com_example_oodgles1_NativeLib_##FNAME
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
extern "C" {

void        FN( onCreate                ) ( JNIEnv* env, jobject self, jobject asset_manager ) ;

void        FN( onPause                 ) ( JNIEnv* env, jobject self ) ;

void        FN( onResume                ) ( JNIEnv* env, jobject self ) ;

void        FN( onDestroy               ) ( JNIEnv* env, jobject self ) ;

void        FN( onSurfaceCreated        ) ( JNIEnv* env, jobject self ) ;

void        FN( onSurfaceChanged        ) ( JNIEnv* env, jobject self, float w, float h ) ;

void        FN( onDrawFrame             ) ( JNIEnv* env, jobject self, float t ) ;

void        FN( enqueueMouseButtonEvent ) ( JNIEnv* env, jobject self, int button, float x, float y, int pressed ) ;

void        FN( enqueueKeyboardEvent    ) ( JNIEnv* env, jobject self, int key, int pressed ) ;

void        FN( enqueueMotionEvent      ) ( JNIEnv* env, jobject self, float x, float y ) ;

void        FN( enqueueFrameEvent       ) ( JNIEnv* env, jobject self, float time ) ;

void        FN( setSceneData            ) ( JNIEnv* env, jobject self, jstring file_name ) ;

} // extern "C"
/* ....................................................................... */
/* ======================================================================= */








/* ======================================================================= */
/* ....................................................................... */
osg::Node*      read_node_file( const std::string& file_name ) ;


osg::Object*    read_object_file( const std::string& file_name ) ;


void            set_scene_data( const std::string& file_name ) ;
/* ....................................................................... */
/* ======================================================================= */








/* ======================================================================= */
/* ....................................................................... */
typedef struct {

    AAssetManager*      mAssetManager ;

    osg::ref_ptr<osgViewer::Viewer> mViewer ;

    osg::Vec2       mWindowSize ;

    osg::Timer      mTimer ;
} LocalData ;


static LocalData    gLocalData ;
/* ....................................................................... */
/* ======================================================================= */








/* ======================================================================= */
/* ....................................................................... */
void
FN( onCreate )
( JNIEnv* env, jobject self, jobject asset_manager )
{
    gLocalData.mAssetManager = NULL ;

    gLocalData.mViewer = NULL ;

    gLocalData.mWindowSize.set(-1, -1) ;




    osg::initNotifyLevel() ;
//     osg::setNotifyLevel(osg::ALWAYS) ;

    psInstallAndroidNotifyHandler() ;

//     psLogLevel = LOG_LEVEL_NONE ;


    gLocalData.mAssetManager = AAssetManager_fromJava(env, asset_manager) ;


    gLocalData.mTimer.setStartTick() ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( onPause )
( JNIEnv* env, jobject self )
{
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( onResume )
( JNIEnv* env, jobject self )
{
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( onDestroy )
( JNIEnv* env, jobject self )
{

    gLocalData.mAssetManager = NULL ;

    gLocalData.mViewer = NULL ;

    gLocalData.mWindowSize.set( -1, -1 ) ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( onSurfaceCreated )
( JNIEnv* env, jobject self )
{
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( onSurfaceChanged )
( JNIEnv* env, jobject self, float w, float h )
{
    gLocalData.mWindowSize = osg::Vec2( w, h ) ;



    gLocalData.mViewer = new osgViewer::Viewer() ;





    osgViewer::Viewer*  viewer = gLocalData.mViewer.get() ;



    viewer->setCameraManipulator( new osgGA::TrackballManipulator() ) ;




    viewer->setThreadingModel( osgViewer::Viewer::CullDrawThreadPerContext ) ;


    viewer->setReleaseContextAtEndOfFrameHint( false ) ;


    viewer->setUpViewerAsEmbeddedInWindow( 0, 0, w, h ) ;


    set_scene_data( "rigidbody.osgb" ) ;





    viewer->realize() ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( onDrawFrame )
( JNIEnv* env, jobject self, float t )
{
    gLocalData.mViewer->frame( t ) ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( enqueueMouseButtonEvent )
( JNIEnv* env, jobject self, int button, float x, float y, int pressed )
{
    osgViewer::Viewer*  viewer = gLocalData.mViewer.get() ;

    const osg::Vec2&    ws = gLocalData.mWindowSize ;


    viewer->getEventQueue()->setMouseInputRange( 0, 0, ws.x(), ws.y() ) ;




    if( button == 1  &&  pressed == 1 ) {

        if( gLocalData.mTimer.time_s() <= 0.3 ) {

            viewer->getEventQueue()->keyPress(osgGA::GUIEventAdapter::KEY_Space) ;
            viewer->getEventQueue()->keyRelease(osgGA::GUIEventAdapter::KEY_Space) ;
        }


        gLocalData.mTimer.setStartTick() ;

    }




    if( pressed ) {
        viewer->getEventQueue()->mouseButtonPress(x, y, button) ;
    } else {
        viewer->getEventQueue()->mouseButtonRelease(x, y, button) ;
    }
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( enqueueKeyboardEvent )
( JNIEnv* env, jobject self, int key, int pressed )
{
    osgViewer::Viewer*  viewer = gLocalData.mViewer.get() ;


    if( pressed ) {
        viewer->getEventQueue()->keyPress(key) ;
    } else {
        viewer->getEventQueue()->keyRelease(key) ;
    }
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( enqueueMotionEvent )
( JNIEnv* env, jobject self, float x, float y )
{
    osgViewer::Viewer*  viewer = gLocalData.mViewer.get() ;

    const osg::Vec2&    ws = gLocalData.mWindowSize ;


    viewer->getEventQueue()->setMouseInputRange( 0, 0, ws.x(), ws.y() ) ;

    viewer->getEventQueue()->mouseMotion(x, y) ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( enqueueFrameEvent )
( JNIEnv* env, jobject self, float time )
{
    osgViewer::Viewer*  viewer = gLocalData.mViewer.get() ;


    viewer->getEventQueue()->frame( time ) ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
FN( setSceneData )
( JNIEnv* env, jobject self, jstring jfile_name )
{
    std::string     file_name = env->GetStringUTFChars( jfile_name, NULL ) ;


    set_scene_data( file_name ) ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
void
set_scene_data( const std::string& file_name )
{
    osg::Node*      graph = read_node_file( file_name ) ;


    gLocalData.mViewer->setSceneData( graph ) ;

    gLocalData.mViewer->realize() ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
osg::Node*
read_node_file( const std::string& file_name )
{
    AAsset* asset = AAssetManager_open(gLocalData.mAssetManager, file_name.c_str(), AASSET_MODE_UNKNOWN ) ;

    long size = AAsset_getLength(asset) ;

    char*   buffer = (char*) malloc (sizeof(char)*size) ;

    AAsset_read (asset,buffer,size);

    AAsset_close(asset);


    std::istringstream  data( std::string(buffer, size) ) ;

    free(buffer) ;





    std::string ext = osgDB::getFileExtension( file_name );


    osgDB::ReaderWriter* rw = osgDB::Registry::instance()->getReaderWriterForExtension( ext );


    PS_ASSERT1( rw.valid() ) ;



    osgDB::ReaderWriter::ReadResult rr = rw->readNode(data) ;




    return rr.takeNode() ;
}
/* ....................................................................... */
/* ======================================================================= */










/* ======================================================================= */
/* ....................................................................... */
osg::Object*
read_object_file( const std::string& file_name )
{
    AAsset* asset = AAssetManager_open(gLocalData.mAssetManager, file_name.c_str(), AASSET_MODE_UNKNOWN ) ;

    long size = AAsset_getLength(asset) ;

    char*   buffer = (char*) malloc (sizeof(char)*size) ;

    AAsset_read (asset,buffer,size);

    AAsset_close(asset);


    std::istringstream  data( std::string(buffer, size) ) ;

    free(buffer) ;





    std::string ext = osgDB::getFileExtension( file_name );


    osgDB::ReaderWriter* rw = osgDB::Registry::instance()->getReaderWriterForExtension( ext );


    PS_ASSERT1( rw.valid() ) ;



    osgDB::ReaderWriter::ReadResult rr = rw->readObject(data) ;




    return rr.takeObject() ;
}
/* ....................................................................... */
/* ======================================================================= */
