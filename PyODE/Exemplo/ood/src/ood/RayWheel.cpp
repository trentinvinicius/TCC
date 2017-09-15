/*!
 * @file RayWheel.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2015 by Rocco Martino                                   *
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
#include <ood/RayWheel>
#include <ood/Notify>
#include <ood/DefaultNearCallback>

#include <iostream>
#include <osg/io_utils>
/* ....................................................................... */
/* ======================================================================= */




using namespace ood ;




/* ======================================================================= */
/* ....................................................................... */
RayWheel::RayWheel(void):
    m_radius        ( 0.4 ),
    m_grip          ( 1.0 ),
    m_brake         ( 0.0 ),
    m_speed         ( 0.0 ),
    m_skid          ( 0.0 ),
    m_colliding     ( false )
{
    m_ray_cast_result = new NearestNotMeRayCastResult() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
RayWheel::RayWheel(const RayWheel& other, const osg::CopyOp& copyop):
    RigidBody       ( other, copyop ),
    m_radius        ( other.m_radius ),
    m_grip          ( other.m_grip ),
    m_brake         ( other.m_brake ),
    m_speed         ( other.m_speed ),
    m_skid          ( other.m_skid ),
    m_colliding     ( other.m_colliding )
{
    m_ray_cast_result = new NearestNotMeRayCastResult() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
RayWheel::RayWheel(const RigidBody& other, const osg::CopyOp& copyop):
    RigidBody       ( other, copyop ),
    m_radius        ( 0.4 ),
    m_grip          ( 1.0 ),
    m_brake         ( 0.0 ),
    m_speed         ( 0.0 ),
    m_skid          ( 0.0 )
{
    m_ray_cast_result = new NearestNotMeRayCastResult() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
RayWheel::~RayWheel(void)
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
bool
RayWheel::collide( const osg::Vec3& direction, const osg::Vec3& fdir1, dContact& contact, Collidable* body )
{
    osg::Vec3   ray_from = getPosition() ;


    osg::Vec3   ray_to = ray_from + direction * m_radius ;



    Space*  space = getWorld()->asSpace() ;



    m_ray_cast_result->reset() ;

    m_ray_cast_result->setMe( body ) ;



    space->performRayCast( ray_from,
                           ray_to,
                           m_ray_cast_result
           ) ;





    if( m_ray_cast_result->hasHit() ) {

        DefaultNearCallback*    near_callback = space->getNearCallback()->asDefaultNearCallback() ;

        PS_ASSERT1( near_callback != NULL ) ;



        const osg::Vec3&    position = m_ray_cast_result->getPosition() ;
        const osg::Vec3&    normal = m_ray_cast_result->getNormal() ;


        osg::Vec3   inv_ray_direction = ray_from - ray_to ;

        ooReal      ray_length = inv_ray_direction.normalize() ;




        ooReal  depth = normal * inv_ray_direction * ( ray_length - m_ray_cast_result->getDistance() ) ;


        dOPE( contact.geom.pos, =, position ) ;
        dOPE( contact.geom.normal, =, normal ) ;

        contact.geom.depth = depth ;

        contact.geom.g1 = NULL ;
        contact.geom.g2 = NULL ;



        contact.surface.mode = dContactApprox1 | dContactSoftERP | dContactSoftCFM | dContactMu2 | dContactFDir1 | dContactSlip2 ;
        contact.surface.mu = m_grip * m_brake ;
        contact.surface.mu2 = m_grip ;
        contact.surface.soft_erp = 0.8 ;
        contact.surface.soft_cfm = 1.0e-5 ;



        dReal   slip2 = fdir1 * getLinearVelocity() / m_radius + m_skid * m_radius ;

        contact.surface.slip2 = 1.0e-6 * slip2 ;

        dOPE( contact.fdir1, =, fdir1 ) ;


        near_callback->addContact( getODEBody(), m_ray_cast_result->getCollidable()->getODEBody(), &contact ) ;


        return true ;

    }


    return false ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
void
RayWheel::propagateFree(ooReal step_size, ooReal torque, ooReal vel)
{
	(void) vel;


    ooReal  inertia = 0.5 * getMass() * m_radius * m_radius * 10 ;

    m_skid += step_size * torque / inertia ;


    m_skid = osg::maximum( (ooReal)0.0, m_skid - step_size * inertia ) ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
void
RayWheel:: propagateConstrained(    ooReal              step_size,
                                    ooReal              torque,
                                    ooReal              vel,
                                    const osg::Vec3&    forces,
                                    const dContact&     contact )
{





    osg::Vec3   normal( contact.geom.normal[0], contact.geom.normal[1], contact.geom.normal[2] ) ;

    osg::Vec3   fdir1( contact.fdir1[0], contact.fdir1[1], contact.fdir1[2] ) ;



    m_speed = osg::absolute( getLinearVelocity() * fdir1 / m_radius ) ;


    osg::Vec3   dir = fdir1 ^ normal ;

    dir = normal ^ dir ;

    dir.normalize() ;




    osg::Vec3   jforce = forces ;

    ooReal  fn = osg::maximum( (ooReal) 0.0, (ooReal) (jforce * normal) * (ooReal) -1.0 ) ;

//         ooReal  ft = jforce * dir ;

    ooReal  fmax = fn * getGrip()/* + ft*/ ;

    ooReal  tmax = fmax * m_radius ;

    ooReal  DF = osg::maximum( (ooReal)0.0, torque - tmax) ;

    ooReal  F = osg::minimum( torque, tmax ) / m_radius ;

    addForce( dir * F ) ;

//         if( DF > 0.0 ) {
        propagateFree( step_size, DF, vel ) ;
//         } else {
//             ooReal  inertia = 0.5 * getMass() * m_radius * m_radius ;
//             m_skid = osg::maximum( 0.0, m_skid - step_size * inertia * 10.0 ) ;
//         }
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
RayWheel*
RayWheel::asRayWheel(void)
{
    return this ;
}
/* ....................................................................... */
/* ======================================================================= */
