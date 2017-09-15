/*!
 * @file oodynamics_actions.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2015 by Rocco Martino                                   *
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
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( ReadAction )

    virtual bool    operator()( SceneData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;

        osg::Node*  graph = osgDB::readNodeFile( args ) ;

        if( graph == NULL ) {
            return false ;
        }

        data->mGraph = graph ;


        data->mManager = findManager( graph ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--read              file_name" ;
    }

ACTION_FOOTER( ReadAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( WriteAction )

    virtual bool    operator()( SceneData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mGraph.valid() ) {
            return false ;
        }

        return osgDB::writeNodeFile( *(data->mGraph), args ) ;
    }


    virtual std::string help(void) const
    {
        return "--write             file_name" ;
    }

ACTION_FOOTER( WriteAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( BindWorldAction )

    virtual bool    operator()( SceneData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mGraph.valid() ) {
            return false ;
        }

        Managers    managers ;

        unsigned int    num_managers = findManagers( data->mGraph, managers ) ;

        Manager*    manager = NULL ;

        for( unsigned int i=0; i<num_managers; i++ ) {

            PS_ASSERT1( managers[i]->getWorld() ) ;

            if( managers[i]->getWorld()->getName() == args ) {
                manager = managers[i] ;

                break ;
            }
        }


        if( ! manager ) {
            return false ;
        }

        data->mManager = manager ;

        return true ;

    }


    virtual std::string help(void) const
    {
        return "--bind-world        world_name" ;
    }

ACTION_FOOTER( BindWorldAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( BindAction )

    virtual bool    operator()( SceneData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mManager.valid() ) {
            return false ;
        }



        PS_ASSERT1( data->mManager->getWorld() ) ;



        ODEObject*  obj = data->mManager->getWorld()->getObjectByName( args ) ;




        if( ! obj ) {
            return false ;
        }

        data->mObject = obj ;

        return true ;

    }


    virtual std::string help(void) const
    {
        return "--bind              object_name" ;
    }

ACTION_FOOTER( BindAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( WriteObjectAction )

    virtual bool    operator()( SceneData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mObject.valid() ) {
            return false ;
        }

        return osgDB::writeObjectFile( *data->mObject, args ) ;
    }


    virtual std::string help(void) const
    {
        return "--write-object      file_name.osg[b,t]" ;
    }

ACTION_FOOTER( WriteObjectAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( ReadObjectAction )

    virtual bool    operator()( SceneData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;

        ODEObject*  obj = dynamic_cast<ODEObject*>( osgDB::readObjectFile( args ) ) ;


        if( ! obj ) {
            return false ;
        }

        data->mManager = NULL ;
        data->mObject = obj ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--read-object       file_name.osg[b,t]" ;
    }

ACTION_FOOTER( ReadObjectAction )
/* ....................................................................... */
/* ======================================================================= */
