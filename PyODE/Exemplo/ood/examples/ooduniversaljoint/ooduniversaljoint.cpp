#include <ood/Manager>
#include <ood/RigidBody>
#include <ood/UniversalJoint>
#include <ood/HingeJoint>
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


    osg::Node*      arm_graphics   = osgDB::readNodeFile("universal_arm.osgt") ;
    osg::Node*      joint_graphics = osgDB::readNodeFile("universal_joint.osgt") ;

    PS_ASSERT1( arm_graphics != NULL ) ;
    PS_ASSERT1( joint_graphics != NULL ) ;



    // setup the scene
    osg::ref_ptr<ood::Manager>   manager = new ood::Manager() ;
    ood::RigidBody*              body1 = new ood::RigidBody() ;
    ood::RigidBody*              body2 = new ood::RigidBody() ;
    ood::Joint*                  hinge1 = new ood::HingeJoint() ;
    ood::Joint*                  hinge2 = new ood::HingeJoint() ;
    ood::Joint*                  universal= new ood::UniversalJoint() ;


    {
        ood::World*  world = new ood::World() ;

        world->addObject(body1) ;
        world->addObject(body2) ;
        world->addObject(universal) ;
        world->addObject(hinge1) ;
        world->addObject(hinge2) ;


        manager->setWorld( world ) ;

        manager->setup(true, 1.0/100.0) ;

        world->setERP(1.0) ;
        world->setCFM(1.0e-5) ;

//         world->setGravity( osg::Vec3() ) ;
    }


    //
    // create the bodies
    //
    {
        body1->getMatrixTransform()->addChild(arm_graphics) ;

        body2->getMatrixTransform()->addChild(arm_graphics) ;
        body2->setQuaternion(  osg::Quat( osg::inDegrees(90.0), osg::Z_AXIS ) * osg::Quat( osg::inDegrees(-150.0), osg::Y_AXIS ) ) ;

        body1->setLinearDamping( 0.0 ) ;
        body1->setAngularDamping( 0.0 ) ;

        body2->setLinearDamping( 0.0 ) ;
        body2->setAngularDamping( 0.0 ) ;
    }



    //
    // create the universal
    //
    {
        universal->setBody1(body1) ;
        universal->setBody2(body2) ;

        universal->setAxis1( osg::X_AXIS ) ;
        universal->setAxis2( osg::Y_AXIS ) ;

        universal->getMatrixTransform()->addChild(joint_graphics) ;
    }



    //
    // create the first hinge
    //
    {
        hinge1->setBody1(body1) ;

        hinge1->setAxis1( osg::Z_AXIS ) ;
    }



    //
    // create the second hinge
    //
    {
        hinge2->setBody1(body2) ;

        hinge2->setAxis1( body2->getQuaternion() * -osg::Z_AXIS ) ;

        const ooReal    FREQUENCY = 100.0 ;
        const ooReal    FORCE = 1.0 ;

        hinge2->setParam( dParamVel1, FREQUENCY * 2.0 * osg::PI ) ;
        hinge2->setParam( dParamFMax1, FORCE ) ;
    }



    osgDB::writeNodeFile(*manager, "output.osgb") ;

    return 0 ;
}
