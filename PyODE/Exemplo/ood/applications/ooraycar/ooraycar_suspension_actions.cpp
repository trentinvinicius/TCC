/*!
 * @file ooraycar_suspension_actions.cpp
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
ACTION_HEADER( SpringFrontAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        if( data->mRayCar->getSuspensionList().size() != 4 ) {
            return false ;
        }


        double  value ;

        if( sscanf( args, "%lf", &value ) != 1 ) {
            return false ;
        }

        data->mRayCar->getSuspension( RayCar::FRONT_LEFT )  ->setSpring( inKgmm(value) ) ;
        data->mRayCar->getSuspension( RayCar::FRONT_RIGHT ) ->setSpring( inKgmm(value) ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--spring-front      spring (Kg * mm)" ;
    }

ACTION_FOOTER( SpringFrontAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( SpringRearAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        if( data->mRayCar->getSuspensionList().size() != 4 ) {
            return false ;
        }


        double  value ;

        if( sscanf( args, "%lf", &value ) != 1 ) {
            return false ;
        }

        data->mRayCar->getSuspension( RayCar::REAR_LEFT )   ->setSpring( inKgmm(value) ) ;
        data->mRayCar->getSuspension( RayCar::REAR_RIGHT )  ->setSpring( inKgmm(value) ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--spring-rear       spring (Kg * mm)" ;
    }

ACTION_FOOTER( SpringRearAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( DamperFrontAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        if( data->mRayCar->getSuspensionList().size() != 4 ) {
            return false ;
        }


        double  value1, value2 ;

        if( sscanf( args, "%lf,%lf", &value1, &value2 ) != 2 ) {
            return false ;
        }

        data->mRayCar->getSuspension( RayCar::FRONT_LEFT )  ->setDamperBound( inKgms(value1) ) ;
        data->mRayCar->getSuspension( RayCar::FRONT_LEFT )  ->setDamperRebound( inKgms(value2) ) ;

        data->mRayCar->getSuspension( RayCar::FRONT_RIGHT ) ->setDamperBound( inKgms(value1) ) ;
        data->mRayCar->getSuspension( RayCar::FRONT_RIGHT ) ->setDamperRebound( inKgms(value2) ) ;


        return true ;
    }


    virtual std::string help(void) const
    {
        return "--damper-front      bound,rebound (Kg / millisecond)" ;
    }

ACTION_FOOTER( DamperFrontAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( DamperRearAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        if( data->mRayCar->getSuspensionList().size() != 4 ) {
            return false ;
        }


        double  value1, value2 ;

        if( sscanf( args, "%lf,%lf", &value1, &value2 ) != 2 ) {
            return false ;
        }

        data->mRayCar->getSuspension( RayCar::REAR_LEFT )   ->setDamperBound( inKgms(value1) ) ;
        data->mRayCar->getSuspension( RayCar::REAR_LEFT )   ->setDamperRebound( inKgms(value2) ) ;

        data->mRayCar->getSuspension( RayCar::REAR_RIGHT )  ->setDamperBound( inKgms(value1) ) ;
        data->mRayCar->getSuspension( RayCar::REAR_RIGHT )  ->setDamperRebound( inKgms(value2) ) ;


        return true ;
    }


    virtual std::string help(void) const
    {
        return "--damper-rear       bound,rebound (Kg / millisecond)" ;
    }

ACTION_FOOTER( DamperRearAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( PreloadFrontAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        if( data->mRayCar->getSuspensionList().size() != 4 ) {
            return false ;
        }


        double  value ;

        if( sscanf( args, "%lf", &value ) != 1 ) {
            return false ;
        }

        data->mRayCar->getSuspension( RayCar::FRONT_LEFT )  ->setPreload( inKg(value) ) ;
        data->mRayCar->getSuspension( RayCar::FRONT_RIGHT ) ->setPreload( inKg(value) ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--preload-front     preload (Kg)" ;
    }

ACTION_FOOTER( PreloadFrontAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( PreloadRearAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        if( data->mRayCar->getSuspensionList().size() != 4 ) {
            return false ;
        }


        double  value ;

        if( sscanf( args, "%lf", &value ) != 1 ) {
            return false ;
        }

        data->mRayCar->getSuspension( RayCar::REAR_LEFT )   ->setPreload( inKg(value) ) ;
        data->mRayCar->getSuspension( RayCar::REAR_RIGHT )  ->setPreload( inKg(value) ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--preload-rear      preload (Kg)" ;
    }

ACTION_FOOTER( PreloadRearAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( RideHeightAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        if( data->mRayCar->getSuspensionList().size() != 4 ) {
            return false ;
        }



        double  front, rear ;

        if( sscanf( args, "%lf,%lf", &front, &rear ) != 2 ) {
            return false ;
        }



        data->mRayCar->computeRideHeight( front, rear ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--ride-height       front,rear (m)" ;
    }

ACTION_FOOTER( RideHeightAction )
/* ....................................................................... */
/* ======================================================================= */
