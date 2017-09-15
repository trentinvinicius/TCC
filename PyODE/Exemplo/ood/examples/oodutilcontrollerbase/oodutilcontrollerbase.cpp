#include <ood/Manager>
#include <ood/World>
#include <ood/RigidBody>
#include <ood/AMotorJoint>
#include <ood/Notify>

#include <oodUtil/ControllerBase>

#include <osgDB/ReadFile>
#include <osgDB/WriteFile>

#include <osgViewer/Viewer>

#include <osg/io_utils>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif




class OOD_EXPORT Controller: public osg::Referenced
{
public:
    Controller(ood::Joint* joint=NULL):
        m_joint(joint) {}


    void    keyDown(const int& key, const int& mask, bool& handled)
    {
        (void) mask ;

        switch( key )
        {
            case 'x':
            {
                m_joint->setParam(  dParamVel1, m_joint->getParam(dParamVel1) + 1.0 ) ;
                m_joint->setParam(  dParamFMax1, 1.0 ) ;
                handled = true ;
            }
            break ;

            case 'X':
            {
                m_joint->setParam(  dParamVel1, m_joint->getParam(dParamVel1) - 1.0 ) ;
                m_joint->setParam(  dParamFMax1, 1.0 ) ;
                handled = true ;
            }
            break ;



            case 'y':
            {
                m_joint->setParam(  dParamVel2, m_joint->getParam(dParamVel2) + 1.0 ) ;
                m_joint->setParam(  dParamFMax2, 1.0 ) ;
                handled = true ;
            }
            break ;

            case 'Y':
            {
                m_joint->setParam(  dParamVel2, m_joint->getParam(dParamVel2) - 1.0 ) ;
                m_joint->setParam(  dParamFMax2, 1.0 ) ;
                handled = true ;
            }
            break ;



            case 'z':
            {
                m_joint->setParam(  dParamVel3, m_joint->getParam(dParamVel3) + 1.0 ) ;
                m_joint->setParam(  dParamFMax3, 1.0 ) ;
                handled = true ;
            }
            break ;

            case 'Z':
            {
                m_joint->setParam(  dParamVel3, m_joint->getParam(dParamVel3) - 1.0 ) ;
                m_joint->setParam(  dParamFMax3, 1.0 ) ;
                handled = true ;
            }
            break ;



            case 'r':
            {
                m_joint->setParam(  dParamVel1, 0.0 ) ;
                m_joint->setParam(  dParamFMax1, 5.0 ) ;
                m_joint->setParam(  dParamVel2, 0.0 ) ;
                m_joint->setParam(  dParamFMax2, 5.0 ) ;
                m_joint->setParam(  dParamVel3, 0.0 ) ;
                m_joint->setParam(  dParamFMax3, 5.0 ) ;
                handled = true ;
            }
            break ;



            default:
                handled = false ;
            break ;
        }
    }


    void    LMB(const bool& pressed, const osg::Vec2& ndc, bool& handled)
    {
        if( pressed ) {
            std::cout << "LMB Down" << std::endl ;
        } else {
            std::cout << "LMB Up" << std::endl ;
        }
        handled = true ;
    }


    void    MMB(const bool& pressed, const osg::Vec2& ndc, bool& handled)
    {
        if( pressed ) {
            std::cout << "MMB Down" << std::endl ;
        } else {
            std::cout << "MMB Up" << std::endl ;
        }
        handled = true ;
    }


    void    RMB(const bool& pressed, const osg::Vec2& ndc, bool& handled)
    {
        if( pressed ) {
            std::cout << "RMB Down" << std::endl ;
        } else {
            std::cout << "RMB Up" << std::endl ;
        }
        handled = true ;
    }


    void    Move(const osg::Vec2& pos, bool& handled)
    {
        std::cout << pos << std::endl ;
        handled = true ;
    }


    void    Frame(bool& request_warp, osg::Vec2& warp, bool& handled)
    {
        request_warp = true ;
        warp.set(0,0) ;
        handled = true ;
    }

private:
    osg::ref_ptr<ood::Joint>     m_joint ;
} ;




int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;

    ood::Manager*    manager = new ood::Manager() ;

    manager->setup(true, 1.0/60.0) ;

    manager->setWorld( new ood::World() ) ;




    ood::MotorJoint*     j = new ood::AMotorJoint() ;
    j->setAxis1Anchor( ood::MotorJoint::BODY1 ) ;
    j->setAxis2Anchor( ood::MotorJoint::BODY1 ) ;
    j->setAxis3Anchor( ood::MotorJoint::BODY1 ) ;




    osg::Node*      axis = osgDB::readNodeFile("axis3.osgt") ;

    PS_ASSERT1( axis != NULL ) ;

    ood::RigidBody*  b1 = new ood::RigidBody() ;

    b1->getMatrixTransform()->addChild(axis) ;


    // gravity off
    b1->setGravityMode(false) ;




    j->setBody1(b1) ;

    manager->getWorld()->addObject(b1) ;
    manager->getWorld()->addObject(j) ;



    osgViewer::Viewer   viewer ;
    viewer.setSceneData(manager) ;
    viewer.realize() ;


    osg::ref_ptr<Controller>    controller = new Controller(j) ;

    oodUtil::ControllerBase* controller_base = new oodUtil::ControllerBase() ;

    controller_base->onKeyPressed()->connect( controller.get(), &Controller::keyDown ) ;
    controller_base->onLeftMouseButton()->connect( controller.get(), &Controller::LMB ) ;
    controller_base->onMiddleMouseButton()->connect( controller.get(), &Controller::MMB ) ;
    controller_base->onRightMouseButton()->connect( controller.get(), &Controller::RMB ) ;
    controller_base->onMouseMoved()->connect( controller.get(), &Controller::Move ) ;
    controller_base->onFrame()->connect( controller.get(), &Controller::Frame ) ;

    viewer.getEventHandlers().push_back( controller_base ) ;


    viewer.run() ;

    return 0 ;
}
