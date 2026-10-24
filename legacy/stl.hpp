#ifndef STL_H
#define STL_H

#include <fstream>
#include "Vector3D.hpp"

using namespace std;

class STL : public ofstream {
     public:
       STL(const char name[]);
       void facet(const Vector3D& v1, const Vector3D& v2, const Vector3D& v3);
       ~STL(void);
};

#endif
