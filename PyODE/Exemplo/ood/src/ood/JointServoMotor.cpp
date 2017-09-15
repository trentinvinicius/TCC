/*!
 * @file JointServoMotor.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2014 - 2017 by Rocco Martino                            *
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
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU Lesser General Public      *
 *   License along with this program; if not, write to the                 *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

/* ======================================================================= */
/* ....................................................................... */
#include <ood/JointServoMotor>
#include <ood/World>
#include <ood/Notify>
/* ....................................................................... */
/* ======================================================================= */




using namespace ood ;




/* ======================================================================= */
/* ....................................................................... */
JointServoMotor::JointServoMotor(void)
    : m_position    ( 0.0 )
    , m_force       ( 0.0 )
    , m_max_vel     ( -1.0 )
    , m_axis        ( (int)Joint::AXIS1 )
    , m_param_fmax  ( dParamFMax )
    , m_param_vel   ( dParamVel )
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
JointServoMotor::JointServoMotor(const JointServoMotor& other, const osg::CopyOp& copyop)
    : ServoMotor        ( other, copyop )
    , m_position        ( other.m_position )
    , m_force           ( other.m_force )
    , m_max_vel         ( other.m_max_vel )
    , m_axis            ( other.m_axis )
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
JointServoMotor::~JointServoMotor(void)
{
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
void
JointServoMotor::operator()(ODEObject* object)
{

    Joint*  joint = object->asJoint() ;
    PS_ASSERT1( joint != NULL ) ;

    World*      world = object->getWorld() ;
    PS_ASSERT1( world != NULL ) ;



    PIDController*  pid = getPIDController() ;

    ooReal  vel = 0.0 ;

    ooReal  err = m_position - joint->getPosition( (Joint::Axis) m_axis ) ;

    if( pid ) {
        vel = pid->solve( err, world->getCurrentStepSize() ) ;
    } else {
        vel = err ;
    }

    if( m_max_vel >= 0.0 ) {

        vel = osg::clampTo( vel, -m_max_vel, m_max_vel ) ;
    }





    joint->setParam( m_param_fmax, m_force ) ;
    joint->setParam( m_param_vel, vel ) ;


    traverse(object) ;
}
/* ....................................................................... */
/* ======================================================================= */




