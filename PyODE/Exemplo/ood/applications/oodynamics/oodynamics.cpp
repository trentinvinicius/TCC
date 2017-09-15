/*!
 * @file oodynamics.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2015 - 2016 by Rocco Martino                            *
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
#include <ood/ThreadedManager>
#include <ood/Notify>

#include <oodUtil/HashTable>

#include <osgDB/WriteFile>
#include <osgDB/ReadFile>
/* ....................................................................... */
/* ======================================================================= */




#if defined(OOD_LIBRARY_STATIC)

USE_SERIALIZER_WRAPPER_LIBRARY(ood) ;
USE_SERIALIZER_WRAPPER_LIBRARY(oodutil) ;

#endif




using namespace ood ;
using namespace oodUtil ;









/* ======================================================================= */
/* ....................................................................... */
class SceneData: public osg::Referenced
{
public:
    osg::ref_ptr<osg::Node>     mGraph ;

    osg::ref_ptr<Manager>       mManager ;

    osg::ref_ptr<ODEObject>     mObject ;
} ;




class Action: public osg::Object
{
public:
    Action(void)
    {
    }

    Action( const Action& other, const osg::CopyOp& copyop=osg::CopyOp::SHALLOW_COPY ):
    osg::Object     ( other, copyop )
    {
    }


    META_Object(oodynamics, Action) ;



    virtual bool    operator()( SceneData* data, const char* args )
    {
        return false ;
    }


    virtual std::string help(void) const
    {
        return "" ;
    }
} ;





#define ACTION_HEADER( ACTION_NAME )    \
class ACTION_NAME: public Action {      \
public: \
    ACTION_NAME(void) {} \
    ACTION_NAME( const ACTION_NAME& other, const osg::CopyOp& copyop=osg::CopyOp::SHALLOW_COPY ): Action(other, copyop) {} \
    META_Object(oodynamics, ACTION_NAME) ;


#define ACTION_FOOTER( ACTION_NAME )    \
protected: \
    virtual ~ACTION_NAME(void) \
    { \
    } \
} ;




#include "oodynamics_actions.cpp"
#include "oodynamics_world_actions.cpp"
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
HashTable*
init_table(void)
{
    HashTable*  table = new HashTable() ;



    table->set( "--read",                   new ReadAction() ) ;
    table->set( "--write",                  new WriteAction() ) ;
    table->set( "--bind-world",             new BindWorldAction() ) ;
    table->set( "--bind",                   new BindAction() ) ;
    table->set( "--write-object",           new WriteObjectAction() ) ;
    table->set( "--read-object",            new ReadObjectAction() ) ;
    table->set( "--add-object",             new AddObjectAction() ) ;
    table->set( "--remove-object",          new RemoveObjectAction() ) ;



    return table ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
void
show_info( osg::Object* obj )
{
    Action* action = dynamic_cast<Action*>( obj ) ;

    if( action ) {
        std::cout << action->help() << std::endl ;
    }
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
int
main( int argc, char** argv)
{
    psSetLogLevel( LOG_LEVEL_DEBUG ) ;


    osg::ref_ptr<SceneData>     scene_data = new SceneData() ;

    osg::ref_ptr<HashTable>     table ;


    table = init_table() ;


    if( argc == 1 ) {
        table->traverseObjects( show_info ) ;
        return 0 ;
    }




    int counter = 1 ;

    while( counter < argc ) {

        const char* action_name = argv[counter++] ;

        if( counter == argc ) {
            PS_FATAL("%s", "Expected something before EOF") ;
            return -1 ;
        }


        osg::ref_ptr<Action>    action = dynamic_cast<Action*>( table->get( action_name ) ) ;

        if( ! action ) {
            PS_FATAL("%s: invalid action", action_name) ;
            continue ;
        }


        action = osg::clone( action.get() ) ;


        const char* params = argv[counter++] ;

        if( ! (*action)( scene_data, params ) ) {
            PS_FATAL("%s %s: execution error ", action_name, params) ;
            continue ;
        }


    }


    table = NULL ;
    scene_data = NULL ;



    return 0 ;
}
/* ....................................................................... */
/* ======================================================================= */
