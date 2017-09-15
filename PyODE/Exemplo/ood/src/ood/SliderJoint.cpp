/*!
 * @file SliderJoint.cpp
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

/* ======================================================================= */
/* ....................................................................... */
#include <ood/SliderJoint>
#include <ood/StaticWorld>
#include <ood/World>
#include <ood/Notify>
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
/* ....................................................................... */
/* ======================================================================= */




using namespace ood ;




/* ======================================================================= */
/* ....................................................................... */
SliderJoint::SliderJoint(void):
    m_stop_mode         ( ERP_CFM ),
    m_spring            ( 1.0 ),
    m_damper_bound      ( 0.0 ),
    m_damper_rebound    ( 0.0 ),
    m_preload           ( 0.0 )
{
    m_ODE_joint = dJointCreateSlider(StaticWorld::instance()->getODEWorld(), NULL) ;

    dJointSetData( m_ODE_joint, this ) ;

    m_functions.SetAxis1    = dJointSetSliderAxis ;
    m_functions.GetAxis1    = dJointGetSliderAxis ;

    m_functions.SetParam    = dJointSetSliderParam ;
    m_functions.GetParam    = dJointGetSliderParam ;


    setRelativePosition( osg::Vec3() ) ;
    setRelativeRotation( osg::Quat() ) ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
SliderJoint::SliderJoint(const SliderJoint& other, const osg::CopyOp& copyop):
    Joint               ( other, copyop ),
    m_stop_mode         ( other.m_stop_mode ),
    m_spring            ( other.m_spring ),
    m_damper_bound      ( other.m_damper_bound ),
    m_damper_rebound    ( other.m_damper_rebound ),
    m_preload           ( other.m_preload )
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
SliderJoint::~SliderJoint(void)
{
    if(m_ODE_joint) {
        dJointDestroy(m_ODE_joint) ;
    }
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
void
SliderJoint::update( ooReal step_size )
{
    if( m_stop_mode == SPRING_DAMPER ) {

        // apply the preload
        const ooReal        load = m_preload - getOrCreateJointFeedback()->getF1().normalize() ;


        if( load > 0.0 ) {

            RigidBody*  body1 = getBody1() ;
            RigidBody*  body2 = getBody2() ;

            PS_ASSERT1( body1 != NULL ) ;
            PS_ASSERT1( body2 != NULL ) ;

            const osg::Vec3 PL = this->getAxis1() * load ;

            const osg::Vec3 pos = body2->getPosition() ;

            body1->addForce( -PL, pos, false, false ) ;

            body2->addForce(  PL, pos, false, false ) ;

        }




        const ooReal    damper = getPositionRate(AXIS1) < 0.0 ? m_damper_rebound : m_damper_bound ;


        ooReal  K1 = step_size * m_spring ;
        ooReal  K2 = K1 + damper ;
        ooReal  ERP = K1 / K2 ;
        ooReal  CFM = 1.0 / K2 ;

        setParam( dParamStopERP1, ERP ) ;
        setParam( dParamStopCFM1, CFM ) ;

    }



    this->Joint::update( step_size ) ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
SliderJoint*
SliderJoint::asSliderJoint(void)
{
    return this ;
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
dJointID
SliderJoint::cloneODEJoint(dWorldID world) const
{
    PS_DBG2("ood::SliderJoint::cloneODEJoint(%p, world=%p)", this, world) ;

    dJointID    j = dJointCreateSlider(world, NULL) ;

    if(dJointIsEnabled(m_ODE_joint)) {
        dJointEnable(j) ;
    } else {
        dJointDisable(j) ;
    }

    dJointSetFeedback(j, dJointGetFeedback(m_ODE_joint)) ;




    {
        dVector3    v ;
        dJointGetSliderAxis(m_ODE_joint, v) ;
        dJointSetSliderAxis(j, v[0], v[1], v[2]) ;
    }


    {
        dVector3        prel ;
        dQuaternion     qrel ;

        dJointSetSliderAutoComputeRelativeValues( j,      dJointGetSliderAutoComputeRelativeValues(m_ODE_joint) ) ;

        dJointGetSliderRelativeRotation( m_ODE_joint, qrel ) ;
        dJointGetSliderRelativePosition( m_ODE_joint, prel ) ;

        dJointSetSliderRelativeRotation( j, qrel ) ;
        dJointSetSliderRelativePosition( j, prel ) ;
    }



    return j ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
ooReal
SliderJoint::getPosition( Axis a ) const
{
    if( a == AXIS1  ) {
        return dJointGetSliderPosition(m_ODE_joint) ;
    }


    return 0.0 ;
}



ooReal
SliderJoint::getPositionRate( Axis a ) const
{
    if( a == AXIS1  ) {
        return dJointGetSliderPositionRate(m_ODE_joint) ;
    }


    return 0.0 ;
}
/* ....................................................................... */
/* ======================================================================= */
