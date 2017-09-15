#include <ood/Manager>
#include <ood/World>
#include <ood/RigidBody>
#include <ood/AMotorJoint>
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

    osg::ref_ptr<ood::Manager>   manager = new ood::Manager() ;

    manager->setup(true, 1.0/60.0) ;

    manager->setWorld( new ood::World() ) ;

    manager->getWorld()->setGravity( osg::Vec3(0.0, 0.0, 0.0) ) ;




    ood::Joint*      motor = new ood::AMotorJoint() ;

    const ooReal    FREQUENCY = 10.0 ;

    motor->setParam(dParamVel2, FREQUENCY * 2.0 * osg::PI) ;
    motor->setParam(dParamFMax2, 0.5) ;




    osg::Node*      axis = osgDB::readNodeFile("axis3.osgt") ;

    PS_ASSERT1( axis != NULL ) ;

    ood::RigidBody*  b1 = new ood::RigidBody() ;
    ood::RigidBody*  b2 = new ood::RigidBody() ;

    b1->getMatrixTransform()->addChild(axis) ;
    b2->getMatrixTransform()->addChild(axis) ;

    b1->setPosition( osg::X_AXIS * -1.5 ) ;
    b2->setPosition( osg::X_AXIS *  1.5 ) ;




    motor->setBody1(b1) ;
    motor->setBody2(b2) ;

    manager->getWorld()->addObject(b1) ;
    manager->getWorld()->addObject(b2) ;
    manager->getWorld()->addObject(motor) ;



    osgDB::writeNodeFile(*manager, "output.osgb") ;

    return 0 ;
}
