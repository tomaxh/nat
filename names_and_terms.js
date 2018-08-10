var settings = {searchURL: 'http://localhost:7990/search'}, 
	settings2 = {searchURL: 'http://localhost:7990/vsearch'},
	settings3 = {searchURL: 'http://localhost:7990/insert'},
	flag = false,
	status,
	categories,
	searchInput,
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
	highlights();

	var container = $('.results').html('');
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
				search();
			});
		if (name == category) {
			cat.addClass('class="font-weight-light"').attr("id","current");
		}
		cats.append(cat);
	});
	container.append(cats);

	var list = $('<div>').addClass('list');
	$.each(results, function(i, one) {
		var item = $('<div>').addClass('item');
		var title = $('<div>').addClass('title');
		
		title.append($('<div>')
						.addClass('main-title')
						.html(one.verified)
						.click(function(){
							var temp=one.description?one.description:"(No Description)";
							
							var text = one.verified+'  -  '+temp;
							console.log(text)
							var dt = new clipboard.DT();
							dt.setData("text/html",text);
							clipboard.write(dt);
						}
					)
				);

		item.append(title);
		item.append($('<div>').addClass('desc').html(one.description ? one.description : "(No description)").attr({"type":"button","data-toggle":"modal","data-target":"#exampleModal"}).click(function(){
			$(".f0").html("<b>Item Id:</b> "+one.id);
			$(".f1").html("<b>Verified Name:</b> "+one.verified);
			$(".f2").html("<b>Verified Alternates:</b> "+one.verified_alternates);
			$(".f3").html("<b>Item Description:</b> "+one.description);
			$(".f4").html("<b>Verification Source:</b> "+one.verification_source);
			$(".f5").html("<b>Relationship:</b> "+one.relationship);
			$(".f6").html("<b>Location:</b> "+one.location);
			$(".f7").html("<b>Item Type:</b> "+one.category);
			$(".f8").html("Created at <b>"+one.created_time+"</b> by <b>"+one.created_by+"</b>");
			$(".f9").html("Modified at <b>"+one.modified_time+"</b> by <b>"+one.modified_by+"</b>");

			update(one)

		
		}));
		item.append($('<div>').addClass('alt-title').html(
			one.verified_alternates ? one.verified_alternates : '(no alternates)'
		));
		list.append(item);
	});
	container.append(list);
	highlights();
}

