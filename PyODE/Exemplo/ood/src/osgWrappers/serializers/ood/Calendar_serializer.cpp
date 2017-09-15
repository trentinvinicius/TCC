/*!
 * @file Calendar_serializer.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2017 by Rocco Martino                                   *
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
#include <ood/Calendar>

#include <osgDB/Registry>

#include <osg/ValueObject>

#include "real_serializer"
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
struct SetLatitudeInDegrees: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {


        if (inputParameters.size() != 3) return false;

        ood::Calendar*  calendar = reinterpret_cast<ood::Calendar*>( objectPtr ) ;

        int  g = dynamic_cast<osg::DoubleValueObject*>(inputParameters[0].get())->getValue() ;
        int  p = dynamic_cast<osg::DoubleValueObject*>(inputParameters[1].get())->getValue() ;
        int  s = dynamic_cast<osg::DoubleValueObject*>(inputParameters[2].get())->getValue() ;

        calendar->setLatitude( osg::inDegrees( g + p / 60.0 + s / 3600.0 ) ) ;

        return true;
    }
} ;
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
REGISTER_OBJECT_WRAPPER( Calendar,
                         new ood::Calendar,
                         ood::Calendar,
                         "osg::Object ood::ODEObject ood::Calendar" )
{
    ADD_UINT_SERIALIZER( SecondsInMinute,    60 ) ;
    ADD_UINT_SERIALIZER( MinutesInHour,      60 ) ;
    ADD_UINT_SERIALIZER( HoursInDay,         24 ) ;
    ADD_UINT_SERIALIZER( DaysInYear,        365 ) ;

    ADD_REAL_SERIALIZER( TemporalProgression, 1.0 ) ;
    ADD_REAL_SERIALIZER( Time, 0.0 ) ;
    ADD_REAL_SERIALIZER( AxisInclination, osg::inDegrees(23.0 + 27.0/60.0) ) ;
    ADD_REAL_SERIALIZER( Latitude, osg::inDegrees(35.0 + 31.0/60.0) ) ;

    ADD_VEC3_SERIALIZER( East, osg::X_AXIS ) ;
    ADD_VEC3_SERIALIZER( North, osg::Y_AXIS ) ;




    ADD_METHOD_OBJECT( "setLatitudeInDegrees", SetLatitudeInDegrees ) ;
}
/* ....................................................................... */
/* ======================================================================= */
