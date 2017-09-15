/*!
 * @file Calendar.inl
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

#ifndef _OOD_CALENDAR_INL
#define _OOD_CALENDAR_INL




// Inline methods - do not edit this line




/* ======================================================================= */
// East
/* ....................................................................... */
inline void
ood::Calendar::setEast( const osg::Vec3& east)
{
    m_east = east ;
}




inline osg::Vec3&
ood::Calendar::getEast(void)
{
    return m_east ;
}




inline const osg::Vec3&
ood::Calendar::getEast(void) const
{
    return m_east ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// North
/* ....................................................................... */
inline void
ood::Calendar::setNorth( const osg::Vec3& north)
{
    m_north = north ;
}




inline osg::Vec3&
ood::Calendar::getNorth(void)
{
    return m_north ;
}




inline const osg::Vec3&
ood::Calendar::getNorth(void) const
{
    return m_north ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// Latitude
/* ....................................................................... */
inline void
ood::Calendar::setLatitude( ooReal latitude)
{
    m_latitude = latitude ;
}




inline ooReal
ood::Calendar::getLatitude(void) const
{
    return m_latitude ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// AxisInclination
/* ....................................................................... */
inline void
ood::Calendar::setAxisInclination( ooReal axis_inclination)
{
    m_axis_inclination = axis_inclination ;
}




inline ooReal
ood::Calendar::getAxisInclination(void) const
{
    return m_axis_inclination ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// Time
/* ....................................................................... */
inline void
ood::Calendar::setTime( ooReal time)
{
    m_time = time ;
}




inline ooReal
ood::Calendar::getTime(void) const
{
    return m_time ;
}
/* ....................................................................... */
/* ======================================================================= */






/* ======================================================================= */
// TemporalProgression
/* ....................................................................... */
inline void
ood::Calendar::setTemporalProgression( ooReal temporal_progression)
{
    m_temporal_progression = temporal_progression ;
}




inline ooReal
ood::Calendar::getTemporalProgression(void) const
{
    return m_temporal_progression ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// SecondsInMinute
/* ....................................................................... */
inline void
ood::Calendar::setSecondsInMinute( unsigned int seconds_in_minute)
{
    m_seconds_in_minute = seconds_in_minute ;
}




inline unsigned int
ood::Calendar::getSecondsInMinute(void) const
{
    return m_seconds_in_minute ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// MinutesInHour
/* ....................................................................... */
inline void
ood::Calendar::setMinutesInHour( unsigned int minutes_in_hour)
{
    m_minutes_in_hour = minutes_in_hour ;
}




inline unsigned int
ood::Calendar::getMinutesInHour(void) const
{
    return m_minutes_in_hour ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// HoursInDay
/* ....................................................................... */
inline void
ood::Calendar::setHoursInDay( unsigned int hours_in_day)
{
    m_hours_in_day = hours_in_day ;
}




inline unsigned int
ood::Calendar::getHoursInDay(void) const
{
    return m_hours_in_day ;
}
/* ....................................................................... */
/* ======================================================================= */





/* ======================================================================= */
// DaysInYear
/* ....................................................................... */
inline void
ood::Calendar::setDaysInYear( unsigned int days_in_year)
{
    m_days_in_year = days_in_year ;
}




inline unsigned int
ood::Calendar::getDaysInYear(void) const
{
    return m_days_in_year ;
}
/* ....................................................................... */
/* ======================================================================= */







#endif /* _OOD_CALENDAR_INL */
