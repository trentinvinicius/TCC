/*!
 * @file RagDoll.inl
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2013 by Rocco Martino                                   *
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

#ifndef _OOD_RAGDOLL_INL
#define _OOD_RAGDOLL_INL




/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline osgAnimation::Bone*
ood::RagDoll::getRootBone(void)
{
    return m_root_bone.get() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ood::RigidBody*
ood::RagDoll::getRootBody(void)
{
    return m_root_body.get() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::RagDoll::dirty(void)
{
    m_dirty = true ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::RagDoll::setSkeleton( osgAnimation::Skeleton* skeleton )
{
    m_skeleton = skeleton ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline osgAnimation::Skeleton*
ood::RagDoll::getSkeleton(void)
{
    return m_skeleton ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline const osgAnimation::Skeleton*
ood::RagDoll::getSkeleton(void) const
{
    return m_skeleton ;
}
/* ....................................................................... */
/* ======================================================================= */




#endif /* _OOD_RAGDOLL_INL */
