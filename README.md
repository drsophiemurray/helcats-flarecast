helcats-flarecast
=================

*Code used to analyse data for the HELCATS-FLARECAST paper*

[![DOI](https://zenodo.org/badge/126829901.svg)](https://zenodo.org/badge/latestdoi/126829901)

This repository contains the code and data used to compare the EU FP7 HELCATS and EU H2020 FLARECAST databases for the 2018 Solar Physics publication, Connecting Coronal Mass Ejections to Their Solar Active Region Sources: Combining Results from the HELCATS and FLARECAST Projects (doi: 10.1007/s11207-018-1287-4). The post-print of the paper is freely available on [arxiv](https://arxiv.org/abs/1803.06529), and ADS BibTex entry is below for convenience:

    @ARTICLE{Murray2018,
                author = {{Murray}, S.~A. and {Guerra}, J.~A. and {Zucca}, P. and {Park}, S.-H. and
                           {Carley}, E.~P. and {Gallagher}, P.~T. and {Vilmer}, N. and
                           {Bothmer}, V.},
                title = "{Connecting Coronal Mass Ejections to Their Solar Active Region Sources: Combining Results from the HELCATS and FLARECAST Projects}",
              journal = {\solphys},
        archivePrefix = "arXiv",
               eprint = {1803.06529},
         primaryClass = "astro-ph.SR",
             keywords = {Active regions, magnetic fields, Coronal mass ejections, initiation and propagation, Flares, forecasting, relation to magnetic field, Sunspots, magnetic fields},
                 year = 2018,
                month = apr,
               volume = 293,
                  eid = {#60},
                pages = {#60},
                  doi = {10.1007/s11207-018-1287-4},
               adsurl = {http://adsabs.harvard.edu/abs/2018SoPh..293...60M},
              adsnote = {Provided by the SAO/NASA Astrophysics Data System}
            }


Code
-------
The LOWCAT catalogue was created with an IDL algorithm originally written by P. Zucca and modified by [S.A. Murray](https://github.com/sophiemurray). The code repositry is available on [Github](https://github.com/sophiemurray/lowcat). ``lowcat_plots.py`` was written by S.A. Murray to anlayse the LOWCAT catalogue properties to create Figures 3, 6, and 7, as well as the histograms in Figures 4, 5, 10, and 11.

The work to compare FLARECAST data to the HELCATS efforts was undertaken by [J. A. Guerra](https://github.com/jorgueagui), with ``HELC_FL_TS.py`` and ``HELCATS_match_FLARECAST_1.py`` relevant to the results outlined in Section 3 of the paper.

It is worth noting that Figure 1 was created by running the [SMART](http://arxiv.org/abs/1006.5898) algorithm originally developed by P. A. Higgins, an IDL code which is also available on [GitHub](https://github.com/pohuigin/smart_library).

Data
-------
The LOWCAT database (which Section 2 of the paper analyses) is available freely on [Figshare](https://figshare.com/articles/HELCATS_LOWCAT/4970222), however ``data/lowcat.json`` is also included here for completeness.

FLARECAST data (which Section 3 of the paper analyses) is freely available via the flarecast.eu [API](http://api.flarecast.eu). The data extracted from this database as of October 2017 has been provided in ``data/flarecast_list.csv``, used to create the relevant histograms of properties in Section 3.

In order to create Figure 3, some location information was extracted from the LOWCAT database. This has been provided at ``/data/flare_ar_loc.sav`` so that the code can be run with it, as well as a sample fits file that is used as a background map for the figure.

License
-------
The content of this project is licensed under the [Creative Commons Attribution 4.0 license](https://creativecommons.org/licenses/by/4.0/), and the underlying source code used to format and display that content is licensed under the [MIT license](https://opensource.org/licenses/mit-license.php). Please reference the Solar Physics publication in all instances, the Figshare database if using the LOWCAT catalogue, and relevant GitHub repositries if using the code.
