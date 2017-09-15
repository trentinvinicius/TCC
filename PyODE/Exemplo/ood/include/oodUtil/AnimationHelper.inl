/*!
 * @file AnimationHelper.inl
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
 *   GNU Lesser General Public License for more details.                   *
 *                                                                         *
 *   You should have received a copy of the GNU Lesser General Public      *
 *   License along with this program; if not, write to the                 *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#ifndef _OODUTIL_ANIMATIONHELPER_INL
#define _OODUTIL_ANIMATIONHELPER_INL

/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
oodUtil::AnimationHelper::setAnimationManagerList( const AnimationManagerList& animation_manager_list )
{
    m_animation_manager_list = animation_manager_list ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline oodUtil::AnimationHelper::AnimationManagerList&
oodUtil::AnimationHelper::getAnimationManagerList(void)
{
    return m_animation_manager_list ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline const oodUtil::AnimationHelper::AnimationManagerList&
oodUtil::AnimationHelper::getAnimationManagerList(void) const
{
    return m_animation_manager_list ;
}
/* ....................................................................... */
/* ======================================================================= */




#endif /* _OODUTIL_ANIMATIONHELPER_INL */
