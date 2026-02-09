// ===== Register Logic =====
const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        if (password.length < 6) {
            alert("Password must be at least 6 characters");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }

        alert("Registered successfully");
        window.location.href = "login.html";
    });
}

// ===== Login Logic =====
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const email = document.getElementById("login_email").value;
        const password = document.getElementById("login_password").value;

        const validUsers = [
            "user1@wewebit.com",
            "user2@wewebit.com",
            "user3@wewebit.com"
        ];

        if (validUsers.includes(email) && password === "12345678") {
            alert("Login successfully");
        } else {
            alert("Invalid email or password");
        }
    });
}

