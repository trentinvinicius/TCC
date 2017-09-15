/*!
 * @file RayCar_serializer.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2012 - 2015 by Rocco Martino                            *
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
#include <ood/RayCar>
#include <ood/Engine>
#include <ood/SliderJoint>

#include <osgDB/Registry>

#include "real_serializer"
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
REGISTER_OBJECT_WRAPPER( RayCar,
                         new ood::RayCar,
                         ood::RayCar,
                         "osg::Object ood::ODEObject ood::Container ood::RayCar" )
{
    ADD_OBJECT_SERIALIZER( Body, ood::RigidBody, NULL ) ;

    ADD_LIST_SERIALIZER( SuspensionList, ood::RayCar::SuspensionList ) ;

    ADD_VEC3_SERIALIZER( UpVersor, osg::Z_AXIS ) ;
    ADD_VEC3_SERIALIZER( FrontVersor, osg::Y_AXIS ) ;

    ADD_REAL_SERIALIZER( Bottom, 0.0 ) ;

    ADD_REAL_SERIALIZER( Drive, 0.5 ) ;
    ADD_REAL_SERIALIZER( Steer, 0.0 ) ;

    ADD_OBJECT_SERIALIZER( Engine, ood::Engine, NULL ) ;
}
/* ....................................................................... */
/* ======================================================================= */