function search() {
	if($('[name="search"]').val().length==0){
		return; 
	}
	while($('[name="search"]').val()[$('[name="search"]').val().length-1]==' '){
		$('[name="search"]').val($('[name="search"]').val().substr(0,$('[name="search"]').val().length-1))

	}
	$('[name="search"]').val($('[name="search"]').val().replace(/\s+/g, ' '));
	
	searchInput = $('[name="search"]').val();

	if(searchInput.includes(" +")){
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
				buildResults(resp.results);
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
	$('[name="search"]').val($('[name="search"]').val().replace(/\s+/g, ' '));
	searchInput = $('[name="search"]').val();
	if(searchInput.includes(" +")){
		category=searchInput.split(" +")[1];
		searchTerm = searchInput.split(" +")[0];
		var url = settings2.searchURL + '?s=' + encodeURIComponent(searchTerm);
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
				$('[name="search"]').val(searchTerm);

	}
	else{
	
		var url = settings2.searchURL + '?s=' + encodeURIComponent($('[name="search"]').val());
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
	
}

function insertItem(){
	var tt = "dasd"
	mdata={
		"verified":"New test 731",
		"verified_plaintext":"Tester2 inserted by new API.",
		"alpha_order":"Tester1 inderted aplha_order.",
		"category":"people",
		"verified_alternates":null,
		"verification_source":null,
		"description":"<b>The testing item 2 inserted by REQUEST and POST method",
		"description_plaintext":"The testing item inserted by REQUEST and POST method",
		"comments":null,
		"relationship":"bibi",
		"location":null,
		"created_time":"2012-01-31",
		"created_by":"Tom",
		"modified_time":null,
		"modified_by":null,
		"revised_time":null
	}
	/*
	$.post({
		type: "POST",
		url: 'http://localhost:7990/insert',
		contentType: "application/json",
		data: JSON.stringify(mdata)
	  });
	  */
	  console.log(JSON.stringify(mdata))
	
	
}

function highlights(){
	if(flag){
		if($('[name="search"]').val()[0]=='!' || $('[name="search"]').val()[0]=='*'){
			$('.main-title, .desc, .alt-title').highlight($('[name="search"]').val().substring(1,));
		}else if($('[name="search"]').val().indexOf("*")>0){
			$('.main-title, .desc, .alt-title').highlight($('[name="search"]').val().substring(0,$('[name="search"]').val().indexOf("*")));
		}else if($('[name="search"]').val()[0]=='?'){
			var tmp = ($('[name="search"]').val().substring(1,).split(" "))
			for (i in tmp){
				$('.main-title, .desc, .alt-title').highlight(tmp[i]);
			}
			// $('.main-title, .desc, .alt-title').highlight(tmp);

		}
		else{
			$('.main-title, .desc, .alt-title').highlight($('[name="search"]').val());
		}
		flag=false;
	}else
	{
		$('.main-title, .desc, .alt-title').removeHighlight();
		flag=true;
	}
}


function insert(){
	var newItem;
	var utc = new Date().toJSON().slice(0,10).replace(/-/g,'-');
	var container = $('.modal-2').html('');
	container.append($('<div>').addClass("modal fade").attr({"id":"myModal","tabindex":"-1", "role":"dialog", "aria-labelledby":"myModalLabel", "aria-hidden":"true"}));
	$('#myModal').append($("<div>").addClass("modal-dialog").attr({"role":"document","id":"modal-dialog2"}));
	$('#modal-dialog2').append($('<div>').addClass('modal-content').attr({"id":"modal-content2"}));
	$('#modal-content2').append($('<div>').addClass('modal-header').attr({"id":"modal-header2"}));
	$('#modal-header2').append($('<h4>').addClass("modal-title").attr({"id":"myModalLabel2"}).html("Create New Item"));
	$('#modal-content2').append($('<div>').addClass('modal-body').attr({"id":"modal-body2"}));
	$('#modal-body2').append($('<div>').addClass('row').attr({"id":"row2"}));
	$('#row2').append($('<button>').addClass("btn btn-primary").html("Print").click(function(){
		var htmltext = quillTitle.root.innerHTML;
		var htmltext2 = quillAlternate.root.innerHTML;
		var htmltext3 = quillDescription.root.innerHTML;
		var htmltext4 = quillAlphasort.root.innerHTML;
		var htmltext5 = quillVerification.root.innerHTML;
		var htmltext6 = quillRlationship.root.innerHTML;
		var htmltext7 = quillLocation.root.innerHTML;
		var htmltext8 = quillComments.root.innerHTML;
		var htmltext9 = quillCategory.root.innerHTML;

		console.log(htmltext+":"+quillTitle.getText()+'\n'+htmltext2+":"+quillAlternate.getText()+'\n'+htmltext3+":"+quillDescription.getText()+'\n'+
		htmltext4+":"+quillAlphasort.getText()+'\n'+
		htmltext5+":"+quillVerification.getText()+'\n'+
		htmltext6+":"+quillRlationship.getText()+'\n'+
		htmltext7+":"+quillLocation.getText()+'\n'+
		htmltext8+":"+quillComments.getText()+'\n'+
		htmltext9+":"+quillCategory.getText()+'\n'+
		utc+'\n'+JSON.stringify(newItem)
		);
	

	}));


	$('#row2').append($('<label>').html("Title: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"titleinput"}));
	var options = {
		theme: 'snow',
		formats: [
			'bold',
			'italic',
			'underline',
			'link'
		  ],
		modules: {
			toolbar: [
			  ['bold', 'italic', 'underline','link'],
			],
		},
	}
	var options2 = {
		theme: 'snow',
		formats: [
			'bold',
			'italic',
			'underline',
			'link'
		  ],
		  modules: {
			toolbar: [
			  [],
			],
		},

	}

	var quillTitle = new Quill("#titleinput",options);
	
	$('#row2').append($('<label>').html("Verified Alternates: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"titleinput2"}));
	var quillAlternate = new Quill("#titleinput2",options);

	$('#row2').append($('<label>').html("Description: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"descriptioninput"}));
	var quillDescription = new Quill("#descriptioninput",options);

	$('#row2').append($('<label>').html("Alphabetical Sort: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"alphasort"}));
	var quillAlphasort = new Quill("#alphasort",options2);

	$('#row2').append($('<label>').html("Verification Source: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"verification"}));
	var quillVerification = new Quill("#verification",options2);

	$('#row2').append($('<label>').html("Relationship: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"relationship"}));
	var quillRlationship = new Quill("#relationship",options2);

	$('#row2').append($('<label>').html("Location: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"location"}));
	var quillLocation = new Quill("#location",options2);

	$('#row2').append($('<label>').html("Comments: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"comments"}));
	var quillComments = new Quill("#comments",options2);

	$('#row2').append($('<label>').html("Item Type: ").addClass("input-labels"));
	$('#row2').append($('<div>').attr({"id":"category"}));
	var quillCategory = new Quill("#category",options2);
	
	$('#modal-content2').append($('<div>').addClass('modal-footer').attr({"id":"modal-footer2"}));
	$('#modal-footer2').append($('<button>').addClass("btn btn-primary").html("iNSERT").click(function(){
		
		newItem = {
			"verified":quillTitle.root.innerHTML,
			"verified_plaintext":quillTitle.getText().slice(0,-1),
			"verified_alternates":quillAlternate.getText().slice(0,-1),
			"verification_source":quillVerification.getText().slice(0,-1),
			"description":quillDescription.root.innerHTML,
			"description_plaintext":quillDescription.getText().slice(0,-1),
			"comments":quillComments.getText().slice(0,-1),
			"relationship":quillRlationship.getText().slice(0,-1),
			"location":quillLocation.getText().slice(0,-1),
			"alpha_order":quillAlphasort.getText().slice(0,-1),
			"created_time":utc,
			"created_by":"Tom",
			"modified_time":utc,
			"modified_by":"Tom",
			"revised_time":utc,
			"category":quillCategory.getText().toLowerCase().slice(0,-1)

		};
		$.post({
			type: "POST",
			url: 'http://localhost:7990/insert',
			contentType: "application/json",
			data: JSON.stringify(newItem)
		  });
	}));

}

function update(itemData){
	$(".u1").html(itemData.verified)
	$(".u2").html(itemData.description);

	$("#update-item").click(function(){
			
		})


}


$('#search').click(search);
$('#vsearch').click(vsearch);
$('#textbox1').keypress(function(e){
	if (e.which ===13){
		search();
	}
});
$('#highlightbutton').click(highlights);
$('#insert').click(insert);
$('#kkbtn').attr({"type":"button","data-toggle":"modal","data-target":"#exampleModal2"});
$('#textbox1').click(function(){category=null})