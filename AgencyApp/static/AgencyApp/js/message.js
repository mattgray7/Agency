function sendMessage(senderUsername, destUsername, contentInput, clearTextInput, callback){
    var errors = []
    if(senderUsername != null && destUsername != null && senderUsername.length > 0 && destUsername.length > 0){
        var content = document.getElementById(contentInput);
        if(content != null && content.value.length > 0){
            var contentValue = content.value;
            if(clearTextInput){
                content.value= "";
            }
            $.ajax({
                    url : "/ajax/sendNewMessage/",
                    data : {"sender": senderUsername, "recipient": destUsername,"content": contentValue},
                    type : 'POST',
                    dataType: "json",
                    success : function(data) {
                        if(data["success"]){
                            hideBlockingPanel();
                            if(callback != null){
                                callback();
                            }
                        }
                    }
            });
        }else{
            errors.push("You must add text to the message");
        }
    }else{
        errors.push("You must add a message recipient")
    }
}

function submitApplication(applicantUsername, postID, contentInput, callback){
    if(applicantUsername != null && postID != null){
        var contentValue;
        var contentDiv = document.getElementById(contentInput)
        if(contentDiv != null){
            contentValue = contentDiv.value;
        }
        $.ajax({
                    url : "/ajax/submitNewApplication/",
                    data : {"applicant": applicantUsername, "postID": postID, "content": contentValue},
                    type : 'POST',
                    dataType: "json",
                    success : function(data) {
                        if(data["success"]){
                            hideBlockingPanel();
                            if(callback != null){
                                callback();
                            }
                        }
                    }
            });
    }
}

function getMessageTime(date){
    var hours = date.getHours()
    var hourString = hours % 12
    if(hourString === 0){
        hourString = 12;
    }

    var AMPMString = "AM";
    if(hours >= 12){
        AMPMString = "PM";
    }

    var minutes = date.getMinutes()
    if(minutes < 10){
        minutes = "0" + minutes;
    }
    //return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    return hourString + ":" + minutes + " " + AMPMString;
}

var daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
function getWeekDateString(date){
    return daysOfWeek[date.getDay()] + " " + getMessageTime(date)
}

var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
function getMonthDateString(date){
    return date.getDate() + " " + months[date.getMonth()] + " " + getMessageTime(date);
}

function getYearDateString(date){
    return date.getDate() + "/" + (date.getMonth()+1) + "/" + date.getFullYear() + " " + getMessageTime(date);
}

function checkForNewDateWrite(lastWrittenDate, newDate){
    var write = true;
    var thresholds = {"minutes": 5}
    if(lastWrittenDate != null){
        if(lastWrittenDate.getFullYear() === newDate.getFullYear()){
            if(lastWrittenDate.getMonth() === newDate.getMonth()){
                if(lastWrittenDate.getDate() === newDate.getDate()){
                    if(lastWrittenDate.getHours() === newDate.getHours()){
                        if(lastWrittenDate.getMinutes() === newDate.getMinutes()){
                            write = false
                        }else{
                            if(Math.abs(lastWrittenDate.getMinutes() - newDate.getMinutes()) <= thresholds["minutes"]){
                                write = false
                            }
                        }
                    }
                }
            }
        }
    }
    return write;
}

function getNextDateString(lastWrittenDate, newDate){
    var dateString = null;
    var dateContent = null;
    var first = false
    if(lastWrittenDate == null || checkForNewDateWrite(lastWrittenDate, newDate)){
        // If first date in message, use current date as comparison for which date string to use
        if(lastWrittenDate == null){
            lastWrittenDate = currentDate;
            first = true;
        }

        var timeOffset = Math.abs(lastWrittenDate.getTime() - newDate.getTime()) / 1000; // now in s
        if(timeOffset < 24 * 60 * 60){
            // Less than a day, check if same day
            if(lastWrittenDate.getDate() === newDate.getDate()){
                // Same day, just need time
                dateContent = getMessageTime(newDate)
            }else{
                // Adjacent days, use week day name
               dateContent = getWeekDateString(newDate)
            }
        }else if(timeOffset < 7 * 24 * 60 * 60){
            // In same week, use week day
            dateContent = getWeekDateString(newDate)
        }else if(timeOffset > 365 * 24 * 60 * 60){
            // In different years, display the year
            dateContent = getYearDateString(newDate)
        }

        // Otherwise, use month string
        if(dateContent == null){
            dateContent = getMonthDateString(newDate);
        }
    }
    if(dateContent != null){
        dateString = "<div style='font-size: 0.65em; color: rgba(0,0,0,0.5); "
        if(!first){
            dateString += " margin-top: 20px; "
        }
        dateString += "'>" + dateContent + "</div>";
    }
    return dateString;
}