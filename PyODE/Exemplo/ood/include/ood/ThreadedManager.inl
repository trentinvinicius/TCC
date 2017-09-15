/*!
 * @file ThreadedManager.inl
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2014 - 2016 by Rocco Martino                            *
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

#ifndef _OOD_THREADEDMANAGER_INL
#define _OOD_THREADEDMANAGER_INL




/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::ThreadedManager::pause( bool wait )
{
    m_pause_request = true ;

    if( wait ) {
        while( ! m_paused ) {
            OpenThreads::Thread::YieldCurrentThread() ;
        }
    }
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::ThreadedManager::unpause(void)
{
    m_pause_request = false ;
    m_paused = false ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline bool
ood::ThreadedManager::rdy(void) const
{
    return m_rdy ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::ThreadedManager::rdy( bool v )
{
    m_rdy = v ;
}
/* ....................................................................... */
/* ======================================================================= */




#endif /* _OOD_THREADEDMANAGER_INL */
