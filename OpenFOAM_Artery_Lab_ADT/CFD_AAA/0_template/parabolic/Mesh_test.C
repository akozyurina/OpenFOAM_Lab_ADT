/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | Copyright (C) 2011-2015 OpenFOAM Foundation
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

#include "fvCFD.H"

 
#include "List.H"


/*
using std::string;
using std::vector;
using std::ifstream;
using std::istringstream;
using std::cout;

using namespace Foam;



using namespace std;
*/



int main(int argc, char *argv[])
{
    #include "setRootCase.H"

    // These two create the time system (instance called runTime) and fvMesh (instance called mesh).
    #include "createTime.H"
    #include "createMesh.H"
      
    word patchName("inlet");
    label patchID = mesh.boundaryMesh().findPatchID(patchName);
    const vectorField& Cf = mesh.boundary()[patchID].Cf();
    const polyPatch& b = mesh.boundaryMesh()[patchID];
    
    vectorField inletField(Cf);
    /*
    const dictionary& transportProperties = db().lookupObject<IOdictionary>
		(
		 "transportProperties"
		);

		
		dictionary contour = transportProperties.subDict("contour");
		
		List<List<double>> phi_R = contour.lookup("phi_R");

*/
     IOdictionary transportProperties
	(
		IOobject
		(
		    "transportProperties", // name of the dictionary
		    runTime.constant(), // location in the case - this one is in constant
		    mesh, // needs the mesh object reference to do some voodoo - unimportant now
		    IOobject::MUST_READ, // the file will be re-read if it gets modified during time stepping
		    IOobject::NO_WRITE // read-only
		)
	);
	
	
	dictionary contour = transportProperties.subDict("contour");
		
	List<List<double>> phi_R = contour.lookup("phi_R");
	
	          
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
         
          
          double area=0.0; 
	  forAll(Cf,faceI)
		{
		  double s=mesh.boundary()[patchID].magSf()[faceI];
		  area+=fabs(s);
		}
          
          
          double us = 0.0; 
	  forAll(Cf,faceI)
		{
		  double uds = mesh.boundary()[patchID].magSf()[faceI] * mag(inletField[faceI]) ;
		  us += fabs(uds);
		}
		
	  Foam::Info << area<< "rtttttttttttttt" <<us << endl;	
	  double U_norm = area / us;
	  
	  fileName outputDir = "./U_norm";
	    // Creathe the directory
	    mkDir(outputDir);

	    // File pointer to direct the output to
		autoPtr<OFstream> outputFilePtr;
	    // Open the file in the newly created directory
	    outputFilePtr.reset(new OFstream(outputDir/"area_us.txt"));

	    // Write stuff
	    outputFilePtr() << area << endl;
	    outputFilePtr() << us << endl;

	  
	  return 0;
	  
	  }
	  
 /*
    // runTime and mesh are instances of objects (or classes).
    // If you are not familiar with what a class or object is, it is HIGHLY RECOMMENDED you visit this
    // website and only come back once you've read everything about classes, inheritance and polymorphism:
    // http://www.cplusplus.com/doc/tutorial/classes/
    // Note how the next lines call functions .timeName(), .C() and .Cf() implemented in the objects.
    // It is also important to realise that mesh.C() and .Cf() return vector fields denoting centres of each
    // cell and internal face.
    // Calling the mesh.C().size() method therefore yields the total size of the mesh.
    Info << "Hello there, the most recent time folder found is " << runTime.timeName() << nl
         << "The mesh has " << mesh.C().size() << " cells and " << mesh.Cf().size()
         << " internal faces in it. Wubalubadubdub!" << nl << endl;

    // It's possible to iterate over every cell in a standard C++ for loop
    for (label cellI = 0; cellI < mesh.C().size(); cellI++)
        if (cellI%20 == 0) // only show every twentieth cell not to spam the screen too much
            Info << "Cell " << cellI << " with centre at " << mesh.C()[cellI] << endl;
    Info << endl; // spacer

    // Each cell is constructed of faces - these may either be internal or constitute a
    // boundary, or a patch in OpenFOAM terms; internal faces have an owner cell
    // and a neighbour.
    for (label faceI = 0; faceI < mesh.owner().size(); faceI++)
        if (faceI%40 == 0)
            Info << "Internal face " << faceI << " with centre at " << mesh.Cf()[faceI]
                 << " with owner cell " << mesh.owner()[faceI]
                 << " and neighbour " << mesh.neighbour()[faceI] << endl;
    Info << endl;

    // Boundary conditions may be accessed through the boundaryMesh object.
    // In reality, each boundary face is also included in the constant/polyMesh/faces
    // description. But, in that file, the internal faces are defined first.
    // In addition, the constant/polyMesh/boundary file defines the starting faceI
    // indices from which boundary face definitions start.
    // OpenFOAM also provides a macro definition for for loops over all entries
    // in a field or a list, which saves up on the amount of typing.
    forAll(mesh.boundaryMesh(), patchI)
    Info << "Patch " << patchI << ": " << mesh.boundary()[patchI].name() << " with "
         << mesh.boundary()[patchI].Cf().size() << " faces. Starts at total face "
         << mesh.boundary()[patchI].start() << endl;
    Info << endl;

    // Faces adjacent to boundaries may be accessed as follows.
    // Also, a useful thing to know about a face is its normal vector and face area.
    label patchFaceI(0);
    forAll(mesh.boundaryMesh(), patchI)
    Info << "Patch " << patchI << " has its face " << patchFaceI << " adjacent to cell "
         << mesh.boundary()[patchI].patch().faceCells()[patchFaceI]
         << ". It has normal vector " << mesh.boundary()[patchI].Sf()[patchFaceI]
         << " and surface area " << mag(mesh.boundary()[patchI].Sf()[patchFaceI])
         << endl;
    Info << endl;

    // For internal faces, method .Sf() can be called directly on the mesh instance.
    // Moreover, there is a shorthand method .magSf() which returns the surface area
    // as a scalar.
    // For internal faces, the normal vector points from the owner to the neighbour
    // and the owner has a smaller cellI index than the neighbour. For boundary faces,
    // the normals always point outside of the domain (they have "imaginary" neighbours
    // which do not exist).

    // It is possible to look at the points making up each face in more detail.
    // First, we define a few shorthands by getting references to the respective
    // objects in the mesh. These are defined as constants since we do not aim to
    // alter the mesh in any way.
    // NOTE: these lists refer to the physical definition of the mesh and thus
    // include boundary faces. Use can be made of the mesh.boundary()[patchI].Cf().size()
    // and mesh.boundary()[patchI].start() methods to check whether the face is internal
    // or lies on a boundary.
    const faceList& fcs = mesh.faces();
    const List<point>& pts = mesh.points();
    const List<point>& cents = mesh.faceCentres();

    forAll(fcs,faceI)
    if (faceI%80==0)
    {
        if (faceI<mesh.Cf().size())
            Info << "Internal face ";
        else
        {
            forAll(mesh.boundary(),patchI)
            if ((mesh.boundary()[patchI].start()<= faceI) &&
                (faceI < mesh.boundary()[patchI].start()+mesh.boundary()[patchI].Cf().size()))
            {
                Info << "Face on patch " << patchI << ", faceI ";
                break; // exit the forAll loop prematurely
            }
        }

        Info << faceI << " with centre at " << cents[faceI]
             << " has " << fcs[faceI].size() << " vertices:";
        forAll(fcs[faceI],vertexI)
        // Note how fcs[faceI] holds the indices of points whose coordinates
        // are stored in the pts list.
        Info << " " << pts[fcs[faceI][vertexI]];
        Info << endl;
    }
    Info << endl;

    
    // Type of a patch may be checked to avoid running into this problem if there
    // is a substantial risk that an empty patch type will appear
    label patchID(0);
    const polyPatch& pp = mesh.boundaryMesh()[patchID];
    if (isA<emptyPolyPatch>(pp))
    {
        // patch patchID is of type "empty".
        Info << "You will not see this." << endl;
    }

  
    word patchName("inlet");
    patchID = mesh.boundaryMesh().findPatchID(patchName);
    Info << "Retrieved patch " << patchName << " at index " << patchID << " using its name only." << nl << endl;

    Info<< "End\n" << endl;
 
     Info<< "faceCenters\n" << endl;

    patchID = mesh.boundaryMesh().findPatchID(patchName);
    
    const polyPatch& b = mesh.boundaryMesh()[patchID];
    const vectorField& bc = b.faceCentres();
    Info << " " << bc;
    
    
    
	    // Include vectorList definition to store edge coordinates
    

	// Create edge list which contains edge to node connectivity
    const edgeList& edges = b.edges();
     
    forAll(edges, edge)
{
   const label& own = edges[edge][0];     // Index of edge owner node
   const label& nei = edges[edge][1];     // Index of edge neighbour node
   //const pointField& points = edges.centre();   // Node coordinates
   const pointField& points = b.points();   // Node coordinates
   // Calculate edge center coordinates by averaging node coordinates
    //Info << " " << 0.5*(points[own] + points[nei]);
}
	    


//cylindricalCS x;


const Foam::vector& v = bc[0];
auto x = v.x();
auto y = v.y();
auto value = Foam::atan2(x,y);
Info << value; // 0.2535141


Info << " vcylindr" << Foam::vector(Foam::hypot(v.x(),v.y()), Foam::atan2(v.y(), v.x()), v.z());
 

 
/*volScalarField Interp1(List<scalar> X, List<scalar> Y,volScalarField& Xi,volScalarField& Yi)
    {
        scalar m;
        scalar b;
        int FOUND;
        int jj;
        forAll(Xi.internalField(),ii)
        {
            FOUND=0; jj=0;
            while((FOUND==0) && (jj<X.size()))
            {
                if(Xi.internalField()[ii]<X[0])
                {
                    Yi.internalField()[ii]=0;
                    FOUND=1;
                }
                else if(Xi.internalField()[ii]>X[X.size()])
                {
                    Yi.internalField()[ii]=Y[jj];
                    FOUND=1;
                }
                else if(Xi.internalField()[ii]>=X[jj] && Xi.internalField()[ii]<X[jj+1])
                {
                    m=(Y[jj+1]-Y[jj])/(X[jj+1]-X[jj]);
                    b=Y[jj]-m*X[jj];
                    Yi.internalField()[ii]=m*Xi.internalField()[ii]+b;
                    FOUND=1;
                };
                jj=jj+1;
            };
        };
        return(Yi);
    }; 
    
  */  
  
/*
  std::vector< std::vector<double> > sarr;
    
    readData("profile.csv", ",", sarr);

    for ( size_t i=0; i<sarr.size(); i++ ) {

        for ( size_t j=0; j<sarr[0].size(); j++ ) {

            cout << sarr[i][j] << "\t";
        }

        cout << "\n";
  
  }
  
  cout << findY(0.0056, sarr);
 return 0;

}

*/
    

