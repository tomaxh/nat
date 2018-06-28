var settings = {searchURL: 'http://localhost:7990/search'}, 
	status,
	categories,
	category;

function processResults(results, time) {
	status = 'Loaded ' + results.length + ' results in ' + time.toFixed(2) + ' second(s)';
	
	var catMap = {};
	$.each(results, function(i, one){
		catMap[one.category] = true;
	});
	categories = [];
	for (var key in catMap) {
		categories.push(key);
	}
}

function buildResults(results) {
	var container = $('.results').html('');
	container.append($('<em>').html(
		status
	));

	var cats = $('<div>').addClass('cats');
	cats.append(
		$('<div>')
			.addClass('cat')
			.html('All')
			.click(function() {
				category = null;
				search();
			})
	)
	$.each(categories, function(i, name) {
		var cat = $('<div>').addClass('cat')
			.html(name)
			.click(function() {
				category = this.innerHTML.replace('&amp;', '&');
				search();
			});
		if (name == category) {
			cat.addClass('current');
		}
		cats.append(cat);
	});
	container.append(cats);
	
	var list = $('<div>').addClass('list');
	$.each(results, function(i, one) {
		var item = $('<div>').addClass('item');
		
		var title = $('<div>').addClass('title');
		title.append($('<div>').addClass('main-title').html(one.verified));
		title.append($('<div>').addClass('alt-title').html(
			one.verified_alternates ? one.verified_alternates : '(no alternates)'
		));
		title.append($('<div>').addClass('badge').html(one.category));

		item.append(title);
		item.append($('<div>').addClass('desc').html(one.description));

		list.append(item);
	});
	container.append(list);
}

function search(searchTerm) {
	var url = settings.searchURL + '?s=' + encodeURIComponent($('[name="search"]').val());
	if (category) {
		url += '&c=' + encodeURIComponent(category);
	}
	console.log(url);

	$.ajax({
		url: url,
		success: function(resp) {
			processResults(resp.results, resp.time);
			buildResults(resp.results);
		}
	});
}

$('.search').click(search);
