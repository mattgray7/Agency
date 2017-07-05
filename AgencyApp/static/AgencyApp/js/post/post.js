function addCreateCastingPost(formDict, formURL, formName, projectInfo){
	var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: -10px;' enctype='multipart/form-data'>";

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
	</table>
	*/
	formString += "<table style='width: 100%;'><tr>"
	var pictureURL = null;
	var mainInputs = ["title", "characterName", "project", "status", "shortCharacterDescription", "characterType"]
	var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; height: 280px; position:relative;'><div style='position: absolute; bottom:0; right: 0; margin-right: 5px;'><ul style='margin-bottom: -14px;'>";
	var mainInputsColumn = "<td class='editPostInputPanel' style='width: 40%; height: 280px; position: relative;'><ul style='position: absolute; bottom: 0; width: 97%; margin-bottom: -8px;'><h1 style='font-size: 2.8em; padding: 0em 0em 0.3em 0em;'>Edit Role</h1>";
	var pictureColumn = "<td style='max-width: 200px; height: 200px; text-align: center;'>";
	var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 25%; height: 600px; position:relative;'><div style='position: absolute; top:0; right: 0; margin-right: 5px; width: 90%; margin-top: 5px;'><ul>";
	var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 80%;height: 600px;'><div style='margin-top: 12px;'><ul>";

	var projectName = "";
	for(var i=0; i < formDict.length; i++){
		var name = "";
		var input = "";
		var hidden = true;
		var value = "";
		var label = "";
		var options = null;
		var extendedNumberOfRows = 0;
		var cancelOnclick = "";
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
			}else if(formElement["key"] == "numRows"){
				extendedNumberOfRows = formElement["value"]
			}else if(formElement["key"] == "cancelButtonOnclick"){
				cancelOnclick = formElement["value"]
			}
		}
		if(name === "postPicture"){
			pictureColumn += '<div id="postPicturePanel" class="postPicture" style="width: 80%; height: 93%; background: #000; margin: 0 auto;"><img id="postPictureImg" src="' + value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin: 0 auto; overflow: hidden;">' + input + "</div>";
			continue;
		}

		if(mainInputs.indexOf(name) > -1){
			// top left column
			mainLabelsColumn += "<li><label for='name'>" + label + "</label></li>";
			mainInputsColumn += "<li><div style='border: 2px solid #FFF; border-radius: 4px;'>"
			if(options){
				var selectForm = createSelectForm(formName, name + "SelectBar", options, value);
				mainInputsColumn += selectForm;
				mainInputsColumn += "<input type='hidden' name='" + name + "' id='" + name + "SelectInput' >";
			}else{
				mainInputsColumn += input;
			}
			mainInputsColumn += '</div></li>'; 
		}else if(!hidden){
			if(extendedNumberOfRows > 1){
				// stupid hack I hate myself right now
				otherLabelsColumn += "<li style='height:" + '' + extendedNumberOfRows*6.1 + 'px;' + "'><label for='name'>" + label + "</label></li>";
				// TODO replace newlines in description as it will break js
				otherInputsColumn += "<li><textarea rows='" + extendedNumberOfRows + "' name='" + name + "' form='" + formName + "' style='height:100px; font-size: 0.9em; width: 95%;'>" + value + "</textarea></li>";
			}else{
				otherLabelsColumn += "<label for='name'>" + label + "</label><br>";
				otherInputsColumn += "<li><div style='border: 2px solid #FFF; border-radius: 4px;'>"
				if(options){
					var selectForm = createSelectForm(formName, name + "SelectBar", options, value);
					otherInputsColumn += selectForm;
					otherInputsColumn += "<input type='hidden' name='" + name + "' id='" + name + "SelectInput' >";
				}else{
					otherInputsColumn += input;
				}
				otherInputsColumn += '</div></li>';
			}
		}else{
			otherInputsColumn += input;
		}	
	}
	
	// Add project link
	var projectTitle = null;
	var projectID = null;
	if(projectInfo != null){
		for(var i=0; i < projectInfo.length; i++){
			if(projectInfo[i]["key"] === "title"){
				projectTitle = projectInfo[i]["value"];
			}else if(projectInfo[i]["key"] === "projectID"){
				projectID = projectInfo[i]["value"];
			}
		}
	}
	mainInputsColumn += "<li><a>"
	if(projectTitle != null){
		mainInputsColumn += projectTitle;
	}else{
		mainInputsColumn += "Not specified";
	}
	mainInputsColumn += "</a></li>";


	mainLabelsColumn += "<li><label for='name'>Project</label></li></ul></div></td>";
	otherLabelsColumn += "</ul></div></td>";
	mainInputsColumn += "</ul></td>";
	otherInputsColumn += "</ul></div></td>";
	pictureColumn += "</td>";
	formString += "<tr>" + mainLabelsColumn + mainInputsColumn + pictureColumn + "</tr>"
	formString += "<tr>" + otherLabelsColumn + otherInputsColumn + "</tr></form>"
	formString += "<tr><td colspan='3' style='width: 100%; position:relative; height: 70px;'><div class='whiteButton blackHover' style='width: 36%; position:absolute; left: 0; bottom: 0; margin-bottom: 10px; margin-left: 20px;' onclick='" + cancelOnclick + "'> Cancel </div><div class='whiteButton blackHover' style='width: 36%; position:absolute; right: 0; bottom: 0; margin-bottom: 10px;' onclick='submitForm(" + '"' + formName + '");' + "'> Create Post</div></td></tr>";
	return formString;
}