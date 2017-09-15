/*!
 * @file Hinge2Joint.cpp
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

/* ======================================================================= */
/* ....................................................................... */
#include <ood/Hinge2Joint>
#include <ood/StaticWorld>
#include <ood/World>
#include <ood/Notify>
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




using namespace ood ;




/* ======================================================================= */
/* ....................................................................... */
Hinge2Joint::Hinge2Joint(void)
{
    m_ODE_joint = dJointCreateHinge2(StaticWorld::instance()->getODEWorld(), NULL) ;

    dJointSetData( m_ODE_joint, this ) ;

    m_functions.SetAxis1    = dJointSetHinge2Axis1 ;
    m_functions.GetAxis1    = dJointGetHinge2Axis1 ;

    m_functions.SetAxis2    = dJointSetHinge2Axis2 ;
    m_functions.GetAxis2    = dJointGetHinge2Axis2 ;

    m_functions.SetAnchor1  = dJointSetHinge2Anchor ;
    m_functions.GetAnchor1  = dJointGetHinge2Anchor ;

    m_functions.GetAnchor2  = dJointGetHinge2Anchor2 ;

    m_functions.SetParam    = dJointSetHinge2Param ;
    m_functions.GetParam    = dJointGetHinge2Param ;


    this->Joint::m_ensure_two_bodies = true ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
Hinge2Joint::Hinge2Joint(const Hinge2Joint& other, const osg::CopyOp& copyop):
    Joint(other, copyop)
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
Hinge2Joint::~Hinge2Joint(void)
{
    if(m_ODE_joint) {
        dJointDestroy(m_ODE_joint) ;
    }
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
dJointID
Hinge2Joint::cloneODEJoint(dWorldID world) const
{
    PS_DBG2("ood::Hinge2Joint::cloneODEJoint(%p, world=%p)", this, world) ;

    dJointID    j = dJointCreateHinge2(world, NULL) ;

    if(dJointIsEnabled(m_ODE_joint)) {
        dJointEnable(j) ;
    } else {
        dJointDisable(j) ;
    }

    dJointSetFeedback(j, dJointGetFeedback(m_ODE_joint)) ;



    {
        dVector3    v ;
        dJointGetHinge2Anchor(m_ODE_joint, v) ;
        dJointSetHinge2Anchor(j, v[0], v[1], v[2]) ;
    }

    {
        dVector3    v ;
        dJointGetHinge2Axis1(m_ODE_joint, v) ;
        dJointSetHinge2Axis1(j, v[0], v[1], v[2]) ;
    }

    {
        dVector3    v ;
        dJointGetHinge2Axis2(m_ODE_joint, v) ;
        dJointSetHinge2Axis2(j, v[0], v[1], v[2]) ;
    }



    return j ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ooReal
Hinge2Joint::getPosition( Axis a ) const
{
    switch( a )
    {
        case AXIS1:     return getAngle1() ;    break ;

        case AXIS2:     return 0.0 ;            break ;

        case AXIS3:     return 0.0 ;            break ;

        default:    PS_ASSERT1( false ) ;       break ;
    }


    return 0.0 ;
}



ooReal
Hinge2Joint::getPositionRate( Axis a ) const
{
    switch( a )
    {
        case AXIS1:     return getAngle1Rate() ;    break ;

        case AXIS2:     return getAngle2Rate() ;    break ;

        case AXIS3:     return 0.0 ;                break ;

        default:    PS_ASSERT1( false ) ;           break ;
    }


    return 0.0 ;
}
/* ....................................................................... */
/* ======================================================================= */
