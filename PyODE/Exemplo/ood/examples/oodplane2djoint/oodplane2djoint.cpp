#include <ood/Manager>
#include <ood/World>
#include <ood/RigidBody>
#include <ood/Plane2DJoint>
#include <ood/Notify>

#include <osgDB/WriteFile>
#include <osgDB/ReadFile>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif




int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;




    /*
     * [1] Create the manager
     */
    osg::ref_ptr<ood::Manager>   manager = new ood::Manager() ;

    manager->setup(true, 1.0/100.0) ;

    manager->setWorld( new ood::World() ) ;




    /*
     * [2] Create a plane
     */
    ood::Transformable*  xform = new ood::Transformable() ;
    {
        osg::Node*  plane = osgDB::readNodeFile( "floor.osgt" ) ;

        PS_ASSERT1( plane != NULL ) ;

        // add the graphic node to the simulation
        xform->getMatrixTransform()->addChild(plane) ;

        // insert the plane into the world
        manager->getWorld()->addObject(xform) ;


        // rotate the plane
        osg::Matrix rotation = osg::Matrix::rotate( osg::Quat(osg::PI / 8.0, osg::Y_AXIS) ) * osg::Matrix::rotate( osg::Quat(osg::PI / 8.0, osg::X_AXIS) ) ;
        osg::Matrix position = osg::Matrix::translate( osg::Z_AXIS * 2.0 ) ;
        xform->getMatrixTransform()->setMatrix( rotation * position ) ;
    }




    /*
     * [3] Create a dynamic cube
     */

    ood::RigidBody*  dynamic_cube = new ood::RigidBody() ;
    {
        osg::Node*      cube = osgDB::readNodeFile("companioncube.osgt") ;

        PS_ASSERT1( cube != NULL ) ;

        // graphics
        dynamic_cube->getMatrixTransform()->addChild(cube) ;

        // insert the cube into the world
        manager->getWorld()->addObject(dynamic_cube) ;
    }




    /*
     * [3] Create the joint
     */
    {
        ood::Joint*  plane2d = new ood::Plane2DJoint() ;

        plane2d->setBody1( dynamic_cube ) ;


        manager->getWorld()->addObject( plane2d ) ;




        const osg::Matrix&  matrix = xform->getMatrixTransform()->getMatrix() ;

        plane2d->setAxis1( osg::Matrix::transform3x3( osg::Z_AXIS, matrix ) ) ;

        plane2d->setAnchor1( osg::Vec3(0,0,0) * matrix ) ;
    }




    /*
     * [5] write out the graph
     */
    osgDB::writeNodeFile(*manager, "output.osgb") ;




    // bye
    return 0 ;
}
