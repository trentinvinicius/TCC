/*!
 * @file World_serializer.cpp
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
#include <ood/World>

#include <osgDB/Registry>

#include <osg/ValueObject>

#include "real_serializer"
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
struct GetObjectByNameMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.empty()) return false;

        ood::World*     world = reinterpret_cast<ood::World*>( objectPtr ) ;




        osg::Object* stringObject = inputParameters[0].get() ;

        std::string     name ;

        osg::StringValueObject* svo = dynamic_cast<osg::StringValueObject*>( stringObject ) ;

        if( svo ) {
            name = svo->getValue() ;
        }


        ood::ODEObject* oo = world->getObjectByName(name) ;

        outputParameters.push_back( oo ) ;

        return true;
    }
};





struct RemoveObjectMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.empty()) return false;

        ood::World*     world = reinterpret_cast<ood::World*>( objectPtr ) ;




        osg::Object* inparam = inputParameters[0].get() ;

        std::string     name ;

        osg::StringValueObject* svo = dynamic_cast<osg::StringValueObject*>( inparam ) ;

        if( svo ) {
            name = svo->getValue() ;


            ood::ODEObject* oo = world->getObjectByName(name) ;

            if( oo ) {
                world->removeObject( oo ) ;
            }


        } else {
            ood::ODEObject* oo = dynamic_cast<ood::ODEObject*>(inparam) ;

            if( oo ) {
                world->removeObject( oo ) ;
            }
        }



        return true;
    }
};





struct AddObjectMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.empty()) return false;

        ood::World*     world = reinterpret_cast<ood::World*>( objectPtr ) ;




        ood::ODEObject* obj = dynamic_cast<ood::ODEObject*>( inputParameters[0].get() ) ;

        if( ! obj ) {
            return false ;
        }


        world->addObject( obj ) ;

        return true;
    }
};





struct SetGravityMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 1) return false;

        ood::World*     world = reinterpret_cast<ood::World*>( objectPtr ) ;

        osg::Vec3   v3 = dynamic_cast<osg::Vec3dValueObject*>(inputParameters[0].get())->getValue() ;


        world->setGravity( v3 ) ;

        return true;
    }
};





struct SetWorldStepMethod: public osgDB::MethodObject
{
    virtual bool run(void* objectPtr, osg::Parameters& inputParameters, osg::Parameters& outputParameters) const
    {
        if (inputParameters.size() != 1) return false;

        ood::World*     world = reinterpret_cast<ood::World*>( objectPtr ) ;

        std::string     ws = dynamic_cast<osg::StringValueObject*>(inputParameters[0].get())->getValue() ;

        if( ws == "dWorldQuickStep" ) {
            world->setWorldStepFunction(dWorldQuickStep) ;

        } else if( ws == "dWorldStep" ) {
            world->setWorldStepFunction(dWorldStep) ;

        } else {
            return false ;
        }

        return true;
    }
};
/* ....................................................................... */
/* ======================================================================= */









/* ======================================================================= */
/* ....................................................................... */
namespace {
static bool checkGravity(const ood::World& world)
{
    return world.getGravity() != osg::Vec3(0, 0, -9.80665) ;
}

static bool writeGravity(osgDB::OutputStream& os, const ood::World& world)
{
    if( world.getGravity() != osg::Vec3(0, 0, -9.80665) ) {
        os << world.getGravity() << std::endl ;
        return true ;
    }
    return false ;
}

static bool readGravity(osgDB::InputStream& is, ood::World& world)
{
    osg::Vec3   g ;
    is >> g ;
    world.setGravity(g) ;
    return true ;
}


static bool checkWorldStepFunction(const ood::World& world)
{
    (void) world ;

    return true ;
}

static bool writeWorldStepFunction(osgDB::OutputStream& os, const ood::World& world)
{
    ood::World::WorldStepPrototype   ws = world.getWorldStepFunction() ;

    if( ws == dWorldQuickStep ) {
        os << "dWorldQuickStep" << std::endl ;

    } else {
        os << "dWorldStep" << std::endl ;
    }

    return true ;
}

static bool readWorldStepFunction(osgDB::InputStream& is, ood::World& world)
{
    std::string ws ;
    is >> ws ;

    if( ws == "dWorldQuickStep" ) {
        world.setWorldStepFunction(dWorldQuickStep) ;

    } else {
        world.setWorldStepFunction(dWorldStep) ;
    }

    return true ;
}
} // anon namespace
/* ....................................................................... */
/* ======================================================================= */




/* ======================================================================= */
/* ....................................................................... */
REGISTER_OBJECT_WRAPPER( World,
                         new ood::World,
                         ood::World,
                         "osg::Object ood::ODEObject ood::World" )
{
    ADD_UINT_SERIALIZER(CurrentFrame, 0) ;
    ADD_REAL_SERIALIZER(SimulationTime, 0.0) ;
    ADD_USER_SERIALIZER(Gravity) ;
    ADD_VEC3_SERIALIZER(Wind, osg::Vec3()) ;
    ADD_REAL_SERIALIZER(WindFrequency, 0.0) ;
    ADD_REAL_SERIALIZER(AirDensity, 1.2929) ;

    ADD_REAL_SERIALIZER(ERP, 0.2) ;
    ADD_REAL_SERIALIZER(CFM, 1.0e-5) ;

    ADD_INT_SERIALIZER(QuickStepNumIterations, 20) ;
    ADD_REAL_SERIALIZER(QuickStepW, 1.3) ;
    ADD_REAL_SERIALIZER(ContactMaxCorrectingVel, FLT_MAX) ;
    ADD_REAL_SERIALIZER(ContactSurfaceLayer, 0.01) ;

    ADD_USER_SERIALIZER(WorldStepFunction) ;

    ADD_LIST_SERIALIZER(ObjectList, ood::ObjectList) ;

    ADD_OBJECT_SERIALIZER( FrontEventsBuffer, ood::Events, NULL ) ;
    ADD_OBJECT_SERIALIZER( BackEventsBuffer, ood::Events, NULL ) ;




    ADD_METHOD_OBJECT( "getObject",     GetObjectByNameMethod   ) ;
    ADD_METHOD_OBJECT( "addObject",     AddObjectMethod         ) ;
    ADD_METHOD_OBJECT( "removeObject",  RemoveObjectMethod      ) ;
    ADD_METHOD_OBJECT( "setGravity",    SetGravityMethod        ) ;
    ADD_METHOD_OBJECT( "setWorldStep",  SetWorldStepMethod      ) ;
}
/* ....................................................................... */
/* ======================================================================= */
