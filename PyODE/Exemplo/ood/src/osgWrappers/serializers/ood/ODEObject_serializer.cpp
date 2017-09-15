/*!
 * @file ODEObject_serializer.cpp
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
#include <ood/ODEObject>

#include <osgDB/Registry>

#include <osg/ValueObject>
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
namespace {

static bool
checkID(const ood::ODEObject& obj)
{
    (void) obj ;
    return true ;
}


static bool
readID(osgDB::InputStream& is, ood::ODEObject& obj)
{
    unsigned int    id ;
    is >> id ;

    obj.setIDInternal(id) ;

    return true ;
}


static bool
writeID(osgDB::OutputStream& os, const ood::ODEObject& obj)
{
    unsigned int    id = obj.getID() ;
    os << id << std::endl ;

    return true ;
}




static bool
checkActorBound(const ood::ODEObject& obj)
{
    return obj.getActorBound().valid() ;
}


static bool
readActorBound(osgDB::InputStream& is, ood::ODEObject& obj)
{
    osg::Vec4   center_and_radius ;

    is >> center_and_radius ;

    obj.setActorBound(
                            osg::BoundingSphere(

                                osg::Vec3(
                                    center_and_radius.x(),
                                    center_and_radius.y(),
                                    center_and_radius.z()
                                ),

                                center_and_radius.w()
                            )
                        ) ;

    return true ;
}


static bool
writeActorBound(osgDB::OutputStream& os, const ood::ODEObject& obj)
{
    const osg::BoundingSphere&  bs = obj.getActorBound() ;
    osg::Vec4   center_and_radius(bs.center(), bs.radius()) ;
    os << center_and_radius << std::endl ;

    return true ;
}





struct SetFloatPropertyMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 2) return false;

        ood::ODEObject* obj = reinterpret_cast<ood::ODEObject*>( objectPtr ) ;


        std::string     ws = dynamic_cast<osg::StringValueObject*>(inputParameters[0].get())->getValue() ;
        float   v = dynamic_cast<osg::DoubleValueObject*>(inputParameters[1].get())->getValue() ;


        obj->setUserValue( ws, v ) ;

        return true;
    }
};





struct GetFloatPropertyMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 1) return false;

        ood::ODEObject* obj = reinterpret_cast<ood::ODEObject*>( objectPtr ) ;


        std::string     ws = dynamic_cast<osg::StringValueObject*>(inputParameters[0].get())->getValue() ;

        float   v = 0.0 ;

        obj->getUserValue( ws, v ) ;

        osg::DoubleValueObject*  fvo = new osg::DoubleValueObject() ;
        fvo->setValue(v) ;

        outputParameters.push_back( fvo ) ;

        return true;
    }
};










struct SetIntPropertyMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 2) return false;


        std::string     ws = dynamic_cast<osg::StringValueObject*>(inputParameters[0].get())->getValue() ;



        ood::ODEObject* obj = reinterpret_cast<ood::ODEObject*>( objectPtr ) ;

        int     v = 0 ;

        osg::IntValueObject*    ivo = dynamic_cast<osg::IntValueObject*>(inputParameters[1].get()) ;

        if( ivo ) {

            v = ivo->getValue() ;

        } else {

            osg::DoubleValueObject*    dvo = dynamic_cast<osg::DoubleValueObject*>(inputParameters[1].get()) ;

            if( dvo ) {
                v = dvo->getValue() ;
            }
        }

        obj->setUserValue( ws, v ) ;

        return true;
    }
};





struct GetIntPropertyMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 1) return false;

        ood::ODEObject* obj = reinterpret_cast<ood::ODEObject*>( objectPtr ) ;


        std::string     ws = dynamic_cast<osg::StringValueObject*>(inputParameters[0].get())->getValue() ;

        int   v = 0 ;

        obj->getUserValue( ws, v ) ;

        osg::IntValueObject*  fvo = new osg::IntValueObject() ;
        fvo->setValue(v) ;

        outputParameters.push_back( fvo ) ;

        return true;
    }
};










struct SetStringPropertyMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 2) return false;

        ood::ODEObject* obj = reinterpret_cast<ood::ODEObject*>( objectPtr ) ;


        std::string     ws = dynamic_cast<osg::StringValueObject*>(inputParameters[0].get())->getValue() ;
        std::string     v = dynamic_cast<osg::StringValueObject*>(inputParameters[1].get())->getValue() ;


        obj->setUserValue( ws, v ) ;

        return true;
    }
};





struct GetStringPropertyMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 1) return false;

        ood::ODEObject* obj = reinterpret_cast<ood::ODEObject*>( objectPtr ) ;


        std::string     ws = dynamic_cast<osg::StringValueObject*>(inputParameters[0].get())->getValue() ;

        std::string     v ;

        obj->getUserValue( ws, v ) ;

        osg::StringValueObject*  svo = new osg::StringValueObject() ;
        svo->setValue(v) ;

        outputParameters.push_back( svo ) ;

        return true;
    }
};

} // anon namespace
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
REGISTER_OBJECT_WRAPPER( ODEObject,
                         new ood::ODEObject,
                         ood::ODEObject,
                         "osg::Object ood::ODEObject" )
{
    ADD_USER_SERIALIZER( ID ) ;
    ADD_OBJECT_SERIALIZER( UpdateCallback, ood::ODECallback, NULL ) ;
    ADD_OBJECT_SERIALIZER( PostUpdateCallback, ood::ODECallback, NULL ) ;
    ADD_OBJECT_SERIALIZER( UserObject, osg::Object, NULL ) ;
    ADD_USER_SERIALIZER( ActorBound ) ;
    ADD_BOOL_SERIALIZER( Actor, false ) ;




    ADD_METHOD_OBJECT( "getFloatProperty", GetFloatPropertyMethod) ;
    ADD_METHOD_OBJECT( "setFloatProperty", SetFloatPropertyMethod) ;

    ADD_METHOD_OBJECT( "getIntProperty", GetIntPropertyMethod) ;
    ADD_METHOD_OBJECT( "setIntProperty", SetIntPropertyMethod) ;

    ADD_METHOD_OBJECT( "getStringProperty", GetStringPropertyMethod) ;
    ADD_METHOD_OBJECT( "setStringProperty", SetStringPropertyMethod) ;
}
/* ....................................................................... */
/* ======================================================================= */
