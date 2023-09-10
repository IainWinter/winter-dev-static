let table = getCapsuleTable();
let tableDOM = document.getElementById("shape-table");

for (let row of table) {
	let rowDOM = tableDOM.insertRow(-1); // Insert a new row at the end of the table

	for (let cell of row) {
		let cellDOM = rowDOM.insertCell();
		cellDOM.innerHTML = cell;
	}
}