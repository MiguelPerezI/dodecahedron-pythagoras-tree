#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include "stl.hpp"
#include "Vector3D.hpp"
#include "Matrix3D.hpp"


using namespace std;


class Torus : public STL {
     public:
	Torus(const char nombre[]);
	void Draw1(   
	             double x1, double x2, double x3, 
                 double x4, double x5, double x6,
                 double x7, double x8, double x9,
				 double x10, double x11, double x12,
				 double x13, double x14, double x15, 
                 double x16, double x17, double x18,
                 double x19, double x20, double x21,
				 double x22, double x23, double x24,
				 double x25, double x26, double x27, 
                 double x28, double x29, double x30,
                 double x31, double x32, double x33,
				 double x34, double x35, double x36,
				 double x37, double x38, double x39,
				 double x40, double x41, double x42,
				 double x43, double x44, double x45,
				 double x46, double x47, double x48,
				 double x49, double x50, double x51,
				 double x52, double x53, double x54,
				 double x55, double x56, double x57,
				 double x58, double x59, double x60,
				 double   r, double   angle,  int n,
				  double  d1, double  d2, double d3
				    
				  );
	 void Draw2(   
	             double x1, double x2, double x3, 
                 double x4, double x5, double x6,
                 double x7, double x8, double x9,
				 double x10, double x11, double x12,
				 double x13, double x14, double x15, 
                 double x16, double x17, double x18,
                 double x19, double x20, double x21,
				 double x22, double x23, double x24,
				 double x25, double x26, double x27, 
                 double x28, double x29, double x30,
                 double x31, double x32, double x33,
				 double x34, double x35, double x36,
				 double x37, double x38, double x39,
				 double x40, double x41, double x42,
				 double x43, double x44, double x45,
				 double x46, double x47, double x48,
				 double x49, double x50, double x51,
				 double x52, double x53, double x54,
				 double x55, double x56, double x57,
				 double x58, double x59, double x60,
				 double   r, double   angle,  int n,
				  double  d1, double  d2, double d3
				     
				  ); 
	 
	 void Draw3(   
	             double x1, double x2, double x3, 
                 double x4, double x5, double x6,
                 double x7, double x8, double x9,
				 double x10, double x11, double x12,
				 double x13, double x14, double x15,
				 double x16, double x17, double x18,
				 double x19, double x20, double x21,
				 double x22, double x23, double x24,
				 double   r, double   angle,  int n    
				  );			  
	 
	 
	 void Draw4(   
	             double x1, double x2, double x3, 
                 double x4, double x5, double x6,
                 double x7, double x8, double x9,
				 double x10, double x11, double x12,
				 double x13, double x14, double x15,
				 double x16, double x17, double x18,
				 double x19, double x20, double x21,
				 double x22, double x23, double x24,
				 double   r, double   angle,  int n    
				  );			  
};


Torus::Torus(const char nombre[]) : STL(nombre)
{
}

