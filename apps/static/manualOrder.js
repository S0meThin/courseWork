document.addEventListener("DOMContentLoaded", () => {
    let qty = document.querySelector(".qtyInput");
    let input = document.querySelector(".upcInput");
    let name = document.querySelector(".name_MO");
    let enterBTN = document.querySelector(".enterBTN")
    let submitBTN = document.querySelector(".submitBTN");
    let list = document.querySelector(".list_MO");
    let arr = [];
    let index = 0;
    
    let ohQty = 0;
    input.addEventListener("change", (e) => {
        document.querySelector('.error-msg').textContent = "UPC not found!";
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
                    ohQty = parseInt(response.main.qty);
                }
                else {
                    document.querySelector('.error-msg').style.display = "block";
                    name.innerHTML = '***'
                }
            })
            }
        }
    );
    enterBTN.addEventListener("click", (e) => {
        if (input.value.length != 12 || qty.value == '') {
            alert("Something wrong");
        }
        else {
            if (ohQty - parseInt(qty.value) < 0 || parseInt(qty.value) <= 0) {
                document.querySelector('.error-msg').textContent = "Inventory qty can`t be lower than 0!";
                document.querySelector('.error-msg').style.display = "block";
                return 
            }
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
                    for (let i = 0; i < arr.length; i++) {
                        if (arr[i]["UPC"] == input.value) {
                            arr[i]["qty"] += parseInt(qty.value);
                            list.children[arr[i]["id"]].innerHTML = arr[i]["id"] + 1 + ") Name: " + response.main.name + " UPC: " + arr[i]["UPC"] + " QTY: " + arr[i]["qty"]
                            return;
                        }
                    }
                    obj = {"id": index++, "UPC": input.value, "qty": parseInt(qty.value)};
                    arr.push(obj);

                    let div = document.createElement("div");
                    div.innerHTML = obj["id"] + 1 + ") Name: " + response.main.name + " UPC: " + obj["UPC"] + " QTY: " + obj["qty"];  
                    list.append(div);
                }
                else {
                    document.querySelector('.error-msg').style.display = "block";
                    name.innerHTML = '***'
                }
            })
        }
    });
    submitBTN.addEventListener("click", (e) => {
        let fetchList = []
        for(let i = 0; i < arr.length; i++) {
            fetchList[i] = {
                upc: `${arr[i]["UPC"]}`, 
                qty: `${arr[i]["qty"]}`
            }
        }

        fetch(`/dest/manual_order`, {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(fetchList)
        })
        .then(response => {
            if (response.ok){
            }
            else {
                document.querySelector('.error-msg').textContent = "Something went wrong!";
                document.querySelector('.error-msg').style.display = "block";
            }
        })
        .catch(error => {
            
        })
    });
});