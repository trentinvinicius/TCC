/*!
 * @file SliderJoint_serializer.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2012 - 2014 by Rocco Martino                            *
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
#include <ood/SliderJoint>

#include <osgDB/Registry>

#include "real_serializer"
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
static bool checkRelativeRotation(const ood::SliderJoint& joint)
{
    return joint.getRelativeRotation() != osg::Quat() ;
}

static bool readRelativeRotation(osgDB::InputStream& is, ood::SliderJoint& joint)
{
    osg::Quat   q ;
    is >> q ;
    joint.setRelativeRotation(q) ;
    return true ;
}

static bool writeRelativeRotation(osgDB::OutputStream& os, const ood::SliderJoint& joint)
{
    osg::Quat   q = joint.getRelativeRotation() ;
    os << q << std::endl ;
    return true ;
}



static bool checkRelativePosition(const ood::SliderJoint& joint)
{
    return joint.getRelativePosition() != osg::Vec3() ;
}

static bool readRelativePosition(osgDB::InputStream& is, ood::SliderJoint& joint)
{
    osg::Vec3   v ;
    is >> v ;
    joint.setRelativePosition(v) ;
    return true ;
}

static bool writeRelativePosition(osgDB::OutputStream& os, const ood::SliderJoint& joint)
{
    osg::Vec3   v = joint.getRelativePosition() ;
    os << v << std::endl ;
    return true ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
REGISTER_OBJECT_WRAPPER( SliderJoint,
                         new ood::SliderJoint,
                         ood::SliderJoint,
                         "osg::Object ood::ODEObject ood::Transformable ood::Joint ood::SliderJoint" )
{
    ADD_BOOL_SERIALIZER( AutoComputeRelativeValues, true ) ;

    ADD_USER_SERIALIZER( RelativeRotation ) ;
    ADD_USER_SERIALIZER( RelativePosition ) ;


    BEGIN_ENUM_SERIALIZER( StopMode, ERP_CFM ) ;
        ADD_ENUM_VALUE( ERP_CFM ) ;
        ADD_ENUM_VALUE( SPRING_DAMPER ) ;
    END_ENUM_SERIALIZER() ;


    ADD_REAL_SERIALIZER( Spring,        1.0 ) ;
    ADD_REAL_SERIALIZER( DamperBound,   0.0 ) ;
    ADD_REAL_SERIALIZER( DamperRebound, 0.0 ) ;
    ADD_REAL_SERIALIZER( Preload,       0.0 ) ;
}
/* ....................................................................... */
/* ======================================================================= */