void Torus::Draw1(
                 double x1, double x2, double x3, 
                 double x4, double x5, double x6,
                 double x7, double x8, double x9,
				 double x10, double x11, double x12,
				 double x13, double x14, double x15, 
                 double x16, double x17, double x18,
                 double x19, double x20, double x21,
				 double x22, double x23, double x24,
				 double x25, double x26, double x27, 
                 double x28, double x29, double x30,
                 double x31, double x32, double x33,
				 double x34, double x35, double x36,
				 double x37, double x38, double x39,
				 double x40, double x41, double x42,
				 double x43, double x44, double x45,
				 double x46, double x47, double x48,
				 double x49, double x50, double x51,
				 double x52, double x53, double x54,
				 double x55, double x56, double x57,
				 double x58, double x59, double x60,
				 double   r, double   angle, int n,
				 double  d1, double  d2, double d3
				 
                 )
{ 
     Vector3D I, J, K;
     I = Vector3D(
	                  1.0, 
	                  0.0,  
		              0.0
				 );
	 
	 J = Vector3D(
	                  0.0, 
	                  1.0,  
		              0.0
				 );			 
     
     K = Vector3D(
	                  0.0, 
	                  0.0,  
		              1.0
				 );
   
	Vector3D v[20] = {
         Vector3D( x1, x2, x3 ),//0
         Vector3D( x4, x5, x6 ),//1
         Vector3D( x7, x8, x9 ),//2
         Vector3D( x10, x11, x12 ),//3
         Vector3D( x13, x14, x15 ),//4
         Vector3D( x16, x17, x18 ),//5
         Vector3D( x19, x20, x21 ),//6
         Vector3D( x22, x23, x24 ),//7
         Vector3D( x25, x26, x27 ),//8
         Vector3D( x28, x29, x30 ),//9
         Vector3D( x31, x32, x33 ),//10
         Vector3D( x34, x35, x36 ),//11
         Vector3D( x37, x38, x39 ),//12
         Vector3D( x40, x41, x42 ),//13
         Vector3D( x43, x44, x45 ),//14
         Vector3D( x46, x47, x48 ),//15
         Vector3D( x49, x50, x51 ),//16
         Vector3D( x52, x53, x54 ),//17
         Vector3D( x55, x56, x57 ),//18
         Vector3D( x58, x59, x60 )
         
         
     };
     
     double gold = (1 + sqrt(2)) / 2;
     
     double g = gold * 0.36;
     double d = gold * 1.125;
     double ROx = 4.0;
     double ROy = 4.0;
     double ROz = 4.0;
     
     Vector3D w[20] = {
          Vector3D( x1, x2, x3 ),//0
         Vector3D( x4, x5, x6 ),//1
         Vector3D( x7, x8, x9 ),//2
         Vector3D( x10, x11, x12 ),//3
         Vector3D( x13, x14, x15 ),//4
         Vector3D( x16, x17, x18 ),//5
         Vector3D( x19, x20, x21 ),//6
         Vector3D( x22, x23, x24 ),//7
         Vector3D( x25, x26, x27 ),//8
         Vector3D( x28, x29, x30 ),//9
         Vector3D( x31, x32, x33 ),//10
         Vector3D( x34, x35, x36 ),//11
         Vector3D( x37, x38, x39 ),//12
         Vector3D( x40, x41, x42 ),//13
         Vector3D( x43, x44, x45 ),//14
         Vector3D( x46, x47, x48 ),//15
         Vector3D( x49, x50, x51 ),//16
         Vector3D( x52, x53, x54 ),//17
         Vector3D( x55, x56, x57 ),//18
         Vector3D( x58, x59, x60 )
        
         };
         
         
         Vector3D u[20] = {
          Vector3D( x1, x2, x3 ),//0
         Vector3D( x4, x5, x6 ),//1
         Vector3D( x7, x8, x9 ),//2
         Vector3D( x10, x11, x12 ),//3
         Vector3D( x13, x14, x15 ),//4
         Vector3D( x16, x17, x18 ),//5
         Vector3D( x19, x20, x21 ),//6
         Vector3D( x22, x23, x24 ),//7
         Vector3D( x25, x26, x27 ),//8
         Vector3D( x28, x29, x30 ),//9
         Vector3D( x31, x32, x33 ),//10
         Vector3D( x34, x35, x36 ),//11
         Vector3D( x37, x38, x39 ),//12
         Vector3D( x40, x41, x42 ),//13
         Vector3D( x43, x44, x45 ),//14
         Vector3D( x46, x47, x48 ),//15
         Vector3D( x49, x50, x51 ),//16
         Vector3D( x52, x53, x54 ),//17
         Vector3D( x55, x56, x57 ),//18
         Vector3D( x58, x59, x60 )
        
         };
         
         Vector3D u1[20] = {
          Vector3D( x1, x2, x3 ),//0
         Vector3D( x4, x5, x6 ),//1
         Vector3D( x7, x8, x9 ),//2
         Vector3D( x10, x11, x12 ),//3
         Vector3D( x13, x14, x15 ),//4
         Vector3D( x16, x17, x18 ),//5
         Vector3D( x19, x20, x21 ),//6
         Vector3D( x22, x23, x24 ),//7
         Vector3D( x25, x26, x27 ),//8
         Vector3D( x28, x29, x30 ),//9
         Vector3D( x31, x32, x33 ),//10
         Vector3D( x34, x35, x36 ),//11
         Vector3D( x37, x38, x39 ),//12
         Vector3D( x40, x41, x42 ),//13
         Vector3D( x43, x44, x45 ),//14
         Vector3D( x46, x47, x48 ),//15
         Vector3D( x49, x50, x51 ),//16
         Vector3D( x52, x53, x54 ),//17
         Vector3D( x55, x56, x57 ),//18
         Vector3D( x58, x59, x60 )
        
         };
         
         Vector3D u2[20] = {
          Vector3D( x1, x2, x3 ),//0
         Vector3D( x4, x5, x6 ),//1
         Vector3D( x7, x8, x9 ),//2
         Vector3D( x10, x11, x12 ),//3
         Vector3D( x13, x14, x15 ),//4
         Vector3D( x16, x17, x18 ),//5
         Vector3D( x19, x20, x21 ),//6
         Vector3D( x22, x23, x24 ),//7
         Vector3D( x25, x26, x27 ),//8
         Vector3D( x28, x29, x30 ),//9
         Vector3D( x31, x32, x33 ),//10
         Vector3D( x34, x35, x36 ),//11
         Vector3D( x37, x38, x39 ),//12
         Vector3D( x40, x41, x42 ),//13
         Vector3D( x43, x44, x45 ),//14
         Vector3D( x46, x47, x48 ),//15
         Vector3D( x49, x50, x51 ),//16
         Vector3D( x52, x53, x54 ),//17
         Vector3D( x55, x56, x57 ),//18
         Vector3D( x58, x59, x60 )
        
         };
     	
     double x = r * cos(angle);
	 double y = r * sin(angle);
if( n == 0)
{

     facet(v[9], v[15], v[14]);
     facet(v[8], v[9], v[14]);
     facet(v[13], v[8], v[14]);
    
	
     facet(v[1], v[7], v[5]);
     facet(v[0], v[1], v[5]);
     facet(v[6], v[0], v[5]);
     
     facet(v[12], v[8], v[13]);
     facet(v[16], v[12], v[13]);
     facet(v[19], v[16], v[13]);
     
     facet(v[17], v[18], v[7]);
     facet(v[2], v[17], v[7]);
     facet(v[1], v[2], v[7]);
     
	 facet(v[18], v[17], v[15]);
     facet(v[10], v[18], v[15]);
     facet(v[9], v[10], v[15]);
     
	 facet(v[4], v[0], v[6]);
     facet(v[19], v[4], v[6]);
     facet(v[16], v[19], v[6]);
     
     facet(v[11], v[10], v[9]);
     facet(v[12], v[11], v[9]);
     facet(v[8], v[12], v[9]);
     
	 facet(v[2], v[1], v[0]);
     facet(v[3], v[2], v[0]);
     facet(v[4], v[3], v[0]);
     
     facet(v[11], v[12], v[16]);
     facet(v[5], v[11], v[16]);
     facet(v[6], v[5], v[16]);
     
     facet(v[14], v[15], v[17]);
     facet(v[3], v[14], v[17]);
     facet(v[2], v[3], v[17]);
     
	 facet(v[7], v[18], v[10]);
     facet(v[5], v[7], v[10]);
     facet(v[11], v[5], v[10]);
     
     facet(v[14], v[3], v[4]);
     facet(v[13], v[14], v[4]);
     facet(v[19], v[13], v[4]);
}
else
{
     facet(v[9], v[15], v[14]);
     facet(v[8], v[9], v[14]);
     facet(v[13], v[8], v[14]);
    
	
     facet(v[1], v[7], v[5]);
     facet(v[0], v[1], v[5]);
     facet(v[6], v[0], v[5]);
     
     facet(v[12], v[8], v[13]);
     facet(v[16], v[12], v[13]);
     facet(v[19], v[16], v[13]);
     
     facet(v[17], v[18], v[7]);
     facet(v[2], v[17], v[7]);
     facet(v[1], v[2], v[7]);
     
	 facet(v[18], v[17], v[15]);
     facet(v[10], v[18], v[15]);
     facet(v[9], v[10], v[15]);
     
	 facet(v[4], v[0], v[6]);
     facet(v[19], v[4], v[6]);
     facet(v[16], v[19], v[6]);
     
     facet(v[11], v[10], v[9]);
     facet(v[12], v[11], v[9]);
     facet(v[8], v[12], v[9]);
     
	 facet(v[2], v[1], v[0]);
     facet(v[3], v[2], v[0]);
     facet(v[4], v[3], v[0]);
     
     facet(v[11], v[12], v[16]);
     facet(v[5], v[11], v[16]);
     facet(v[6], v[5], v[16]);
     
     facet(v[14], v[15], v[17]);
     facet(v[3], v[14], v[17]);
     facet(v[2], v[3], v[17]);
     
	 facet(v[7], v[18], v[10]);
     facet(v[5], v[7], v[10]);
     facet(v[11], v[5], v[10]);
     
     facet(v[14], v[3], v[4]);
     facet(v[13], v[14], v[4]);
     facet(v[19], v[13], v[4]);
     
     for(double k = 0.0; k <= 0.0; ++k )
     {
	 
     Matrix3D R = Matrix3D('x', 3.1415926535 * (1.0 / ROx) )*
	              Matrix3D('y', 3.1415926535 * (0.0 / ROy)) *
				  Matrix3D('z', 3.1415926535 * (0.0 / ROz));
     Vector3D p;
      p = Vector3D(
	                  0.0, 
	                  0.0,  
		              1.0 * d
				 );
     
     for (int k=0; k<20; ++k)
	 v[k]= R*v[k];
	 
	 for (int k=0; k<20; ++k)
	 v[k]= operator * ( g, v[k]);
     
     for (int k=0; k<20; ++k)
     v[k] = operator + (v[k], p);
    
     Draw1(
                 v[0].x(), v[0].y(), v[0].z(), 
                 v[1].x(), v[1].y(), v[1].z(),
                 v[2].x(), v[2].y(), v[2].z(),
				 v[3].x(), v[3].y(), v[3].z(),
				 v[4].x(), v[4].y(), v[4].z(),
				 v[5].x(), v[5].y(), v[5].z(),
				 v[6].x(), v[6].y(), v[6].z(),
				 v[7].x(), v[7].y(), v[7].z(),
				 v[8].x(), v[8].y(), v[8].z(),
				 v[9].x(), v[9].y(), v[9].z(),
				 v[10].x(), v[10].y(), v[10].z(),
				 v[11].x(), v[11].y(), v[11].z(),
				 v[12].x(), v[12].y(), v[12].z(),
				 v[13].x(), v[13].y(), v[13].z(),
				 v[14].x(), v[14].y(), v[14].z(),
				 v[15].x(), v[15].y(), v[15].z(),
				 v[16].x(), v[16].y(), v[16].z(),
				 v[17].x(), v[17].y(), v[17].z(),
				 v[18].x(), v[18].y(), v[18].z(),
				 v[19].x(), v[19].y(), v[19].z(),
				        r,    angle,       n-1,
				        d1 , d2, d3
				 
                 );
                 
     facet(w[9], w[15], w[14]);
     facet(w[8], w[9], w[14]);
     facet(w[13], w[8], w[14]);
    
	
     facet(w[1], w[7], w[5]);
     facet(w[0], w[1], w[5]);
     facet(w[6], w[0], w[5]);
     
     facet(w[12], w[8], w[13]);
     facet(w[16], w[12], w[13]);
     facet(w[19], w[16], w[13]);
     
     facet(w[17], w[18], w[7]);
     facet(w[2], w[17], w[7]);
     facet(w[1], w[2], w[7]);
     
	 facet(w[18], w[17], w[15]);
     facet(w[10], w[18], w[15]);
     facet(w[9], w[10], w[15]);
     
	 facet(w[4], w[0], w[6]);
     facet(w[19], w[4], w[6]);
     facet(w[16], w[19], w[6]);
     
     facet(w[11], w[10], w[9]);
     facet(w[12], w[11], w[9]);
     facet(w[8], w[12], w[9]);
     
	 facet(w[2], w[1], w[0]);
     facet(w[3], w[2], w[0]);
     facet(w[4], w[3], w[0]);
     
     facet(w[11],w[12], w[16]);
     facet(w[5], w[11], w[16]);
     facet(w[6], w[5], w[16]);
     
     facet(w[14],w[15], w[17]);
     facet(w[3], w[14], w[17]);
     facet(w[2], w[3], w[17]);
     
	 facet(w[7], w[18], w[10]);
     facet(w[5], w[7], w[10]);
     facet(w[11], w[5], w[10]);
     
     facet(w[14], w[3], w[4]);
     facet(w[13], w[14], w[4]);
     facet(w[19], w[13], w[4]);
    //   d = 0.45 *gold;
     
      p = Vector3D(
	                  -0.5 * d, ////////Q1
	                  0.31 * d,  
		              0.81 * d
				 );
     
     Vector3D h[2] = {
	                   Vector3D(-0.24, 0.62, 0.0),//proyXYp
	                   Vector3D(-0.24, 0.62,-0.38),//palanca
	                   
	                 };
	 
     /////coordenadas esfericas de p
     //ángulo phi
     double P_pro_p_k = operator * ( h[0], I);
     double abs_I = abs(I);
     double abs_pro_p = abs(h[0]);
     double phi = acos( (P_pro_p_k) / ( abs_pro_p * abs_I) );
     
    //ángulo teta
    
     double P_p_k = operator * ( h[1], -K);
     double abs_K = abs(K);
     double abs_p = abs(h[1]);
     double teta = acos( (P_p_k) / ( abs_p * abs_K) );
     
     Matrix3D Rz_phi1 = Matrix3D('x', 0.0 )*
	                    Matrix3D('y', 0.0 ) *
				        Matrix3D('z', phi);
				        
     Matrix3D Ry_teta1 = Matrix3D('x', 0.0 ) *
	                    Matrix3D('y', teta ) *
				        Matrix3D('z',  0.0);
				       // ROx = 4.0;
	 Matrix3D R_alpha = Matrix3D('x', 3.1415926535 * (0.0 / ROx) )*
	                    Matrix3D('y', 3.1415926535 * (0.0 / ROy) ) *
				        Matrix3D('z', 3.1415926535 * (1.0 / ROz) );	
						        
     Matrix3D Ry_teta2 = Matrix3D('x', 0.0  )*
	                     Matrix3D('y',-teta ) *
				         Matrix3D('z', 0.0);  
						    
	 Matrix3D Rz_phi2 = Matrix3D('x', 0.0 )*
	                    Matrix3D('y', 0.0 ) *
				        Matrix3D('z', -phi);	        
    
     for (int k=0; k<20; ++k)
	 w[k]= (Rz_phi1) *
	       (Ry_teta1) *
		      R_alpha *
		   (Ry_teta2) *
		    (Rz_phi2) *     
		          w[k];
	 
	 for (int k=0; k<20; ++k)
	 w[k]= operator * (g, w[k]);
     
     for (int k=0; k<20; ++k)
     w[k] = operator + (w[k], p);
     
     Draw1(
                 w[0].x(), w[0].y(), w[0].z(), 
                 w[1].x(), w[1].y(), w[1].z(),
                 w[2].x(), w[2].y(), w[2].z(),
				 w[3].x(), w[3].y(), w[3].z(),
				 w[4].x(), w[4].y(), w[4].z(),
				 w[5].x(), w[5].y(), w[5].z(),
				 w[6].x(), w[6].y(), w[6].z(),
				 w[7].x(), w[7].y(), w[7].z(),
				 w[8].x(), w[8].y(), w[8].z(),
				 w[9].x(), w[9].y(), w[9].z(),
				 w[10].x(), w[10].y(), w[10].z(),
				 w[11].x(), w[11].y(), w[11].z(),
				 w[12].x(), w[12].y(), w[12].z(),
				 w[13].x(), w[13].y(), w[13].z(),
				 w[14].x(), w[14].y(), w[14].z(),
				 w[15].x(), w[15].y(), w[15].z(),
				 w[16].x(), w[16].y(), w[16].z(),
				 w[17].x(), w[17].y(), w[17].z(),
				 w[18].x(), w[18].y(), w[18].z(),
				 w[19].x(), w[19].y(), w[19].z(),
				        r,    angle,       n-1,
				 d1, d2, d3
                 );       
                 
                 
     
	 
	 
	           
     facet(u[9], u[15],u[14]);
     facet(u[8], u[9], u[14]);
     facet(u[13],u[8], u[14]);
    
	
     facet(u[1], u[7], u[5]);
     facet(u[0], u[1], u[5]);
     facet(u[6], u[0], u[5]);
     
     facet(u[12],u[8], u[13]);
     facet(u[16],u[12],u[13]);
     facet(u[19],u[16],u[13]);
     
     facet(u[17],u[18],u[7]);
     facet(u[2], u[17],u[7]);
     facet(u[1], u[2], u[7]);
     
	 facet(u[18],u[17],u[15]);
     facet(u[10],u[18],u[15]);
     facet(u[9], u[10],u[15]);
     
	 facet(u[4], u[0], u[6]);
     facet(u[19],u[4], u[6]);
     facet(u[16],u[19],u[6]);
     
     facet(u[11],u[10],u[9]);
     facet(u[12],u[11],u[9]);
     facet(u[8], u[12],u[9]);
    
	 facet(u[2], u[1], u[0]);
     facet(u[3], u[2], u[0]);
     facet(u[4], u[3], u[0]);
    
     facet(u[11],u[12],u[16]);
     facet(u[5], u[11],u[16]);
     facet(u[6], u[5], u[16]);
    
     facet(u[14],u[15],u[17]);
     facet(u[3], u[14],u[17]);
     facet(u[2], u[3], u[17]);
     
	 facet(u[7], u[18],u[10]);
     facet(u[5], u[7], u[10]);
     facet(u[11],u[5], u[10]);
     
     facet(u[14],u[3], u[4]);
     facet(u[13],u[14],u[4]);
     facet(u[19],u[13],u[4]);
       d = gold *1.125;
     
      p = Vector3D(
	                  -0.31 * d, ///Q2
	                  0.81 * d,  
		              0.5 * d
				 );
	  
	  Vector3D m[2] = {
	                   Vector3D( 0.62, 0.38, 0.0),//proyXYp
	                   Vector3D( 0.62, 0.38,-0.24),//palanca
	                   
	                 };
				 
     /////coordenadas esfericas de p
     //ángulo phi
     P_pro_p_k = operator * ( m[0], I);
     abs_I = abs(I);
     abs_pro_p = abs(m[0]);
     phi = acos( (P_pro_p_k) / ( abs_pro_p * abs_I) );
     
    //ángulo teta
    
     P_p_k = operator * ( m[1], -K);
     abs_K = abs(K);
     abs_p = abs(m[1]);
     teta = acos( (P_p_k) / ( abs_p * abs_K) );
     
    
     Rz_phi1 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y', 0.0 ) *
				        Matrix3D('z', phi);
				        
     Ry_teta1 =         Matrix3D('x', 0.0 )*
	                    Matrix3D('y', teta)*
				        Matrix3D('z', 0.0);
				        ROz = 4.0;
	  R_alpha =   Matrix3D('x', 3.1415926535 * (0.0 / ROx) )*
	              Matrix3D('y', 3.1415926535 * (0.0 / ROy)) *
				  Matrix3D('z', 3.1415926535 * (1.0 / ROz));
				  	        
     Ry_teta2 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y',-teta ) *
				        Matrix3D('z', 0.0);     
				        
	 Rz_phi2 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y', 0.0 ) *
				        Matrix3D('z', -phi);	        
    
     for (int k=0; k<20; ++k)
	 u[k]=  (Rz_phi1) *
	       (Ry_teta1) *
		      R_alpha *
		   (Ry_teta2) *
		    (Rz_phi2) *     
		          u[k];
	 
	 for (int k=0; k<20; ++k)
	 u[k]= operator * (g, u[k]);
     
     for (int k=0; k<20; ++k)
     u[k] = operator + (u[k], p);
    
     Draw1(
                 u[0].x(), u[0].y(), u[0].z(), 
                 u[1].x(), u[1].y(), u[1].z(),
                 u[2].x(), u[2].y(), u[2].z(),
				 u[3].x(), u[3].y(), u[3].z(),
				 u[4].x(), u[4].y(), u[4].z(),
				 u[5].x(), u[5].y(), u[5].z(),
				 u[6].x(), u[6].y(), u[6].z(),
				 u[7].x(), u[7].y(), u[7].z(),
				 u[8].x(), u[8].y(), u[8].z(),
				 u[9].x(), u[9].y(), u[9].z(),
				 u[10].x(), u[10].y(), u[10].z(),
				 u[11].x(), u[11].y(), u[11].z(),
				 u[12].x(), u[12].y(), u[12].z(),
				 u[13].x(), u[13].y(), u[13].z(),
				 u[14].x(), u[14].y(), u[14].z(),
				 u[15].x(), u[15].y(), u[15].z(),
				 u[16].x(), u[16].y(), u[16].z(),
				 u[17].x(), u[17].y(), u[17].z(),
				 u[18].x(), u[18].y(), u[18].z(),
				 u[19].x(), u[19].y(), u[19].z(),
				        r,    angle,       n-1,
				 d1, d2, d3
                 );        
       
	           
     facet(u1[9], u1[15],u1[14]);
     facet(u1[8], u1[9], u1[14]);
     facet(u1[13],u1[8], u1[14]);
    
	
     facet(u1[1], u1[7], u1[5]);
     facet(u1[0], u1[1], u1[5]);
     facet(u1[6], u1[0], u1[5]);
     
     facet(u1[12],u1[8], u1[13]);
     facet(u1[16], u1[12],u1[13]);
     facet(u1[19],u1[16],u1[13]);
     
     facet(u1[17],u1[18],u1[7]);
     facet(u1[2], u1[17],u1[7]);
     facet(u1[1], u1[2], u1[7]);
     
	 facet(u1[18],u1[17],u1[15]);
     facet(u1[10],u1[18],u1[15]);
     facet(u1[9], u1[10],u1[15]);
     
	 facet(u1[4], u1[0], u1[6]);
     facet(u1[19],u1[4], u1[6]);
     facet(u1[16],u1[19],u1[6]);
     
     facet(u1[11],u1[10],u1[9]);
     facet(u1[12],u1[11],u1[9]);
     facet(u1[8], u1[12],u1[9]);
    
	 facet(u1[2], u1[1], u1[0]);
     facet(u1[3], u1[2], u1[0]);
     facet(u1[4], u1[3], u1[0]);
    
     facet(u1[11],u1[12],u1[16]);
     facet(u1[5], u1[11],u1[16]);
     facet(u1[6], u1[5], u1[16]);
    
     facet(u1[14],u1[15],u1[17]);
     facet(u1[3], u1[14],u1[17]);
     facet(u1[2], u1[3], u1[17]);
     
	 facet(u1[7], u1[18],u1[10]);
     facet(u1[5], u1[7], u1[10]);
     facet(u1[11],u1[5], u1[10]);
     
     facet(u1[14],u1[3], u1[4]);
     facet(u1[13],u1[14],u1[4]);
     facet(u1[19],u1[13],u1[4]);
       d = gold *1.125;
     
      p = Vector3D(
	                  0.31 * d, ///Q3
	                  0.81 * d,  
		              0.5 * d
				 );
	  
	  Vector3D m1[2] = {
	                   Vector3D( -0.62,0.38, 0.0),//proyXYp
	                   Vector3D( -0.62,0.38,-0.24),//palanca
	                   
	                 };
				 
     /////coordenadas esfericas de p
     //ángulo phi
     P_pro_p_k = operator * ( m1[0], I);
     abs_I = abs(I);
     abs_pro_p = abs(m1[0]);
     phi = acos( (P_pro_p_k) / ( abs_pro_p * abs_I) );
     
    //ángulo teta
    
     P_p_k = operator * ( m1[1], -K);
     abs_K = abs(K);
     abs_p = abs(m1[1]);
     teta = acos( (P_p_k) / ( abs_p * abs_K) );
     
    
     Rz_phi1 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y', 0.0 ) *
				        Matrix3D('z', phi);
				        
     Ry_teta1 =         Matrix3D('x', 0.0 )*
	                    Matrix3D('y', teta)*
				        Matrix3D('z', 0.0);
				        ROz = 4.0;
	  R_alpha =   Matrix3D('x', 3.1415926535 * (0.0 / ROx) )*
	              Matrix3D('y', 3.1415926535 * (0.0 / ROy)) *
				  Matrix3D('z', 3.1415926535 * (-1.0 / ROz));
				  	        
     Ry_teta2 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y',-teta ) *
				        Matrix3D('z', 0.0);     
				        
	 Rz_phi2 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y', 0.0 ) *
				        Matrix3D('z', -phi);	        
    
     for (int k=0; k<20; ++k)
	 u1[k]=  (Rz_phi1) *
	       (Ry_teta1) *
		      R_alpha *
		   (Ry_teta2) *
		    (Rz_phi2) *     
		          u1[k];
	 
	 for (int k=0; k<20; ++k)
	 u1[k]= operator * (g, u1[k]);
     
     for (int k=0; k<20; ++k)
     u1[k] = operator + (u1[k], p);
    
     Draw1(
                 u1[0].x(), u1[0].y(), u1[0].z(), 
                 u1[1].x(), u1[1].y(), u1[1].z(),
                 u1[2].x(), u1[2].y(), u1[2].z(),
				 u1[3].x(), u1[3].y(), u1[3].z(),
				 u1[4].x(), u1[4].y(), u1[4].z(),
				 u1[5].x(), u1[5].y(), u1[5].z(),
				 u1[6].x(), u1[6].y(), u1[6].z(),
				 u1[7].x(), u1[7].y(), u1[7].z(),
				 u1[8].x(), u1[8].y(), u1[8].z(),
				 u1[9].x(), u1[9].y(), u1[9].z(),
				 u1[10].x(), u1[10].y(), u1[10].z(),
				 u1[11].x(), u1[11].y(), u1[11].z(),
				 u1[12].x(), u1[12].y(), u1[12].z(),
				 u1[13].x(), u1[13].y(), u1[13].z(),
				 u1[14].x(), u1[14].y(), u1[14].z(),
				 u1[15].x(), u1[15].y(), u1[15].z(),
				 u1[16].x(), u1[16].y(), u1[16].z(),
				 u1[17].x(), u1[17].y(), u1[17].z(),
				 u1[18].x(), u1[18].y(), u1[18].z(),
				 u1[19].x(), u1[19].y(), u1[19].z(),
				        r,    angle,       n-1,
				 d1, d2, d3
                 );    
	 
	 
	 
	           
     facet(u2[9], u2[15],u2[14]);
     facet(u2[8], u2[9], u2[14]);
     facet(u2[13],u2[8], u2[14]);
    
	
     facet(u2[1], u2[7], u2[5]);
     facet(u2[0], u2[1], u2[5]);
     facet(u2[6], u2[0], u2[5]);
     
     facet(u2[12],u2[8], u2[13]);
     facet(u2[16],u2[12],u2[13]);
     facet(u2[19],u2[16],u2[13]);
     
     facet(u2[17],u2[18],u2[7]);
     facet(u2[2], u2[17],u2[7]);
     facet(u2[1], u2[2], u2[7]);
     
	 facet(u2[18],u2[17],u2[15]);
     facet(u2[10],u2[18],u2[15]);
     facet(u2[9], u2[10],u2[15]);
     
	 facet(u2[4], u2[0], u2[6]);
     facet(u2[19],u2[4], u2[6]);
     facet(u2[16],u2[19],u2[6]);
     
     facet(u2[11],u2[10],u2[9]);
     facet(u2[12],u2[11],u2[9]);
     facet(u2[8], u2[12],u2[9]);
    
	 facet(u2[2], u2[1], u2[0]);
     facet(u2[3], u2[2], u2[0]);
     facet(u2[4], u2[3], u2[0]);
    
     facet(u2[11],u2[12],u2[16]);
     facet(u2[5], u2[11],u2[16]);
     facet(u2[6], u2[5], u2[16]);
    
     facet(u2[14],u2[15],u2[17]);
     facet(u2[3], u2[14],u2[17]);
     facet(u2[2], u2[3], u2[17]);
     
	 facet(u2[7], u2[18],u2[10]);
     facet(u2[5], u2[7], u2[10]);
     facet(u2[11],u2[5], u2[10]);
    
     facet(u2[14],u2[3], u2[4]);
     facet(u2[13],u2[14],u2[4]);
     facet(u2[19],u2[13],u2[4]);
       d = gold *1.125;
     
      p = Vector3D(
	                  0.5 * d, ///Q3
	                  0.31 * d,  
		              0.81 * d
				 );
	  
	  Vector3D m2[2] = {
	                   Vector3D( 0.24,0.62, 0.0),//proyXYp
	                   Vector3D( 0.24,0.62,-0.38),//palanca
	                   
	                 };
				 
     /////coordenadas esfericas de p
     //ángulo phi
     P_pro_p_k = operator * ( m2[0], I);
     abs_I = abs(I);
     abs_pro_p = abs(m2[0]);
     phi = acos( (P_pro_p_k) / ( abs_pro_p * abs_I) );
     
    //ángulo teta
    
     P_p_k = operator * ( m2[1], -K);
     abs_K = abs(K);
     abs_p = abs(m2[1]);
     teta = acos( (P_p_k) / ( abs_p * abs_K) );
     
    
     Rz_phi1 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y', 0.0 ) *
				        Matrix3D('z', phi);
				        
     Ry_teta1 =         Matrix3D('x', 0.0 )*
	                    Matrix3D('y', teta)*
				        Matrix3D('z', 0.0);
				        ROz = 4.0;
	  R_alpha =   Matrix3D('x', 3.1415926535 * (0.0 / ROx) )*
	              Matrix3D('y', 3.1415926535 * (0.0 / ROy)) *
				  Matrix3D('z', 3.1415926535 * (-1.0 / ROz));
				  	        
     Ry_teta2 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y',-teta ) *
				        Matrix3D('z', 0.0);     
				        
	 Rz_phi2 =          Matrix3D('x', 0.0 )*
	                    Matrix3D('y', 0.0 ) *
				        Matrix3D('z', -phi);	        
    
     for (int k=0; k<20; ++k)
	 u2[k]=  (Rz_phi1) *
	       (Ry_teta1) *
		      R_alpha *
		   (Ry_teta2) *
		    (Rz_phi2) *     
		          u2[k];
	 
	 for (int k=0; k<20; ++k)
	 u2[k]= operator * (g, u2[k]);
     
     for (int k=0; k<20; ++k)
     u2[k] = operator + (u2[k], p);
    
     Draw1(
                 u2[0].x(), u2[0].y(), u2[0].z(), 
                 u2[1].x(), u2[1].y(), u2[1].z(),
                 u2[2].x(), u2[2].y(), u2[2].z(),
				 u2[3].x(), u2[3].y(), u2[3].z(),
				 u2[4].x(), u2[4].y(), u2[4].z(),
				 u2[5].x(), u2[5].y(), u2[5].z(),
				 u2[6].x(), u2[6].y(), u2[6].z(),
				 u2[7].x(), u2[7].y(), u2[7].z(),
				 u2[8].x(), u2[8].y(), u2[8].z(),
				 u2[9].x(), u2[9].y(), u2[9].z(),
				 u2[10].x(), u2[10].y(), u2[10].z(),
				 u2[11].x(), u2[11].y(), u2[11].z(),
				 u2[12].x(), u2[12].y(), u2[12].z(),
				 u2[13].x(), u2[13].y(), u2[13].z(),
				 u2[14].x(), u2[14].y(), u2[14].z(),
				 u2[15].x(), u2[15].y(), u2[15].z(),
				 u2[16].x(), u2[16].y(), u2[16].z(),
				 u2[17].x(), u2[17].y(), u2[17].z(),
				 u2[18].x(), u2[18].y(), u2[18].z(),
				 u2[19].x(), u2[19].y(), u2[19].z(),
				        r,    angle,       n-1,
				 d1, d2, d3
                 );    
	                      
 }
     
}
     
     
 
	 
	 

}






