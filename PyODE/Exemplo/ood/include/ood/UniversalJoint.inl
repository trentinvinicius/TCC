/*!
 * @file UniversalJoint.inl
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2010 - 2017 by Rocco Martino                            *
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

#ifndef _OOD_UNIVERSALJOINT_INL
#define _OOD_UNIVERSALJOINT_INL

/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ooReal
ood::UniversalJoint::getAngle1(void) const
{
    return dJointGetUniversalAngle1(m_ODE_joint) ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ooReal
ood::UniversalJoint::getAngle2(void) const
{
    return dJointGetUniversalAngle2(m_ODE_joint) ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ooReal
ood::UniversalJoint::getAngle1Rate(void) const
{
    return dJointGetUniversalAngle1Rate(m_ODE_joint) ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ooReal
ood::UniversalJoint::getAngle2Rate(void) const
{
    return dJointGetUniversalAngle2Rate(m_ODE_joint) ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
inline void
ood::UniversalJoint::setAutoComputeRelativeValues( bool auto_compute_relative_values )
{
    dJointSetUniversalAutoComputeRelativeValues( m_ODE_joint, auto_compute_relative_values ) ;
}




inline bool
ood::UniversalJoint::getAutoComputeRelativeValues(void) const
{
    return dJointGetUniversalAutoComputeRelativeValues(m_ODE_joint) != 0 ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
inline void
ood::UniversalJoint::setRelativeRotation1( const osg::Quat& relative_rotation )
{
    dQuaternion q ;

    q[0] = relative_rotation.w() ;
    q[1] = relative_rotation.x() ;
    q[2] = relative_rotation.y() ;
    q[3] = relative_rotation.z() ;

    dJointSetUniversalRelativeRotation1( m_ODE_joint, q ) ;
}




inline osg::Quat
ood::UniversalJoint::getRelativeRotation1(void) const
{
    dQuaternion q ;

    dJointGetUniversalRelativeRotation1( m_ODE_joint, q ) ;

    return osg::Quat( q[1], q[2], q[3], q[0] ) ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
inline void
ood::UniversalJoint::setRelativeRotation2( const osg::Quat& relative_rotation )
{
    dQuaternion q ;

    q[0] = relative_rotation.w() ;
    q[1] = relative_rotation.x() ;
    q[2] = relative_rotation.y() ;
    q[3] = relative_rotation.z() ;

    dJointSetUniversalRelativeRotation2( m_ODE_joint, q ) ;
}




inline osg::Quat
ood::UniversalJoint::getRelativeRotation2(void) const
{
    dQuaternion q ;

    dJointGetUniversalRelativeRotation2( m_ODE_joint, q ) ;

    return osg::Quat( q[1], q[2], q[3], q[0] ) ;
}
/* ....................................................................... */
/* ======================================================================= */




#endif /* _OOD_UNIVERSALJOINT_INL */
