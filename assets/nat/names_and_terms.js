var settings = {searchURL: 	'http://tree.lass.leg.bc.ca/nat-api/search'}, 
	settings2 = {searchURL: 'http://tree.lass.leg.bc.ca/nat-api/vsearch'},
	settings3 = {searchURL: 'http://tree.lass.leg.bc.ca/nat-api/insert'},
	settings4 = {searchURL: 'http://tree.lass.leg.bc.ca/nat-api/delete'},
	settings5 = {searchURL: 'http://tree.lass.leg.bc.ca/nat-api/get'},
	flag = false,
	status,
	categories,
	searchInput,
	currentid,
	category,
	selectItem;
	recentVerified = "@",
	recentStyles = "@ +style";


function processResults(results, time) {
	if (results.length < 3000){
		status = 'Loaded ' + results.length + ' results in ' + time.toFixed(2) + ' second(s)';
	}else{
		status ='There are more than 3000 results; ' + 'Loaded ' + results.length + ' results in ' + time.toFixed(2) + ' second(s)';

	}
	var catMap = {};
	$.each(results, function(i, one){
		catMap[one.category] = true;
	});
	categories = [];
	for (var key in catMap) {
		categories.push(key);
		categories.sort();
	}
}

function buildResults(results) {
	highlights();
	$('.result-title2').html('');
	
	var container = $('.results').html('');

	if($('[name="search"]').val()=='@'){
		$('.result-title').html('Recent Verifications');
	}else{
		$('.result-title').html('Search Results');
	}
	container.append($('<em>').attr('style','margin-left:10').html(
		status
	));

	var cats = $('<div>').addClass('cats');
	cats.append(
		$('<div>')
			.addClass('cat')
			.html('All')
			.click(function() {
				category = null;
				var tmp = $('[name="search"]').val().split(" +")[0];
				$('[name="search"]').val(tmp)
				search();
			})
	)
	

	$.each(categories, function(i, name) {
		var cat = $('<div>').addClass('cat')
			.html(name)
			.click(function() {
				category = this.innerHTML.replace('&amp;', '&');
				console.log(category)
				search();
			});
	
		if (name == category) {
			cat.addClass('class="font-weight-light"').attr("id","current");
		}else if(name == "style"){
			cat.css('background-color', '#82E0AA');
		}
		cats.append(cat);
	});
	container.append(cats);

	var list = $('<div>').addClass('list');
	$.each(results, function(i, one) {
		var item = $('<div>').addClass('item');
		var title = $('<div>').addClass('title');
		title.append($('<div>')
						.addClass('main-title').attr({"id":i})
						.html(one.verified)
						.click(function(){

							var temp=one.description?one.description_plaintext:"";
							var text = one.verified_plaintext+' - '+temp;
							text = text.replace(/<p>|<\/p>/g,'');
							console.log(text);
							copy(text);

							copySelected("default",results.length,i);

						}
					)
				);

		item.append(title);
		item.append($('<div>').addClass('desc').html(one.description ? one.description : "(No description)").attr({"type":"button","data-toggle":"modal","data-target":"#exampleModal"}).click(function(){
			
			$(".modal-1 .f0").html("<b>Item Id:</b> "+one.id);
			$(".modal-1 .f1").html("<b>Verified Name:</b> "+"<p>"+one.verified+"</p>");
			$(".modal-1 .f2").html("<b>Verified Alternates:</b> "+"<p>"+one.verified_alternates+"</p>");
			$(".modal-1 .f3").html("<b>Item Description:</b> "+"<p>"+one.description+"</p>");
			$(".modal-1 .f4").html("<b>Verification Source:</b> "+"<p>"+one.verification_source+"</p>");
			$(".modal-1 .f5").html("<b>Relationship:</b> "+"<p>"+one.relationship+"</p>");
			$(".modal-1 .f6").html("<b>Location:</b> "+"<p>"+one.location+"</p>");
			$(".modal-1 .f7").html("<b>Item Type:</b> "+"<p>"+one.category+"</p>");
			$(".modal-1 .f7-1").html("<b>Comments:</b> "+"<p>"+one.comments+"</p>");
			$(".modal-1 .f8").html("Created at <b>"+one.created_time+"</b> by <b>"+one.created_by+"</b>");
			$(".modal-1 .f9").html("Modified at <b>"+one.modified_time+"</b> by <b>"+one.modified_by+"</b>");
			$(".modal-1 #update-item").attr({"type":"button","data-toggle":"modal","data-target":".modal-3 #myModal"});
			selectItem = one;
		
		}));

		var alts = one.verified_alternates ? one.verified_alternates :''
		alts = alts.replace(/<br>|<p>|<\/p>/g,'')
		item.append($('<div>').addClass('alt-title').html(
			one.verified_alternates ? alts : '<p></p>'
			
		));			

		list.append(item);
	});
	container.append(list);
	highlights();

}
function buildRecentStyles(results){
	$('.result-title2').html('Recent Styles');

	var container = $('.results');

	var list = $('<div>').addClass('list verified-styles split2');
	list.append("<div>").attr({"padding-left":"50px"});;
	$.each(results, function(i, one) {
		var item = $('<div>').addClass('item');
		var title = $('<div>').addClass('title');
		
		title.append($('<div>')
						.addClass('recent-main-title').attr({"id":i})
						.html(one.verified)
						.click(function(){
							var temp=one.description?one.description_plaintext:"";
							
							var text = one.verified_plaintext+' - '+temp;
							text = text.replace(/<p>|<\/p>/g,'');

							console.log(text)
							copy(text)
							copySelected("default",results.length,i);

						}
					)
				);
		item.append(title);
		item.append($('<div>').addClass('desc').html(one.description ? one.description : "(No description)").attr({"type":"button","data-toggle":"modal","data-target":"#exampleModal"})
		.click(function(){$(".modal-1 .f0").html("<b>Item Id:</b> "+one.id);
		$(".modal-1 .f1").html("<b>Verified Name:</b> "+"<p>"+one.verified+"</p>");
		$(".modal-1 .f2").html("<b>Verified Alternates:</b> "+"<p>"+one.verified_alternates+"</p>");
		$(".modal-1 .f3").html("<b>Item Description:</b> "+"<p>"+one.description+"</p>");
		$(".modal-1 .f4").html("<b>Verification Source:</b> "+"<p>"+one.verification_source+"</p>");
		$(".modal-1 .f5").html("<b>Relationship:</b> "+"<p>"+one.relationship+"</p>");
		$(".modal-1 .f6").html("<b>Location:</b> "+"<p>"+one.location+"</p>");
		$(".modal-1 .f7").html("<b>Item Type:</b> "+"<p>"+one.category+"</p>");
		$(".modal-1 .f7-1").html("<b>Comments:</b> "+"<p>"+one.comments+"</p>");
		$(".modal-1 .f8").html("Created at <b>"+one.created_time+"</b> by <b>"+one.created_by+"</b>");
		$(".modal-1 .f9").html("Modified at <b>"+one.modified_time+"</b> by <b>"+one.modified_by+"</b>");
		$(".modal-1 #update-item").attr({"type":"button","data-toggle":"modal","data-target":".modal-3 #myModal"});
		selectItem = one;}));

		var alts = one.verified_alternates ? one.verified_alternates :''
		alts = alts.replace(/<br>|<p>|<\/p>/g,'')
		item.append($('<div>').addClass('alt-title').html(
			one.verified_alternates ? alts : '<p></p>'
			
		));			

		list.append(item);
	});
	container.append(list);

	
}
function buildRecentResults(results){
	$('.result-title').html('Recently Verified');


	var container = $('.results');

	var list = $('<div>').addClass('list verified-terms split');
	list.append("<div>").attr({"padding-left":"50px"});
	$.each(results, function(i, one) {
		var item = $('<div>').addClass('item');
		var title = $('<div>').addClass('title');
		
		title.append($('<div>')
						.addClass('recent-main-title').attr({"id":i})
						.html(one.verified)
						.click(function(){
							var temp=one.description?one.description_plaintext:"";
							

							var text = one.verified_plaintext+' - '+temp;
							text = text.replace(/<p>|<\/p>/g,'');

							console.log(text)
							copy(text)
							// copySelected("default",results.length,i);

						}
					)
				);
		item.append(title);
		item.append($('<div>').addClass('desc').html(one.description ? one.description : "(No description)").attr({"type":"button","data-toggle":"modal","data-target":"#exampleModal"}).click(function(){$(".modal-1 .f0").html("<b>Item Id:</b> "+one.id);
		$(".modal-1 .f1").html("<b>Verified Name:</b> "+"<p>"+one.verified+"</p>");
		$(".modal-1 .f2").html("<b>Verified Alternates:</b> "+"<p>"+one.verified_alternates+"</p>");
		$(".modal-1 .f3").html("<b>Item Description:</b> "+"<p>"+one.description+"</p>");
		$(".modal-1 .f4").html("<b>Verification Source:</b> "+"<p>"+one.verification_source+"</p>");
		$(".modal-1 .f5").html("<b>Relationship:</b> "+"<p>"+one.relationship+"</p>");
		$(".modal-1 .f6").html("<b>Location:</b> "+"<p>"+one.location+"</p>");
		$(".modal-1 .f7").html("<b>Item Type:</b> "+"<p>"+one.category+"</p>");
		$(".modal-1 .f7-1").html("<b>Comments:</b> "+"<p>"+one.comments+"</p>");
		$(".modal-1 .f8").html("Created at <b>"+one.created_time+"</b> by <b>"+one.created_by+"</b>");
		$(".modal-1 .f9").html("Modified at <b>"+one.modified_time+"</b> by <b>"+one.modified_by+"</b>");
		$(".modal-1 #update-item").attr({"type":"button","data-toggle":"modal","data-target":".modal-3 #myModal"});
		selectItem = one;}));
		
		var alts = one.verified_alternates ? one.verified_alternates :''
		alts = alts.replace(/<br>|<p>|<\/p>/g,'')
		item.append($('<div>').addClass('alt-title').html(
			one.verified_alternates ? alts : '<p></p>'
			
		));			

		list.append(item);
	});
	container.append(list);

}