void Torus::Draw2(
                 double x1, double x2, double x3, 
                 double x4, double x5, double x6,
                 double x7, double x8, double x9,
				 double x10, double x11, double x12,
				 double x13, double x14, double x15, 
                 double x16, double x17, double x18,
                 double x19, double x20, double x21,
				 double x22, double x23, double x24,
				 double x25, double x26, double x27, 
                 double x28, double x29, double x30,
                 double x31, double x32, double x33,
				 double x34, double x35, double x36,
				 double x37, double x38, double x39,
				 double x40, double x41, double x42,
				 double x43, double x44, double x45,
				 double x46, double x47, double x48,
				 double x49, double x50, double x51,
				 double x52, double x53, double x54,
				 double x55, double x56, double x57,
				 double x58, double x59, double x60,
				 double   r, double   angle, int n,
				 double  d1, double  d2, double d3
				 
                 )
                 {
	Vector3D v[20] = {
         Vector3D( x1, x2, x3 ),//0
         Vector3D( x4, x5, x6 ),//1
         Vector3D( x7, x8, x9 ),//2
         Vector3D( x10, x11, x12 ),//3
         Vector3D( x13, x14, x15 ),//4
         Vector3D( x16, x17, x18 ),//5
         Vector3D( x19, x20, x21 ),//6
         Vector3D( x22, x23, x24 ),//7
         Vector3D( x25, x26, x27 ),//8
         Vector3D( x28, x29, x30 ),//9
         Vector3D( x31, x32, x33 ),//10
         Vector3D( x34, x35, x36 ),//11
         Vector3D( x37, x38, x39 ),//12
         Vector3D( x40, x41, x42 ),//13
         Vector3D( x43, x44, x45 ),//14
         Vector3D( x46, x47, x48 ),//15
         Vector3D( x49, x50, x51 ),//16
         Vector3D( x52, x53, x54 ),//17
         Vector3D( x55, x56, x57 ),//18
         Vector3D( x58, x59, x60 )
         
         
     };
     
     double gold = (1 + sqrt(2)) / 2;
     
     double g = gold * 0.5;
     double d = gold * 1.25;
     
     Vector3D w[20] = {
          Vector3D( x1, x2, x3 ),//0
         Vector3D( x4, x5, x6 ),//1
         Vector3D( x7, x8, x9 ),//2
         Vector3D( x10, x11, x12 ),//3
         Vector3D( x13, x14, x15 ),//4
         Vector3D( x16, x17, x18 ),//5
         Vector3D( x19, x20, x21 ),//6
         Vector3D( x22, x23, x24 ),//7
         Vector3D( x25, x26, x27 ),//8
         Vector3D( x28, x29, x30 ),//9
         Vector3D( x31, x32, x33 ),//10
         Vector3D( x34, x35, x36 ),//11
         Vector3D( x37, x38, x39 ),//12
         Vector3D( x40, x41, x42 ),//13
         Vector3D( x43, x44, x45 ),//14
         Vector3D( x46, x47, x48 ),//15
         Vector3D( x49, x50, x51 ),//16
         Vector3D( x52, x53, x54 ),//17
         Vector3D( x55, x56, x57 ),//18
         Vector3D( x58, x59, x60 )
        
         };
     	
     double x = r * cos(angle);
	 double y = r * sin(angle);
if( n == 0)
{

     facet(v[9], v[15], v[14]);
     facet(v[8], v[9], v[14]);
     facet(v[13], v[8], v[14]);
    
	
     facet(v[1], v[7], v[5]);
     facet(v[0], v[1], v[5]);
     facet(v[6], v[0], v[5]);
     
     facet(v[12], v[8], v[13]);
     facet(v[16], v[12], v[13]);
     facet(v[19], v[16], v[13]);
     
     facet(v[17], v[18], v[7]);
     facet(v[2], v[17], v[7]);
     facet(v[1], v[2], v[7]);
     
	 facet(v[18], v[17], v[15]);
     facet(v[10], v[18], v[15]);
     facet(v[9], v[10], v[15]);
     
	 facet(v[4], v[0], v[6]);
     facet(v[19], v[4], v[6]);
     facet(v[16], v[19], v[6]);
     
     facet(v[11], v[10], v[9]);
     facet(v[12], v[11], v[9]);
     facet(v[8], v[12], v[9]);
     
	 facet(v[2], v[1], v[0]);
     facet(v[3], v[2], v[0]);
     facet(v[4], v[3], v[0]);
     
     facet(v[11], v[12], v[16]);
     facet(v[5], v[11], v[16]);
     facet(v[6], v[5], v[16]);
     
     facet(v[14], v[15], v[17]);
     facet(v[3], v[14], v[17]);
     facet(v[2], v[3], v[17]);
     
	 facet(v[7], v[18], v[10]);
     facet(v[5], v[7], v[10]);
     facet(v[11], v[5], v[10]);
     
     facet(v[14], v[3], v[4]);
     facet(v[13], v[14], v[4]);
     facet(v[19], v[13], v[4]);
}
else
{
     facet(v[9], v[15], v[14]);
     facet(v[8], v[9], v[14]);
     facet(v[13], v[8], v[14]);
    
	
     facet(v[1], v[7], v[5]);
     facet(v[0], v[1], v[5]);
     facet(v[6], v[0], v[5]);
     
     facet(v[12], v[8], v[13]);
     facet(v[16], v[12], v[13]);
     facet(v[19], v[16], v[13]);
     
     facet(v[17], v[18], v[7]);
     facet(v[2], v[17], v[7]);
     facet(v[1], v[2], v[7]);
     
	 facet(v[18], v[17], v[15]);
     facet(v[10], v[18], v[15]);
     facet(v[9], v[10], v[15]);
     
	 facet(v[4], v[0], v[6]);
     facet(v[19], v[4], v[6]);
     facet(v[16], v[19], v[6]);
     
     facet(v[11], v[10], v[9]);
     facet(v[12], v[11], v[9]);
     facet(v[8], v[12], v[9]);
     
	 facet(v[2], v[1], v[0]);
     facet(v[3], v[2], v[0]);
     facet(v[4], v[3], v[0]);
     
     facet(v[11], v[12], v[16]);
     facet(v[5], v[11], v[16]);
     facet(v[6], v[5], v[16]);
     
     facet(v[14], v[15], v[17]);
     facet(v[3], v[14], v[17]);
     facet(v[2], v[3], v[17]);
     
	 facet(v[7], v[18], v[10]);
     facet(v[5], v[7], v[10]);
     facet(v[11], v[5], v[10]);
     
     facet(v[14], v[3], v[4]);
     facet(v[13], v[14], v[4]);
     facet(v[19], v[13], v[4]);
     
     for(double k = 0.0; k <= 0.0; ++k )
     {
	 
     Matrix3D R = Matrix3D('x', 3.1415926535 * (0.0 / 4.0) )*
	              Matrix3D('y', 3.1415926535 * (1.0 / 4.0)) *
				  Matrix3D('z', 3.1415926535 * (0.0 / 4.0));
     Vector3D p;
      p = Vector3D(
	                  1.0 * d, 
	                  0.0,  
		              0.0
				 );
     
     for (int k=0; k<20; ++k)
	 v[k]= R*v[k];
	 
	 for (int k=0; k<20; ++k)
	 v[k]= operator * ( g, v[k]);
     
     for (int k=0; k<20; ++k)
     v[k] = operator + (v[k], p);
     
     /*Draw2(
                 v[0].x(), v[0].y(), v[0].z(), 
                 v[1].x(), v[1].y(), v[1].z(),
                 v[2].x(), v[2].y(), v[2].z(),
				 v[3].x(), v[3].y(), v[3].z(),
				 v[4].x(), v[4].y(), v[4].z(),
				 v[5].x(), v[5].y(), v[5].z(),
				 v[6].x(), v[6].y(), v[6].z(),
				 v[7].x(), v[7].y(), v[7].z(),
				 v[8].x(), v[8].y(), v[8].z(),
				 v[9].x(), v[9].y(), v[9].z(),
				 v[10].x(), v[10].y(), v[10].z(),
				 v[11].x(), v[11].y(), v[11].z(),
				 v[12].x(), v[12].y(), v[12].z(),
				 v[13].x(), v[13].y(), v[13].z(),
				 v[14].x(), v[14].y(), v[14].z(),
				 v[15].x(), v[15].y(), v[15].z(),
				 v[16].x(), v[16].y(), v[16].z(),
				 v[17].x(), v[17].y(), v[17].z(),
				 v[18].x(), v[18].y(), v[18].z(),
				 v[19].x(), v[19].y(), v[19].z(),
				        r,    angle,       n-1,
				        d1 , d2, d3
				 
                 );*/
                 
     facet(w[9], w[15], w[14]);
     facet(w[8], w[9], w[14]);
     facet(w[13], w[8], w[14]);
    
	
     facet(w[1], w[7], w[5]);
     facet(w[0], w[1], w[5]);
     facet(w[6], w[0], w[5]);
     
     facet(w[12], w[8], w[13]);
     facet(w[16], w[12], w[13]);
     facet(w[19], w[16], w[13]);
     
     facet(w[17], w[18], w[7]);
     facet(w[2], w[17], w[7]);
     facet(w[1], w[2], w[7]);
     
	 facet(w[18], w[17], w[15]);
     facet(w[10], w[18], w[15]);
     facet(w[9], w[10], w[15]);
     
	 facet(w[4], w[0], w[6]);
     facet(w[19], w[4], w[6]);
     facet(w[16], w[19], w[6]);
     
     facet(w[11], w[10], w[9]);
     facet(w[12], w[11], w[9]);
     facet(w[8], w[12], w[9]);
     
	 facet(w[2], w[1], w[0]);
     facet(w[3], w[2], w[0]);
     facet(w[4], w[3], w[0]);
     
     facet(w[11],w[12], w[16]);
     facet(w[5], w[11], w[16]);
     facet(w[6], w[5], w[16]);
     
     facet(w[14],w[15], w[17]);
     facet(w[3], w[14], w[17]);
     facet(w[2], w[3], w[17]);
     
	 facet(w[7], w[18], w[10]);
     facet(w[5], w[7], w[10]);
     facet(w[11], w[5], w[10]);
     
     facet(w[14], w[3], w[4]);
     facet(w[13], w[14], w[4]);
     facet(w[19], w[13], w[4]);
       d = gold *1.05;
          R = Matrix3D('x', 3.1415926535 * (0.0 / 4.0) )*
	              Matrix3D('y', 3.1415926535 * (1.0 / 4.0)) *
				  Matrix3D('z', 3.1415926535 * (0.0 / 5.0));
     
      p = Vector3D(
	                  -1.0 * gold * 1.25, 
	                  0.0,  
		              0.0
				 );
     
     for (int k=0; k<20; ++k)
	 w[k]= R*w[k];
	 
	 for (int k=0; k<20; ++k)
	 w[k]= operator * (g, w[k]);
     
     for (int k=0; k<20; ++k)
     w[k] = operator + (w[k], p);
     
    /* Draw2(
                 w[0].x(), w[0].y(), w[0].z(), 
                 w[1].x(), w[1].y(), w[1].z(),
                 w[2].x(), w[2].y(), w[2].z(),
				 w[3].x(), w[3].y(), w[3].z(),
				 w[4].x(), w[4].y(), w[4].z(),
				 w[5].x(), w[5].y(), w[5].z(),
				 w[6].x(), w[6].y(), w[6].z(),
				 w[7].x(), w[7].y(), w[7].z(),
				 w[8].x(), w[8].y(), w[8].z(),
				 w[9].x(), w[9].y(), w[9].z(),
				 w[10].x(), w[10].y(), w[10].z(),
				 w[11].x(), w[11].y(), w[11].z(),
				 w[12].x(), w[12].y(), w[12].z(),
				 w[13].x(), w[13].y(), w[13].z(),
				 w[14].x(), w[14].y(), w[14].z(),
				 w[15].x(), w[15].y(), w[15].z(),
				 w[16].x(), w[16].y(), w[16].z(),
				 w[17].x(), w[17].y(), w[17].z(),
				 w[18].x(), w[18].y(), w[18].z(),
				 w[19].x(), w[19].y(), w[19].z(),
				        r,    angle,       n-1,
				 d1, d2, d3
                 );  */      
                 
                 
                          
 }
     
}
     
     
 
	 
	 

	 

                 	
				 }
               
			   
			   
	
