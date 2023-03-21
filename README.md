# PTECiScienceSubmission

# Computer-Aided Designs

A flow system was fabricated to flow media through a custom 3D-printed bubble trap (bubbleTrap.stl), a central commercially availabe channel slide, and into a final 3D-printed media reservoir (mediaReservoir.stl). An interlocking tray was laser-cut into corrugated polypropylene and built to house four flow systems in parallel (corrugated_polypropylene_base.svg, corrugated_polypropylene_top_and_middle.svg).

# Multiphysics Modeling

Ansys Fluent was used to create a three-dimensional (3D) approximation of the fluid path within a channel slide. The fluid path was modelled as an elliptical channel with 0.4 mm height, 5 mm width, and 50 mm length with cylindrical inlets and outlets of diameter 3.5 mm and height 5.8 mm. Shear stress was estimated along a centerline at the bottom surface of the channel, where cells would be attached, under a range of simulated volumetric flow rates (0.694-300 µL/min), which correspond to initial velocities of 1.2 x 10-8 and 5.2 x 10-4 m/s for nutritive and physiological flow conditions, respectively, calculated using the flow rate divided by the cross-sectional area. These initial flow rates were selected using a guess-and-check approach until shear stress was in the physiological range of 0.3 and 1.2 dyn/cm2. Cell media was approximated to have the viscosity and density of water, similar to previous work. After setting the initial and boundary conditions, the software solves governing conservation of mass and momentum equations to calculate shear stress. 

# Experimental Methods and Imaging

Human immortalized proximal tubule epithelial cells (PTECs) were cultured in channel slides and exposed to fluidic shear stress using the flow system for 3 days and subsequently fixed, immunostained, and imaged. For each chip, five widefield images were collected on a 60x oil objective with a Nikon Eclipse Ti-S inverted fluorescent microscope. Additionally, five confocal z-stacks were collected with a maximum step size of 0.4 µm on a 60x oil objective with a Nikon C2 point-scanning confocal microscope. 

# Image Analysis

Two-dimensional 60x widefield images were analyzed for cell area and cell circularity through custom ImageJ scripts (morphoLibJ.ijm) implementing the MorphoLibJ plugin (Legland, Arganda-Carreras and Andrey 2016). Additional scripts quantified the percentage of cells expressing cilia using the find maxima function on the acetylated tubulin stain (ciliaCount.ijm) normalized over the total number of cells in an image (nucleiCount.ijm).  

Three-dimensional 60x confocal z-stacks were analyzed to approximate tissue thickness (orthogonalView_cellHeight_sampling.ijm), cilia length (orthogonalView_ciliaLength.ijm), and laminin layer thickness (orthogonalView_lamininThickness_sampling.ijm) through custom scripts implementing the binarized maximum intensity projection of the orthogonal view of z stacks. For tissue thickness and laminin layer thickness, scripts implemented the plot profile function then iterated through 10 pre-defined regions of interest to approximate cell height (ROISet_cellHeight_lamininSampling.zip). 

Finally, scripts analyzed 3D ZO-1 (stackZO1PixelCount.ijm), acetylated tubulin (stackCiliaPixelCount.ijm), and Na/K-ATPase coverage (stackNaKPixelCount.ijm) by summing all of the ZO-1, acetylated tubulin, or Na/K-ATPase pixels in the stack normalized over the total number of cells in the stack. 

Finally, spreadsheets containing plot profile or histogram data from ImageJ scripts were sorted and analyzed through custom python scripts (cellHeight.py, lamininThickness.py, pixelCoverage.py, ciliaLength.py) implemented in Brev.dev, a browser-based developer environment (San Francisco, CA, USA). 
