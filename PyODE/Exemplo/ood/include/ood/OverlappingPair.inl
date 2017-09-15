/*!
 * @file OverlappingPair.inl
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2010 by Rocco Martino                                   *
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

#ifndef _OOD_OVERLAPPINGPAIR_INL
#define _OOD_OVERLAPPINGPAIR_INL

/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ood::Collidable*
ood::OverlappingPair::getCollidable1(void)
{
    return m_collidable1.get() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ood::Collidable*
ood::OverlappingPair::getCollidable2(void)
{
    return m_collidable2.get() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::OverlappingPair::setCollidables(ood::Collidable* collidable1, ood::Collidable* collidable2)
{
    m_collidable1 = collidable1 ;
    m_collidable2 = collidable2 ;
}
/* ....................................................................... */
/* ======================================================================= */




#endif /* _OOD_OVERLAPPINGPAIR_INL */