function recentSearch(keyword){
	if(keyword==recentVerified){	
		$('[name="search"]').val(keyword);
		
		while(keyword[keyword.length-1]==' '){
			keyword=keyword.substr(0,keyword.length-1)

		}
		keyword=(keyword.replace(/\s+/g, ' '));
		
		searchInput = keyword;

		if(searchInput.indexOf(" +")>0){
			category=searchInput.split(" +")[1];
			searchTerm = searchInput.split(" +")[0];
			var url = settings.searchURL + '?s=' + encodeURIComponent(searchTerm);
			if (category) {
				url += '&c=' + encodeURIComponent(category);
			}
			console.log(url);

			$.ajax({
				url: url,
				success: function(resp) {
					processResults(resp.results, resp.time);
					buildRecentResults(resp.results);

				}
			});
			$('[name="search"]').val(searchTerm);

		}
		else{
		
			var url = settings.searchURL + '?s=' + encodeURIComponent($('[name="search"]').val());
			if (category) {
				url += '&c=' + encodeURIComponent(category);
		}
			console.log(url);

			$.ajax({
				url: url,
				success: function(resp) {
					processResults(resp.results, resp.time);
					buildRecentResults(resp.results);

			}
		});
		}
		$('[name="search"]').val('');
	}else{
		$('[name="search"]').val(keyword);
		while(keyword[keyword.length-1]==' '){
			keyword=keyword.substr(0,keyword.length-1)

		}
		keyword=(keyword.replace(/\s+/g, ' '));
		
		searchInput = keyword;

		if(searchInput.indexOf(" +")>0){
			category=searchInput.split(" +")[1];
			searchTerm = searchInput.split(" +")[0];
			var url = settings.searchURL + '?s=' + encodeURIComponent(searchTerm);
			if (category) {
				url += '&c=' + encodeURIComponent(category);
			}
			console.log(url);

			$.ajax({
				url: url,
				success: function(resp) {
					processResults(resp.results, resp.time);
					buildRecentStyles(resp.results);

				}
			});
			$('[name="search"]').val(searchTerm);
		}
		else{
		
			var url = settings.searchURL + '?s=' + encodeURIComponent($('[name="search"]').val());
			if (category) {
				url += '&c=' + encodeURIComponent(category);
		}
			console.log(url);

			$.ajax({
				url: url,
				success: function(resp) {
					processResults(resp.results, resp.time);
					buildRecentStyles(resp.results);
					console.log("done style")

			}
		});
		}
		$('[name="search"]').val('');
	}
	


}
function search() {
	if($('[name="search"]').val().length==0){
		return;
	}
	while($('[name="search"]').val()[$('[name="search"]').val().length-1]==' '){
		$('[name="search"]').val($('[name="search"]').val().substr(0,$('[name="search"]').val().length-1))

	}
	$('[name="search"]').val($('[name="search"]').val().replace(/\s+/g, ' ').replace(/b\.c\./gi,'b.c'));
	
	searchInput = $('[name="search"]').val()

	if(searchInput.indexOf(" +")>0){
		category=searchInput.split(" +")[1];
		searchTerm = searchInput.split(" +")[0];
		var url = settings.searchURL + '?s=' + encodeURIComponent(searchTerm);

		if (category) {
			url += '&c=' + encodeURIComponent(category);

		}
		
		let st = ($('#stemcheck').prop('checked')==(true)) ? "stemon" : "stemoff"
		url += '&m=' + encodeURIComponent(st)
		console.log(url);

		$.ajax({
			url: url,
			success: function(resp) {
				processResults(resp.results, resp.time);
				buildResults(resp.results);
			}
		});
		$('[name="search"]').val(searchTerm);
	}
	else{
	
		var url = settings.searchURL + '?s=' + encodeURIComponent($('[name="search"]').val());
		if (category) {
			console.log(category)

			url += '&c=' + encodeURIComponent(category);

		
		}
		let st = ($('#stemcheck').prop('checked')==(true)) ? "stemon" : "stemoff"
		url += '&m=' + encodeURIComponent(st)
		console.log(url);

		$.ajax({
			url: url,
			success: function(resp) {
				processResults(resp.results, resp.time);
				buildResults(resp.results);
		}
	});
	}
}

