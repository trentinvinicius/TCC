/*!
 * @file ServoMotor.inl
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

#ifndef _OOD_SERVOMOTOR_INL
#define _OOD_SERVOMOTOR_INL




// Inline methods - do not edit this line




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::ServoMotor::setPIDController( PIDController* pid_controller )
{
    m_pid_controller = pid_controller ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ood::PIDController*
ood::ServoMotor::getPIDController(void)
{
    return m_pid_controller ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline const ood::PIDController*
ood::ServoMotor::getPIDController(void) const
{
    return m_pid_controller ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ood::PIDController*
ood::ServoMotor::getOrCreatePIDController(void)
{
    if( ! m_pid_controller.valid() ) {
        m_pid_controller = new PIDController() ;
    }

    return m_pid_controller ;
}
/* ....................................................................... */
/* ======================================================================= */







#endif /* _OOD_SERVOMOTOR_INL */
