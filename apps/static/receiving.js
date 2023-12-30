document.addEventListener("DOMContentLoaded", () => {
    let input = document.querySelector(".delInput");
    let date = document.querySelector(".expDelDate");
    let totalP = document.querySelector(".totalP")
    let submitBTN = document.querySelector(".submitInput");
    input.addEventListener("change", (e) => {
        if (input.value.length == 9) {
            fetch(`/dest/orderInfo/${input.value}/`, {
                method: "GET",
            })
            .then((result) => {
                if(result.ok) {
                    return result.json();
                }
                console.log("something went wrong!");
            })
            .then((response) => {
                submitBTN.style.display = "inline-block";
                console.log(response);
                if (response.ord_n == "RCD") {
                    document.querySelector(".error-msg").style.display = 'block';
                    document.querySelector(".error-msg").innerHTML = 'Already Received!';
                    totalP.innerHTML = response.numberOfP;
                    date.innerHTML = response.expDelD;
                    submitBTN.style.display = "none";
                }
                else if (response.ord_n == "NA") {
                    document.querySelector('.error-msg').style.display = "block";
                    totalP.innerHTML = '***';
                    date.innerHTML = "***";
                }
                else {
                    document.querySelector(".error-msg").style.display = 'none';
                    totalP.innerHTML = response.numberOfP;
                    date.innerHTML = response.expDelD;
                }
            })
            }
        }
    );
    submitBTN.addEventListener("click", (e) => {
        if (input.value.length != 9) {
            alert("Something wrong");
        }
        else {
            fetch(`/dest/receiving`, {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({delN: `${input.value}`})
            })
            .then(response => {
                if (response.ok){
                    console.log("receivied " + input.value)
                }
            })
            .catch(error => {
                
            })
        }
    });
});