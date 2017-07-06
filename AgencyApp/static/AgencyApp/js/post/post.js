function addCreateCastingPost(formDict, formURL, formName){
	var formString = "<form method='post' action='" + formURL + "' id='" + formName + "' class='form-style-1' style='width: 90%; background: none; margin-left: 3.2%;' enctype='multipart/form-data'>";
	formString += "<table style='width: 100%;'><tr>"

	// Fill post picture string
	var pictureField = formDict["postPicture"];
	var pictureColumn = '<td style="text-align: center; width: 30%;"><div id="postPicturePanel" class="postPicture" style="width: 270px; height: 292px; background: #000; margin-left: 10px; margin-top: 118px;"><img id="postPictureImg" src="' + pictureField.value + '" style="max-width:100%; max-height:100%;"/></div><div style="width: 60%; margin-left: 25%; overflow: hidden;">' + pictureField.input + "</div></td>";

	// Fill text content
	var sectionMap = {"Details": ["title", "project", "characterType", "status", "paid", "hoursPerWeek", "startDate", "endDate"],
					  "Character": ["characterName", "shortCharacterDescription", "description", "skills", "languages"],
					  "Performer": ["actorName"],
					  "Physical": ["hairColor", "eyeColor", "complexion", "height", "build", "gender", "ageRange"],
					  "hidden": ["csrf_token", "postID", "source", "next", "destination", "projectID", "poster"]}
	var mainLabelsColumn = "<td class='editPostLabelPanel' style='width: 20%; position:relative; line-height: 38.2px;'><div style='margin-top: 30px;'><ul style='margin-bottom: -14px;'>";
	var mainInputsColumn = "<td class='editPostInputPanel' style='width: 50%; position: relative; line-height: 39px;'><h1 style='font-size: 2.8em; padding: 0em 0em 0.3em 0em; margin-top: 15px;'>Edit Role</h1><ul style='margin-top: -20px;'>";
	var otherLabelsColumn = "<td class='editPostLabelPanel' style='width: 30%; min-width: 170px; height: 600px; position:relative;'><div style='position: absolute; top:0; right: 0; margin-right: 5px; width: 90%; margin-top: 5px;'><ul>";
	var otherInputsColumn = "<td class='editPostInputPanel' colspan='2' style='width: 70%;'><div style='margin-top: -6px;'><ul>";
	for(sectionTitle in sectionMap){
		var fieldList = sectionMap[sectionTitle];
		var sectionInputTableElement = null;
		var sectionLabelTableElement = null;
		var sectionClass = null;
		if(sectionTitle === "Details" || sectionTitle === "Production"){
			sectionLabelTableElement = mainLabelsColumn;
			sectionInputTableElement = mainInputsColumn;
			sectionClass = "editPostMainSectionTitle";
		}else{
			sectionLabelTableElement = otherLabelsColumn;
			sectionInputTableElement = otherInputsColumn;
			sectionClass = "editPostOtherSectionTitle";
		}

		if(sectionTitle != "hidden"){
			sectionLabelTableElement += "<div style='position: relative; height: 50px;'> <h2 class='" + sectionClass + "' style='position: absolute; z-index: 1; right: 0; margin-left: 80px;'> " + sectionTitle + "</h2><div style='position: absolute; z-index: 0; width: 250%; border: 1px solid #7c7b7b; height: 0px; bottom: 0; margin-bottom: 15px; margin-left: 20px;'></div></div>"
			sectionInputTableElement += "<div style='height: 60px;'></div>";

			for(i in fieldList){
				var fieldName = sectionMap[sectionTitle][i];
				var field = formDict[fieldName];
				console.log(fieldName)

				// Add project
				if(fieldName === "project"){
					sectionLabelTableElement += "<label for='name'>Project</label><br>";
					if(field.title != null){
						sectionInputTableElement += "<li style='margin-top: 6px;'><a  onclick='redirectToPost(" + '"' + field.projectID + '"' + ");'>" + field.title + "</a></li>";
					}else{
						sectionInputTableElement += "<li style='color: #1e1e1e; font-weight: 900; margin-top: 5px;'>Not specified</li>";
					}
					continue;
				}else if(fieldName === "actorName"){
					if(field.value != null && field.value.length > 0){
						var actorDict = formDict["actor"]

						// Add actor text panel
						if(actorDict.cleanName != null && actorDict.username != null){
							sectionLabelTableElement += "<div style='height: 165px;'></div>";
							
							sectionInputTableElement+= "<div style='width: 100%; position: relative; height: 161px;' class='editCastMemberPanel'>"
							sectionInputTableElement += '<div style="position: absolute; left: 0;"><h2>' + actorDict.cleanName + "</h2></div>";
							// Add actor profile picture panel
							sectionInputTableElement += '<div style="position: absolute; right: 0; margin-top: 2px; margin-right: 2px;"><div id="actorPicturePanel" class="postPicture" style="width: 100px; height: 100px; background: #000;"><img id="actorPictureImg" src="' + actorDict.profilePictureURL + '" style="max-width:100%; max-height:100%;"/></div></div>';
						}else{
							sectionLabelTableElement += "<label for='name'>Search</label><br>";

							sectionInputTableElement+= "<div style='width: 100%; position: relative; height: 37px;' class='editCastMemberPanel'>"
							sectionInputTableElement += '<div style="position: absolute; left: 0;"><input type="text" name="performerSearchText"></div>';
						}
						sectionInputTableElement += "</div>";
					}
					continue;
				}
				if(!field.hidden || field.name === "status"){
					if(field.numRows > 1){
						// stupid hack I hate myself right now
						sectionLabelTableElement += "<li style='height:" + '' + field.numRows*5.9 + 'px;' + "'><label for='name'>" + field.label + "</label></li>";
						// TODO replace newlines in description as it will break js
						sectionInputTableElement += "<li><textarea rows='" + field.numRows + "' name='" + field.name + "' form='" + formName + "' style='height:100px; font-size: 0.9em; width: 97.7%;'>" + field.value + "</textarea></li>";
					}else{
						sectionLabelTableElement += "<label for='name'>" + field.label + "</label><br>";
						sectionInputTableElement += "<li>"
						if(field.options){
							var selectForm = createSelectForm(formName, field.name + "SelectBar", field.options, field.value);
							sectionInputTableElement += selectForm;
							sectionInputTableElement += "<input type='hidden' name='" + field.name + "' id='" + field.name + "SelectInput' >";
						}else{
							sectionInputTableElement += field.input;
						}
						sectionInputTableElement += '</li>';
					}
				}else if(field.input != null && field.input.length > 0){
					sectionInputTableElement += field.input;
				}
			}
		}else{
			for(i in fieldList){
				var fieldName = sectionMap[sectionTitle][i];
				var field = formDict[fieldName];
				sectionInputTableElement += field.input;
			}
		}
		if(sectionTitle === "Details" || sectionTitle === "Production"){
			mainLabelsColumn = sectionLabelTableElement;
			mainInputsColumn = sectionInputTableElement;
		}else{
			otherLabelsColumn = sectionLabelTableElement + "<div style='height: 20px'></div>";
			otherInputsColumn = sectionInputTableElement + "<div style='height: 10px'></div>";
		}

	}

	mainLabelsColumn += "</ul></div></td>";
	otherLabelsColumn += "</ul></div></td>";
	mainInputsColumn += "</ul></td>";
	otherInputsColumn += "</ul></div></td>";
	formString += "<tr>" + mainLabelsColumn + mainInputsColumn + pictureColumn + "</tr>"
	formString += "<tr>" + otherLabelsColumn + otherInputsColumn + "</tr></form>"
	formString += "<tr><td colspan='3' style='width: 100%; position:relative; height: 70px;'><div class='whiteButton blackHover' style='width: 36%; position:absolute; left: 0; bottom: 0; margin-bottom: 10px; margin-left: 20px;' onclick='" + formDict["cancelButton"]["onclick"] + "'> Cancel </div><div class='whiteButton blackHover' style='width: 36%; position:absolute; right: 0; bottom: 0; margin-bottom: 10px;' onclick='submitForm(" + '"' + formName + '");' + "'> Create Post</div></td></tr>";
	return formString;
}