function vsearch() {
	if($('[name="search"]').val().length==0){
		return; 
	}
	while($('[name="search"]').val()[$('[name="search"]').val().length-1]==' '){
		$('[name="search"]').val($('[name="search"]').val().substr(0,$('[name="search"]').val().length-1))

	}
	$('[name="search"]').val($('[name="search"]').val().replace(/\s+/g, ' ').replace(/b\.c\./gi,'b.c'));
	searchInput = $('[name="search"]').val();
	if(searchInput.indexOf(" +")>0){
		category=searchInput.split(" +")[1];
		searchTerm = searchInput.split(" +")[0];
		var url = settings2.searchURL + '?s=' + encodeURIComponent(searchTerm);
		if (category) {
			url += '&c=' + encodeURIComponent(category);
		}

		let st = ($('#stemcheck').prop('checked')==(true)) ? "stemon" : "stemoff"
		url += '&m=' + encodeURIComponent(st)
		console.log(url);

		$.ajax({
			url: url,
			success: function(resp) {
				processResults(resp.results, resp.time);
				buildResults(resp.results);
			}
		});
				$('[name="search"]').val(searchTerm);

	}
	else{
	
		var url = settings2.searchURL + '?s=' + encodeURIComponent($('[name="search"]').val());
		if (category) {
			url += '&c=' + encodeURIComponent(category);
	}
<<<<<<< HEAD

		console.log(url);
=======
	
	let st = ($('#stemcheck').prop('checked')==(true)) ? "stemon" : "stemoff"
	url += '&m=' + encodeURIComponent(st)
	console.log(url);
>>>>>>> stemming

		$.ajax({
			url: url,
			success: function(resp) {
				processResults(resp.results, resp.time);
				buildResults(resp.results);
		}
	});
	}
	
}


