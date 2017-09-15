/*!
 * @file oodynamics_world_actions.cpp
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
ACTION_HEADER( AddObjectAction )

    virtual bool    operator()( SceneData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        PS_ASSERT1( data->mManager.valid() ) ;
        PS_ASSERT1( data->mManager->getWorld() ) ;


        ODEObject*  obj = dynamic_cast<ODEObject*>( osgDB::readObjectFile( args ) ) ;

        if( obj == NULL ) {
            return false ;
        }

        data->mManager->getWorld()->addObject( obj ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--add-object        file_name" ;
    }

ACTION_FOOTER( AddObjectAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( RemoveObjectAction )

    virtual bool    operator()( SceneData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        PS_ASSERT1( data->mManager.valid() ) ;
        PS_ASSERT1( data->mManager->getWorld() ) ;


        ODEObject*  obj = data->mManager->getWorld()->getObjectByName( args ) ;

        if( obj == NULL ) {
            return false ;
        }

        data->mManager->getWorld()->removeObject( obj ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--remove-object     object_name" ;
    }

ACTION_FOOTER( RemoveObjectAction )
/* ....................................................................... */
/* ======================================================================= */