void Torus::Draw3(
                 double x1, double x2, double x3, 
                 double x4, double x5, double x6,
                 double x7, double x8, double x9,
				 double x10, double x11, double x12,
				 double x13, double x14, double x15,
				 double x16, double x17, double x18,
				 double x19, double x20, double x21,
				 double x22, double x23, double x24,
				 double   r, double   angle, int n
				 
                 )
{ 
   double d = 1.0;
	Vector3D v[8] = {
         Vector3D( x1, x2 * d, x3 ),//0
         Vector3D( x4, x5 * d , x6 ),//1
         Vector3D( x7, x8 * d, x9 ),//2
         Vector3D( x10, x11 * d, x12 ),//3
         Vector3D( x13, x14 * d, x15 ),
         Vector3D( x16, x17 * d, x18 ),
         Vector3D( x19, x20 * d, x21 ),
         Vector3D( x22, x23 * d, x24 )
         
         
     };
     
     //cout<<v[0].x()<<endl<<v[0].y()<<endl<<v[0].z();
     
     
     Vector3D w[8] = {
         Vector3D( x1, x2 * d, x3 ),//0
         Vector3D( x4, x5 * d , x6 ),//1
         Vector3D( x7, x8 * d, x9 ),//2
         Vector3D( x10, x11 * d, x12 ),//3
         Vector3D( x13, x14 * d, x15 ),
         Vector3D( x16, x17 * d, x18 ),
         Vector3D( x19, x20 * d, x21 ),
         Vector3D( x22, x23 * d, x24 )
        
         };
     	
     double x = r * cos(angle);
	 double y = r * sin(angle);
if( n == 0)
{

     facet(v[2], v[0], v[1]); 
     facet(v[1], v[3], v[2]);
     
     facet(v[6], v[2], v[3]);
     facet(v[3], v[7], v[6]);
     
     facet(v[4], v[6], v[5]);
     facet(v[5], v[6], v[7]);
     
     facet(v[0], v[4], v[1]);
     facet(v[4], v[5], v[1]);
     
     facet(v[0], v[2], v[4]);
     facet(v[4], v[2], v[6]);
     
     facet(v[1], v[5], v[3]);
     facet(v[3], v[5], v[7]);
     
     
     facet(w[2], w[0], w[1]); 
     facet(w[1], w[3], w[2]);
     
     facet(w[6], w[2], w[3]);
     facet(w[3], w[7], w[6]);
     
     facet(w[4], w[6], w[5]);
     facet(w[5], w[6], w[7]);
     
     facet(w[0], w[4], w[1]);
     facet(w[4], w[5], w[1]);
     
     facet(w[0], w[2], w[4]);
     facet(w[4], w[2], w[6]);
     
     facet(w[1], w[5], w[3]);
     facet(w[3], w[5], w[7]);
}
else
{
     facet(v[2], v[0], v[1]); 
     facet(v[1], v[3], v[2]);
     
     facet(v[6], v[2], v[3]);
     facet(v[3], v[7], v[6]);
     
     facet(v[4], v[6], v[5]);
     facet(v[5], v[6], v[7]);
     
     facet(v[0], v[4], v[1]);
     facet(v[4], v[5], v[1]);
     
     facet(v[0], v[2], v[4]);
     facet(v[4], v[2], v[6]);
     
     facet(v[1], v[5], v[3]);
     facet(v[3], v[5], v[7]);
     
     for(double k = 0.0; k <= 0.0; ++k )
     {
	 
     Matrix3D R = Matrix3D('x', 0.0) * Matrix3D('y', 0.0) * Matrix3D('z', angle);
     Vector3D p;
      p = Vector3D(
	               -r*0.5, 
	                  ((2.0* (x*0.5*sqrt(2))) - ((x*0.5*sqrt(2)) - (x * 0.7)) ),  
					 0.0
				 );
     
     for (int k=0; k<8; ++k)
	 v[k]= R*v[k];
	 
	 for (int k=0; k<8; ++k)
	 v[k]= operator * (x, v[k]);
     
     for (int k=0; k<8; ++k)
     v[k] = operator + (v[k], p);
     
     Draw3(
                 v[0].x(), v[0].y(), v[0].z(), 
                 v[1].x(), v[1].y(), v[1].z(),
                 v[2].x(), v[2].y(), v[2].z(),
				 v[3].x(), v[3].y(), v[3].z(),
				 v[4].x(), v[4].y(), v[4].z(),
				 v[5].x(), v[5].y(), v[5].z(),
				 v[6].x(), v[6].y(), v[6].z(),
				 v[7].x(), v[7].y(), v[7].z(),
				        r,    angle,       n-1
				 
                 );
                 
      facet(w[2], w[0], w[1]); 
     facet(w[1], w[3], w[2]);
     
     facet(w[6], w[2], w[3]);
     facet(w[3], w[7], w[6]);
     
     facet(w[4], w[6], w[5]);
     facet(w[5], w[6], w[7]);
     
     facet(w[0], w[4], w[1]);
     facet(w[4], w[5], w[1]);
     
     facet(w[0], w[2], w[4]);
     facet(w[4], w[2], w[6]);
     
     facet(w[1], w[5], w[3]);
     facet(w[3], w[5], w[7]);           
       
       R = Matrix3D('x', 0.0) * Matrix3D('y', 0.0) * Matrix3D('z', -angle);
       
      p = Vector3D(
	               r*0.5, 
	                 ( (2.0* (y*0.5*sqrt(2))) - ((y*0.5*sqrt(2)) - (y * 0.7)) ),  
					0.0
				 );
     
     for (int k=0; k<8; ++k)
	 w[k]= R*w[k];
	 
	 for (int k=0; k<8; ++k)
	 w[k]= operator * (y, w[k]);
     
     for (int k=0; k<8; ++k)
     w[k] = operator + (w[k], p);
     
     Draw3(
                 w[0].x(), w[0].y(), w[0].z(), 
                 w[1].x(), w[1].y(), w[1].z(),
                 w[2].x(), w[2].y(), w[2].z(),
				 w[3].x(), w[3].y(), w[3].z(),
				 w[4].x(), w[4].y(), w[4].z(),
				 w[5].x(), w[5].y(), w[5].z(),
				 w[6].x(), w[6].y(), w[6].z(),
				 w[7].x(), w[7].y(), w[7].z(),
				        r,    angle,       n-1
				 
                 );          
                 
                 
                          
 }
     
}
     
     
 
	 
	 

}

		     
                 
	
void Torus::Draw4(
                 double x1, double x2, double x3, 
                 double x4, double x5, double x6,
                 double x7, double x8, double x9,
				 double x10, double x11, double x12,
				 double x13, double x14, double x15,
				 double x16, double x17, double x18,
				 double x19, double x20, double x21,
				 double x22, double x23, double x24,
				 double   r, double   angle, int n
				 
                 )
{ 
   double d = 1.0;
	Vector3D v[8] = {
         Vector3D( x1, x2 * d, x3 ),//0
         Vector3D( x4, x5 * d , x6 ),//1
         Vector3D( x7, x8 * d, x9 ),//2
         Vector3D( x10, x11 * d, x12 ),//3
         Vector3D( x13, x14 * d, x15 ),
         Vector3D( x16, x17 * d, x18 ),
         Vector3D( x19, x20 * d, x21 ),
         Vector3D( x22, x23 * d, x24 )
         
         
     };
     
     //cout<<v[0].x()<<endl<<v[0].y()<<endl<<v[0].z();
     
     
     Vector3D w[8] = {
         Vector3D( x1, x2 * d, x3 ),//0
         Vector3D( x4, x5 * d , x6 ),//1
         Vector3D( x7, x8 * d, x9 ),//2
         Vector3D( x10, x11 * d, x12 ),//3
         Vector3D( x13, x14 * d, x15 ),
         Vector3D( x16, x17 * d, x18 ),
         Vector3D( x19, x20 * d, x21 ),
         Vector3D( x22, x23 * d, x24 )
        
         };
     	
     double x = r * cos(angle);
	 double y = r * sin(angle);
if( n == 0)
{

     facet(v[2], v[0], v[1]); 
     facet(v[1], v[3], v[2]);
     
     facet(v[6], v[2], v[3]);
     facet(v[3], v[7], v[6]);
     
     facet(v[4], v[6], v[5]);
     facet(v[5], v[6], v[7]);
     
     facet(v[0], v[4], v[1]);
     facet(v[4], v[5], v[1]);
     
     facet(v[0], v[2], v[4]);
     facet(v[4], v[2], v[6]);
     
     facet(v[1], v[5], v[3]);
     facet(v[3], v[5], v[7]);
     
     
     facet(w[2], w[0], w[1]); 
     facet(w[1], w[3], w[2]);
     
     facet(w[6], w[2], w[3]);
     facet(w[3], w[7], w[6]);
     
     facet(w[4], w[6], w[5]);
     facet(w[5], w[6], w[7]);
     
     facet(w[0], w[4], w[1]);
     facet(w[4], w[5], w[1]);
     
     facet(w[0], w[2], w[4]);
     facet(w[4], w[2], w[6]);
     
     facet(w[1], w[5], w[3]);
     facet(w[3], w[5], w[7]);
}
else
{
     facet(v[2], v[0], v[1]); 
     facet(v[1], v[3], v[2]);
     
     facet(v[6], v[2], v[3]);
     facet(v[3], v[7], v[6]);
     
     facet(v[4], v[6], v[5]);
     facet(v[5], v[6], v[7]);
     
     facet(v[0], v[4], v[1]);
     facet(v[4], v[5], v[1]);
     
     facet(v[0], v[2], v[4]);
     facet(v[4], v[2], v[6]);
     
     facet(v[1], v[5], v[3]);
     facet(v[3], v[5], v[7]);
     
     for(double k = 0.0; k <= 0.0; ++k )
     {
	 
     Matrix3D R = Matrix3D('x', 0.0) * Matrix3D('y', 0.0) * Matrix3D('z', angle);
     Vector3D p;
      p = Vector3D(
	               r*0.5, 
	                  -((2.0* (x*0.5*sqrt(2))) - ((x*0.5*sqrt(2)) - (x * 0.7)) ),  
					 0.0
				 );
     
     for (int k=0; k<8; ++k)
	 v[k]= R*v[k];
	 
	 for (int k=0; k<8; ++k)
	 v[k]= operator * (x, v[k]);
     
     for (int k=0; k<8; ++k)
     v[k] = operator + (v[k], p);
     
     Draw4(
                 v[0].x(), v[0].y(), v[0].z(), 
                 v[1].x(), v[1].y(), v[1].z(),
                 v[2].x(), v[2].y(), v[2].z(),
				 v[3].x(), v[3].y(), v[3].z(),
				 v[4].x(), v[4].y(), v[4].z(),
				 v[5].x(), v[5].y(), v[5].z(),
				 v[6].x(), v[6].y(), v[6].z(),
				 v[7].x(), v[7].y(), v[7].z(),
				        r,    angle,       n-1
				 
                 );
                 
      facet(w[2], w[0], w[1]); 
     facet(w[1], w[3], w[2]);
     
     facet(w[6], w[2], w[3]);
     facet(w[3], w[7], w[6]);
     
     facet(w[4], w[6], w[5]);
     facet(w[5], w[6], w[7]);
     
     facet(w[0], w[4], w[1]);
     facet(w[4], w[5], w[1]);
     
     facet(w[0], w[2], w[4]);
     facet(w[4], w[2], w[6]);
     
     facet(w[1], w[5], w[3]);
     facet(w[3], w[5], w[7]);           
       
       R = Matrix3D('x', 0.0) * Matrix3D('y', 0.0) * Matrix3D('z', -angle);
       
      p = Vector3D(
	               -r*0.5, 
	                - ( (2.0* (y*0.5*sqrt(2))) - ((y*0.5*sqrt(2)) - (y * 0.7)) ),  
					0.0
				 );
     
     for (int k=0; k<8; ++k)
	 w[k]= R*w[k];
	 
	 for (int k=0; k<8; ++k)
	 w[k]= operator * (y, w[k]);
     
     for (int k=0; k<8; ++k)
     w[k] = operator + (w[k], p);
     
     Draw4(
                 w[0].x(), w[0].y(), w[0].z(), 
                 w[1].x(), w[1].y(), w[1].z(),
                 w[2].x(), w[2].y(), w[2].z(),
				 w[3].x(), w[3].y(), w[3].z(),
				 w[4].x(), w[4].y(), w[4].z(),
				 w[5].x(), w[5].y(), w[5].z(),
				 w[6].x(), w[6].y(), w[6].z(),
				 w[7].x(), w[7].y(), w[7].z(),
				        r,    angle,       n-1
				 
                 );          
                 
                 
                          
 }
     
}
     
     
 
	 
	 

}

		     
                 

