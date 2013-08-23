Date.prototype.getWeek = function() {
	var onejan = new Date(this.getFullYear(),0,1);
	return Math.ceil((((this - onejan) / 86400000) + onejan.getDay()+1)/7);
}

$('#date-picker-day')
	.datepicker({
		weekStart: 1,
		minViewMode: 0,
		todayBtn: "linked",
		calendarWeeks: true
	})
	.on('changeDate', function(action){
		var year = action.date.getFullYear();
		var month =  action.date.getMonth() + 1;
		var day = action.date.getDate()
		var url_base = '/stechuhr/reports/day/';
		window.location = url_base + year + '/' + month + '/' + day + '/';
	});

$('#date-picker-week')
	.datepicker({
		weekStart: 1,
		minViewMode: 0,
		todayBtn: "linked",
		calendarWeeks: true
	})
	.on('changeDate', function(action){
		var year = action.date.getFullYear();
		var week = action.date.getWeek();
		var url_base = '/stechuhr/reports/week/';
		window.location = url_base + year + '/' + week + '/';
	});

$('#date-picker-month')
	.datepicker({
		weekStart: 1,
		minViewMode: 1,
		todayBtn: "linked"
	})
	.on('changeDate', function(action){
		var year = action.date.getFullYear();
		var month = action.date.getMonth() + 1;
		var url_base = '/stechuhr/reports/month/';
		window.location = url_base + year + '/' + month + '/';
	});

/** vim: set ft=javascript ts=4 sw=4 : */
