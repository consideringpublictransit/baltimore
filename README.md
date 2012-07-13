Considering Public Transit
========================

Data and code supporting the paper **Considering Public Transit:  New Insights into job and food access for low-income residents in Baltimore, Md** by Plano, Darby, and Jadud.

Brief Synopsis
====
We completed a transit access analysis using transportation analysis zones and travel time via public transit between zones across Baltimore City and County, MD. We determined the number of healthy food stores, or supermarkets, and employment opportunities accessible from a particular origin zone for all zones in the metropolitan area.

The Data
===

Running the Analysis
===
We used the command

<pre>
  python full-analysis.py taz.sqlite 30
</pre>

to generate an analysis based on a 30-minute travel window and

<pre>
  python full-analysis.py taz.sqlite 45
</pre>

to generate results based on a 45-minute travel window. Both <code>taz.sqlite</code> and <code>time.sqlite</code> need to be in the script directory for the analysis to be completed. Similar analyses for other cities (that use this script) would need equivalent data tables in the SQLite format.

Citing this Work
====
TBA