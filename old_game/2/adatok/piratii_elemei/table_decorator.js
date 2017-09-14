
var table_decorator_dev_mode = false;

function hasClass(ele,cls) {
	return ele.className ? ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)')) : false;
}
function addClass(ele,cls) {
	if (!this.hasClass(ele,cls)) ele.className += " "+cls;
}
function removeClass(ele,cls) {
	if (hasClass(ele,cls)) {
		var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
		ele.className=ele.className.replace(reg,' ');
	}
}

var tableControl = null;

$(document).ready(function()
{
	var ts = document.getElementsByTagName('table');

	tableControl = document.createElement('div');
	tableControl.id = 'table-control';

	for (var i = 0; i < ts.length; i++)
	{
		var trs = ts[i].rows;
		var spanning = new Array();
		var tableScope = null;
		var inHead = false;
		var columnClasses = new Array();

		if (table_decorator_dev_mode === true)
		{
			var n = ts[i];
			while (n && !hasClass(n, 'panel')) n = n.parentNode;
		
			if (n) {
				var locationAnnotaion = window.location.toString();
				if ((p = locationAnnotaion.lastIndexOf('/')) != -1) 
					locationAnnotaion = locationAnnotaion.substring(p + 1);
				if ((p = locationAnnotaion.indexOf('.page.html')) != -1) 
					locationAnnotaion = locationAnnotaion.substring(0, p);
				
				var tid = ts[i].id;
				if (!tid) {
					var nts = n.getElementsByTagName('table');
					for (tid = 0; tid < nts.length; tid++) {
						if (nts[tid] == ts[i]) 
							break;
					}
				}
				var tableOverwritesId = locationAnnotaion + '-' + n.id + '-' + tid;
				ts[i].tableOverwritesId = tableOverwritesId;
				
				
				ts[i].update = updateTable;
				ts[i].save = saveTable;
				ts[i].update();
			}
		}

		var parityCounter = 0;
		var pairedClasses = new Array("odd-odd", "odd-even", "even-odd", "even-even");

		for (var j = 0; j < trs.length; j++)
		{
			if (trs[j].parentNode !== tableScope)
			{
				spanning = new Array();
				tableScope = trs[j].parentNode;
				inHead = tableScope.tagName == "THEAD";
			}

			if (!inHead)
			{
				addClass(trs[j], (parityCounter % 2 == 0) ? 'even' : 'odd');
				addClass(trs[j], pairedClasses[parityCounter % 4]);
				parityCounter++;
			}

			var tds = trs[j].cells;
			var idx = 0;

			for (var k = 0; k < tds.length; k++)
			{
				var td = tds[k];

				if (table_decorator_dev_mode === true)
				{
					if (td.innerHTML.indexOf('<') == -1 || (td.firstChild.tagName == "A" && td.firstChild.className.indexOf('button') == -1))
					{
						td.originalContent = td.innerHTML;
						td.onclick = tableCellOnClickHandler;
					}
				}
				if (inHead === true)
				{
					while (spanning[idx] > 0) idx++;
					for (var l = 0; l < td.colSpan; l++)
					{
						if (td.tagName == "TH" && td.className != "") columnClasses[idx] = (columnClasses[idx]) ? columnClasses[idx] + ' ' + td.className : td.className;
						spanning[idx++] = td.rowSpan;
					}
				}
				else
				{
					while (spanning[idx] > 0) idx++;
					addClass(td, 'col'+(idx+1));
					if (columnClasses[idx]) addClass(td, columnClasses[idx]);
					for (var l = 0; l < td.colSpan; l++) spanning[idx++] = td.rowSpan;
				}
			}
			for (k = 0; k < spanning.length; k++) spanning[k]--;
		}		
	}
});

function tableCellOnClickHandler(e)
{
	if (!e)
	{
		var e = window.event;
		e.cancelBubble = true;
	}
	else e.stopPropagation();

	if (e.target) targ = e.target;
	else if (e.srcElement) targ = e.srcElement;
	if (targ.nodeType == 3) // defeat Safari bug
		targ = targ.parentNode;

	if (targ.tagName != "TD") return;

	var cell = (this.innerHTML.indexOf('<') != -1) ? this.firstChild : this;

	ret = prompt("Cellaba valo HTML ide:", cell.innerHTML);
	// alert(ret);
	if (ret === null) {
		this.modified = false;
		cell.innerHTML = this.originalContent;
	}
	else
	{
		this.modified = true;
		cell.innerHTML = ret;
	}
}

function updateTable()
{
	var table = this;
	var td = null;

	new Ajax.Request('engine/cell_overwrites.php?id=' + table.tableOverwritesId,
	{
		method:'get',
		onSuccess: function(transport)
		{
			var json = transport.responseText.evalJSON();
			for (var i = 0; i < json.length; i++) 
				for (var j = 0; j < json[i].length; j++)
			{
				if (json[i][j] !== null)
				{
					td = table.rows[i].cells[j];
					if (td.tagName == "TD")
					{
						td.modified = true;
						if (td.innerHTML.indexOf('<') == -1)
						{
							td.innerHTML = json[i][j];						
						}
						else if (td.firstChild.tagName == "A" && td.firstChild.className.indexOf('button') == -1)
						{
							td.firstChild.innerHTML = json[i][j];
						}						
					}
				}
			}
		}
	});
}

function saveTables()
{
	var ts = document.getElementsByTagName("table");
	for (var i = 0; i < ts.length; i++)
	{
		if (ts[i].save)
		{
//			alert("saving: "+ts[i].tableOverwritesId);
			ts[i].save();
//			break;
		}
	}
	alert('saving..');
}

function saveTable()
{
	var table = this;
	var data = new Array();
	
	for (var i = 0; i < table.rows.length; i++)
	{
		data[i] = new Array();
		for (var j = 0; j < table.rows[i].cells.length; j++)
		{
			cell = table.rows[i].cells[j];
			text = null;
			if (cell.modified = true && typeof(cell.firstChild) != "undefined")
			{
				if (cell.innerHTML.indexOf('<') == -1)
				{
					text = cell.innerText || cell.textContent;
				}
				else
				{
					if (cell.firstChild.tagName == "A")
					{
						text = cell.firstChild.innerText || cell.firstChild.textContent;
					}					
				}
			}
			data[i][j] = text;
		}
	}
//	return alert(JSON.stringify(data));

//	alert(JSON.stringify(data));
	new Ajax.Request('engine/cell_overwrites.php?id=' + table.tableOverwritesId,
	{
		method: 'post',
		parameters: 'data=' + encodeURIComponent(JSON.stringify(data)) // data.toJSON()
//        onComplete: alert('saved')
	});
}

