#include <ood/Manager>
#include <ood/ManagerUpdateCallback>
#include <ood/RigidBody>
#include <ood/Notify>

#include <osgDB/ReadFile>
#include <osgDB/WriteFile>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif





int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;

    // graphics
    osg::Node*      r3_axis = osgDB::readNodeFile("axis3.osgt") ;

    PS_ASSERT1( r3_axis != NULL ) ;



    /*
     * [1] create and configure the manager
     */
    osg::ref_ptr<ood::Manager>   manager = new ood::Manager() ;


    // ManagerUpdateCallback::operator() calls the Manager::frame method
    manager->addUpdateCallback( new ood::ManagerUpdateCallback() ) ;

    // Divert the visitors
    manager->setAcceptVisitors( true ) ;

    // the step size
    manager->setStepSize( 1.0/60.0 ) ;


    // a shortcut for the 3 previous calls is:
    //
    // manager->setup(  true,       // divert all visitors
    //                  1.0 / 60.0  // the step size
    //              ) ;



    /*
     * [2] create the world
     */
    manager->setWorld( new ood::World() ) ;


    // no gravity
    manager->getWorld()->setGravity( osg::Vec3(0, 0, 0) ) ;


    /*
     * [3] create a body
     */
    {
        // create
        ood::RigidBody*  body = new ood::RigidBody() ;

        manager->getWorld()->addObject( body ) ;


        // graphics
        body->getMatrixTransform()->addChild( r3_axis ) ;


        // Let the body spin
        const ooReal    FREQUENCY = 1.0/4.0 ;

        body->setAngularVelocity( osg::Vec3(0.0, 0.0, FREQUENCY * 2.0 * osg::PI) ) ;


        // disable damping
        body->setLinearDamping(0.0) ;
        body->setAngularDamping(0.0) ;
    }


    /*
     * [5] write out the graph
     */
    osgDB::writeNodeFile(*manager, "output.osgb") ;


    return 0 ;
}
