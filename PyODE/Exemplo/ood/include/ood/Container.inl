/*!
 * @file Container.inl
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

#ifndef _OOD_CONTAINER_INL
#define _OOD_CONTAINER_INL

/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
// inline bool
// ood::Container::removeObject(ood::ODEObject* obj, bool preserve_order)
// {
//     if( ! obj ) {
//         return false ;
//     }
//
//     unsigned int    idx = getObjectIdx(obj) ;
//
//     if( idx != ODEOBJECT_NOT_FOUND ) {
//         return removeObject(idx, preserve_order) ;
//     }
//
//     return false ;
// }
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline bool
ood::Container::hasObject(const ODEObject* obj) const
{
    return getObjectIdx(obj) != ODEOBJECT_NOT_FOUND ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::Container::setObjectList(const ObjectList& object_list)
{
    clear() ;

    ObjectList::const_iterator  itr = object_list.begin() ;
    ObjectList::const_iterator  itr_end = object_list.end() ;


    while( itr != itr_end ) {

        addObject( *itr++ ) ;

    }
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline ood::ObjectList&
ood::Container::getObjectList(void)
{
    return m_object_list ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline const ood::ObjectList&
ood::Container::getObjectList(void) const
{
    return m_object_list ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
template<class T>
inline void
ood::Container::traverseObjects(T& t, void (T::*member)(ODEObject*))
{
    ObjectList::iterator    itr = m_object_list.begin() ;
    ObjectList::iterator    itr_end = m_object_list.end() ;


    while( itr != itr_end ) {

        (t.*member)( *itr++ ) ;

    }
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::Container::setMatrix( const osg::Matrix& matrix )
{
    setMatrix( matrix, true ) ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline void
ood::Container::setMatrix( const osg::Matrix& matrix, bool apply_transform )
{
    if( apply_transform ) {
        transform( matrix * osg::Matrix::inverse( m_matrix ) ) ;
    }

    m_matrix = matrix ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline osg::Matrix&
ood::Container::getMatrix(void)
{
    return m_matrix ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline const osg::Matrix&
ood::Container::getMatrix(void) const
{
    return m_matrix ;
}
/* ....................................................................... */
/* ======================================================================= */




#endif /* _OOD_CONTAINER_INL */
