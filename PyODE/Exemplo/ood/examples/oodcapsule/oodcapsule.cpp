#include <ood/Manager>
#include <ood/Space>
#include <ood/TriMesh>
#include <ood/Capsule>
#include <ood/DefaultNearCallback>
#include <ood/Notify>
#include <ood/CommonWorldOperations>

#include <oodUtil/CreateTriMeshFromNode>

#include <osgViewer/Viewer>

#include <osg/CullFace>
#include <osg/Math>
#include <osg/PositionAttitudeTransform>

#include <osgDB/ReadFile>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif




#ifndef STEP_SIZE
    #define STEP_SIZE  (1.0/60.0)
#endif

#ifndef INT_TIME
    #define INT_TIME 0.5
#endif



// This class removes a body if it falls down below [0, 0, -1]
class RemoveObjectCallback: public ood::ODECallback
{
public:
    virtual void    operator()(ood::ODEObject* obj)
    {
        ood::RigidBody*  body = obj->asRigidBody() ;

        if( body->getPosition().z() < -1.0 ) {
            body->getWorld()->addOperation( new ood::RemoveObjectOperation(body) ) ;
        }
    }
} ;



// create a body every dt seconds
class AddCapsuleCallback: public ood::ODECallback
{
public:
    AddCapsuleCallback(float dt):
        m_dt(dt),
        m_start_time(0.0)
    {
        m_template = _createTemplate() ;
    }


    virtual void    operator()(ood::ODEObject* obj)
    {
        ood::World*  world = obj->asWorld() ;

        float   dt = world->getSimulationTime() - m_start_time ;

        if( dt >= m_dt ) {
            m_start_time = world->getSimulationTime() ;

            world->addOperation( new ood::AddObjectOperation(_createObject()) ) ;
        }
    }



private:
    float   _rand(void) { return (float)rand() / (float)RAND_MAX ; }



    ood::ODEObject*  _createObject(void)
    {
        ood::Collidable* collidable = static_cast<ood::Collidable*>( m_template->clone(osg::CopyOp::SHALLOW_COPY) ) ;

        ooReal  X = 2 * _rand() - 1 ;
        ooReal  Y = 2 * _rand() - 1 ;
        ooReal  Z = _rand() + 5 ;

        collidable->setPosition( osg::Vec3(X, Y, Z) ) ;


        return collidable ;
    }





    ood::Collidable* _createTemplate(void)
    {
        osg::Node*  graphics = osgDB::readNodeFile("capsule.osgt") ;
        PS_ASSERT1( graphics != NULL ) ;




        ood::Capsule*    capsule = new ood::Capsule() ;
        capsule->setSize( osg::Vec3(0.5, 0.5, 1.0) ) ;

        capsule->getOrCreateStateSet()->setAttributeAndModes( new osg::CullFace(osg::CullFace::BACK) ) ;



        capsule->getMatrixTransform()->addChild(graphics) ;


        capsule->addUpdateCallback( new RemoveObjectCallback() ) ;

        capsule->setMass(15.0) ;


        return capsule ;
    }



private:
    float   m_dt ;
    float   m_start_time ;

    osg::ref_ptr<ood::Collidable> m_template ;
} ;




int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;

    srand( time(NULL) ) ;


    // the root node
    osg::Group*     root = new osg::Group() ;


    /*
     * [1] create the manager
     */
    ood::Manager*    manager = new ood::Manager() ;
    {
        manager->setup(true, STEP_SIZE) ;

        // setup the space
        ood::Space*  space = new ood::Space() ;
        manager->setWorld( space ) ;

        space->setWorldStepFunction(dWorldQuickStep) ;


        // add the manager to the simulation
        root->addChild(manager) ;
    }



    /*
     * [2] Create the floor
     */
    {
        osg::Node*  floor_graphics = osgDB::readNodeFile("floor.osgt") ;
        PS_ASSERT1( floor_graphics != NULL ) ;

        floor_graphics->getOrCreateStateSet()->setAttributeAndModes( new osg::CullFace(osg::CullFace::BACK) ) ;

        ood::TriMesh*    trimesh = oodUtil::createTriMeshFromNode(floor_graphics) ;

        // hold the trimesh
        trimesh->setKinematic(true) ;


        // graphics
        trimesh->getMatrixTransform()->addChild( floor_graphics ) ;



        manager->getWorld()->addObject(trimesh) ;
    }



    /*
     * [3] This callback will create a new cube every INT_TIME seconds
     */
    manager->getWorld()->addUpdateCallback( new AddCapsuleCallback(INT_TIME) ) ;



    osgViewer::Viewer   viewer ;
    viewer.setSceneData(root) ;
    viewer.realize() ;

    return viewer.run() ;
}
