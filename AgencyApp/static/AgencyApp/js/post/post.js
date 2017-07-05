function addCreateCastingPost(formDict, formURL, formName, projectInfo){
	var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: -10px;' enctype='multipart/form-data'>";
	formString += "<table style='width: 100%;'><tr>"

	// Fill post picture string
	var pictureField = formDict["postPicture"];
	var pictureColumn = '<td style="max-width: 200px; height: 200px; text-align: center;"><div id="postPicturePanel" class="postPicture" style="width: 80%; height: 93%; background: #000; margin: 0 auto;"><img id="postPictureImg" src="' + pictureField.value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin: 0 auto; overflow: hidden;">' + pictureField.input + "</div></td>";

	// Fill text content
	var sectionMap = {"Details": ["title", "characterType", "status"],
					  "Production": ["paid", "hoursPerWeek", "startDate", "endDate"],
					  "The Role": ["characterName", "shortCharacterDescription", "description", "skills", "languages"],  
					  "Physical": ["hairColor", "eyeColor", "complexion", "height", "build", "gender", "ageRange"]}
	var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; height: 280px; position:relative;'><div style='position: absolute; bottom:0; right: 0; margin-right: 5px;'><ul style='margin-bottom: -14px;'>";
	var mainInputsColumn = "<td class='editPostInputPanel' style='width: 40%; height: 280px; position: relative;'><ul style='position: absolute; bottom: 0; width: 97%; margin-bottom: -8px;'><h1 style='font-size: 2.8em; padding: 0em 0em 0.3em 0em;'>Edit Role</h1>";
	var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 25%; height: 600px; position:relative;'><div style='position: absolute; top:0; right: 0; margin-right: 5px; width: 90%; margin-top: 5px;'><ul>";
	var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 80%;height: 600px;'><div style='margin-top: 12px;'><ul>";
	for(sectionTitle in sectionMap){
		var fieldList = sectionMap[sectionTitle];
		var sectionInputTableElement = null;
		var sectionLabelTableElement = null;
		if(sectionTitle === "Details" || sectionTitle === "Production"){
			sectionLabelTableElement = mainLabelsColumn;
			sectionInputTableElement = mainInputsColumn;
		}else{
			sectionLabelTableElement = otherLabelsColumn;
			sectionInputTableElement = otherInputsColumn;
		}

		for(i in fieldList){
			var fieldName = sectionMap[sectionTitle][i];
			var field = formDict[fieldName];
			if(!field.hidden){
				if(field.numRows > 1){
					// stupid hack I hate myself right now
					sectionLabelTableElement += "<li style='height:" + '' + field.numRows*6.1 + 'px;' + "'><label for='name'>" + field.label + "</label></li>";
					// TODO replace newlines in description as it will break js
					sectionInputTableElement += "<li><textarea rows='" + field.numRows + "' name='" + field.name + "' form='" + formName + "' style='height:100px; font-size: 0.9em; width: 94.5%;'>" + field.value + "</textarea></li>";
				}else{
					sectionLabelTableElement += "<label for='name'>" + field.label + "</label><br>";
					sectionInputTableElement += "<li><div style='border: 2px solid #FFF; border-radius: 4px;'>"
					if(field.options){
						var selectForm = createSelectForm(formName, field.name + "SelectBar", field.options, field.value);
						sectionInputTableElement += selectForm;
						sectionInputTableElement += "<input type='hidden' name='" + field.name + "' id='" + field.name + "SelectInput' >";
					}else{
						sectionInputTableElement += field.input;
					}
					sectionInputTableElement += '</div></li>';
				}
			}else if(field.input != null && field.input.length > 0){
				sectionInputTableElement += field.input;
			}
		}
		if(sectionTitle === "Details" || sectionTitle === "Production"){
			mainLabelsColumn = sectionLabelTableElement;
			mainInputsColumn = sectionInputTableElement;
		}else{
			otherLabelsColumn = sectionLabelTableElement;
			otherInputsColumn = sectionInputTableElement;
		}

	}
	
	// Add project link
	var projectTitle = null;
	var projectID = null;
	if(projectInfo != null){
		projectTitle = projectInfo.title;
		projectID = projectInfo.projectID;
	}
	mainInputsColumn += "<li style='margin-bottom: -5px;'><a  onclick='redirectToPost(" + '"' + projectID + '"' + ");'>"
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
	formString += "<tr>" + mainLabelsColumn + mainInputsColumn + pictureColumn + "</tr>"
	formString += "<tr>" + otherLabelsColumn + otherInputsColumn + "</tr></form>"
	formString += "<tr><td colspan='3' style='width: 100%; position:relative; height: 70px;'><div class='whiteButton blackHover' style='width: 36%; position:absolute; left: 0; bottom: 0; margin-bottom: 10px; margin-left: 20px;' onclick='" + formDict["cancelButton"]["onclick"] + "'> Cancel </div><div class='whiteButton blackHover' style='width: 36%; position:absolute; right: 0; bottom: 0; margin-bottom: 10px;' onclick='submitForm(" + '"' + formName + '");' + "'> Create Post</div></td></tr>";
	return formString;
}