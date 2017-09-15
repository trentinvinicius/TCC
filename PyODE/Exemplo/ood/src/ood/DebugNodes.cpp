/*!
 * @file DebugDrawables.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2016 - 2017 by Rocco Martino                            *
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
#include <ood/Box>
#include <ood/Cylinder>
#include <ood/Sphere>
#include <ood/Capsule>
#include <ood/TriMesh>

#include <osg/ShapeDrawable>
/* ....................................................................... */
/* ======================================================================= */




using namespace ood ;




/* ======================================================================= */
/* ....................................................................... */
osg::Node*
Transformable::createDebugNode(void)
{

    float radius = osg::maximum( 0.1f, getActorBound().radius() ) ;



    osg::Shape*     shape = new osg::Sphere( osg::Vec3(), radius ) ;

    osg::ShapeDrawable* drawable = new osg::ShapeDrawable( shape ) ;


    osg::TessellationHints* th = new osg::TessellationHints() ;

    th->setDetailRatio( 0.125 ) ;

    drawable->setTessellationHints( th ) ;



    return drawable ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
osg::Node*
Collidable::createDebugNode(void)
{

    osg::Box*   shape = new osg::Box() ;

    osg::ShapeDrawable* drawable = new osg::ShapeDrawable( shape ) ;


    shape->setHalfLengths(  getSize() * 0.5 ) ;



    return drawable ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
osg::Node*
Box::createDebugNode(void)
{

    osg::Box*   shape = new osg::Box() ;

    osg::ShapeDrawable* drawable = new osg::ShapeDrawable( shape ) ;


    shape->setHalfLengths(  getSize() * 0.5 ) ;



    return drawable ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
osg::Node*
Cylinder::createDebugNode(void)
{

    osg::Cylinder*  shape = new osg::Cylinder() ;

    osg::ShapeDrawable* drawable = new osg::ShapeDrawable( shape ) ;


    osg::Vec3   size = getSize() ;


    shape->setRadius(  ( size.x() + size.y() )* 0.25 ) ;

    shape->setHeight( size.z() ) ;


    osg::TessellationHints* th = new osg::TessellationHints() ;

    th->setDetailRatio( 0.2 ) ;

    drawable->setTessellationHints( th ) ;



    return drawable ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
osg::Node*
Sphere::createDebugNode(void)
{
    osg::Vec3   size = getSize() ;

    float radius = ( size.x() + size.y() + size.z() ) / 6.0 ;



    osg::Shape*     shape = new osg::Sphere( osg::Vec3(), radius ) ;

    osg::ShapeDrawable* drawable = new osg::ShapeDrawable( shape ) ;


    osg::TessellationHints* th = new osg::TessellationHints() ;

    th->setDetailRatio( 0.25 ) ;

    drawable->setTessellationHints( th ) ;



    return drawable ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
osg::Node*
Capsule::createDebugNode(void)
{

    osg::Capsule*   shape = new osg::Capsule() ;

    osg::ShapeDrawable* drawable = new osg::ShapeDrawable( shape ) ;


    osg::Vec3   size = getSize() ;

    float   radius = ( size.x() + size.y() ) * 0.25 ;

    shape->setRadius(  radius ) ;

    shape->setHeight( size.z() - 2.0 * radius ) ;


    osg::TessellationHints* th = new osg::TessellationHints() ;

    th->setDetailRatio( 0.25 ) ;

    drawable->setTessellationHints( th ) ;



    return drawable ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
osg::Node*
TriMesh::createDebugNode(void)
{

    osg::TriangleMesh*     shape = new osg::TriangleMesh() ;

    osg::ShapeDrawable* drawable = new osg::ShapeDrawable( shape ) ;


    shape->setVertices( m_vertex_array ) ;
    shape->setIndices( m_index_array ) ;



    return drawable ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
osg::Node*
Joint::createDebugNode(void)
{
    return new osg::Node() ;
}
/* ....................................................................... */
/* ======================================================================= */
