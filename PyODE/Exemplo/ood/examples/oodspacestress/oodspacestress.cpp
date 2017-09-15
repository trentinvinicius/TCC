#include <ood/Manager>
#include <ood/Space>
#include <ood/DefaultNearCallback>
#include <ood/Notify>

#include <osgDB/ReadFile>
#include <osgDB/WriteFile>

#include <ood/CommonWorldOperations>

#include <osgViewer/Viewer>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif




class BodyRemover: public ood::ODECallback
{
public:
    virtual void    operator()(ood::ODEObject* obj)
    {
        ood::RigidBody*  body = obj->asRigidBody() ;
        PS_ASSERT1( body != NULL ) ;

        const osg::Vec3 p = body->getPosition() ;

        if( body->getPosition().z() < -25.0 ) {
            body->getWorld()->addOperation( new ood::RemoveObjectOperation(body) ) ;
        }

        traverse(obj) ;
    }
} ;




class BoxEmitter: public ood::ODECallback
{
public:
    BoxEmitter(ooReal g=0.025)
    {
        _init() ;
        m_g = g ;
    }


    virtual void operator()(ood::ODEObject* obj)
    {
        ood::World*  world = obj->asWorld() ;
        PS_ASSERT1( world != NULL ) ;

        m_dt += world->getCurrentStepSize() ;

        if( m_dt >= m_g ) {
            m_dt = 0.0 ;

            _createBody(world) ;
        }

        traverse(obj) ;
    }


private:
    void    _init(void)
    {
        ood::ODECallback*    cbk = new BodyRemover() ;


        m_boxes[0] = dynamic_cast<ood::RigidBody*>( osgDB::readObjectFile("woodenbox1.osgt") ) ;
        PS_ASSERT1( m_boxes[0].get() ) ;

        m_boxes[1] = dynamic_cast<ood::RigidBody*>( osgDB::readObjectFile("woodenbox2.osgt") ) ;
        PS_ASSERT1( m_boxes[1].get() ) ;

        m_boxes[2] = dynamic_cast<ood::RigidBody*>( osgDB::readObjectFile("woodenbox3.osgt") ) ;
        PS_ASSERT1( m_boxes[2].get() ) ;

        m_boxes[3] = dynamic_cast<ood::RigidBody*>( osgDB::readObjectFile("woodenbox4.osgt") ) ;
        PS_ASSERT1( m_boxes[3].get() ) ;

        m_dt = 0.0 ;


        for(int i=0; i<4; i++) {
            m_boxes[i]->setUpdateCallback( cbk ) ;
            m_boxes[i]->setAutoDisableFlag(true) ;
            m_boxes[i]->setAutoDisableLinearThreshold(0.5) ;
            m_boxes[i]->setAutoDisableAngularThreshold(0.5) ;
            m_boxes[i]->setAutoDisableSteps(30) ;
            m_boxes[i]->setAutoDisableTime(0.5) ;
            m_boxes[i]->setAutoDisableAverageSamplesCount(5) ;
            m_boxes[i]->setDamping(0.025, 0.025) ;
        }
    }


    void    _createBody(ood::World* world)
    {
        ood::RigidBody*  box = static_cast<ood::RigidBody*>( m_boxes[ rand() % 4 ]->clone(osg::CopyOp::SHALLOW_COPY) ) ;

        box->setPosition( osg::Z_AXIS * 10 ) ;

        world->addOperation( new ood::AddObjectOperation(box) ) ;
    }


    osg::ref_ptr<ood::RigidBody> m_boxes[4] ;
    ooReal                          m_dt ;
    ooReal                          m_g ;
} ;




int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;


    ood::Manager*    manager = new ood::Manager() ;


    manager->setup(true, 1.0/60.0) ;



    ood::Space*  space = new ood::Space() ;
    manager->setWorld( space ) ;



    ood::DefaultNearCallback*    near_cbk = new ood::DefaultNearCallback() ;
    space->setNearCallback( near_cbk ) ;



    ood::CollisionParameters*    collision_params = new ood::CollisionParameters() ;
    near_cbk->setCollisionParameters(collision_params) ;



    ood::Transformable*  base = dynamic_cast<ood::Transformable*>( osgDB::readObjectFile("space_stress_trimesh.osgt") ) ;
    PS_ASSERT1( base != NULL ) ;

    manager->getWorld()->addObject(base) ;

    base->getMatrixTransform()->getOrCreateStateSet()->setMode(GL_CULL_FACE, osg::StateAttribute::ON) ;



    manager->getWorld()->addUpdateCallback( new BoxEmitter() ) ;



    collision_params->setMaxContactNum(128) ;


    space->setWorldStepFunction( dWorldQuickStep ) ;
    space->setQuickStepNumIterations(1) ;
    space->setQuickStepW(1.75) ;




    osg::ref_ptr<osgViewer::Viewer>   viewer = new osgViewer::Viewer() ;

    viewer->setSceneData(manager) ;
//     viewer->setUpViewInWindow(0, 0, 600, 400) ;
    viewer->realize() ;

    return viewer->run() ;
}
