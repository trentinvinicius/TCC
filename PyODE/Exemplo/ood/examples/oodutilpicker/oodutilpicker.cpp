#include <ood/Manager>
#include <ood/Space>
#include <ood/Box>
#include <ood/Notify>

#include <oodUtil/Picker>
#include <oodUtil/ControllerBase>

#include <osgViewer/Viewer>

#include <osgDB/ReadFile>
#include <osgDB/WriteFile>

#include <osgGA/TrackballManipulator>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif




class MyHandler: public oodUtil::ControllerBase
{
public:
    MyHandler( oodUtil::Picker* picker = NULL ):
    m_picker(picker)
    {
        onLeftMouseButton()->connect(this, &MyHandler::lmb) ;
        onRightMouseButton()->connect(this, &MyHandler::rmb) ;
        onMouseMoved()->connect(this, &MyHandler::moved) ;
    }


    void    lmb(const bool& pressed, const osg::Vec2& ndc, bool& handled)
    {
//         handled = true ;


        if( ! pressed ) {

            ood::Collidable* picked = m_picker->pick( m_mouse_co ) ;

            if( picked ) {
                picked->setAngularVelocity( picked->getAngularVelocity() + osg::Z_AXIS * osg::PI ) ;
            }
        }
    }


    void    rmb(const bool& pressed, const osg::Vec2& ndc, bool& handled)
    {
//         handled = true ;


        if( ! pressed ) {

            ood::Collidable* picked = m_picker->pick( m_mouse_co ) ;

            if( picked ) {
                picked->setAngularVelocity( osg::Vec3(0,0,0) ) ;
            }
        }
    }


    void    moved(const osg::Vec2& co, bool& handled)
    {
//         handled = true ;

        // normalized
        m_mouse_co = co ;
    }


private:
    osg::ref_ptr<oodUtil::Picker>    m_picker ;

    osg::Vec2   m_mouse_co ;
} ;




int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;


    osg::Node*      cube = osgDB::readNodeFile("companioncube.osgt") ;

    PS_ASSERT1( cube != NULL ) ;

    /*
     * [1] Create the manager
     */
    osg::ref_ptr<ood::Manager>   manager = new ood::Manager() ;
    manager->setup(true, 1.0/60.0) ;

    /*
     * [2] Create the space
     */
    ood::Space*  space = new ood::Space() ;
    manager->setWorld( space ) ;



    // no gravity
    space->setGravity( osg::Vec3(0,0,0) ) ;



    /*
     * [3] Create some boxes
     */
    {
        // create the body and insert it into the world
        osg::ref_ptr<ood::Collidable>    body_tmpl = new ood::Box() ;

        body_tmpl->setSize( osg::Vec3(1, 1, 1) ) ;

        // the mass
        body_tmpl->setMass(512) ;


        // graphics
        body_tmpl->getMatrixTransform()->addChild( cube ) ;



        for(int r=-2; r<=2; r++) {
            for(int c=-2; c<=2; c++) {
                ood::RigidBody*  body = osg::clone( body_tmpl.get() ) ;

                body->setPosition( osg::Vec3(r*2, 0.0, c*2) ) ;

                space->addObject( body ) ;
            }
        }
    }





    /*
     * [4] Create the viewer and setup the picker
     */
    osgViewer::Viewer   viewer ;

    viewer.setSceneData( manager.get() ) ;

    viewer.realize() ;

    oodUtil::Picker* picker = new oodUtil::Picker() ;

    picker->setSpace( space ) ;
    picker->setCamera( viewer.getCamera() ) ;


    viewer.addEventHandler( new MyHandler( picker ) ) ;




    /*
     * [5] run
     */

    return viewer.run() ;
}
