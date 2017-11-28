<?php $path = "/home/pi/Documents/Netzkaffeekasse/"; ?>

<!DOCTYPE html>
<html>
<head>
	<title>Netzkaffeekasse</title>
	<style>
		html, body
		{
			width: 100%;
			height: 100%;
			max-width: 100%;
			max-height: 100%;
			overflow: hidden;
			margin: 0;
			padding: 0;
			background-color: #00001c;
			color: #FFFAFA;
			cursor: none;
		}

		#titlecontent
		{
			height: 15%;
			max-height: 15%;
			min-height: 200px;
			margin: 0 auto;
			overflow: hidden;
			text-align: center;
		}

		#imagecontent
		{
			height: 60%;
			max-height: 60%;
			width: 100%;
			margin: 0 auto;
			overflow: hidden;
		}

		#logcontent
		{
			position: absolute;
			height: 20%;
			max-height: 20%;
			bottom: 30px;
			overflow: hidden;
			width: 100%;
		}
		
		#footercontent
		{
			position: absolute;
			height: 25px;
			bottom: 0px;
			padding-top: 5px;
			text-align: center;
			width: 100%;
			z-index:100;
			border-top; 2px solid #FFFAFA;
			background-color: #333366;
		}

		.image
		{
			display: block;
			max-width: 100%;
			max-height: 100%;
			margin: 0 auto;
		}
	</style>
</head>
<body>

<div id="titlecontent">
	<h1>NETZKAFFEEKASSE</h1>

<?php
	// the total value
	$f = file_get_contents($path."TOTAL.nkk");
	if($f)
	{
		echo("<h2>TOTAL: $f CHF</h2>");
	}else{
		echo("There is no TOTAL file now.<br />");
	}

	// the actual text to show.
	$fa = file_get_contents($path."ACTUALTEXT.nkk");
	if($fa)
	{
		echo("<h3>$fa</h3>");
	}else{
		echo("There is no ACTUAL file now.<br />");
	}

	// the actual time stamp for the reloadeing image.
	$ftt = file_get_contents($path."ACTUALTIMESTAMP.nkk");
	if(!$ftt)
	{
		$ftt="null";
	}
?>

</div>
<div id="imagecontent">
	<img class="image" src="IMAGES/latest.jpg?ts=<?php echo($ftt); ?>" />
</div>

<div id="logcontent">
<h3>LOG:</h3>
<pre>
<?php
	$flog = file_get_contents($path."LOG.nkk");
	if($flog)
	{
		echo($flog);
	}else{
		echo("Could not open LOG file.");
	}
?>
</pre></div>

<div id="footercontent">
by ben0bi...please wait <span id="timerUI">10</span> seconds for reload.
</div>

<script>
var count = 10;
function loop()
{
	document.getElementById("timerUI").innerHTML = count;
	count-=1;
	if(count<=0)
		location.reload(true);
	setTimeout(loop, 1000);
}

// scroll down on the log.
var logDiv = document.getElementById("logcontent");
logDiv.scrollTop = logDiv.scrollHeight;

loop();
</script>

</body>
</html>

