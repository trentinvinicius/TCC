#include <ood/Manager>
#include <ood/Space>
#include <ood/Box>
#include <ood/TriMesh>
#include <ood/DefaultNearCallback>
#include <ood/Notify>

#include <oodUtil/CreateTriMeshFromNode>

#include <osgDB/ReadFile>
#include <osgDB/WriteFile>

#include <osg/MatrixTransform>




#ifndef OOD_DATA_PATH
#define OOD_DATA_PATH "../../data"
#endif




ood::TriMesh*
create_cube(float size)
{
    ood::TriMesh*    trimesh = new ood::TriMesh() ;


    osg::Vec3Array* vs = new osg::Vec3Array() ;
    osg::IntArray*  is = new osg::IntArray() ;

    trimesh->setVertexArray(vs) ;
    trimesh->setIndexArray(is) ;


    const float scale = size * 0.5 ;

    // lower plane
    vs->push_back(  osg::Vec3(-1, -1, -1) * scale   ) ;
    vs->push_back(  osg::Vec3( 1, -1, -1) * scale   ) ;
    vs->push_back(  osg::Vec3( 1,  1, -1) * scale   ) ;
    vs->push_back(  osg::Vec3(-1,  1, -1) * scale   ) ;

    // upper plane
    vs->push_back(  osg::Vec3(-1, -1,  1) * scale   ) ;
    vs->push_back(  osg::Vec3( 1, -1,  1) * scale   ) ;
    vs->push_back(  osg::Vec3( 1,  1,  1) * scale   ) ;
    vs->push_back(  osg::Vec3(-1,  1,  1) * scale   ) ;


    // Bottom/Top (Z)  Near/Far (Y)  Left/Right (X)
    const int   BNL = 0 ;
    const int   BNR = 1 ;
    const int   BFR = 2 ;
    const int   BFL = 3 ;
    const int   TNL = 4 ;
    const int   TNR = 5 ;
    const int   TFR = 6 ;
    const int   TFL = 7 ;

#define ADD_TRIANGLE(A, B, C) is->push_back(A) ; is->push_back(B); is->push_back(C) ;
    // bottom
    ADD_TRIANGLE(BNL, BFL, BNR) ;
    ADD_TRIANGLE(BFL, BFR, BNR) ;

    // up
    ADD_TRIANGLE(TFL, TNL, TNR) ;
    ADD_TRIANGLE(TNR, TFR, TFL) ;

    // front
    ADD_TRIANGLE(BNL, BNR, TNL) ;
    ADD_TRIANGLE(TNL, BNR, TNR) ;

    // back
    ADD_TRIANGLE(TFL, BFR, BFL) ;
    ADD_TRIANGLE(TFL, TFR, BFR) ;

    // left
    ADD_TRIANGLE(BFL, BNL, TNL) ;
    ADD_TRIANGLE(BFL, TNL, TFL) ;

    // right
    ADD_TRIANGLE(BFR, TFR, TNR) ;
    ADD_TRIANGLE(BFR, TNR, BNR) ;

#undef ADD_TRIANGLE



    trimesh->build() ;


    return trimesh ;
}




int
main(int argc, char** argv)
{
    osgDB::Registry::instance()->getDataFilePathList().push_back( OOD_DATA_PATH ) ;

    osg::Node*      weight = osgDB::readNodeFile("companioncube.osgt") ;
    PS_ASSERT1( weight != NULL ) ;

    /*
     * [1] create the manager
     */
    osg::ref_ptr<ood::Manager>   manager = new ood::Manager() ;


    manager->setup(true, 1.0/120.0) ;

    /*
     * [2] create the space
     */
    ood::Space*  space = new ood::Space() ;
    manager->setWorld( space ) ;


    /*
     * [3] create a dynamic body
     */
    {
        // create
        ood::TriMesh*    trimesh = create_cube(1.0) ;
        manager->getWorld()->addObject( trimesh ) ;


        // graphics
        trimesh->getMatrixTransform()->addChild( weight ) ;


        // raise the body
        trimesh->setPosition( osg::Vec3(0.0, 0.0, 5.0) ) ;


        trimesh->setMass( 1.0 ) ;
    }


    /*
     * [4] create a kinematic triangle mesh
     */
    {
        osg::MatrixTransform*   transform = new osg::MatrixTransform() ;

        transform->setMatrix( osg::Matrix::scale( osg::Vec3(2.0, 2.0, 2.0) ) ) ;

        transform->addChild( weight ) ;

        transform->getOrCreateStateSet()->setMode( GL_NORMALIZE, osg::StateAttribute::ON ) ;


        // create
        ood::TriMesh*    trimesh = oodUtil::createTriMeshFromNode(transform) ;
        manager->getWorld()->addObject( trimesh ) ;


        // graphics
        trimesh->getMatrixTransform()->addChild( transform ) ;


        // this body is not dynamic
        trimesh->setKinematic(true) ;


        trimesh->setMass( 1.0 ) ;
    }


    /*
     * [5] write the graph
     */
    osgDB::writeNodeFile(*manager, "output.osgb") ;


    return 0 ;
}
