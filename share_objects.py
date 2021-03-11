import os

register = {}

workingDir = os.getcwd()
softwareDir = os.path.join(workingDir, "analysis_toolkit_data")
curvesDir = os.path.join(softwareDir, "curves")
plotsDir = os.path.join(softwareDir, "plots")
picturesDir = os.path.join(softwareDir, "pictures")
moviesDir = os.path.join(softwareDir, "movies")
valuesDir = os.path.join(softwareDir, "values")
animatorDir = os.path.join(softwareDir, "animator")
metapostDir = os.path.join(softwareDir, "metapost")

current_platform_system = ""
