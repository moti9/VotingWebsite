function createChoices() {
    const numChoices = document.getElementById("choices").value;
    if (numChoices>10 || numChoices<2) {
        alert("Please enter valid number of choices(Maximum-10)");
        return;
    }
    const container = document.getElementById("input-container");
    container.innerHTML = "";
    for (let i = 1; i <= numChoices; i++) {
        const div=document.createElement('div')
        div.className="mb-3 row m-2"
        // Label Create
        const label = document.createElement('label');
        label.className = "form-label"
        label.innerHTML = 'Choice ' + (i);
        div.appendChild(label);
        //Create Input
        const input = document.createElement("input");
        input.type = "text";
        input.required=true;
        input.name = "choice" + i;
        input.className = "form-control";
        input.placeholder = "Choice " + i;

        const divi=document.createElement('div')
        divi.className="col-sm-10"
        
        divi.appendChild(input)
        div.appendChild(divi)
        container.appendChild(div);
    }
}

createChoices();