document.addEventListener("DOMContentLoaded", () => {

  const passwordInput = document.querySelector('input[name="password"]');
  if (!passwordInput) return;

  const bar = document.getElementById("passwordStrengthBar");
  const text = document.getElementById("passwordStrengthText");

  const reqLength = document.getElementById("req-length");
  const reqUpper = document.getElementById("req-upper");
  const reqLower = document.getElementById("req-lower");
  const reqNumber = document.getElementById("req-number");
  const reqSymbol = document.getElementById("req-symbol");

  function updateRequirement(element, met) {
    element.classList.toggle("text-danger", !met);
    element.classList.toggle("text-success", met);
  }

  function checkStrength(pw) {
    let score = 0;


    const lengthOK = pw.length >= 8;
    const upperOK = /[A-Z]/.test(pw);
    const lowerOK = /[a-z]/.test(pw);
    const numberOK = /\d/.test(pw);
    const symbolOK = /[^\w\s]/.test(pw);

    // Update score based on conditions met
    if (lengthOK) score++;
    if (upperOK) score++;
    if (lowerOK) score++;
    if (numberOK) score++;
    if (symbolOK) score++;

    // Tick requirement if met
    updateRequirement(reqLength, lengthOK);
    updateRequirement(reqUpper, upperOK);
    updateRequirement(reqLower, lowerOK);
    updateRequirement(reqNumber, numberOK);
    updateRequirement(reqSymbol, symbolOK);

    return score;
  }

  passwordInput.addEventListener("input", () => {

    const pw = passwordInput.value;
    const score = checkStrength(pw);

    //Translate score into percentage
    const percent = (score / 5) * 100;
    bar.style.width = `${percent}%`;

    if (score <= 2) {
      bar.className = "progress-bar bg-danger";
      text.textContent = "Weak";
    } else if (score === 3 || score === 4) {
      bar.className = "progress-bar bg-warning";
      text.textContent = "Almost there";
    } else {
      bar.className = "progress-bar bg-success";
      text.textContent = "Strong password";
    }
  });

});