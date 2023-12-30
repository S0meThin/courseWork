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
})