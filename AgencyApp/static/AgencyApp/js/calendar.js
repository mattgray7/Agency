'use strict';
function loadCalendar(calendarID){
		var $dayNumber = $('#' + calendarID + ' .header-current-day-number');
		$(document).keyup(function(e) {
			/*if (e.keyCode == 27) {
          		$dayNumber.text(', ' + $('#' + calendarID + ' .gotcha').text());
				$//('.gotcha').animate({'top':'-50px', 'opacity': '0'},300, function(){});
				$('#' + calendarID + ' .small-wrapper').slideUp(300);
				$('#' + calendarID + ' .header-current-day-number').animate({'top':'0'}, 500, 'easeInOutBack', function(){
				$(this).animate({'right':'0'});
				$('#' + calendarID + ' .calendar-header').animate({'color':'black'});
				$('#' + calendarID + ' .month-wrapper').animate({'margin-right':'0'}, 500, 'easeInOutBack');
				$('#' + calendarID + ' .header-prev-month, ' + '#' + calendarID + ' .header-next-month, ' + '#' + calendarID + ' .header-prev-year, ' + '#' + calendarID + ' .header-next-year').animate({'width':'0'});

				//$('.gotcha').parent().animate({'color':'#808080'});
				//$('.gotcha').remove();
			});*/

				//$('.gotcha').animate({});
				$('#' + calendarID + '.calendar-header').on('click',function(e){
					if(activeCalendar === calendarID){
						clickCalendar(e);
						$dayNumber.text(', ' + getRandomArbitrary(1,30));//
					}
				});		
			//};
		});
	
	

		function clickCalendar(e){
			e.stopPropagation();
			$('#' + calendarID + ' .calendar-header').animate({'color':'#808080'});
			var t = $('#' + calendarID + ' .header-current-month').text();
			$('#' + calendarID + ' .header-current-month').text(t.replace(',',''));
			$('#' + calendarID + ' .header-prev-month, ' + '#' + calendarID + ' .header-next-month, ' + '#' + calendarID + ' .header-prev-year, ' + '#' + calendarID + ' .header-next-year').animate({'width':'12px'},400, 'easeInOutBack');
			$('#' + calendarID + ' .header-current-day-number').animate({'right':'6px'});
			$('#' + calendarID + ' .month-wrapper').animate({'margin-right':'50px'},400, 'easeInOutBack', function(){
				$('#' + calendarID + ' .small-wrapper').slideDown(250, function(){});
        		$('#' + calendarID + ' .header-current-day-number').animate({'top':'60px'});
				var res = $dayNumber.text().replace(',','');
				//findItem(parseInt(res));		
			});
			$('#' + calendarID + ' .calendar-header').off('click');
		};	


		function getRandomArbitrary(min, max) {
				return Math.floor(Math.random() * (max - min) + min);
		}
		
    function findItem(val){
				//$('.gotcha').remove();
		    $('#' + calendarID + ' .column-item').not('.weekday, .prev-month, .next-month').each( function() {
		        if($(this).text() == val){
								$(this).append('<div class="gotcha"></div>');
								$(this).animate({'color':'white'},250);
								var pos = $(this).position();
								 var block = $(this).find('.gotcha').first();
				block.text($(this).text());
        var pos = $(this).position();
        block.css({'top': '-50px', 
									 'left': pos.left, 
									 'opacity': 0})
						 .animate({'top':pos.top,
											'opacity': '1'}, 400, 'easeInOutBack');
            }
        });
    }
	
		$('#' + calendarID + ' .calendar-header').on('click',function(e){
			clickCalendar(e);
		});	
	

    $('#' + calendarID + ' .column-item').not('.weekday').on('click', function(){
    		if(calendarID === activeCalendar){
    			var calendarType = calendarID.replace("Calendar", "")
    			
    			// Weird bug where if gotcha exists in class, .text() will return double value (eg 2323 for mnumber 23)
    			var clickedNumber = parseInt($(this).text())
    			if($(this).find('.gotcha').length > 0){
    				clickedNumber = $(this).find('.gotcha').first().text()
    			}

    			// Prevent user from clicking invalid date shown in calendar (ie before previous date, last month, etc)
    			if(calendarMonths[calendarType]["month"] === currentDate.getMonth() && calendarMonths[calendarType]["year"] === currentDate.getFullYear()){
	    			if(clickedNumber < currentDate.getDate()){
	    				if(!$(this).hasClass("next-month")){
	    					// Can't select previous
	    					return;
	    				}
	    			}else if(clickedNumber > currentDate.getDate()){
	    				if($(this).hasClass("prev-month")){
	    					return;
	    				}
	    			}else{
	    				$('#' + calendarID + ' .today').removeClass("today")
	    			}
	    		}

	    		var clickedNumberMonth = calendarMonths[calendarType]["month"]
	    		var clickedNumberYear = calendarMonths[calendarType]["year"]
	    		if($(this).hasClass("prev-month")){
	    			clickedNumberMonth -= 1;
	    			if(clickedNumberMonth < 0){
	    				clickedNumberMonth = 11;
	    				clickedNumberYear -= 1;
	    			}
	    		}else if($(this).hasClass("next-month")){
	    			clickedNumberMonth += 1
	    			if(clickedNumberMonth > 11){
	    				clickedNumberMonth = 0;
	    				clickedNumberYear += 1
	    			}
	    		}

	    		// Check if date is already selected
	    		var formattedDate = clickedNumberYear + "-" + clickedNumberMonth + "-" + clickedNumber;
	    		var existingDateIndex = -1;
	    		for(var i=0; i < selectedDates[calendarType].length; i++){
	    			if(selectedDates[calendarType][i] === formattedDate){
	    				existingDateIndex = i;
	    				break;
	    			}
	    		}

	    		if(existingDateIndex > -1){
	    			console.log("date is selected, so removing")
	    			// Check if it has gotcha class, if so remove it
	    			selectedDates[calendarType].splice(existingDateIndex, 1)
	    			if($(this).find('.gotcha').length > 0){
		    			$(this).find('.gotcha').fadeOut(300,function(){
		    				$(this).parent().animate({'color':'#808080'}, 250);
							$(this).remove();
						});
						return;
					}
		    	}
		    		// Otherwise, add gotcha class
		    		selectedDates[calendarType].push(formattedDate)
		    		$(this).css({'color':'white'});
					$('#' + calendarID + ' .gotcha').parent().animate({'color':'#808080'}, 250);
		        	$(this).prepend('<div class="gotcha"></div>');
		        	var block = $(this).find('.gotcha').first();
					block.text($(this).text());
		       		var pos = $(this).position();
		     		block.css({'top': 0, 
							   'left': pos.left, 
							   'opacity': 0}).animate({'top':pos.top,
													   'opacity': '1'}, 350, 'easeInOutBack');
		    	
				$('#' + calendarID + ' .calendar-base').on('click', function(e){
				  	if(e.stopPropogation){
				      	e.stopPropogation();
				    }
				});
			}
		});
};


