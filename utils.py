import os
#html template for all the website
html_base_page = """<!DOCTYPE html>
<html>
    <head>
    <style>

    </style>
    <head>


  <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.0/socket.io.js"> 
    </script>


		<meta name="description" content="VintFind - Bot Vinted gratuit et extrêmement rapide !">
		<title>VintFind - Bot Vinted Gratuit</title
		
		<link rel="icon" type="image/png" href="../logo.png" />
<meta name="a.validate.02" content="YvCgN-LzcXagyPBmWuItQEuQfRTspM44uMtk" />
    
<!--<script src="https://cdn.adf.ly/js/entry.js"></script>-->
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2431492642839080"
     crossorigin="anonymous"></script>
        <link rel="stylesheet" href="../index.css"></link>
        <script src="../index.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    </head>
    <body>
        <div id="main">
            <button onclick="topFunction()" id="topbutton" title="Go to top"><i class="fas fa-arrow-up"></i></button>
        <div id="div1"><h1>VintFind</h1></div>

<a href="../index.html">Toutes les marques</a><br><br><br>
<!--LA-->
<br><br><br><br>
<!--ICI-->

                       
                
                        
                
                        
                
    
            </div>
             <div id="footer"></div>
						 
        </body>

    <script>
        var socket = io.connect('https://vintfind.fr:' + location.port);
        socket.on('connect', function() {
            console.log('Connected to server');
        });
        socket.on('reload_page', function() {
            console.log('Reloading page');
            location.reload();
        });
    </script>

</html>
"""


class Style():
	BLACK = '\033[30m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'
	UNDERLINE = '\033[4m'
	RESET = '\033[0m'


def get_short_link(url):
	url = f"http://adfoc.us/serve/sitelinks/?id=807979&url={url}"
	return url


#format an empty html file with the template removing all products
def clearfile(filename):
	if filename != "index.html":
		filename = os.path.join("./specific", str(filename))
	try:
		with open(filename, "w+") as f:
			f.write(html_base_page)
	except:
		print("error")
	print(f"File {str(filename)} formated")


#writes the given text in the given location in the given file
def write_html(text, filename, location):
	if location == "ici":
		location = '<!--ICI-->'
	if location == "la":
		location = '<!--LA-->'
	if filename != "index.html":
		filename = os.path.join("./specific", str(filename))
	print(str(f"Writing text in {str(filename)} at location {str(location)}"))
	try:
		with open(filename, 'r+') as f:
			lines = f.readlines()
			for i, line in enumerate(lines):
				if line.startswith(location):
					lines[i] += text
			f.truncate()
			f.seek(0)
			for line in lines:
				f.write(line)
	except:
		print("error")
	print("Finished writing")