function highlights(){
	if(flag){
		if($('[name="search"]').val()[0]=='!' || $('[name="search"]').val()[0]=='*'){
			$('.main-title, .desc, .alt-title').highlight($('[name="search"]').val().substring(1));
		}else if($('[name="search"]').val().indexOf("*")>0){
			$('.main-title, .desc, .alt-title').highlight($('[name="search"]').val().substring(0,$('[name="search"]').val().indexOf("*")));
		}else if($('[name="search"]').val()[0]=='"'){
			$('.main-title, .desc, .alt-title').highlight($('[name="search"]').val().substring(1,$('[name="search"]').val().length-1));

			// $('.main-title, .desc, .alt-title').highlight(tmp);

		}
		else{
			
			var tmp = ($('[name="search"]').val().split(" "))
			for (i in tmp){
				$('.main-title, .desc, .alt-title').highlight(tmp[i]);
			}
		}
		flag=false;
	}else if($('[name="search"]').val()==''){
		return		
	}
	else
	{
		$('.main-title, .desc, .alt-title').removeHighlight();
		flag=true;
	}



}


function insert(){
	var newItem;
	var utc = new Date().toJSON().slice(0,10).replace(/-/g,'-');
	var categories = ["brand names","events & awards","miscellaneous","modes of transport","non-english words & phrases","--first nations and indigenous peoples words & phrases","organizations","--crown corporations & government agencies","--health sector organizations","--first nations and indigenous peoples organizations","--k-12 organizations","--post-secondary organizations","--federal & other jurisdictions","--local governments & regional districts","--ministries","--unions","people","--fictional personal names & nicknames","--first nations and indigenous peoples leaders & officials & councillors & elders","--government & legislature & statutory officers employees","--mlas & elected officials","--parliamentary officials & statutory officers","places","--cities & towns","--fictional place names & nicknames","--parks","--physical infrastructure","--resource infrastructure","programs & initiatives","specialized terms and jargon","style","works","--accords & charters & conventions & declarations","--legislation","--reports & studies"];

	var container = $('.modal-2').html('');
	container.append($('<div>').addClass("modal fade").attr({"id":"myModal","tabindex":"-1", "role":"dialog", "aria-labelledby":"myModalLabel", "aria-hidden":"true"}));
	$('.modal-2 #myModal').append($("<div>").addClass("modal-dialog").attr({"role":"document","id":"modal-dialog2"}));
	$('.modal-2 #modal-dialog2').append($('<div>').addClass('modal-content').attr({"id":"modal-content2"}));
	$('.modal-2 #modal-content2').append($('<div>').addClass('modal-header').attr({"id":"modal-header2"}));
	$('.modal-2 #modal-header2').append($('<h4>').addClass("modal-title").attr({"id":"myModalLabel2"}).html("Create New Item"));
	$('.modal-2 #modal-content2').append($('<div>').addClass('modal-body').attr({"id":"modal-body2"}));
	$('.modal-2 #modal-body2').append($('<div>').addClass('row').attr({"id":"row2"}));
	
	$('.modal-2 #row2').append($('<label>').html("Title: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"titleinput"}));
	var reqOptions = {
		theme: 'snow',
		formats: [
			'bold',
			'italic',
			'underline',
			'link',
			'script',
		],
		modules: {
			toolbar: [
			['bold', 'italic', 'underline','link',{ 'script': 'sub'}, { 'script': 'super' }],
			],
		},
		placeholder: 'This is a required field.'
	}
	var options = {
		theme: 'snow',
		formats: [
			'bold',
			'italic',
			'underline',
			'link',
			'script',

		],
		modules: {
			toolbar: [
			['bold', 'italic', 'underline','link',{ 'script': 'sub'}, { 'script': 'super' }],
			],
		},
	}
	var options2 = {
		theme: 'snow',
		formats: [
			'bold',
			'italic',
			'underline',
			'link',
			'script',

		],
		modules: {
			toolbar: [
			[],
			],
		},

	}

	var quillTitle = new Quill("#titleinput",reqOptions);
	$('.modal-2 #row2').append($('<label>').html("Verified Alternates: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"titleinput2"}));
	var quillAlternate = new Quill("#titleinput2",options);
	

	$('.modal-2 #row2').append($('<label>').html("Description: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"descriptioninput"}));
	var quillDescription = new Quill("#descriptioninput",options);

	$('.modal-2 #row2').append($('<label>').html("Alphabetical Sort: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"alphasort"}));
	var quillAlphasort = new Quill("#alphasort",reqOptions);

	$('.modal-2 #row2').append($('<label>').html("Verification Source: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"verification"}));
	var quillVerification = new Quill("#verification",reqOptions);

	$('.modal-2 #row2').append($('<label>').html("Relationship: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"relationship"}));
	var quillRlationship = new Quill("#relationship",options2);

	$('.modal-2 #row2').append($('<label>').html("Location: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"location"}));
	var quillLocation = new Quill("#location",options2);

	$('.modal-2 #row2').append($('<label>').html("Comments: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"comments"}));
	var quillComments = new Quill("#comments",options2);

	$('.modal-2 #row2').append($('<label>').html("Item Type: ").addClass("input-labels"));
	$('.modal-2 #row2').append($('<div>').attr({"id":"category"}));
	$('.modal-2 #category').append($('<div>').addClass("btn-group"));
	$('.modal-2 .btn-group').append($('<button>').addClass("btn btn-default dropdown-toggle").attr({"type":"button","data-toggle":"dropdown","id":"selectCat"}).html("Select Category ").append($("<span>").addClass("caret")))
	$('.modal-2 .btn-group').append($('<ul>').addClass("dropdown-menu scrollable-menu").attr({"role":"menu","id":"dropdown"}));
	
	for (i in categories){
		$('.modal-2 #dropdown').append($('<li><a href="#">'+ categories[i] + '</a></li>'))

	}
	$('.modal-2 #dropdown > li').click(function(){
		$('.modal-2 #selectCat').text(($(this).text()).split('--')[1] ?($(this).text()).split('--')[1] : ($(this).text()) );
	})
	
	
	
	// var quillCategory = new Quill("#category",options2);
	
	$('.modal-2 #modal-content2').append($('<div>').addClass('modal-footer').attr({"id":"modal-footer2"}));
	$('.modal-2 #modal-footer2').append($('<button>').addClass("btn btn-primary").html("INSERT").click(function(){
		

		if(quillTitle.root.innerHTML=="<p><br></p>"||$('.modal-2 #selectCat').text()=="Select Category "||quillAlphasort.root.innerHTML=="<p><br></p>"||quillVerification.root.innerHTML=="<p><br></p>"){
			alert("Enter required information.")
			return
		}
		var tmp = quillDescription.root.innerHTML
		if (tmp =="<p><br></p>"){
			tmp = null;
		}
	
		newItem = {
			"verified":quillTitle.root.innerHTML,
			"verified_plaintext":quillTitle.getText().slice(0,-1),
			"verified_alternates":quillAlternate.root.innerHTML,
			"verification_source":quillVerification.getText().slice(0,-1),
			"description":tmp,
			"description_plaintext":quillDescription.getText().slice(0,-1),
			"comments":quillComments.getText().slice(0,-1),
			"relationship":quillRlationship.getText().slice(0,-1),
			"location":quillLocation.getText().slice(0,-1),
			"alpha_order":quillAlphasort.getText().slice(0,-1),
			"created_time":utc,
			"created_by":getCookie("user"),
			"modified_time":utc,
			"modified_by":getCookie("user"),
			"revised_time":utc,
			"category":$('#selectCat').text()

		};
		var url = "http://tree.lass.leg.bc.ca/nat-api/insert"
		$.post({
			type: "POST",
			url: url,
			contentType: "application/json",
			data: JSON.stringify(newItem)
		});
		$(".modal-2 #modal-footer2 #close-btn").click();
		
	}));

	$('.modal-2 #modal-footer2').append($('<button>').attr({"id":"close-btn","data-dismiss":"modal"}).addClass("btn btn-secondary").html("Cancel"))

}

function update(){
	var updateItem;
	var utc = new Date().toJSON().slice(0,10).replace(/-/g,'-');
	var categories =  ["brand names","events & awards","miscellaneous","modes of transport","non-english words & phrases","--first nations and indigenous peoples words & phrases","organizations","--crown corporations & government agencies","--health sector organizations","--first nations and indigenous peoples organizations","--k-12 organizations","--post-secondary organizations","--federal & other jurisdictions","--local governments & regional districts","--ministries","--unions","people","--fictional personal names & nicknames","--first nations and indigenous peoples leaders & officials & councillors & elders","--government & legislature & statutory officers employees","--mlas & elected officials","--parliamentary officials & statutory officers","places","--cities & towns","--fictional place names & nicknames","--parks","--physical infrastructure","--resource infrastructure","programs & initiatives","specialized terms and jargon","style","works","--accords & charters & conventions & declarations","--legislation","--reports & studies"];

	var reqOptions = {
		theme: 'snow',
		formats: [
			'bold',
			'italic',
			'underline',
			'link',
			'script'

		],
		modules: {
			toolbar: [
			['bold', 'italic', 'underline','link',{ 'script': 'sub'}, { 'script': 'super' }],
			],
			
		},
		placeholder: 'This is a required field.',
		
		
	}
	var options = {
		theme: 'snow',
		formats: [
			'bold',
			'italic',
			'underline',
			'link',
			'script',
			'code',
			'size',
			
		],
		modules: {
			toolbar: [
			['bold', 'italic', 'underline','link',{ 'script': 'sub'}, { 'script': 'super' }],
			],
		},
	}
	var options2 = {
		theme: 'snow',
		formats: [
			'bold',
			'italic',
			'underline',
			'link',
			'script'
		],
		modules: {
			toolbar: [
			[],
			],
		},

	}
			

	var container = $('.modal-3').html('');
	container.append($('<div>').addClass("modal fade").attr({"id":"myModal","tabindex":"-1", "role":"dialog", "aria-labelledby":"myModalLabel", "aria-hidden":"true"}));
	$('.modal-3 #myModal').append($("<div>").addClass("modal-dialog").attr({"role":"document","id":"modal-dialog2"}));
	$('.modal-3 #modal-dialog2').append($('<div>').addClass('modal-content').attr({"id":"modal-content2"}));
	$('.modal-3 #modal-content2').append($('<div>').addClass('modal-header').attr({"id":"modal-header2"}));
	$('.modal-3 #modal-header2').append($('<h4>').addClass("modal-title").attr({"id":"myModalLabel2"}).html("Update Item Entry"));
	$('.modal-3 #modal-content2').append($('<div>').addClass('modal-body').attr({"id":"modal-body2"}));
	$('.modal-3 #modal-body2').append($('<div>').addClass('row').attr({"id":"row2"}));
	
	$('.modal-3 #row2').append($('<label>').html("Title: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').html(selectItem.verified));
	$('.modal-3 #row2').append($('<div>').attr({"id":"titleinput"}));
	var quillTitle = new Quill(".modal-3 #titleinput",reqOptions);
	quillTitle.setContents({
		"ops":[
			{"insert":selectItem.verified.replace(/<p>|<\/p>|<br>/g, "")}
		]
	})
	

	$('.modal-3 #row2').append($('<label>').html("Verified Alternates: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').html(selectItem.verified_alternates));
	$('.modal-3 #row2').append($('<div>').attr({"id":"titleinput2"}));
	var quillAlternate = new Quill(".modal-3 #titleinput2",options);
	if (selectItem.verified_alternates){
		quillAlternate.setContents({
			"ops":[
				{"insert":selectItem.verified_alternates.replace(/<p>|<\/p>|<br>/g, "")}
			]
		})
	}

	$('.modal-3 #row2').append($('<label>').html("Description: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').html(selectItem.description));
	$('.modal-3 #row2').append($('<div>').attr({"id":"descriptioninput"}));
	var quillDescription = new Quill(".modal-3 #descriptioninput",options);
	if (selectItem.description){
		quillDescription.setContents({
			"ops":[
				{"insert":selectItem.description.replace(/<p>|<\/p>|<br>/g, "")}
			]
		})
	}

	$('.modal-3 #row2').append($('<label>').html("Alphabetical Sort: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').html(selectItem.alpha_order));
	$('.modal-3 #row2').append($('<div>').attr({"id":"alphasort"}));
	var quillAlphasort = new Quill(".modal-3 #alphasort",reqOptions);
	quillAlphasort.setContents({
		"ops":[
			{"insert":selectItem.alpha_order.replace(/<p>|<\/p>|<br>/g, "")}
		]
	})

	$('.modal-3 #row2').append($('<label>').html("Verification Source: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').html(selectItem.verification_source));
	$('.modal-3 #row2').append($('<div>').attr({"id":"verification"}));
	var quillVerification = new Quill(".modal-3 #verification",reqOptions);
	if (selectItem.verification_source){
		quillVerification.setContents({
			"ops":[
				{"insert":selectItem.verification_source.replace(/<p>|<\/p>|<br>/g, "")}
			]
		})
	}

	$('.modal-3 #row2').append($('<label>').html("Relationship: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').html(selectItem.relationship));
	$('.modal-3 #row2').append($('<div>').attr({"id":"relationship"}));
	var quillRlationship = new Quill(".modal-3 #relationship",options2);
	if(selectItem.relationship){
		quillRlationship.setContents({
			"ops":[
				{"insert":selectItem.relationship.replace(/<p>|<\/p>|<br>/g, "")}
			]
		})
	}

	$('.modal-3 #row2').append($('<label>').html("Location: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').html(selectItem.location));
	$('.modal-3 #row2').append($('<div>').attr({"id":"location"}));
	var quillLocation = new Quill(".modal-3 #location",options2);
	if (selectItem.location){
		quillLocation.setContents({
			"ops":[
				{"insert":selectItem.location.replace(/<p>|<\/p>|<br>/g, "")}
			]
		})
	}
	$('.modal-3 #row2').append($('<label>').html("Comments: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').html(selectItem.comments));
	$('.modal-3 #row2').append($('<div>').attr({"id":"comments"}));
	var quillComments = new Quill(".modal-3 #comments",options2);
	if (selectItem.comments){
		quillComments.setContents({
			"ops":[
				{"insert":selectItem.comments.replace(/<p>|<\/p>|<br>/g, "")}
			]
		})
	}
	$('.modal-3 #row2').append($('<label>').html("Item Type: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').attr({"id":"category"}));
	$('.modal-3 #category').append($('<div>').addClass("btn-group"));
	$('.modal-3 .btn-group').append($('<button>').addClass("btn btn-default dropdown-toggle").attr({"type":"button","data-toggle":"dropdown","id":"selectCat"}).html(selectItem.category).append($("<span>").addClass("caret")))
	$('.modal-3 .btn-group').append($('<ul>').addClass("dropdown-menu scrollable-menu").attr({"role":"menu","id":"dropdown"}));
	
	$('.modal-3 #row2').append($('<label>').html("Status: ").addClass("input-labels"));
	$('.modal-3 #row2').append($('<div>').attr({"id":"status"}));
	$('.modal-3 #status').append($('<div>').addClass("btn-group"));
	$('.modal-3 #status .btn-group').append($('<button>').addClass("btn btn-default dropdown-toggle").attr({"type":"button","data-toggle":"dropdown","id":"selectStat"}).html("Show").append($("<span>").addClass("caret")))

	$('.modal-3 #status .btn-group').append($('<ul>').addClass("dropdown-menu scrollable-menu").attr({"role":"menu","id":"dropdown"}));

	$('.modal-3 #status #dropdown').append($('<li><a href="#">'+ "Ignore" + '</a></li>'))
	$('.modal-3 #status #dropdown').append($('<li><a href="#">'+ "Show" + '</a></li>'))
	$('.modal-3 #status #dropdown > li').click(function(){
		$('.modal-3 #status #selectStat').text(($(this).text()));
	})

	for (i in categories){
		$('.modal-3 #category #dropdown').append($('<li><a href="#">'+ categories[i] + '</a></li>'))

	}
	$('.modal-3 #category #dropdown > li').click(function(){
		$('.modal-3 #category #selectCat').text(($(this).text()).split('--')[1] ?($(this).text()).split('--')[1] : ($(this).text()) );
	})
	
	$('.modal-3 #modal-content2').append($('<div>').addClass('modal-footer').attr({"id":"modal-footer2"}));
	$('.modal-3 #modal-footer2').append($('<button>').addClass("btn btn-primary").html("Update").click(function(){
		

		if(quillTitle.root.innerHTML=="<p><br></p>"||$('.modal-3 #selectCat').text()=="Select Category "||quillAlphasort.root.innerHTML=="<p><br></p>"||quillVerification.root.innerHTML=="<p><br></p>"){
			alert("Enter required information.")
			return
		}

		var tmp = quillDescription.root.innerHTML
		if (tmp =="<p><br></p>"){
			tmp = null;
		}
		if ($('.modal-3 #status #selectStat').text()=="Ignore"){
			let t = new Date();
			t.setDate(t.getDate()-3);
			utc = t.toJSON().slice(0,10).replace(/-/g,'-');
		}
		updateItem = {
			"id":selectItem.id,
			"verified":quillTitle.root.innerHTML,
			"verified_plaintext":quillTitle.getText().slice(0,-1),
			"verified_alternates":quillAlternate.root.innerHTML,
			"verification_source":quillVerification.getText().slice(0,-1),
			"description":tmp,
			"description_plaintext":quillDescription.getText().slice(0,-1),
			"comments":quillComments.getText().slice(0,-1),
			"relationship":quillRlationship.getText().slice(0,-1),
			"location":quillLocation.getText().slice(0,-1),
			"alpha_order":quillAlphasort.getText().slice(0,-1),
			"modified_time":utc,
			"modified_by":getCookie('user'),
			"revised_time":utc,
			"category":$('#selectCat').text()

		};
		$.post({
			type: "POST",
			url: "http://tree.lass.leg.bc.ca/nat-api/update",
			contentType: "application/json",
			data: JSON.stringify(updateItem)
		});
		$(".modal-3 #modal-footer2 #close-btn").click();
		
	}));




	$('.modal-3 #modal-footer2').append($('<button>').attr({"id":"close-btn","data-dismiss":"modal"}).addClass("btn btn-secondary").html("Cancel"))

	$('#search').click()

}

function deleteItem(){

	// console.log($(".f0").html().split('</b> ')[1])
		if(confirm("Confirm to delete item " +$(".f0").html().split('</b> ')[1])){
			var url = settings4.searchURL + '?' + $(".f0").html().split('</b> ')[1];
			$.ajax({
				url: url,
				success: function(resp) {
					processResults(resp.results, resp.time);
					buildResults(resp.results);
				}
			});
			$(".modal-1 #btn-modify").click()
			$('#search').click()

	
		}else{return}
}
//update for copy selected
function copySelected(mode,resultLength,id){

	if (mode=='default'){
		$('.results .item #'+id).css("border-left","6px solid red");

		for (var i =0; i <resultLength; i++){
			if (i != id){
				$('.item #'+i).css("border-style","none");

			}
		}
	
	}

}
//update copy for IE
function copy(itemString)
{
    var aux = document.createElement("div");
    aux.setAttribute("contentEditable", true);
    aux.innerHTML = itemString
    document.body.appendChild(aux);
    window.getSelection().selectAllChildren(aux);
    document.execCommand("copy");
    document.body.removeChild(aux);
    console.log("COPY");
}

//update auth
function getCookie(name){
	var value = "; " + document.cookie;
	var parts = value.split("; " + name +"=");
	if (parts.length == 2) return parts.pop().split(";").shift();
}
//update auth
function checkMainPage(){
	if (getCookie('group') == "etls" || getCookie('group') == "researchers" ){

		$('#insert, #deleteOne, #update-item').show();

	}else{
		$('#insert, #deleteOne, #update-item').hide()
	}
	
	var userInfo1 = (getCookie("user"))?getCookie("user"):"Unrecognized";
	var userInfo = "Welcome, "+userInfo1;
	console.log(userInfo);
	$('#welcome').html(userInfo);
}




//update auth
function clearCookie(){
	var keys = document.cookie.match(/[^ =;]+(?=\=)/g);
	console.log("enter")
	if(keys) {
		for(var i = keys.length; i--;)
			document.cookie = keys[i] + '=0;expires=' + new Date(0).toUTCString()
			console.log("clear")
	}
	location.reload();
}

// update auth
function checkAuth(){
	var credentials;
	var authorized={
		username:null,
		usergroup:null,
	};
	credentials = {
		username: $('#username').val(),
		password: $('#password').val(),
	}
	$.post({
		type: "POST",
		url: "http://tree.lass.leg.bc.ca/nat-api/auth",
		contentType: "text",
		data: JSON.stringify(credentials),
		complete: function(resp) {
			authorized.username = resp.responseJSON.full_name;
			authorized.usergroup = resp.responseJSON.groups;
			
			document.cookie = "user=" + authorized.username;
			document.cookie = "group=" + authorized.usergroup;

			console.log(resp);
			console.log(authorized.username+" "+authorized.usergroup);
			console.log("cookie is: "+document.cookie);
			location.reload();
		}

	});
}

// update auth
function userAuth(){
	
	$('#auth').attr({"type":"button","data-toggle":"modal","data-target":"#user-auth"})
	
	$('.modal-4 #log-in-btn').click(checkAuth);

	$('.modal-4 #password').keypress(function(e){
		if (e.which ===13){
			checkAuth();
		}
	});
}

function toTheTop(){


	function scrollFunction() {
		if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
			document.getElementById("myBtn").style.display = "block";
		} else {
			document.getElementById("myBtn").style.display = "none";
		}

	}

	// When the user clicks on the button, scroll to the top of the document
	
	window.onscroll = function() {scrollFunction()};
}

function topFunction() {
	$('html, body').animate({ scrollTop: 0 }, 'fast');
	$("#textbox1").focus();
}

function logging(){
	window.alert(
		"'Top' button now selects the textarea automatically. \n"
	)
}


toTheTop();
userAuth();

$('#home').click(function(){location.reload()})
$('#logout').click(clearCookie);
$('.result').ready(function(){
					checkMainPage();
					recentSearch(recentVerified);
					recentSearch(recentStyles);
				
				})




$('#search').click(search);
$('#vsearch').click(vsearch);
$('#textbox1').keypress(function(e){
	if (e.which ===13){
		search();
	}
});
$('#highlightbutton').click(highlights);
$('#insert').click(insert);
$('#textbox1').click(function(){category=null});
$('.modal-1 #update-item').click(update);
$('.modal-1 #deleteOne').click(deleteItem);
