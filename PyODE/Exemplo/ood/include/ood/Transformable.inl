/*!
 * @file Transformable.inl
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

#ifndef _OOD_TRANSFORMABLE_INL
#define _OOD_TRANSFORMABLE_INL

/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
inline const osgGA::CameraManipulator*
ood::Transformable::getCameraManipulator(void) const
{
    return m_camera_manipulator.get() ;
}





inline osgGA::CameraManipulator*
ood::Transformable::getCameraManipulator(void)
{
    return m_camera_manipulator.get() ;
}





inline void
ood::Transformable::setCameraManipulatorCenter(const osg::Vec3& center)
{
    m_camera_manipulator_center = center ;
}





inline const osg::Vec3&
ood::Transformable::getCameraManipulatorCenter(void) const
{
    return m_camera_manipulator_center ;
}





inline void
ood::Transformable::setCameraManipulatorDirection(const osg::Vec3& direction)
{
    m_camera_manipulator_direction = direction ;

    m_camera_manipulator_direction.normalize() ;
}





inline const osg::Vec3&
ood::Transformable::getCameraManipulatorDirection(void) const
{
    return m_camera_manipulator_direction ;
}





inline void
ood::Transformable::setCameraManipulatorUp(const osg::Vec3& up)
{
    m_camera_manipulator_up = up ;

    m_camera_manipulator_up.normalize() ;
}





inline const osg::Vec3&
ood::Transformable::getCameraManipulatorUp(void) const
{
    return m_camera_manipulator_up ;
}





inline void
ood::Transformable::setCameraManipulatorUpObjectSpace(bool flag)
{
    m_camera_manipulator_up_object = flag ;
}





inline bool
ood::Transformable::getCameraManipulatorUpObjectSpace(void) const
{
    return m_camera_manipulator_up_object ;
}





inline void
ood::Transformable::setCameraManipulatorElasticity(unsigned int elasticity)
{
    m_camera_manipulator_elasticity = elasticity ;
}





inline unsigned int
ood::Transformable::getCameraManipulatorElasticity(void) const
{
    return m_camera_manipulator_elasticity ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
inline void
ood::Transformable::setMatrixTransform(osg::MatrixTransform* transform)
{
    m_matrix_transform = transform ;
}





inline osg::MatrixTransform*
ood::Transformable::getMatrixTransform(void)
{
    return m_matrix_transform.get() ;
}





inline const osg::MatrixTransform*
ood::Transformable::getMatrixTransform(void) const
{
    return m_matrix_transform.get() ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
inline osg::StateSet*
ood::Transformable::getOrCreateStateSet(void)
{
    return m_matrix_transform->getOrCreateStateSet() ;
}





inline osg::StateSet*
ood::Transformable::getStateSet(void)
{
    return m_matrix_transform->getStateSet() ;
}





inline const osg::StateSet*
ood::Transformable::getStateSet(void) const
{
    return m_matrix_transform->getStateSet() ;
}





inline void
ood::Transformable::setStateSet(osg::StateSet* stateset)
{
    return m_matrix_transform->setStateSet(stateset) ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
inline void
ood::Transformable::setVisibility( bool visibility )
{
    m_visibility = visibility ;
}





inline bool
ood::Transformable::getVisibility(void)
{
    return m_visibility ;
}





inline bool
ood::Transformable::getVisibility(void) const
{
    return m_visibility ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
// DebugNode
/* ....................................................................... */
inline void
ood::Transformable::setDebugNode( osg::Node* debug_node)
{
    m_debug_node = debug_node ;
}




inline osg::Node*
ood::Transformable::getDebugNode(void)
{
    return m_debug_node ;
}




inline const osg::Node*
ood::Transformable::getDebugNode(void) const
{
    return m_debug_node ;
}




inline osg::Node*
ood::Transformable::getOrCreateDebugNode(void)
{
    if( ! m_debug_node.valid() ) {
        m_debug_node = createDebugNode() ;
    }


    return m_debug_node ;
}
/* ....................................................................... */
/* ======================================================================= */






#endif /* _OOD_TRANSFORMABLE_INL */
