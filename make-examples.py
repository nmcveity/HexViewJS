
import string
import base64
import cgi

doc_template = string.Template("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
	<title>Nick's Hex Viewer</title>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js" type="text/javascript"></script>
	<script src="hexview.js" type="text/javascript"></script>
	<script type="text/javascript">
		function toggle_example(name, e)
		{
			var link = $$("a#" + name)
			var div = $$("div#" + name + "_div")
			
			if (link.text() == "(show source)")
			{
				div.slideDown("slow")
				link.text("(hide source)")
			}
			else
			{
				div.slideUp("slow")
				link.text("(show source)")
			}
			
			e.preventDefault();
		}
		
		$$(window).load(function () {
			$$("a#example1").click(function (e) { toggle_example('example1', e); })
			$$("a#example2").click(function (e) { toggle_example('example2', e); })
			$$("a#example3").click(function (e) { toggle_example('example3', e); })
			$$("a#example4").click(function (e) { toggle_example('example4', e); })
		})
	</script>
	<link rel="stylesheet" type="text/css" href="hexview.default.css" />
</head>
<body>
	${examples}
</body>
</html>""")

hex_template = string.Template("""
	<div class="hexviewwindow" title="${title}">
		${base64_data}
		<form id="hexviewwindow_params">
			<input type="hidden" name="highlights" value="${highlights}" />
			<input type="hidden" name="row_width" value="${row_width}" />
			<input type="hidden" name="word_size" value="${word_size}" />
			<input type="hidden" name="caption" value="${title}" />
		</form>
	</div>
""")

example_template = string.Template("""
	<p>A simple example showing the top of a random JPEG file:</p>
	${first}
	<blockquote>
		<a href="show" id="example1">(show source)</a>
		<div id="example1_div" style="display: none;">
			<pre>
			${first_source}
			</pre>
		</div>
	</blockquote>
	<p>You can adjust the bytes per row:</p>
	${second}
	<blockquote>
		<a id="example2" href="nowhere">(show source)</a>
		<div id="example2_div" style="display: none;">
			<pre>
			${second_source}
			</pre>
		</div>
	</blockquote>
	<p>And you can adjust the word size:</p>
	${third}
	<blockquote>
		<a id="example3" href="nowhere">(show source)</a>
		<div id="example3_div" style="display: none;">
			<pre>
			${third_source}
			</pre>
		</div>
	</blockquote>
	<p>Here is another example showing an executable file header, you can specify parts of the binary data to highlight:</p>
	${fourth}
	<blockquote>
		<a id="example4" href="nowhere">(show source)</a>
		<div id="example4_div" style="display: none;">
			<pre>
			${fourth_source}
			</pre>
		</div>
	</blockquote>
	
""")

def to_base64(f):
	infile = open(f, "rb")
	data = infile.read()
	infile.close()
	b64 = base64.b64encode(data)
	res = []
	while len(b64) > 0:
		res.append(b64[0:64])
		b64 = b64[64:]
	print res
	return "\n\t\t".join(res)

example_1 = hex_template.substitute(title="JPEG file contents", row_width=16, word_size=1, highlights="", base64_data=to_base64("example1.bin"))
example_2 = hex_template.substitute(title="JPEG file contents", row_width=8, word_size=1, highlights="", base64_data=to_base64("example1.bin"))
example_3 = hex_template.substitute(title="JPEG file contents", row_width=16, word_size=4, highlights="", base64_data=to_base64("example1.bin"))
example_4 = hex_template.substitute(title=".exe file header", row_width=16, word_size=2, highlights="16:17:#F4FA58:Initial value of SP register,128:152:#54FAF8:Portable Executable signature and header", base64_data=to_base64("example2.exe.bin"))

examples = example_template.substitute(first=example_1, first_source=cgi.escape(example_1), second=example_2, second_source=cgi.escape(example_2), third=example_3, third_source=cgi.escape(example_3), fourth=example_4, fourth_source=cgi.escape(example_4))

out = open("examples.html", "wt")
out.write(doc_template.substitute(examples=examples))
out.close()
