document.addEventListener("DOMContentLoaded", () => {
    let qty = document.querySelector(".qtyInput");
    let input = document.querySelector(".upcInput");
    let name = document.querySelector(".IC_name");
    let submitBTN = document.querySelector(".submitInput");
    let list = document.querySelector(".listOfChanges");
    input.addEventListener("change", (e) => {
        if (input.value.length == 12) {
            fetch(`/dest/item/${input.value}`, {
                method: "GET",
            })
            .then((result) => {
                if(result.ok) {
                    return result.json();
                }
                console.log("something went wrong!");
            })
            .then((response) => {
                if (response.main != "NA") {
                    document.querySelector(".error-msg").style.display = 'none';
                    name.innerHTML = response.main.name;
                }
                else {
                    document.querySelector('.error-msg').style.display = "block";
                    name.innerHTML = '***'
                }
            })
            }
        }
    );
    submitBTN.addEventListener("click", (e) => {
        if (input.value.length != 12 || qty.value == '') {
            alert("Something wrong");
        }
        else {
            fetch(`/dest/inventory_count`, {
                method: "PUT",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ upc: `${input.value}`, qty: `${qty.value}`})
            })
            .then(response => {
                if (response.ok){
                    let div = document.createElement("div");
                    div.innerHTML = "Name: " + name.textContent + " - UPC: " + input.value + " - QTY: " + qty.value;
                    list.append(div);
                }
            })
            .catch(error => {
                
            })
        }
    });
});