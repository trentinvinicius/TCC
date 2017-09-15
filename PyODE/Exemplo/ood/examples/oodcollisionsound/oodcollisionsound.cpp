#include <ood/Manager>
#include <ood/Space>
#include <ood/TriMesh>
#include <ood/Box>
#include <ood/DefaultNearCallback>
#include <ood/Notify>
#include <ood/CommonWorldOperations>

#include <oodUtil/CreateTriMeshFromNode>

#include <osgViewer/Viewer>

#include <osg/CullFace>
#include <osg/Math>

#include <oos/Source>
#include <oos/Buffer>
#include <oos/ALState>

#include <osgDB/ReadFile>




#ifndef STEP_SIZE
    #define STEP_SIZE  (1.0/60.0)
#endif

#ifndef INT_TIME
    #define INT_TIME 2.5
#endif




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif



osg::ref_ptr<oos::Buffer>  hit_sound ;




namespace {
class PlayVisitor: public osg::NodeVisitor
{
    public:
        PlayVisitor(ooReal gain = 1.0): osg::NodeVisitor(TRAVERSE_ALL_CHILDREN), m_gain(gain) {}

        virtual void    apply(osg::Node& node)
        {
            oos::Source*   source = dynamic_cast<oos::Source*>(&node) ;

            if( source ) {

                if( ! source->isPlaying() || source->getParam(oos::Source::GAIN) < m_gain ) {
                    source->setParam( oos::Source::GAIN, m_gain ) ;
                    source->play() ;
                }

//                 source->play() ;
            }

            traverse(node) ;
        }

    private:
        ooReal  m_gain ;
} ;



class SoundCollisionCallback: public ood::CollisionCallback
{
public:
    virtual void    operator()(ood::Collidable* owner, ood::Collidable* other, ood::NearCallback* near_callback)
    {
        ood::DefaultNearCallback*    cbk = near_callback->asDefaultNearCallback() ;

        osg::Vec3   p ;
        osg::Vec3   n ;

        const ood::DefaultNearCallback::CollisionResult& cr = cbk->getCollisionResult() ;

        for(unsigned int i=0; i<cr.getContacts().size(); i++) {
            p.x() += cr.getContacts()[i].x() ;
            p.y() += cr.getContacts()[i].y() ;
            p.z() += cr.getContacts()[i].z() ;
        }

        for(unsigned int i=0; i<cr.getNormals().size(); i++) {
            n.x() += cr.getNormals()[i].x() ;
            n.y() += cr.getNormals()[i].y() ;
            n.z() += cr.getNormals()[i].z() ;
        }

        p /= cr.getContacts().size() ;

        n.normalize() ;


        ood::RigidBody*  b1 = owner ;
        ood::RigidBody*  b2 = other ;

        osg::Vec3   v1 = b1->getPointVelocity( p, false ) ;
        osg::Vec3   v2 = b2->getPointVelocity( p, false ) ;

        osg::Vec3   vv = v1 - v2 ;


        ooReal      v = vv * n ;

        ooReal      m = b1->getMass() + b2->getMass() ;
        ooReal      e = 0.5 * m * v * v ;


        if( e > 1.0 ) {
            osg::ref_ptr<osg::NodeVisitor>  nv = new PlayVisitor( osg::clampTo(e/50.0, 0.0, 1.0) ) ;
            owner->accept(*nv) ;
        }

        traverse(owner, other, near_callback) ;
    }
} ;

osg::ref_ptr<SoundCollisionCallback>    sound_cbk = new SoundCollisionCallback() ;



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



// create a body in [0, 0, 5]
class AddCubeCallback: public ood::ODECallback
{
public:
    AddCubeCallback(float dt):
        m_dt(dt),
        m_start_time(0.0)
    {
        m_templates[0] = _createTemplate("woodenbox1.osgt") ;
        m_templates[1] = _createTemplate("woodenbox2.osgt") ;
        m_templates[2] = _createTemplate("woodenbox3.osgt") ;
        m_templates[3] = _createTemplate("woodenbox4.osgt") ;
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
        const unsigned int  template_idx = rand() % 4 ;

        ood::Collidable* collidable = static_cast<ood::Collidable*>( m_templates[template_idx]->clone(osg::CopyOp::SHALLOW_COPY) ) ;
        collidable->setPosition( osg::Vec3(2 * _rand() - 1, 2 * _rand() - 1, 4 + 2 * _rand()) ) ;

        return collidable ;
    }


    ood::Collidable* _createTemplate(const std::string& graphics)
    {
        osg::Object*    woodenbox = osgDB::readObjectFile(graphics) ;
        PS_ASSERT1( woodenbox != NULL ) ;

        ood::Collidable* box = dynamic_cast<ood::Collidable*>( woodenbox ) ;
        PS_ASSERT1( box != NULL ) ;

        box->setDamping(0.01, 0.01) ;
        box->setAutoDisableLinearThreshold(0.1) ;
        box->setAutoDisableAngularThreshold(0.1) ;

        box->getOrCreateStateSet()->setAttributeAndModes( new osg::CullFace(osg::CullFace::BACK) ) ;


        box->addUpdateCallback( new RemoveObjectCallback() ) ;

        box->setCollisionCallback( sound_cbk.get() ) ;

        oos::Source*   source = new oos::Source() ;

        source->setBuffer( hit_sound.get() ) ;

        box->getMatrixTransform()->addChild( source ) ;


        return box ;
    }



private:
    float   m_dt ;
    float   m_start_time ;

    osg::ref_ptr<ood::Collidable> m_templates[4] ;
} ;

}




int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;


    oos::ALState::instance()->setDistanceModel(oos::ALState::EXPONENT_DISTANCE_CLAMPED) ;

    hit_sound = dynamic_cast<oos::Buffer*>( osgDB::readObjectFile("sounds/hit.wav") ) ;


    PS_ASSERT1( hit_sound ) ;


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


        // tuning
        space->setERP(0.2) ;
        space->setCFM(1.0e-5) ;

        space->setWorldStepFunction(dWorldQuickStep) ;

        ood::DefaultNearCallback*    ncbk = space->getNearCallback()->asDefaultNearCallback() ;
        ncbk->getCollisionParameters()->setMode( dContactApprox1 ) ;


        // add the manager to the simulation
        root->addChild(manager) ;
    }



    /*
     * [2] Create the floor
     */
    {
        osg::Node*  floor_graphics = osgDB::readNodeFile("ground.osgt") ;
        PS_ASSERT1( floor_graphics != NULL ) ;


        ood::TriMesh*    trimesh = oodUtil::createTriMeshFromNode(floor_graphics) ;

        // face culling
        trimesh->getOrCreateStateSet()->setAttributeAndModes( new osg::CullFace(osg::CullFace::BACK) ) ;

        // hold the trimesh
        trimesh->setKinematic(true) ;


        // graphics
        trimesh->getMatrixTransform()->addChild( floor_graphics ) ;


        manager->getWorld()->addObject(trimesh) ;
    }



    /*
     * [3] This callback will create a new cube every INT_TIME seconds
     */
    manager->getWorld()->addUpdateCallback( new AddCubeCallback(INT_TIME) ) ;



    osgViewer::Viewer   viewer ;
    viewer.setSceneData(root) ;
    viewer.realize() ;

    return viewer.run() ;
}
