class populating{
  constructor(){

  }

  populateSales(StoreN) {
    fetch(`/owner/salesInfo/${StoreN}`, {
      method:"GET"
    })
    .then(response => {
      if (response.ok) {
        return response.json()
      }
    })
    .then(result => {
      let div = document.querySelector(".store-info-div");
      div.innerHTML = '';
      div.innerHTML = "Sales:"
      console.log(result);
      for(let i = 0; i < result.transactions.length; i++) {
        let d = document.createElement("div");
        d.innerHTML = "Name: " + result.transactions[i].name + " UPC: " + result.transactions[i].upc + " Qty: " + result.transactions[i].qty + " Total retail: $" + result.transactions[i].retail + " Total price: $" + result.transactions[i].price;
        d.style.fontSize = '20px';
        div.append(d);
      } 
      let total = document.querySelector(".store-total-div");
      console.log(total);
      total.textContent = 'Total turnover for ' + result.month + ": $" + result.turnover + ' Total profit: $' + result.profit ; 
    })
  }

  populateReturns(StoreN) {
    fetch(`/owner/returnsInfo/${StoreN}`, {
      method:"GET"
    })
    .then(response => {
      if (response.ok) {
        return response.json()
      }
    })
    .then(result => {
      let div = document.querySelector(".store-info-div");
      div.innerHTML = '';
      for(let i = 0; i < result.transactions.length; i++) {
        let d = document.createElement("div");
        d.innerHTML = "Name: " + result.transactions[i].name + " UPC: " + result.transactions[i].upc + " Qty: " + result.transactions[i].qty + " Total retail: $" + result.transactions[i].retail + " Total price: $" + result.transactions[i].price + " User: " + result.transactions[i].user;
        div.append(d);
      }
      let total = document.querySelector(".store-total-div");
      console.log(result);
      total.textContent = 'Total returns ' + result.month + ": $" + result.totalM + ' Pieces returned: ' + result.totalP; 
    })
  }

  populateItem(StoreN) {
    let input = document.querySelector(".ALinput");


    if (input.value.length == 12) {
      let upc = input.value
      fetch(`/owner/itemsInfo/${StoreN}/${upc}`, {
        method:"GET"
      })
      .then(response => {
        if (response.ok) {
          return response.json()
        }
      })
      .then(result => {
        console.log(result)
        let div = document.querySelector(".store-info-div");
        div.innerHTML = '';
        if (result.main == 'NA') {
          document.querySelector(".error-msg").style.display = 'block';
          return;
        }
  
        div.innerHTML = "Name: " + result.main.name + " In inventory: " + result.main.oh
        let div2 = document.createElement("div");
        div2.innerHTML = "\nAverage Sales: " + result.transaction.avg + "/week"
        div.append(div2)
        let div3 = document.createElement("div");
        div3.innerHTML = "Transactions: ";
        div.append(div3);
        for(let i = 0; i < result.transaction.list.length; i++) {
          let d = document.createElement("div");
          d.innerHTML = result.transaction.list[i].type + " qty: " + result.transaction.list[i].qty;
          div.append(d);
        }

      })
    }
  }


}

document.addEventListener("DOMContentLoaded", () => {

    document.querySelector(".Logout-BTN").addEventListener("click", (e) => {
      let status = confirm("Are you sure you want to log out?");
      if (status) {
          fetch('/login/', {
              method: "PUT",
          })            
          .then((result) => {
              if(result.ok) {
                  window.location.href = "/login";

                  return result.json();
              }
              console.log("something went wrong!");
          })
      }
  })

    let stores = document.querySelectorAll('.owner-store');
    if (document.querySelector('.type').dataset.page == "items") {
      document.querySelector(".hide").style.display = "block";
    }
    stores.forEach(function(store) {
        store.addEventListener("click", function(e) {
          let storeN = e.target.dataset.store;
          const pop = new populating();
          switch(document.querySelector('.type').dataset.page){
            case "sales":
              pop.populateSales(storeN);
              break;
            case "returns":
              pop.populateReturns(storeN);
              break;
            case "items":
              pop.populateItem(storeN);
              break;
          }
        });
      });
})