function enableCalendar(calendarType){
    $('#' + calendarType + 'Calendar .calendar-base').css("cursor", "default")
    $('#' + calendarType + 'Calendar .column-item').css("cursor", "pointer")
    $('#' + calendarType + 'Calendar .calendar-base').css("background", "#FFF")
}

function disableCalendar(calendarType){
    $('#' + calendarType + 'Calendar .calendar-base').css("cursor", "not-allowed")
    $('#' + calendarType + 'Calendar .calendar-base').css("background", "rgba(0,0,0,0.02)")
    $('#' + calendarType + 'Calendar .column-item').css("cursor", "not-allowed")
    $('#' + calendarType + 'Calendar .column-item').not('.prev-month').not('.next-month').css("color", "#808080")
    $('#' + calendarType + 'Calendar .gotcha').remove();
}

function toggleCalendarMonth(direction, calendarID){
	var calendarType = calendarID.replace("Calendar", "")
	if(calendarID === activeCalendar){
	    if(calendarMonths[calendarType] != null){
	        var currentMonth = calendarMonths[calendarType]["month"]
	        var currentYear = calendarMonths[calendarType]["year"]
	        if(currentMonth != null && currentYear != null){
	        	if(direction === "next"){
		            var nextMonth = currentMonth + 1;
		            var nextYear = currentYear
		            if(currentMonth === 11){
		                nextMonth = 0
		                nextYear += 1;
		            }
		        }else{
		        	var nextMonth = currentMonth - 1;
		            var nextYear = currentYear
		            if(currentMonth === 0){
		                nextMonth = 11
		                nextYear -= 1;
		            }
		        }
	            $('#' + calendarID + ' .small-wrapper').html(getCalendarString(calendarType, nextMonth, nextYear))
	            $('#' + calendarID + ' .header-current-month').html(months[nextMonth])
	            $('#' + calendarID + ' .header-current-year').html(nextYear)
	            loadCalendar(calendarID)
	        }
	    }
	}
}

function toggleCalendarYear(direction, calendarID){
	var calendarType = calendarID.replace("Calendar", "")
	if(calendarID === activeCalendar){
	    if(calendarMonths[calendarType] != null){
	        var currentMonth = calendarMonths[calendarType]["month"]
	        var currentYear = calendarMonths[calendarType]["year"]
	        if(currentMonth != null && currentYear != null){
	        	if(direction === "next"){
		            var nextYear = currentYear + 1
		        }else{
		            var nextYear = currentYear - 1
		        }
	            $('#' + calendarID + ' .small-wrapper').html(getCalendarString(calendarType, currentMonth, nextYear))
	            $('#' + calendarID + ' .header-current-year').html(nextYear)
	            loadCalendar(calendarID)
	        }
	    }
	}
}

var weekdays = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
function _daysInMonth(month,year) {
    return new Date(year, month+1, 0).getDate();
}

function getCalendarData(month, year){
	var calendarData = []
	var daysInMonth = _daysInMonth(month, year)
	var firstDay = new Date(year, month, 1);
	var lastDay = new Date(year, month + 1, 0);

	var previousMonth = month-1;
	if(previousMonth < 0){
		previousMonth = 11
	}
	var daysInPreviousMonth = _daysInMonth(previousMonth, year)

	var dateList = []
	// Prepend previous month days
	for(var i=0; i < firstDay.getDay(); i++){
		dateList.push(daysInPreviousMonth + i - firstDay.getDay() + 1)
	}
	// Add current month days
	for(var i=1; i < daysInMonth + 1; i++){
		dateList.push(i)
	}
	// Add next month days
	for(var i=1; i < (7-lastDay.getDay()); i++){
		dateList.push(i)
	}

	for(var i=0; i < Math.ceil(dateList.length / 7); i++){
		var week = [];
		var firstDayOfWeekIndex = i*7
		for(var j=firstDayOfWeekIndex; j < firstDayOfWeekIndex + 7; j++){
			week.push(dateList[j])
		}
		calendarData.push(week)
	}
	return calendarData
}
 