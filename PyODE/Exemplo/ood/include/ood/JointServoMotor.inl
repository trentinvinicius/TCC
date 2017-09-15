/*!
 * @file JointServoMotor.inl
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
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU Lesser General Public      *
 *   License along with this program; if not, write to the                 *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#ifndef _OOD_JOINTSERVOMOTOR_INL
#define _OOD_JOINTSERVOMOTOR_INL




// Inline methods - do not edit this line




/* ======================================================================= */
// Position
/* ....................................................................... */
inline void
ood::JointServoMotor::setPosition( ooReal position )
{
    m_position = position ;
}




inline ooReal
ood::JointServoMotor::getPosition(void) const
{
    return m_position ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// Force
/* ....................................................................... */
inline void
ood::JointServoMotor::setForce( ooReal force )
{
    m_force = force ;
}




inline ooReal
ood::JointServoMotor::getForce(void) const
{
    return m_force ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// MaxVel
/* ....................................................................... */
inline void
ood::JointServoMotor::setMaxVel( ooReal max_vel)
{
    m_max_vel = max_vel ;
}




inline ooReal
ood::JointServoMotor::getMaxVel(void) const
{
    return m_max_vel ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// Angle
/* ....................................................................... */
inline void
ood::JointServoMotor::setAxis( int axis )
{
    m_axis = axis ;

    switch( axis )
    {
        case Joint::AXIS1:
            m_param_fmax = dParamFMax1 ;
            m_param_vel = dParamVel1 ;
        break ;


        case Joint::AXIS2:
            m_param_fmax = dParamFMax2 ;
            m_param_vel = dParamVel2 ;
        break ;


        case Joint::AXIS3:
            m_param_fmax = dParamFMax3 ;
            m_param_vel = dParamVel3 ;
        break ;
    }
}




inline int
ood::JointServoMotor::getAxis(void) const
{
    return m_axis ;
}
/* ....................................................................... */
/* ======================================================================= */







#endif /* _OOD_JOINTSERVOMOTOR_INL */
