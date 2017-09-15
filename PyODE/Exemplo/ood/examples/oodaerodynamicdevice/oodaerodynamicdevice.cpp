#include <ood/Manager>
#include <ood/Space>
#include <ood/Box>
#include <ood/TriMesh>
#include <ood/AerodynamicDevice>
#include <ood/Notify>

#include <oodUtil/CreateTriMeshFromNode>

#include <osgDB/WriteFile>
#include <osgDB/ReadFile>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif




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

    manager->setup(true, 1.0/100.0) ;

    manager->setWorld( new ood::Space() ) ;


    manager->getWorld()->setWind( osg::Vec3(-1.0, 0.0, 0.0) ) ;
    manager->getWorld()->setWindFrequency( 4.0 ) ;




    /*
     * [3] Create a kinematic plane as floor
     */
    {
        osg::Node*  plane = osgDB::readNodeFile( "floor.osgt" ) ;

        PS_ASSERT1( plane != NULL ) ;



        // build the motionless trimesh
        ood::TriMesh*    trim = oodUtil::createTriMeshFromNode(plane) ;

        trim->setKinematic(true) ;


        // add the trimesh to the space
        manager->getWorld()->addObject(trim) ;

        // add the graphic node to the simulation
        trim->getMatrixTransform()->addChild(plane) ;
    }




    /*
     * [4] Create a dynamic cube without an aerodynamic device
     */
    {
        ood::Collidable*     box = new ood::Box() ;
        box->setSize( osg::Vec3(1, 1, 1) ) ;

        // graphics
        box->getMatrixTransform()->addChild(cube) ;

        // move the cube to the left
        box->setPosition( osg::Vec3(-4, 0.0, 10.0) ) ;

        // insert the cube into the world
        manager->getWorld()->addObject(box) ;
    }




    /*
     * [5] Create a cube with an aerodynamic device
     */
    {
        ood::Collidable*     box = new ood::Box() ;
        box->setSize( osg::Vec3(1, 1, 1) ) ;

        // graphics
        box->getMatrixTransform()->addChild(cube) ;

        // move the cube to the right
        box->setPosition( osg::Vec3(4, 0.0, 10.0) ) ;

        // insert the cube into the world
        manager->getWorld()->addObject(box) ;



        // setup the aerodynamic device
        ood::AerodynamicDevice*  ad = new ood::AerodynamicDevice() ;

        // just a drag point in the front lower left vertex
        ad->addDragPoint( osg::Vec4(-0.5, -0.5, -0.5, 5.0) ) ;

        box->addUpdateCallback( ad ) ;
    }




    /*
     * [6] write out the graph
     */
    osgDB::writeNodeFile(*manager, "output.osgb") ;




    // bye
    return 0 ;
}
