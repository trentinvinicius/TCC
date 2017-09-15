/*!
 * @file ooraycar_engine_actions.cpp
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
#include <ood/RigidBody>
#include <ood/SliderJoint>
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( EngineAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }

        osg::ref_ptr<osg::Object>   obj = osgDB::readObjectFile(args) ;

        Engine*     engine = dynamic_cast<Engine*>( obj.get() ) ;

        if( ! engine ) {
            return false ;
        }


        data->mRayCar->setEngine( engine ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--engine            file_name" ;
    }

ACTION_FOOTER( EngineAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( WriteEngineAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        if( ! data->mRayCar->getEngine() ) {
            return false ;
        }

        return osgDB::writeObjectFile( *data->mRayCar->getEngine(), args );
    }


    virtual std::string help(void) const
    {
        return "--write-engine      file_name" ;
    }

ACTION_FOOTER( WriteEngineAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( DriveAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }

        double  value ;

        if( sscanf( args, "%lf", &value ) != 1 ) {
            return false ;
        }

        data->mRayCar->setDrive( value ) ;


        return true ;
    }


    virtual std::string help(void) const
    {
        return "--write-engine      file_name" ;
    }

ACTION_FOOTER( DriveAction )
/* ....................................................................... */
/* ======================================================================= */
