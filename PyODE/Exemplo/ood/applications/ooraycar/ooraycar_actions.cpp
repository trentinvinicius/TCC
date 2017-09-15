/*!
 * @file ooraycar_actions.cpp
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
#include <ood/RayWheel>
#include <ood/SliderJoint>

#include <iostream>
#include <osg/io_utils>
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( CreateAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;

        data->mRayCar = new RayCar() ;

        data->mRayCar->setName( args ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--create            car_name" ;
    }

ACTION_FOOTER( CreateAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( InitAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;

        Container*  container = dynamic_cast<Container*>( osgDB::readObjectFile( args ) ) ;

        if( container == NULL ) {
            return false ;
        }

        data->mRayCar->setObjectList( container->getObjectList() ) ;





        RigidBody*      body = dynamic_cast<RigidBody*>( data->mRayCar->getObjectByName("oo_body") ) ;

        data->mRayCar->setBody( body ) ;



        Transformable*  bottom = dynamic_cast<Transformable*>( data->mRayCar->getObjectByName("oo_bottom") ) ;


        data->mRayCar->setBottom( ( body->getPosition() - bottom->getMatrixTransform()->getMatrix().getTrans() ).length() ) ;






        std::vector< osg::ref_ptr<RayWheel> >  wheel_list ;


        {
            std::vector< osg::ref_ptr<RigidBody> >  body_list ;

            body_list.push_back(  dynamic_cast<RigidBody*>( data->mRayCar->getObjectByName("oo_wheel_fl") ) ) ;
            body_list.push_back(  dynamic_cast<RigidBody*>( data->mRayCar->getObjectByName("oo_wheel_fr") ) ) ;
            body_list.push_back(  dynamic_cast<RigidBody*>( data->mRayCar->getObjectByName("oo_wheel_rl") ) ) ;
            body_list.push_back(  dynamic_cast<RigidBody*>( data->mRayCar->getObjectByName("oo_wheel_rr") ) ) ;


            for( unsigned int i=0; i<body_list.size(); i++ ) {

                osg::ref_ptr<RayWheel>  wheel = new RayWheel( * body_list[i] ) ;

                unsigned int    idx = data->mRayCar->getObjectIdx( body_list[i] ) ;

                if( idx == ODEOBJECT_NOT_FOUND ) {
                    return false ;
                }

                wheel_list.push_back( wheel ) ;

                data->mRayCar->setObject( idx, wheel ) ;

            }
        }




        RayCar::SuspensionList&     suspension_list = data->mRayCar->getSuspensionList() ;

        suspension_list.clear() ;

        for( unsigned int i=0; i<wheel_list.size(); i++ ) {


            wheel_list[i]->setRadius( wheel_list[i]->getActorBound().radius() ) ;



            SliderJoint*    slider = new SliderJoint() ;

            slider->setBody1( body ) ;

            slider->setBody2( wheel_list[i] ) ;

            slider->setAxis1( body->getQuaternion() * data->mRayCar->getUpVersor() ) ;

            slider->setParam( dParamLoStop1, 0.0 ) ;
            slider->setParam( dParamHiStop1, 0.0 ) ;

            slider->setParam( dParamERP, 1.0 ) ;
            slider->setParam( dParamCFM, 0.0 ) ;
            slider->setParam( dParamStopERP, 1.0 ) ;
            slider->setParam( dParamStopCFM, 0.0 ) ;





            slider->setStopMode( SliderJoint::SPRING_DAMPER ) ;



            ooReal  spring = inKgmm( 2 ) ;
            ooReal  damp = inKgms( 1 ) ;


            slider->setSpring( spring ) ;
            slider->setDamperBound( damp ) ;
            slider->setDamperRebound( damp ) ;



            slider->setAutoComputeRelativeValues( false ) ;


            slider->setRelativePosition( wheel_list[i]->getQuaternion().inverse() * ( body->getPosition() - wheel_list[i]->getPosition() ) ) ;
            slider->setRelativeRotation( wheel_list[i]->getQuaternion() * body->getQuaternion().inverse()  ) ;


            suspension_list.push_back( slider ) ;


            data->mRayCar->addObject( slider ) ;
        }



        return true ;
    }


    virtual std::string help(void) const
    {
        return "--init              file_name" ;
    }

ACTION_FOOTER( InitAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( ReadAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;

        RayCar* raycar = dynamic_cast<RayCar*>( osgDB::readObjectFile( args ) ) ;

        if( raycar == NULL ) {
            return false ;
        }

        data->mRayCar = raycar ;

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

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }

        return osgDB::writeObjectFile( *(data->mRayCar), args ) ;
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
ACTION_HEADER( GripAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        double  value1, value2 ;

        if( sscanf( args, "%lf,%lf", &value1, &value2 ) != 2 ) {
            return false ;
        }

        data->mRayCar->getWheel( RayCar::FRONT_LEFT )->setGrip( value1 ) ;
        data->mRayCar->getWheel( RayCar::FRONT_RIGHT )->setGrip( value1 ) ;
        data->mRayCar->getWheel( RayCar::REAR_LEFT )->setGrip( value2 ) ;
        data->mRayCar->getWheel( RayCar::REAR_RIGHT )->setGrip( value2 ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--grip              front,rear [0,inf)" ;
    }

ACTION_FOOTER( GripAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( TranslateAction )

    virtual bool    operator()( RayCarData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mRayCar.valid() ) {
            return false ;
        }


        double  x, y, z ;

        if( sscanf( args, "%lf,%lf,%lf", &x, &y, &z ) != 3 ) {
            return false ;
        }




        data->mRayCar->transform( osg::Matrix::translate( osg::Vec3(x, y, z) ) ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--translate         x,y,z" ;
    }

ACTION_FOOTER( TranslateAction )
/* ....................................................................... */
/* ======================================================================= */
