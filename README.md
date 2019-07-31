# Intro

This repository contains python-based analysis scripts for the basic NOVO simulations as well as the analysis results.
The repository is meant for sharing the simulation data, analysis scripts and the results

# Simulations and Analysis

The Monte Carlo simulations are run using MCNP6.2 from Los Alamos National Laboratories, USA.
We consider the following in the basic simulations and analysis (applying to both neutrons and gamma-rays)

- Total efficiency
- Original multiplicities w/o segmentation
- Multiplicities with segmentation (i.e. number of responding segments / elements)
- Multiplicity distributions with and w/o segmentation
- Energy deposition distributions (in the 1st, 2nd and 3rd scatter events) with and w/o segmentation
- Distributions of (with and w/o segmentation):
  -- The distance between the 1st and 2nd scatter events
  -- The distance between the 2nd and 3rd scatter events
  -- TOF between the 1st and 2nd scatter events
  -- TOF between the 2nd and 3rd scatter events
- Mean energy deposition in the 1st, 2nd and 3rd scatter events with and w/o segmentation
- Mean distance travelled (1st - 2nd & 2nd - 3rd scatter events) with and w/o segmentation
- Mean TOF (1st - 2nd & 2nd - 3rd scatter events) with and w/o segmentation
- Intrinsic pile-up (fraction of detections with multiple interactions in the 1st, 2nd and 3rd responding segments)
- Detector load (total, max. & min.) per segment per incident particle
- Detector load distributions per segment per incident particle

# Usage

The idea is to ensure transparency of the work that's been done so far. This is the only way to uncover any potential errors in the analysis.
So if you want to be able to use the scripts given here; either download them directly or use

git clone https://github.com/ilkermeric/NOVOBasics.git

Of course, you need to have both numpy and matplotlib installed and configured correctly in your computing environment.

Also, you will need to download the MCNP output files in binary format from the following link (git is not the environment for large files):

https://drive.google.com/open?id=1gVsTBE_sNr3DE-QIsZEukqztjKEGqEu7

If you want to run the entire chain of analysis then you will need to have the MCNP output files and all the python scripts in the same folder. Also, runanalysis.sh are shell scripts that you can run for an automated execution of the analysis chain.

You can enter your comments on the results, scripts and any other aspect in the wiki page:

https://github.com/ilkermeric/NOVOBasics.wiki.git

# Author

* Ilker Meric ([ilkermeric][])

[ilkermeric]:  https://github.com/ilkermeric
