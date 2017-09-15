/*!
 * @file Vec3Interpolator_serializer.cpp
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

/* ======================================================================= */
/* ....................................................................... */
#include <ood/Interpolator>

#include <osgDB/Registry>

#include <osg/ValueObject>
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
struct GetNumPointsMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {

        ood::Vec3Interpolator*     interpolator = reinterpret_cast<ood::Vec3Interpolator*>( objectPtr ) ;

        osg::IntValueObject*    ivo = new osg::IntValueObject() ;

        ivo->setValue( interpolator->getPointList().size() ) ;

        outputParameters.push_back( ivo ) ;

        return true;
    }
};





struct SetDirtyMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {

        ood::Vec3Interpolator*     interpolator = reinterpret_cast<ood::Vec3Interpolator*>( objectPtr ) ;

        interpolator->setDirty( true ) ;

        return true;
    }
};




struct GetPointTimeMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 1) return false;

        ood::Vec3Interpolator*     interpolator = reinterpret_cast<ood::Vec3Interpolator*>( objectPtr ) ;

        osg::Object* indexObject = inputParameters[0].get();

        unsigned int index = 0;
        osg::DoubleValueObject* dvo = dynamic_cast<osg::DoubleValueObject*>(indexObject);
        if (dvo) index = static_cast<unsigned int>(dvo->getValue());
        else
        {
            osg::UIntValueObject* uivo = dynamic_cast<osg::UIntValueObject*>(indexObject);
            if (uivo) index = uivo->getValue();
        }


        if( index >= interpolator->getPointList().size() ) {
            return false ;
        }


        const ood::Vec3Interpolator::Point&   p = interpolator->getPointList()[index] ;

        osg::DoubleValueObject*  fvo = new osg::DoubleValueObject() ;

        fvo->setValue( p.first ) ;

        outputParameters.push_back( fvo ) ;

        return true;
    }
};




struct GetPointPositionMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 1) return false;

        ood::Vec3Interpolator*     interpolator = reinterpret_cast<ood::Vec3Interpolator*>( objectPtr ) ;

        osg::Object* indexObject = inputParameters[0].get();

        unsigned int index = 0;
        osg::DoubleValueObject* dvo = dynamic_cast<osg::DoubleValueObject*>(indexObject);
        if (dvo) index = static_cast<unsigned int>(dvo->getValue());
        else
        {
            osg::UIntValueObject* uivo = dynamic_cast<osg::UIntValueObject*>(indexObject);
            if (uivo) index = uivo->getValue();
        }


        if( index >= interpolator->getPointList().size() ) {
            return false ;
        }


        const ood::Vec3Interpolator::Point&   p = interpolator->getPointList()[index] ;

        osg::Vec3dValueObject*   vvo = new osg::Vec3dValueObject() ;

        vvo->setValue( p.second ) ;

        outputParameters.push_back( vvo ) ;

        return true;
    }
};




struct SetPointTimeMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 2) return false;

        ood::Vec3Interpolator*     interpolator = reinterpret_cast<ood::Vec3Interpolator*>( objectPtr ) ;

        osg::Object* indexObject = inputParameters[0].get();
        osg::Object* tObject = inputParameters[1].get();

        unsigned int index = 0;
        {
            osg::DoubleValueObject* dvo = dynamic_cast<osg::DoubleValueObject*>(indexObject);
            if (dvo) index = static_cast<unsigned int>(dvo->getValue());
            else
            {
                osg::UIntValueObject* uivo = dynamic_cast<osg::UIntValueObject*>(indexObject);
                if (uivo) index = uivo->getValue();
            }
        }



        float   t = 0.0 ;
        {
            osg::DoubleValueObject* dvo  = dynamic_cast<osg::DoubleValueObject*>(tObject);

            t = dvo->getValue() ;
        }



        if( index >= interpolator->getPointList().size() ) {
            return false ;
        }





        ood::Vec3Interpolator::Point&   p = interpolator->getPointList()[index] ;

        p.first = t ;

        return true;
    }
};




struct SetPointPositionMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 2) return false;

        ood::Vec3Interpolator*     interpolator = reinterpret_cast<ood::Vec3Interpolator*>( objectPtr ) ;

        osg::Object* indexObject = inputParameters[0].get();
        osg::Object* v3Object = inputParameters[1].get();

        unsigned int index = 0;
        {
            osg::DoubleValueObject* dvo = dynamic_cast<osg::DoubleValueObject*>(indexObject);
            if (dvo) index = static_cast<unsigned int>(dvo->getValue());
            else
            {
                osg::UIntValueObject* uivo = dynamic_cast<osg::UIntValueObject*>(indexObject);
                if (uivo) index = uivo->getValue();
            }
        }


        osg::Vec3   v3 ;
        {
            osg::Vec3dValueObject* vvo  = dynamic_cast<osg::Vec3dValueObject*>(v3Object);

            v3 = vvo->getValue() ;
        }


        if( index >= interpolator->getPointList().size() ) {
            return false ;
        }




        ood::Vec3Interpolator::Point&   p = interpolator->getPointList()[index] ;

        p.second = v3 ;

        interpolator->setDirty(true) ;

        return true;
    }
};
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
namespace {
static bool checkPointList(const ood::Vec3Interpolator& interpolator)
{
    return interpolator.getPointList().size() != 0 ;
}

static bool writePointList(osgDB::OutputStream& os, const ood::Vec3Interpolator& interpolator)
{
    const ood::Vec3Interpolator::PointList&  points = interpolator.getPointList() ;
    unsigned int            size = points.size() ;

    if( size > 0 ) {
        os << size << os.BEGIN_BRACKET << std::endl ;

        for(unsigned int i=0; i<size; i++) {
            os << points[i].first << points[i].second << std::endl ;
        }

        os << os.END_BRACKET << std::endl ;
    }

    return true ;
}

static bool readPointList(osgDB::InputStream& is, ood::Vec3Interpolator& interpolator)
{
    unsigned int    size = 0 ;

    is >> size >> is.BEGIN_BRACKET ;

    if( size != 0 ) {
        ood::Vec3Interpolator::PointList points ;

        for(unsigned int i=0; i<size; i++) {

            ooReal      t ;
            osg::Vec3   v ;
            is >> t ;
            is >> v ;

            points.push_back( ood::Vec3Interpolator::Point(t, v) ) ;

        }

        is >> is.END_BRACKET ;

        interpolator.setPointList(points) ;
    }

    return true ;
}
} // anon namespace
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
REGISTER_OBJECT_WRAPPER( Vec3Interpolator,
                         NULL /*new ood::Vec3Interpolator*/,
                         ood::Vec3Interpolator,
                         "osg::Object ood::InterpolatorBase ood::Vec3Interpolator" )
{
    ADD_USER_SERIALIZER(PointList) ;



    ADD_METHOD_OBJECT( "getNumPoints",      GetNumPointsMethod ) ;

    ADD_METHOD_OBJECT( "getPointTime",      GetPointTimeMethod ) ;
    ADD_METHOD_OBJECT( "getPointPosition",  GetPointPositionMethod ) ;

    ADD_METHOD_OBJECT( "setPointTime",      SetPointTimeMethod ) ;
    ADD_METHOD_OBJECT( "setPointPosition",  SetPointPositionMethod ) ;

    ADD_METHOD_OBJECT( "setDirty",          SetDirtyMethod ) ;
}
/* ....................................................................... */
/* ======================================================================= */
