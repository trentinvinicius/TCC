/*!
 * @file ooengine_actions.cpp
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
#include <ood/LinearInterpolator>
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( CreateAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;

        data->mEngine = new Engine() ;

        data->mEngine->setName( args ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--create            engine_name" ;
    }

ACTION_FOOTER( CreateAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( ReadAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;

        osg::ref_ptr<osg::Object>   obj = osgDB::readObjectFile( args ) ;

        Engine* engine = dynamic_cast<Engine*>( obj.get() ) ;

        if( engine == NULL ) {
            return false ;
        }

        data->mEngine = engine ;

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

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }

        return osgDB::writeObjectFile( *(data->mEngine), args ) ;
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
ACTION_HEADER( InitTorqueCurveAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }


        ScalarInterpolator*     torque_curve = new LinearInterpolator() ;

        torque_curve->setName( args ) ;

        data->mEngine->setTorqueCurve( torque_curve ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--init-torque-curve curve_name" ;
    }

ACTION_FOOTER( InitTorqueCurveAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( AddTorquePointAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }


        ScalarInterpolator*     torque_curve = data->mEngine->getTorqueCurve() ;

        if( ! torque_curve ) {
            return false ;
        }




        double  RPM, Nm ;


        if( sscanf( args, "%lf,%lf", &RPM, &Nm ) != 2 ) {
            return false ;
        }


        torque_curve->addPoint( inRPM(RPM), Nm ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--add-torque-point  RPM,Nm" ;
    }

ACTION_FOOTER( AddTorquePointAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( LimitsAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }




        double  speed_min, speed_max ;


        if( sscanf( args, "%lf,%lf", &speed_min, &speed_max ) != 2 ) {
            return false ;
        }


        data->mEngine->setSpeedStall( inRPM(speed_min) ) ;
        data->mEngine->setSpeedLimit( inRPM(speed_max) ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--limits            rpm_min,rpm_max" ;
    }

ACTION_FOOTER( LimitsAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( InertiaAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }




        double  inertia ;


        if( sscanf( args, "%lf", &inertia ) != 1 ) {
            return false ;
        }


        data->mEngine->setInertia( inertia ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--inertia           real" ;
    }

ACTION_FOOTER( InertiaAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( DragAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }




        double  drag ;


        if( sscanf( args, "%lf", &drag ) != 1 ) {
            return false ;
        }


        data->mEngine->setDrag( drag ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--drag              real" ;
    }

ACTION_FOOTER( DragAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( InitGearListAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }


        data->mEngine->getGearList().clear() ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--init-gear-list    list_name" ;
    }

ACTION_FOOTER( InitGearListAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( AddGearAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }

        double  ratio = 0.0 ;


        if( sscanf( args, "%lf", &ratio ) != 1 ) {
            return false ;
        }

        

        data->mEngine->getGearList().push_back( ratio ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--add-gear          ratio" ;
    }

ACTION_FOOTER( AddGearAction )
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ACTION_HEADER( FinalAction )

    virtual bool    operator()( EngineData* data, const char* args )
    {
        PS_DBG("%s(%p)", className(), this) ;


        if( ! data->mEngine.valid() ) {
            return false ;
        }

        double  final = 0.0 ;


        if( sscanf( args, "%lf", &final ) != 1 ) {
            return false ;
        }



        data->mEngine->setFinal( final ) ;

        return true ;
    }


    virtual std::string help(void) const
    {
        return "--final             real" ;
    }

ACTION_FOOTER( FinalAction )
/* ....................................................................... */
/* ======================================================================= */
