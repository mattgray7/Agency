function addCreateCastingPost(formDict, formURL, formName){
	var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none;'>";

	//Add table
	/*
	<table>
		<tr>
			<td> top left input labels
			<td> top/main input boxes
			<td> Edit picture panel
		</tr>
		<tr>
			<td> left input labels
			<td colspan=2> rest of content
		</tr>
	</tabl>
	*/
	formString += "<table style='width: 100%;'><tr>"
	var pictureURL = null;
	var mainInputs = ["title", "characterName", "project", "status", "shortCharacterDescription"]
	var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; position:relative;'><div style='position: absolute; bottom:0; right: 0; margin-right: 5px; margin-bottom: -8px;'>";
	var mainInputsColumn = "<td class='editPostInputPanel' style='width: 40%; position: relative;'><ul style='position: absolute; bottom: 0; width: 97%; margin-bottom: -8px;'><h1 style='font-size: 2.5em; padding: 0em 0em 0.2em 0em;'>Edit Role</h1>";
	var pictureColumn = "<td style='max-width: 200px; height: 200px; border: 2px solid #000'>";
	var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; position:relative;'><div style='position: absolute; top:0; right: 0; margin-right: 5px;'>";
	var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 80%;'><ul>";
	for(var i=0; i < formDict.length; i++){
		var name = "";
		var input = "";
		var hidden = true;
		var value = "";
		var label = "";
		var options = null;
		for(var j=0; j < formDict[i].length; j++){
			var formElement = formDict[i][j];
			if(formElement["key"] == "name"){
				name = formElement["value"];
			}else if(formElement["key"] == "input"){
				input = formElement["value"];
			}else if(formElement["key"] == "hidden"){
				hidden = formElement["value"];
			}else if(formElement["key"] == "value"){	
				value = formElement["value"]
			}else if(formElement["key"] == "label"){
				label = formElement["value"]
			}else if(formElement["key"] == "options"){
				options = formElement["value"];
			}
		}
		if(name === "postPicture"){
			//pictureColumn += '<div style="min-width: 300px; max-width: 300px;"><div id="postPicturePanel" class="postPicture" style="width: 100%; height: 300px; "><div style="max-width:100%; max-height: 400px; min-width: 100%; min-height: 300px; background: #000; border: 1px solid #FFF; border-radius:3px; position: relative; overflow: hidden; margin-top: -2px; margin-left: -7px;"><div id="postPicture" style="padding: 3em 0em 0em 0em"><img id="postPictureImg" src="' + value + '" style="min-width: 100%; max-width:100%; max-height:100%;"/></div></div></div></div>';
			pictureColumn += '<div id="postPicturePanel" class="postPicture" style="width: 98%; height: 100%; background: #000;"><img id="postPictureImg" src="' + value + '" style="max-width:100%; max-height:100%;"/></div>'
			continue;
		}

		if(mainInputs.indexOf(name) > -1){
			console.log(name)
			console.log(options)
			// top left column
			mainLabelsColumn += "<label for='name'>" + label + "</label><br>";
			mainInputsColumn += "<li><div style='border: 2px solid #FFF; border-radius: 4px;'>"
			if(options){
				console.log(value)
				var selectForm = createSelectForm(formName, name + "SelectBar", options, value);
				mainInputsColumn += selectForm;
			}else{
				mainInputsColumn += input;
			}
			mainInputsColumn += '</div></li>'; 
		}else if(!hidden){
			otherLabelsColumn += "<label for='name'>" + label + "</label><br>";
			otherInputsColumn += "<li><div style='border: 2px solid #FFF; border-radius: 4px;'>"
			if(options){
				var selectForm = createSelectForm(formName, name + "SelectBar", options, value);
				otherInputsColumn += selectForm;
			}else{
				otherInputsColumn += input;
			}
			otherInputsColumn += '</div></li>'; 
		}else{
			otherInputsColumn += input;
		}

		/*if(!hidden){
			if(name === "description"){
				inputsColumn += "<textarea cols='100' rows ='20' name='description' form='" + formName + "' style='height:100px; font-size: 0.9em;'>" + value + "</textarea></li>"
			}else{
				inputsColumn += "<div style='background: #efefef; border: 2px solid #FFF; border-radius: 4px;'>"
				if(options){
					var selectForm = createSelectForm(formName, name + "SelectBar", options, value);
					inputsColumn += selectForm;
				}else{
					inputsColumn += input;
				}
				inputsColumn += '</div>'; 
			}
		}else{
			inputsColumn += input;
		}*/		
	}
	mainLabelsColumn += "</div></td>";
	otherLabelsColumn += "</div></td>";
	mainInputsColumn += "</ul></td>";
	otherInputsColumn += "</ul></td>";
	pictureColumn += "</td>";
	formString += "<tr>" + mainLabelsColumn + mainInputsColumn + pictureColumn + "</tr>"
	formString += "<tr>" + otherLabelsColumn + otherInputsColumn + "</tr></form>"
	formString += "<tr><td colspan='3' style='width: 100%; position:relative; height: 100px;'><div class='whiteButton blackHover' style='width: 36%; position:absolute; left: 0; bottom: 0; margin-bottom: 10px;'> Cancel </div><div class='whiteButton blackHover' style='width: 36%; position:absolute; right: 0; bottom: 0; margin-bottom: 10px'> Create Post</div></td></tr>";
	return formString;
}