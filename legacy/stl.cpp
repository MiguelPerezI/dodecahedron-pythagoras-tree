#include <iostream>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include "Vector3D.hpp"
#include "stl.hpp"

using namespace std;

STL::STL(const char name[]) : ofstream(name)
{
   *this << "solid ESFM\n";
}


void STL::facet(const Vector3D& v1, const Vector3D& v2, const Vector3D& v3)
{
   Vector3D n= unit( (v2-v1) % (v3-v1) );

   *this << "facet normal ";
   *this << std::scientific
         << n.x() << " " << n.y() << " " << n.z() << endl;
   *this << "\touter loop\n"
         << "\t\tvertex " << v1.x() << " " << v1.y() << " " << v1.z() << endl
         << "\t\tvertex " << v2.x() << " " << v2.y() << " " << v2.z() << endl
         << "\t\tvertex " << v3.x() << " " << v3.y() << " " << v3.z() << endl
         << "\tendloop\n"
         << "endfacet\n";
}


STL::~STL(void)
{
   *this << "endsolid ESFM\n";
}


