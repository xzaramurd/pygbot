
function logs_init() {
	entries = document.getElementsByClassName('entry');
	for (i = 0; i < entries.length; i++) {
		entries[i].style.color = md5(entries[i].id).slice(0, 6);
	}
	dates = document.getElementsByClassName('date');
	
	for (i = 0; i < dates.length; i++) {
		date_str = dates[i].textContent.split(' ');
		date = new Date(date_str[0] + 'T' + date_str[1] + 'Z');
		dates[i].innerHTML = date.toLocaleString(); 
	}

	texts = document.getElementsByClassName('text');
	var autolinker = new Autolinker();

	for (i = 0; i < texts.length; i++) {
		linked_str = autolinker.link(texts[i].textContent);
		texts[i].innerHTML = linked_str;
	}

}
