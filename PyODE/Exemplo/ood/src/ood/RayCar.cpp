/*!
 * @file RayCar.cpp
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
#include <ood/RayCar>
#include <ood/RayWheel>
#include <ood/SliderJoint>
#include <ood/Notify>
#include <ood/CommonRayCastResults>
#include <ood/DefaultNearCallback>

#include <iostream>
#include <osg/io_utils>
/* ....................................................................... */
/* ======================================================================= */




using namespace ood ;




/* ======================================================================= */
/* ....................................................................... */
RayCar::RayCar(void):
    m_up_versor     ( osg::Z_AXIS ),
    m_front_versor  ( osg::Y_AXIS ),
    m_drive         ( 0.5 ),
    m_steer         ( 0.0 ),
    m_bottom        ( 0.0 )
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
RayCar::RayCar(const RayCar& other, const osg::CopyOp& copyop):
    Container           ( other, copyop ),
    m_up_versor         ( other.m_up_versor ),
    m_front_versor      ( other.m_front_versor ),
    m_engine            ( osg::clone( m_engine.get(), copyop ) ),
    m_drive             ( other.m_drive ),
    m_steer             ( other.m_steer ),
    m_bottom            ( other.m_bottom )
{


    unsigned int    idx ;




    //
    // Find the body and the suspensions in the container
    //





    if( other.getBody() ) {


        idx = other.getObjectIdx( other.getBody() ) ;


        PS_ASSERT1( idx != ODEOBJECT_NOT_FOUND ) ;


        ODEObject*  obj = getObject( idx ) ;


        PS_ASSERT1( obj ) ;
        PS_ASSERT1( obj->asRigidBody() ) ;


        setBody( obj->asRigidBody() ) ;
    }








    if( other.getSuspensionList().size() != 0 ) {

        PS_ASSERT1( other.getSuspensionList().size() == NUM_SUSPENSIONS ) ;




//         m_suspension_list.clear() ;





        for( int i=0; i<NUM_SUSPENSIONS; i++ ) {




            SuspensionSelect which = (SuspensionSelect) i ;




            {
                idx = other.getObjectIdx( other.getSuspension(which) ) ;


                PS_ASSERT1( idx != ODEOBJECT_NOT_FOUND ) ;



                ODEObject*  obj = getObject( idx ) ;


                PS_ASSERT1( obj ) ;
                PS_ASSERT1( obj->asSliderJoint() ) ;


                m_suspension_list.push_back( obj->asSliderJoint() ) ;
            }
        }
    }
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
RayCar::~RayCar(void)
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
void
RayCar::update( ooReal step_size )
{
    PS_ASSERT1( m_suspension_list.size() == NUM_SUSPENSIONS ) ;

    PS_ASSERT1( getWorld() ) ;
    PS_ASSERT1( getWorld()->asSpace() ) ;


    osg::Vec3   fdir1_rear = m_body->getQuaternion() * m_front_versor ;


    osg::Vec3   fdir1_front = osg::Quat( m_steer, m_up_versor ) * m_front_versor ;

    fdir1_front = m_body->getQuaternion() * fdir1_front ;


    osg::Vec3   fdirs[NUM_SUSPENSIONS] ;
    {
        fdirs[ FRONT_LEFT ] = fdir1_front ;
        fdirs[ FRONT_RIGHT ] = fdir1_front ;
        fdirs[ REAR_LEFT ] = fdir1_rear ;
        fdirs[ REAR_RIGHT ] = fdir1_rear ;
    }
    






    ooReal  vmax = 0.0 ;

    ooReal  torques[NUM_SUSPENSIONS] ;
    {
        ooReal  torque = 0.5 * enginePropagate( step_size, vmax ) ;

        torques[ FRONT_LEFT ] = torque * m_drive ;
        torques[ FRONT_RIGHT ] = torque * m_drive ;

        torques[ REAR_LEFT ] = torque * (1.0 - m_drive) ;
        torques[ REAR_RIGHT ] = torque * (1.0 - m_drive) ;
    }







    dContact    contact ;


    for( unsigned int i=0; i<NUM_SUSPENSIONS; i++ ) {

        SuspensionSelect    which = ( SuspensionSelect ) i ;


        RayWheel*   wheel = getWheel( which ) ;


        if(   wheel->collide( m_up_versor * -1.0, fdirs[i], contact, m_body->asCollidable() )   ) {


            wheel->setColliding( true ) ;



            wheel->propagateConstrained(    step_size,
                                            torques[which],
                                            vmax,
                                            getSuspension( which )->getOrCreateJointFeedback()->getF2(),
                                            contact
                                       ) ;


        } else {


            wheel->setColliding( false ) ;

            wheel->propagateFree(   step_size,
                                    torques[ which ],
                                    vmax
                                ) ;

        }

    }







    this->Container::update( step_size ) ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
void
RayCar::postUpdate( ooReal step_size )
{
    m_engine->feedback( step_size, computeAverageSpeed() ) ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
/* ....................................................................... */
ooReal
RayCar::computeAverageSpeed(void) const
{


//     osg::Vec3   fdir1_rear = m_body->getQuaternion() * m_front_versor ;
// 
// 
//     osg::Vec3   fdir1_front = osg::Quat( m_steer, m_up_versor ) * m_front_versor ;
// 
//     fdir1_front = m_body->getQuaternion() * fdir1_front ;
// 
// 
//     ooReal  v1 = m_body->getPointVelocity( getWheel( FRONT_LEFT )->getPosition() ) * fdir1_front + getWheel(FRONT_LEFT)->getSkid() ;
//     ooReal  v2 = m_body->getPointVelocity( getWheel( FRONT_RIGHT )->getPosition() ) * fdir1_front + getWheel(FRONT_RIGHT)->getSkid() ;
//     ooReal  v3 = m_body->getPointVelocity( getWheel( REAR_LEFT )->getPosition() ) * fdir1_rear + getWheel(REAR_LEFT)->getSkid() ;
//     ooReal  v4 = m_body->getPointVelocity( getWheel( REAR_RIGHT )->getPosition() ) * fdir1_rear + getWheel(REAR_RIGHT)->getSkid() ;



    ooReal  v1 = getWheel( FRONT_LEFT )->getSpeed() + getWheel(FRONT_LEFT)->getSkid() ;
    ooReal  v2 = getWheel( FRONT_RIGHT )->getSpeed() + getWheel(FRONT_RIGHT)->getSkid() ;
    ooReal  v3 = getWheel( REAR_LEFT )->getSpeed() + getWheel(REAR_LEFT)->getSkid() ;
    ooReal  v4 = getWheel( REAR_RIGHT )->getSpeed() + getWheel(REAR_RIGHT)->getSkid() ;


    v1 *= 0.5 * m_drive  ;
    v2 *= 0.5 * m_drive  ;
    v3 *= 0.5 * (1.0 - m_drive)  ;
    v4 *= 0.5 * (1.0 - m_drive)  ;


    return v1 + v2 + v3 + v4 ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
/* ....................................................................... */
ooReal
RayCar::enginePropagate( ooReal step_size, ooReal& vmax )
{
    PS_ASSERT1( m_engine.valid() ) ;



    ooReal  vel, fmax ;


    ooReal  dvdt = m_engine->propagate( step_size, vel, fmax ) ;

    if( dvdt < 0.0 ) {
        fmax *= -1.0 ;
    }

    if( m_engine->getRatio() < 0.0 ) {
        fmax *= -1.0 ;
    }


    vmax = vel ;


    return fmax ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
void
RayCar::computeRideHeight( ooReal front_ride_height, ooReal rear_ride_height )
{
    PS_ASSERT1( m_suspension_list.size() == NUM_SUSPENSIONS ) ;
    PS_ASSERT1( m_body.valid() ) ;



    osg::Vec3   anchors[NUM_SUSPENSIONS] ;


    for( int i=0; i<NUM_SUSPENSIONS; i++ ) {

        anchors[i] = m_suspension_list[i]->getRelativeRotation() * ( m_suspension_list[ i ]->getRelativePosition() * -1.0 ) ;

        anchors[i] -= m_up_versor * ( m_up_versor * anchors[ i ] ) ;
    }





    osg::Vec3 front_position =  ( anchors[FRONT_RIGHT] + anchors[FRONT_LEFT] ) * 0.5 ;

    osg::Vec3 rear_position =   ( anchors[REAR_RIGHT] + anchors[REAR_LEFT] ) * 0.5 ;



    ooReal  front_distance = front_position * m_front_versor ;

    ooReal  rear_distance = rear_position * m_front_versor ;


    ooReal  ratio = front_distance / ( front_distance - rear_distance ) ;

    ratio = osg::clampTo( ratio, (ooReal) 0.0, (ooReal) 1.0 ) ;


    ooReal  force_front = m_body->getMass() * ratio * 0.5 * 9.81 ;

    ooReal  force_rear = m_body->getMass() * (1.0 - ratio) * 0.5 * 9.81 ;





    ooReal  heights[NUM_SUSPENSIONS] ;

    heights[FRONT_LEFT]     = - 0.4 + m_bottom + front_ride_height + force_front / m_suspension_list[FRONT_LEFT]->getSpring() ;

    heights[FRONT_RIGHT]    = - 0.4 + m_bottom + front_ride_height + force_front / m_suspension_list[FRONT_RIGHT]->getSpring() ;

    heights[REAR_LEFT]      = - 0.4 + m_bottom + rear_ride_height + force_rear / m_suspension_list[REAR_LEFT]->getSpring() ;

    heights[REAR_RIGHT]     = - 0.4 + m_bottom + rear_ride_height + force_rear / m_suspension_list[REAR_RIGHT]->getSpring() ;





    for( int i=0; i<NUM_SUSPENSIONS; i++ ) {

        m_suspension_list[ i ]->setRelativePosition( m_suspension_list[i]->getRelativeRotation().inverse() * (anchors[i] - m_up_versor * heights[i]) * -1.0 ) ;
    }
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
RayWheel*
RayCar::getWheel(SuspensionSelect which)
{
    PS_ASSERT1( m_suspension_list.size() == NUM_SUSPENSIONS ) ;

    return m_suspension_list[which]->getBody2()->asRayWheel() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
const RayWheel*
RayCar::getWheel(SuspensionSelect which) const
{
    PS_ASSERT1( m_suspension_list.size() == NUM_SUSPENSIONS ) ;

    return m_suspension_list[which]->getBody2()->asRayWheel() ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
SliderJoint*
RayCar::getSuspension(SuspensionSelect which)
{
    PS_ASSERT1( m_suspension_list.size() == NUM_SUSPENSIONS ) ;

    return m_suspension_list[which] ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
const SliderJoint*
RayCar::getSuspension(SuspensionSelect which) const
{
    PS_ASSERT1( m_suspension_list.size() == NUM_SUSPENSIONS ) ;

    return m_suspension_list[which] ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
RayCar*
RayCar::asRayCar(void)
{
    return this ;
}
/* ....................................................................... */
/* ======================================================================= */
