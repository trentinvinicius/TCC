#include <ood/Manager>
#include <ood/World>
#include <ood/RigidBody>
#include <ood/LMotorJoint>
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


    osg::ref_ptr<ood::Manager>   manager = new ood::Manager() ;
    manager->setup(true, 1.0/60.0) ;

    manager->setWorld( new ood::World() ) ;
    manager->getWorld()->setGravity( osg::Vec3(0.0, 0.0, 0.0) ) ;


    ood::RigidBody*  b1 = new ood::RigidBody() ;
    ood::RigidBody*  b2 = new ood::RigidBody() ;

    ood::Joint*      j = new ood::LMotorJoint() ;


    osg::Node*      graphics = osgDB::readNodeFile("companioncube.osgt") ;
    PS_ASSERT1( graphics != NULL ) ;


    b1->getMatrixTransform()->addChild(graphics) ;
    b2->getMatrixTransform()->addChild(graphics) ;

    b1->setPosition( osg::X_AXIS * -1.0 + osg::Z_AXIS ) ;
    b2->setPosition( osg::X_AXIS *  1.0 - osg::Z_AXIS ) ;



    j->setBody1(b1) ;
    j->setBody2(b2) ;

    j->setParam(dParamVel, 1.0) ;
    j->setParam(dParamFMax, 0.1) ;

    manager->getWorld()->addObject(b1) ;
    manager->getWorld()->addObject(b2) ;
    manager->getWorld()->addObject(j) ;


    osgDB::writeNodeFile(*manager, "output.osgb") ;


    return 0 ;
}
