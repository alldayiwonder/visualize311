import csv
import shapefile
import sys
from bokeh.plotting import *
from bokeh.objects import HoverTool
from collections import OrderedDict
from collections import Counter

###########################################################
# Visualizes counts of NYC 311 data for 2014 per zip code #
###########################################################

complaints_file = '/Users/Steve/GitHub/visualize311/311_limitedcolumns2014.csv'  # https://data.cityofnewyork.us/Social-Services/311_alldata2014/r96j-ebm2
zipBorough_file = '/Users/Steve/GitHub/visualize311/zip_borough.csv'  # <zip> <borough>
shape_file = '/Users/Steve/GitHub/visualize311/tl_2013_us_zcta510/tl_2013_us_zcta510.shp'  # https://www.census.gov/geo/maps-data/data/tiger-line.html

#complaints_file = sys.argv[1]
#zipBorough_file = sys.argv[2]
#shape_file = sys.argv[3]

def getZipBorough(zipBoroughFilename):
  with open(zipBoroughFilename) as f:
    csvReader = csv.reader(f)
    csvReader.next()

    return {row[0]: row[1] for row in csvReader}

def getComplaints(complaints_file):
  # Read all complaints data and count number of complaints in each zip code
  global complaints_dict
  complaints_dict = dict((key, {}) for key in zipBorough)
  with open(complaints_file) as f:
    reader = csv.reader(f, delimiter=",")
    next(reader)
    complaints_dict=Counter()
    for row in reader:
      incident_zip = row[8]
      if incident_zip in zipBorough:
        complaints_dict[incident_zip] += 1

  return complaints_dict

def drawPlot(shapeFilename, zipBorough):
  global center_lat
  global center_lng
  center_lat = []
  center_lng = []
  circle_size = []

  # Read the ShapeFile
  shapefile_dat = shapefile.Reader(shapeFilename)

  # Creates a dictionary for zip: {lat_list: [], lng_list: []}.
  zipCodes = []
  polygons = {'lat_list': [], 'lng_list': []}
  record_index = 0

  zip_count=[]
  for r in shapefile_dat.iterRecords():
    currentZip = r[0]

    # Keeps only zip codes in NY area, gets total complaint count in currentZip
    if currentZip in zipBorough:
      zipCodes.append(currentZip)

      try:
        zip_count.append(complaints_dict[currentZip])
      except KeyError:
        zip_count.append(0)

      # Get the center lat/long of the zip to plot the circles and set the size based on number of complaints
      center_lat.append(float(r[7]))
      center_lng.append(float(r[8]))
      size = (complaints_dict[currentZip])*0.001
      circle_size.append(size)

      # Gets shape for this zip.
      shape = shapefile_dat.shapeRecord(record_index).shape
      points = shape.points

      # Breaks into lists for lat/lng.
      lngs = [p[0] for p in points]
      lats = [p[1] for p in points]

      # Stores lat/lng for current zip shape.
      polygons['lng_list'].append(lngs)
      polygons['lat_list'].append(lats)

      # Stores lat/long for the x/y values to plot the points

    record_index += 1

  # Data to Display for the Hover
  source = ColumnDataSource(
    data=dict(
        currentZip=zipCodes,
        zip_count=zip_count
    )
  )

  # Creates the Plot
  output_file("311_countsZip.html")

  # Creates the polygons
  patches(polygons['lng_list'],
          polygons['lat_list'],
          source=source,
          fill_color='white',
          line_color="gray",
          tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
          plot_width=1100,
          plot_height=700,
          title="311 Complaints per Zip Code in 2014",
  )

  # Draws Points on top of map.
  hold()

  scatter(center_lng,
          center_lat,
          fill_color='red',
          color='red',
          line_alpha=0.1,
          size=circle_size)

  hover = curplot().select(dict(type=HoverTool))
  hover.tooltips = OrderedDict([
    ("Zip Code", "@currentZip"),
    ("Complaint Count", "@zip_count")
  ])

  show()


if __name__ == "__main__":

  zipBorough = getZipBorough(zipBorough_file)  # Get dict of zip (key) and borough (value)

  getComplaints(complaints_file)  # Get a dict of zips with nested dicts with agency complaint counts for each zip

  drawPlot(shape_file, zipBorough)  # Draw plot, open browser