int main(int argc, char* argv[])
{

    
    int n = 1;
    double r = 1.0;
    double angle = 3.14159265358979 * 0.25;
    double a = r * 0.5;
    
    double gold= (1 + sqrt(5))/2;
    double g1= 1/gold;
    double g2= 1/(gold*gold);
     
     Torus t("000DodecaDragon5.stl");
     t.Draw1( 
	        g2, 0.0,  1.0,//0   b4   P1
	       -g2 , 0.0, 1.0,// 1    P2
	       -g1  ,  g1,   g1,//2    P3
	        0.0, 1.0, g2,//3       P4 
			 g1, g1, g1,//4        P5	 
	       0.0,-1.0, g2,//5   b1     p6
	       g1, -g1, g1,//6    b2     p7
		    -g1, -g1, g1,//7       p8
		    g2, 0.0, -1.0,//8    a4  p9
		    -g2,  0.0, -1.0,//9  a3  p10
		    -g1, -g1,-g1,//10      p11
		    0.0,-1.0,-g2,//11      p12
		    g1, -g1, -g1,//12      p13
		    g1 ,g1 , -g1,//13    a5  p14
		     0.0, 1.0, -g2,//14   a1  p15
		    -g1, g1, -g1,//15    a2  p16
		    1.0, -g2, 0.0,//16      p17
		   -1.0, g2, 0.0,//17      p18
		   -1.0,-g2, 0.0,//18      p19
		   1.0, g2, 0.0, //19    b3
		   r, angle, n,
		   0.0, 0.0, 0.0
	         );
	
	/*
     t.Draw2( 
	        g2, 0.0,  1.0,//0   b4   P1
	       -g2 , 0.0, 1.0,// 1    P2
	       -g1  ,  g1,   g1,//2    P3
	        0.0, 1.0, g2,//3       P4 
			 g1, g1, g1,//4        P5	 
	       0.0,-1.0, g2,//5   b1     p6
	       g1, -g1, g1,//6    b2     p7
		    -g1, -g1, g1,//7       p8
		    g2, 0.0, -1.0,//8    a4  p9
		    -g2,  0.0, -1.0,//9  a3  p10
		    -g1, -g1,-g1,//10      p11
		    0.0,-1.0,-g2,//11      p12
		    g1, -g1, -g1,//12      p13
		    g1 ,g1 , -g1,//13    a5  p14
		     0.0, 1.0, -g2,//14   a1  p15
		    -g1, g1, -g1,//15    a2  p16
		    1.0, -g2, 0.0,//16      p17
		   -1.0, g2, 0.0,//17      p18
		   -1.0,-g2, 0.0,//18      p19
		   1.0, g2, 0.0, //19    b3
		   r, angle, n,
		   0.0, 0.0, 0.0
	         );
	
	
     t.Draw3( 
	        -a, -a, -a,
	         a, -a, -a,
	        -a, -a,  a,
			 a, -a,  a,
			-a,  a, -a,
			 a,  a, -a,
			-a,  a,  a,
			 a,  a,  a,
			 r, angle, n
			 );	    
            
		   t.Draw4( 
	        -a, -a, -a,
	         a, -a, -a,
	        -a, -a,  a,
			 a, -a,  a,
			-a,  a, -a,
			 a,  a, -a,
			-a,  a,  a,
			 a,  a,  a,
			 r, angle, n
			 );
		    */

			  
			  
			  
     return EXIT_SUCCESS;
}




