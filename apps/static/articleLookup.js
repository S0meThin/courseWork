
document.addEventListener("DOMContentLoaded", () => {
    let name = document.querySelector(".nameOfProd");
    let oh = document.querySelector(".ohOfProd");
    let pack = document.querySelector(".packOfProd");
    let onOrder = document.querySelector(".ooOfProd");
    let nextShipDate = document.querySelector(".nsdOfProd");
    let or = document.querySelector(".orOfProd");
    let nextRetDate = document.querySelector(".nrdOfProd");
    let listOfTransa = document.querySelector(".list_of_transa");
    let avgSales = document.querySelector(".avg-sales");
    
    let input = document.querySelector(".ALinput");
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
                console.log(response);
                listOfTransa.innerHTML = ''
                if (response.main != "NA") {
                    document.querySelector(".error-msg").style.display = 'none';
                    name.innerHTML = response.main.name;
                    oh.innerHTML = response.main.oh;
                    pack.innerHTML = response.main.pack;
                    onOrder.innerHTML = response.main.oo;
                    nextShipDate.innerHTML = response.main.nsd;
                    or.innerHTML = response.main.or;
                    nextRetDate.innerHTML = response.main.nrd;
                    for (let i = 0; i < response.transaction.list.length; i++) {
                        let div = document.createElement("div");
                        div.textContent = `Type: ${response.transaction.list[i].type} - qty: ${response.transaction.list[i].qty} - date: ${response.transaction.list[i].date}` 
                        listOfTransa.append(div)
                    }
                    let fl = parseFloat(response.transaction.avg)
                    avgSales.innerHTML = fl.toFixed(2);
                }
                else {
                    name.innerHTML = '';
                    oh.innerHTML = '';
                    pack.innerHTML = '';
                    onOrder.innerHTML = '';
                    nextShipDate.innerHTML = '';
                    or.innerHTML = '';
                    nextRetDate.innerHTML = '';

                    document.querySelector(".error-msg").style.display = 'block';
                }
            })
            .catch((error) => {
                console.log(error);
            })
        }
    });
});