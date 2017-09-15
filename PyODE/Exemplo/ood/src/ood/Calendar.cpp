/*!
 * @file Calendar.cpp
 * @author Rocco Martino
 */
/***************************************************************************
 *   Copyright (C) 2017 by Rocco Martino                                   *
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
#include <ood/Calendar>
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
Calendar::Calendar(void)
    : m_east                    ( osg::X_AXIS )
    , m_north                   ( osg::Y_AXIS )
    , m_latitude                ( osg::inDegrees(35.0 + 31.0/60.0) )
    , m_axis_inclination        ( osg::inDegrees(23.0 + 27.0/60.0) )
    , m_time                    ( 0.0 )
    , m_temporal_progression    ( 1.0 )
    , m_seconds_in_minute       ( 60 )
    , m_minutes_in_hour         ( 60 )
    , m_hours_in_day            ( 24 )
    , m_days_in_year            ( 365 )
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
Calendar::Calendar(const Calendar& other, const osg::CopyOp& copyop)
    : OObject                   ( other, copyop )
    , m_east                    ( other.m_east )
    , m_north                   ( other.m_north )
    , m_latitude                ( other.m_latitude )
    , m_axis_inclination        ( other.m_axis_inclination )
    , m_time                    ( other.m_time )
    , m_temporal_progression    ( other.m_temporal_progression )
    , m_seconds_in_minute       ( other.m_seconds_in_minute )
    , m_minutes_in_hour         ( other.m_minutes_in_hour )
    , m_hours_in_day            ( other.m_hours_in_day )
    , m_days_in_year            ( other.m_days_in_year )
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
Calendar::~Calendar(void)
{
}
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
void
Calendar::update(ooReal step_size)
{
    m_time += step_size * m_temporal_progression ;

    this->OObject::update(step_size) ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
void
Calendar::computeDate( ooReal time,
                       unsigned int& day,
                       unsigned int& hour,
                       unsigned int& minute,
                       unsigned int& second
                     )
{
    PS_ASSERT1( time >= 0.0 ) ;


    // should cache this
    unsigned int    seconds_in_year = m_days_in_year * m_hours_in_day * m_seconds_in_minute * m_minutes_in_hour ;
    unsigned int    seconds_in_day = m_hours_in_day * m_seconds_in_minute * m_minutes_in_hour ;
    unsigned int    seconds_in_hour = m_seconds_in_minute * m_minutes_in_hour ;


    unsigned int    t = (unsigned int) time  %  seconds_in_year ;


    day = t / seconds_in_day ;

    hour = (t % seconds_in_day) / seconds_in_hour ;

    minute = ( (t % seconds_in_day) % seconds_in_hour ) / m_seconds_in_minute ;

    second = t % m_seconds_in_minute ;
}
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
void
Calendar::computeSunPosition( ooReal time, osg::Vec3& dir )
{
    PS_ASSERT1( time >= 0.0 ) ;



    unsigned int    seconds_in_year = m_days_in_year * m_hours_in_day * m_seconds_in_minute * m_minutes_in_hour ;
    unsigned int    seconds_in_day = m_hours_in_day * m_seconds_in_minute * m_minutes_in_hour ;

    unsigned int    tmp = (unsigned int) time  %  seconds_in_year ;


    ooReal  rot = 2.0 * osg::PI * (ooReal)(tmp % seconds_in_day) / (ooReal) seconds_in_day ;

    ooReal  rev = 2.0 * osg::PI * (ooReal)(tmp) / (ooReal) seconds_in_year ;


    osg::Quat   q ;


    // latitude
    q = osg::Quat( m_latitude, m_east ) ;

    // rotate back to compensate the revolution
    q = q * osg::Quat( rev, m_north ) ;

    // inclination
    q = q * osg::Quat( m_axis_inclination, m_east ) ;

    // revolution
    q = q * osg::Quat( -rev, m_north ) ;


    // now it's noon, rotate to current time

    q = osg::Quat( osg::PI - rot, m_north ) * q ;


    dir = q * (m_east ^ m_north) ;

    dir.normalize() ;
}
/* ....................................................................... */
/* ======================================================================= */



