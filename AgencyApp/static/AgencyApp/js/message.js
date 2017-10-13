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

function getMessageTime(date){
    var hours = date.getHours()
    var AMPMString = "AM";
    if(hours > 12){
        AMPMString = "PM";
    }

    var minutes = date.getMinutes()
    if(minutes < 10){
        minutes = "0" + minutes;
    }
    //return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    return (hours%12) + ":" + minutes + " " + AMPMString;
}

function getWeekDateString(date){
    return "Mon " + getMessageTime(date)
}

function getMonthDateString(date){
    return "October 13 " + getMessageTime(date);
}

function getYearDateString(date){
    return getMonthDateString(date) + "2016"
}

function checkForNewDateWrite(lastWrittenDate, newDate){
    var write = true;
    var thresholds = {"minutes": 5}
    if(lastWrittenDate != null){
        if(lastWrittenDate.getYear() === newDate.getYear()){
            if(lastWrittenDate.getMonth() === newDate.getMonth()){
                if(lastWrittenDate.getDay() === newDate.getDay()){
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
    var dateString = null
    var dateContent = null;
    if(lastWrittenDate == null){
        dateContent = getMonthDateString(newDate)
    }else{
        if(checkForNewDateWrite(lastWrittenDate, newDate)){
            var timeOffset = Math.abs(lastWrittenDate.getTime() - newDate.getTime()) / 1000; // now in s
            if(timeOffset < 24 * 60 * 60){
                // Less than a day, check if same day
                if(lastWrittenDate.getDay() === newDate.getDay()){
                    // Same day, just need time
                    dateContent = getMessageTime(newDate)
                }else{
                   dateContent = getWeekDateString(newDate)
                }
            }else if(timeOffset < 7 * 24 * 60 * 60){
                dateContent = getWeekDateString(newDate)
            }else if(timeOffset > 365 * 24 * 60 * 60){
                dateContent = getYearDateString(newDate)
            }
            if(dateContent == null){
                dateContent = getMonthDateString(newDate);
            }
        }
    }
    if(dateContent != null){
        dateString = "<div style='font-size: 0.65em; color: rgba(0,0,0,0.5); margin-top: 20px;'>" + dateContent + "</div>";
    }
    return dateString;
}