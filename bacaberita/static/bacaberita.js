$(document).ready(function() {
	$('#cat a').click(function() {
		var href = $(this).attr('href');
		var url = href.replace(/\/read\//, "/json/");

		read(url);

		return false;
	});
});

function read(url) {
	$.getJSON(url, function(data) {
		render(data);
	});
}

function render(data) {
	console.log(data);
	var html = "";
	var len = data.length;

	var oc = $('#articles');

	oc.empty();
	
	for (var i=0; i<len; i++) {
		html += '<div class="feed">';
		html += '<h2><a href="' + data[i].url + '">' + data[i].title + '</a></h2>';
		html += '<div id="feed-' + data[i].id + '"></div>';
		html += '</div>';
	}
	oc.html(html);

	for (var i=0; i<len; i++) {
		var of = $('#feed-' + data[i].id);

		var alen = data[i].entries.length;
		for (var j=0; j<alen; j++) {
			var content = '';
			if (data[i].entries[j].content != null) {
				content = data[i].entries[j].content;
			}

			html = '';
			html += '<div class="article">';
			html += '<h3><a href="' + data[i].entries[j].url + '">' + data[i].entries[j].title + '</a></h3>';
			html += '<div class="content">' + content + '</div>';
			html += '</div>';

			of.append(html)
		}
	}
}

