/*!
 * @file FindObjects.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2011 - 2017 by Rocco Martino                            *
 *   martinorocco@gmail.com                                                *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU Lesser General Public License as        *
 *   published by the Free Software Foundation; either version 2.1 of the  *
 *   License, or (at your option) any later version.                       *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Lesser General Public License for more details.                   *
 *                                                                         *
 *   You should have received a copy of the GNU Lesser General Public      *
 *   License along with this program; if not, write to the                 *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

/* ======================================================================= */
/* ....................................................................... */
#include <oodUtil/FindObjects>

#include <ood/Manager>
#include <ood/World>
#include <ood/Joint>
#include <ood/CharacterBase>

#include <osg/Geode>
#include <osg/Texture2D>
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
namespace
{
    class FindManagersVisitor: public osg::NodeVisitor
    {
    public:
        FindManagersVisitor(oodUtil::Managers& managers):
            osg::NodeVisitor    ( TRAVERSE_ALL_CHILDREN ),
            m_managers          ( managers ) {}


        virtual ~FindManagersVisitor(void) {}


        virtual void    reset(void)
        {
            m_managers.clear() ;
        }


        virtual void    apply(osg::Node& node)
        {
            ood::Manager*    manager = dynamic_cast<ood::Manager*>( &node ) ;

            if( manager != NULL ) {
                m_managers.push_back( manager ) ;
            }

            traverse( node ) ;
        }

    private:
        oodUtil::Managers&   m_managers ;
    } ;




    class FindNodeVisitor: public osg::NodeVisitor
    {
    public:
        FindNodeVisitor(const std::string& name):
            osg::NodeVisitor(TRAVERSE_ALL_CHILDREN),
            m_name(name) {}


        ~FindNodeVisitor(void) {}


        virtual void    apply(osg::Node& node)
        {
            if( ( ! m_node.valid() )  && (node.getName() == m_name) ) {
                m_node = &node ;
            } else {
                traverse(node) ;
            }
        }


        osg::Node*  getNode(void)
        {
            return m_node.get() ;
        }

    private:
        osg::ref_ptr<osg::Node> m_node ;
        std::string             m_name ;
    } ;




    class FindTexture2DVisitor: public osg::NodeVisitor
    {
    public:
        FindTexture2DVisitor(const std::string& name):
            osg::NodeVisitor(TRAVERSE_ALL_CHILDREN),
            m_name(name) {}


        ~FindTexture2DVisitor(void) {}


        virtual void    apply(osg::Node& node)
        {
            if( m_texture.valid() ) {
                return ;
            }


            if( node.getStateSet() ) {
                apply( *node.getStateSet() ) ;
            }

            traverse(node) ;
        }


        virtual void    apply(osg::Geode& geode)
        {
            if( m_texture.valid() ) {
                return ;
            }

            if( geode.getStateSet() ) {
                apply( *geode.getStateSet() ) ;
            }

            for( unsigned int i=0; i<geode.getNumDrawables(); i++ ) {
                osg::Drawable*  drawable = geode.getDrawable(i) ;

                if( drawable ) {
                    apply( *drawable ) ;
                }
            }

            traverse(geode) ;
        }


        virtual void    apply(osg::Drawable& drawable)
        {
            if( m_texture.valid() ) {
                return ;
            }


            if( drawable.getStateSet() ) {
                apply( *drawable.getStateSet() ) ;
            }

            traverse(drawable) ;
        }


        virtual void    apply(osg::StateSet& stateset)
        {
            for( unsigned int i=0; i<stateset.getTextureAttributeList().size(); i++ ) {
                osg::Texture2D* texture = dynamic_cast<osg::Texture2D*>( stateset.getTextureAttribute(i, osg::StateAttribute::TEXTURE) ) ;

                if (texture) {
                    if( texture->getName() == m_name ) {
                        m_texture = texture ;
                        break ;
                    }
                }
            }
        }


        osg::Texture2D* getTexture2D(void)
        {
            return m_texture.get() ;
        }

    private:
        osg::ref_ptr<osg::Texture2D>    m_texture ;
        std::string                     m_name ;
    } ;









    class FindStateSetVisitor: public osg::NodeVisitor
    {
    public:
        FindStateSetVisitor(const std::string& name):
            osg::NodeVisitor(TRAVERSE_ALL_CHILDREN),
            m_name(name) {}


        ~FindStateSetVisitor(void) {}


        virtual void    apply(osg::Node& node)
        {
            if( m_state_set.valid() ) {
                return ;
            }


            if( node.getStateSet() ) {
                apply( *node.getStateSet() ) ;
            }

            traverse(node) ;
        }


