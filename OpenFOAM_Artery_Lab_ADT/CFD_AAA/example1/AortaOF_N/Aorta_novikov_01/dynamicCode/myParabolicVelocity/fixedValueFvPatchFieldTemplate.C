/*---------------------------------------------------------------------------*  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "fixedValueFvPatchFieldTemplate.H"
#include "addToRunTimeSelectionTable.H"
#include "fvPatchFieldMapper.H"
#include "volFields.H"
#include "surfaceFields.H"
#include "unitConversion.H"
//{{{ begin codeInclude

//}}} end codeInclude


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    // dynamicCode:
    // SHA1 = 18196034663db4825ed471beac05efb1ac65d43e
    //
    // unique function name that can be checked if the correct library version
    // has been loaded
    void myParabolicVelocity_18196034663db4825ed471beac05efb1ac65d43e(bool load)
    {
        if (load)
        {
            // code that can be explicitly executed after loading
        }
        else
        {
            // code that can be explicitly executed before unloading
        }
    }
}

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

makeRemovablePatchTypeField
(
    fvPatchVectorField,
    myParabolicVelocityFixedValueFvPatchVectorField
);


const char* const myParabolicVelocityFixedValueFvPatchVectorField::SHA1sum =
    "18196034663db4825ed471beac05efb1ac65d43e";


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

myParabolicVelocityFixedValueFvPatchVectorField::
myParabolicVelocityFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF
)
:
    fixedValueFvPatchField<vector>(p, iF)
{
    if (false)
    {
        Info<<"construct myParabolicVelocity sha1: 18196034663db4825ed471beac05efb1ac65d43e"
            " from patch/DimensionedField\n";
    }
}


myParabolicVelocityFixedValueFvPatchVectorField::
myParabolicVelocityFixedValueFvPatchVectorField
(
    const myParabolicVelocityFixedValueFvPatchVectorField& ptf,
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    fixedValueFvPatchField<vector>(ptf, p, iF, mapper)
{
    if (false)
    {
        Info<<"construct myParabolicVelocity sha1: 18196034663db4825ed471beac05efb1ac65d43e"
            " from patch/DimensionedField/mapper\n";
    }
}


myParabolicVelocityFixedValueFvPatchVectorField::
myParabolicVelocityFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const dictionary& dict
)
:
    fixedValueFvPatchField<vector>(p, iF, dict)
{
    if (false)
    {
        Info<<"construct myParabolicVelocity sha1: 18196034663db4825ed471beac05efb1ac65d43e"
            " from patch/dictionary\n";
    }
}


myParabolicVelocityFixedValueFvPatchVectorField::
myParabolicVelocityFixedValueFvPatchVectorField
(
    const myParabolicVelocityFixedValueFvPatchVectorField& ptf
)
:
    fixedValueFvPatchField<vector>(ptf)
{
    if (false)
    {
        Info<<"construct myParabolicVelocity sha1: 18196034663db4825ed471beac05efb1ac65d43e"
            " as copy\n";
    }
}


myParabolicVelocityFixedValueFvPatchVectorField::
myParabolicVelocityFixedValueFvPatchVectorField
(
    const myParabolicVelocityFixedValueFvPatchVectorField& ptf,
    const DimensionedField<vector, volMesh>& iF
)
:
    fixedValueFvPatchField<vector>(ptf, iF)
{
    if (false)
    {
        Info<<"construct myParabolicVelocity sha1: 18196034663db4825ed471beac05efb1ac65d43e "
            "as copy/DimensionedField\n";
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

myParabolicVelocityFixedValueFvPatchVectorField::
~myParabolicVelocityFixedValueFvPatchVectorField()
{
    if (false)
    {
        Info<<"destroy myParabolicVelocity sha1: 18196034663db4825ed471beac05efb1ac65d43e\n";
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void myParabolicVelocityFixedValueFvPatchVectorField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        Info<<"updateCoeffs myParabolicVelocity sha1: 18196034663db4825ed471beac05efb1ac65d43e\n";
    }

//{{{ begin code
    #line 35 "/home/imcool/Desktop/OpenFOAM_Lab_ADT/OpenFOAM_Artery_Lab_ADT/CFD_AAA/example1/AortaOF_N/Aorta_novikov_01/0/U/boundaryField/inlet"
const dictionary& transportProperties = db().lookupObject<IOdictionary>
		(
		 "transportProperties"
		);


		dictionary profile = transportProperties.subDict("profile");
		
		List<List<double>> t_u = profile.lookup("t_u");
		
		dictionary contour = transportProperties.subDict("contour");
		
		List<List<double>> phi_R = contour.lookup("phi_R");


                //интерполяция периодического сигна
                
               
       	double t = this->db().time().value();
                
                double delta_t = fabs(t_u[1][0] - t_u[0][0]);
	        int tmin_id = int(t/delta_t);
	        int tmax_id = tmin_id + 1;
	    
	        double t_min = t_u[tmin_id][0];
	        double u_min = t_u[tmin_id][1];
	        double t_max = t_u[tmax_id][0];
	        double u_max = t_u[tmax_id][1];
	    
	        double u_t = u_min + (t - t_min) * (u_max - u_min) / (t_max - t_min);
                
                
            
		 const vectorField& Cf = patch().Cf();
		 vectorField& inletField = *this;
                
          
          forAll (Cf, faceI)
          {       
          
                 //double U_norm = 1;
                 
                 
          	  const double x = Cf[faceI][0];
          	  const double y = Cf[faceI][1];
          	  const double z = Cf[faceI][2];
          	  
		  double r = Foam::hypot(x, y);
		  double phi = Foam::atan2(y, x);
		  
		  
		  // интерполяция R_phi
		  
		  //double R_phi = findY(phi, sarr_phi);
		
       
                  double delta_phi = fabs(phi_R[1][0] - phi_R[0][0]);
	          int phimin_id = int(fabs((phi-phi_R[0][0])/delta_phi));
	          int phimax_id = phimin_id + 1;
	    
	          double phi_min = phi_R[phimin_id][0];
	          double R_min = phi_R[phimin_id][1];
	          double phi_max = phi_R[phimax_id][0];
	          double R_max = phi_R[phimax_id][1];
	          
	         
		 
		  double R_phi = R_min + (phi - phi_min) * (R_max - R_min) / (phi_max - phi_min);
		
                  inletField[faceI] = vector(0, 0, (1 -  Foam::pow( (r / R_phi), 2)));
          }
         
          
          dictionary areaf = transportProperties.subDict("area");
		
	  List<double> area = areaf.lookup("area");
	  
	  dictionary usf = transportProperties.subDict("us");
		
	  List<double> us = usf.lookup("us");
	  
	
	  
	  double U_norm = u_t * area[0]/us[0];
	  //Info <<"inlet area = "<< area << "us"<< us<< endl;
          inletField = inletField * U_norm;
          
          //Info <<"inlet area = "<<area<< us << u_t << U_norm << endl;
        
          /*operator==
                (
                inletField
                );
         
            */
//}}} end code

    this->fixedValueFvPatchField<vector>::updateCoeffs();
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

