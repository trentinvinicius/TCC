#include <ood/Manager>
#include <ood/Space>
#include <ood/Box>
#include <ood/AMotorJoint>
#include <ood/BallJoint>
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

    manager->setWorld( new ood::Space() ) ;

    manager->getWorld()->setGravity( osg::Vec3(0.0, 0.0, -3.0) ) ;





    ood::Box*            base = new ood::Box() ;
    {
        const osg::Vec3 size = osg::Vec3(10, 10, 1) ;

        base->setSize( size ) ;
        base->setPosition( osg::Vec3(0.0, 0.0, 0.0) ) ;
        base->setMass(1.0e4) ;

        osg::Node*  graphics = osgDB::readNodeFile("ground.osgt") ;
        PS_ASSERT1( graphics != NULL ) ;

        base->getMatrixTransform()->addChild( graphics ) ;
    }



    osg::Node*  weight_graphics = osgDB::readNodeFile("companioncube.osgt") ;
    PS_ASSERT1( weight_graphics != NULL ) ;


    ood::Box*            weight1 = new ood::Box() ;
    {
        weight1->setSize( osg::Vec3(1, 1, 1) ) ;
        weight1->setPosition( osg::Vec3(4.0, -4.0, 5.0) ) ;
        weight1->setMass(512.0) ;

        weight1->getMatrixTransform()->addChild( weight_graphics ) ;
    }


    ood::Box*            weight2 = new ood::Box() ;
    {
        weight2->setSize( osg::Vec3(1, 1, 1) ) ;
        weight2->setPosition( osg::Vec3(4.0, 0.0, 5.0) ) ;
        weight2->setMass(512.0) ;

        weight2->getMatrixTransform()->addChild( weight_graphics ) ;
    }


    ood::Box*            weight3 = new ood::Box() ;
    {
        weight3->setSize( osg::Vec3(1, 1, 1) ) ;
        weight3->setPosition( osg::Vec3(4.0, 4.0, 5.0) ) ;
        weight3->setMass(512.0) ;

        weight3->getMatrixTransform()->addChild( weight_graphics ) ;
    }




    ood::BallJoint*  ball = new ood::BallJoint() ;
    {
        ball->setBody1(base) ;

        ball->setAnchor1( osg::Vec3(0.0, 0.0, 0.0) ) ;
    }




    ood::AMotorJoint*    motor = new ood::AMotorJoint() ;
    {

        motor->setBody1(base) ;


        motor->setAxis1(osg::Z_AXIS ) ;
        motor->setAxis3(osg::Y_AXIS ) ;



        motor->setMotorMode(dAMotorEuler) ;


        motor->setParam(dParamLoStop1, 0.0) ;
        motor->setParam(dParamHiStop1, 0.0) ;
        motor->setParam(dParamLoStop2, 0.0) ;
        motor->setParam(dParamHiStop2, 0.0) ;
        motor->setParam(dParamLoStop3, -osg::PI / 12.0) ;
        motor->setParam(dParamHiStop3, osg::PI / 12.0) ;


        motor->setAxis1Anchor( ood::AMotorJoint::WORLD ) ;
        motor->setAxis3Anchor( ood::AMotorJoint::WORLD ) ;
    }





    {
        manager->getWorld()->addObject( ball ) ;
        manager->getWorld()->addObject( motor ) ;
        manager->getWorld()->addObject( base ) ;
        manager->getWorld()->addObject( weight1 ) ;
        manager->getWorld()->addObject( weight2 ) ;
        manager->getWorld()->addObject( weight3 ) ;
    }



    osgDB::writeNodeFile(*manager, "output.osgb") ;

    return 0 ;
}
