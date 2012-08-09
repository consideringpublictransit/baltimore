Considering Public Transit
========================

Data and code supporting the paper **Considering Public Transit:  New Insights into job and food access for low-income residents in Baltimore, Md** by Plano, Darby, Shaffer, and Jadud.

The code in this repository is made available under a GPL3 or later license. The full GPL3 license is included in this repository in the file <code>gpl-3.0.txt</code>.

The data in this repository (contained within the SQLite and CSV files) is made available under a Creative Commons Attribution-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" href="http://purl.org/dc/dcmitype/Dataset" property="dct:title" rel="dct:type">Considering Public Transit:  New Insights into job and food access for low-income residents in Baltimore, Md</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/consideringpublictransit/baltimore" property="cc:attributionName" rel="cc:attributionURL">Chris Plano, Kate Darby, Matt Jadud</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.


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