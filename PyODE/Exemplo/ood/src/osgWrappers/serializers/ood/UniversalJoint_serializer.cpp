/*!
 * @file UniversalJoint_serializer.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2012 - 2017 by Rocco Martino                            *
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
#include <ood/UniversalJoint>

#include <osgDB/Registry>
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
static bool checkRelativeRotation1(const ood::UniversalJoint& joint)
{
    (void) joint ;
    return true ;
}

static bool readRelativeRotation1(osgDB::InputStream& is, ood::UniversalJoint& joint)
{
    osg::Quat   q ;
    is >> q ;
    joint.setRelativeRotation1(q) ;
    return true ;
}

static bool writeRelativeRotation1(osgDB::OutputStream& os, const ood::UniversalJoint& joint)
{
    osg::Quat   q = joint.getRelativeRotation1() ;
    os << q << std::endl ;
    return true ;
}


static bool checkRelativeRotation2(const ood::UniversalJoint& joint)
{
    (void) joint ;
    return true ;
}

static bool readRelativeRotation2(osgDB::InputStream& is, ood::UniversalJoint& joint)
{
    osg::Quat   q ;
    is >> q ;
    joint.setRelativeRotation2(q) ;
    return true ;
}

static bool writeRelativeRotation2(osgDB::OutputStream& os, const ood::UniversalJoint& joint)
{
    osg::Quat   q = joint.getRelativeRotation2() ;
    os << q << std::endl ;
    return true ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
REGISTER_OBJECT_WRAPPER( UniversalJoint,
                         new ood::UniversalJoint,
                         ood::UniversalJoint,
                         "osg::Object ood::ODEObject ood::Transformable ood::Joint ood::UniversalJoint" )
{
    ADD_BOOL_SERIALIZER( AutoComputeRelativeValues, true ) ;

    ADD_USER_SERIALIZER( RelativeRotation1 ) ;
    ADD_USER_SERIALIZER( RelativeRotation2 ) ;
}
/* ....................................................................... */
/* ======================================================================= */
