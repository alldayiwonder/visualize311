<h1> Visualize 311 </h1>

<h3> Count </h3>

Run as python 311_countsZip.py [complaintsfile] [zipboroughfile] [shapefile]

Python script to read NYC 311 data, count number of complaints per zip code, and visualize as circles for each zip. The size of each circle is proportional to the number of complaints in the zip code.

<h6> Dependencies: </h6>
<ul> Python 2.7.8 </ul>
<ul> Bokeh visualization library: http://bokeh.pydata.org/en/latest/ </ul>
<ul> Complaintsfile in CSV format: https://data.cityofnewyork.us/Social-Services/311_limitedcolumns2014/r96j-ebm2 </ul>
<ul> Shapefile: https://www.census.gov/geo/maps-data/data/tiger-line.html </ul>
<ul> Note: this script was used with the 2013 TIGER/Line Shapefiles </ul>


