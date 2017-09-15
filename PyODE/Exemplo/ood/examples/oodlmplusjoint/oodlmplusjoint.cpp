#include <ood/Manager>
#include <ood/Space>
#include <ood/RigidBody>
#include <ood/LMPlusJoint>
#include <ood/Notify>

#include <osgDB/ReadFile>
#include <osgDB/WriteFile>

#include <osg/MatrixTransform>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif




int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;


    osg::Node*      cube = osgDB::readNodeFile("companioncube.osgt") ;
    PS_ASSERT1( cube != NULL ) ;

    osg::Node*      transparent_box = osgDB::readNodeFile("transparent_box.osgt") ;
    PS_ASSERT1( transparent_box != NULL ) ;

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


    /*
     * [3] Create a dynamic body
     */
    ood::RigidBody*  dynamic_body = new ood::RigidBody() ;
    {
        ood::RigidBody*  body = dynamic_body ;

        manager->getWorld()->addObject( body ) ;

        // the mass
        body->setMass(1.0) ;


        // graphics
        body->getMatrixTransform()->addChild( cube ) ;


        // lift up the box
        body->setPosition( osg::Vec3(0.0, 0.0, 4.0) ) ;


        // let the box spin around the Z axis... for no reason
//         body->addTorque( osg::Vec4(0.0, 0.0, 100.0 / manager->getStepSize(), 1.0) ) ;
    }


    /*
     * [4] create a kinematic cube
     */
    ood::RigidBody*  kinematic_body = new ood::RigidBody() ;
    {
        ood::RigidBody*  body = kinematic_body ;

        manager->getWorld()->addObject( body ) ;


        // graphics
        osg::MatrixTransform*   mt = new osg::MatrixTransform( osg::Matrix::scale( osg::Vec3(10,10,10) ) ) ;
        mt->addChild( transparent_box ) ;
        body->getMatrixTransform()->addChild( mt ) ;


        // make the body insensitive to the forces
        body->setKinematic(true) ;

        const ooReal    v = 2.0 * osg::PI * 1.0/16.0 ;

        body->setAngularVelocity( osg::Vec3(v, v, v) ) ;

        body->setAngularDamping( 0.0 ) ;
    }


    /*
     * [5] createthe joint
     */
    {
        ood::LMPlusJoint*    joint = new ood::LMPlusJoint() ;

        joint->setAxis1Anchor( ood::MotorJoint::BODY1) ;
        joint->setAxis2Anchor( ood::MotorJoint::BODY1) ;
        joint->setAxis3Anchor( ood::MotorJoint::BODY1) ;

        joint->setAxis1( osg::X_AXIS ) ;
        joint->setAxis2( osg::Y_AXIS ) ;
        joint->setAxis3( osg::Z_AXIS ) ;

        joint->setParam( dParamLoStop1, -5.0 ) ;
        joint->setParam( dParamHiStop1,  5.0 ) ;

        joint->setParam( dParamLoStop2, -5.0 ) ;
        joint->setParam( dParamHiStop2,  5.0 ) ;

        joint->setParam( dParamLoStop3, -5.0 ) ;
        joint->setParam( dParamHiStop3,  5.0 ) ;

        joint->setBody1( kinematic_body ) ;
        joint->setBody2( dynamic_body ) ;

        manager->getWorld()->addObject( joint ) ;
    }


    /*
     * [6] save the result
     */
    osgDB::writeNodeFile(*manager, "output.osgb") ;


    return 0 ;
}