        virtual void    apply(osg::Geode& geode)
        {
            if( m_state_set.valid() ) {
                return ;
            }

            if( geode.getStateSet() ) {
                apply( *geode.getStateSet() ) ;
            }

            for( unsigned int i=0; i<geode.getNumDrawables(); i++ ) {
                osg::Drawable*  drawable = geode.getDrawable(i) ;

                if( drawable ) {
                    apply( *drawable ) ;
                }
            }

            traverse(geode) ;
        }


        virtual void    apply(osg::Drawable& drawable)
        {
            if( m_state_set.valid() ) {
                return ;
            }


            if( drawable.getStateSet() ) {
                apply( *drawable.getStateSet() ) ;
            }

            traverse(drawable) ;
        }


        virtual void    apply(osg::StateSet& stateset)
        {
            if( stateset.getName() == m_name ) {
                m_state_set = &stateset ;
            }
        }


        osg::StateSet* getStateSet(void)
        {
            return m_state_set.get() ;
        }

    private:
        osg::ref_ptr<osg::StateSet>     m_state_set ;
        std::string                     m_name ;
    } ;
} // anon namespace
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
osg::Node*
oodUtil::findNode( osg::Node* graph, const std::string& name )
{
    FindNodeVisitor v(name) ;

    graph->accept(v) ;

    return v.getNode() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
osg::Texture2D*
oodUtil::findTexture2D( osg::Node* graph, const std::string& name )
{
    FindTexture2DVisitor    v(name) ;

    graph->accept(v) ;

    return v.getTexture2D() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
osg::StateSet*
oodUtil::findStateSet( osg::Node* graph, const std::string& name )
{
    FindStateSetVisitor v(name) ;

    graph->accept(v) ;

    return v.getStateSet() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
ood::Manager*
oodUtil::findManager( osg::Node* graph )
{
    Managers    managers ;

    if( findManagers( graph, managers ) ) {
        return managers[0] ;
    }

    return NULL ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
unsigned int
oodUtil::findManagers( osg::Node* graph, oodUtil::Managers& managers )
{
    FindManagersVisitor nv(managers) ;

    graph->accept(nv) ;

    return managers.size() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
unsigned int
oodUtil::findJoints(ood::World* world, Joints& joints, const std::string& regex)
{


    ood::ObjectList  objects ;

    if( regex != "" ) {

        world->getObjectsByRegexName(regex, objects) ;

    } else {

        objects = world->getObjectList() ;
    }



    ood::ObjectList::iterator    itr = objects.begin() ;
    ood::ObjectList::iterator    itr_end = objects.end() ;

    while( itr != itr_end ) {
        ood::Joint*  joint = (*itr++)->asJoint() ;

        if( joint ) {
            joints.push_back(joint) ;
        }
    }


    return joints.size() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
unsigned int
oodUtil::findCharacters(ood::World* world, Characters& characters, const std::string& regex)
{


    ood::ObjectList  objects ;

    if( regex != "" ) {

        world->getObjectsByRegexName(regex, objects) ;

    } else {

        objects = world->getObjectList() ;
    }




    ood::ObjectList::iterator    itr = objects.begin() ;
    ood::ObjectList::iterator    itr_end = objects.end() ;

    while( itr != itr_end ) {
        ood::CharacterBase*  character = (*itr++)->asCharacterBase() ;

        if( character ) {
            characters.push_back(character) ;
        }
    }


    return characters.size() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
unsigned int
oodUtil::findRigidBodies(ood::World* world, RigidBodies& bodies, const std::string& regex)
{


    ood::ObjectList  objects ;

    if( regex != "" ) {

        world->getObjectsByRegexName(regex, objects) ;

    } else {

        objects = world->getObjectList() ;
    }




    ood::ObjectList::iterator    itr = objects.begin() ;
    ood::ObjectList::iterator    itr_end = objects.end() ;

    while( itr != itr_end ) {
        ood::RigidBody*  body = (*itr++)->asRigidBody() ;

        if( body ) {
            bodies.push_back(body) ;
        }
    }


    return bodies.size() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
unsigned int
oodUtil::findWorlds( osg::Node* graph, oodUtil::Worlds& worlds )
{
    Managers    ms ;

    findManagers( graph, ms ) ;


    for(unsigned int i=0; i<ms.size(); i++) {
        if( ms[i]->getWorld() ) {
            worlds.push_back( ms[i]->getWorld() ) ;
        }
    }

    return worlds.size() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
ood::World*
oodUtil::findWorld( osg::Node* graph )
{
    Worlds  worlds ;

    if( findWorlds( graph, worlds) ) {
        return worlds[0] ;
    }

    return NULL ;
}
/* ....................................................................... */
/* ======================================================================= */
