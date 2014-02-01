import os

def BuilHTMLGraph(suist,env,eco,soc,labels):
	header=["label","environmental","economic","social","sustainability"]
	data=[]
	for i in range(len(labels)):
		row=[]
		row.append(labels[i])
		row.append(env[i])
		row.append(eco[i])
		row.append(soc[i])
		row.append(suist[i])
		data.append(row)
	currentDIR = unicode(os.path.abspath( os.path.dirname(__file__)))
	log=open(os.path.join(currentDIR,"log.html"),"w")
	log.write(currentDIR)
	HTMLfile=open(os.path.join(currentDIR,"barGraph.html"),"w")

	HTMLfile.write("""<!DOCTYPE html>
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<title>Sustainability box</title>
		<meta name="keywords" content="">
		<meta name="description" content="" />
		<link href="http://fonts.googleapis.com/css?family=Open+Sans:400,300,600,700|Archivo+Narrow:400,700" rel="stylesheet" type="text/css">
		<link href="default.css" rel="stylesheet" type="text/css" media="all" />
		<script type="text/javascript" src="https://www.google.com/jsapi"></script>
		<script type="text/javascript">
			google.load("visualization", "1", {packages:["corechart"]});
			google.setOnLoadCallback(drawChart);
			function drawChart() {
				var dataBar = google.visualization.arrayToDataTable([\n""")
	HTMLfile.write(str(header[:-1])+",\n")
	for r in range(len(data[:-1])):
		HTMLfile.write(str(data[r][:-1])+",\n") #last doesn't printed
	HTMLfile.write(str(data[r+1][:-1]))
	HTMLfile.write("\n]);\n")
	HTMLfile.write("""	var optionsBar = {
			  title: 'bars of sustainability',
			  isStacked: 'true' 
			};
				var dataBubble = google.visualization.arrayToDataTable([\n""")
	HTMLfile.write(str(header)+",\n")
	for r in range(len(data[:-1])):
		HTMLfile.write(str(data[r])+",\n")
	HTMLfile.write(str(data[r+1]))
	HTMLfile.write("\n]);\n")
	HTMLfile.write("""	var optionsBubble = {
			title: 'bubbles of sustainability',
			colorAxis: {colors: ['red', 'green']},
			hAxis: {title: 'environmental'},
			vAxis: {title: 'economic'},
			};

			var chartBar = new google.visualization.ColumnChart(document.getElementById('bar_div'));
			chartBar.draw(dataBar, optionsBar);
			var chartBubble = new google.visualization.BubbleChart(document.getElementById('bubble_div'));
			chartBubble.draw(dataBubble, optionsBubble)
		  }
		</script>""")
	HTMLfile.write("""
	  </head>
	  <body>
	  <div id="logo" class="container"><h1>Graph of sustainability</h1>
		<br></br>
		<div id="bar_div" style="width: 900px; height: 500px;"  border='0'></div>
		<br><hr>
		<div id="bubble_div" style="width: 900px; height: 500px;"  border='1'></div>
		<br><hr>
		<img class="aligncenter" src='histogram.png' style="width: 900px; height: 500px;"  border='0'/>
		<br><hr>
		<img class="aligncenter" src='points.png' style="width: 900px; height: 500px;"  border='0'/><hr>
	  </body>
	</html>""")
	HTMLfile.close()
	log.close()
