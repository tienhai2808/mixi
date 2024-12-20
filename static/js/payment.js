const cardNumber = document.querySelector("[card-number]");
if (cardNumber) {
  const buttonBuy = document.querySelector("[button-buy]");
  const paymentImg = document.querySelector("[payment-img]");
  buttonBuy.addEventListener("click", () => {
    paymentImg.classList.remove("d-none");
  });
} else {
  const formCash = document.querySelector("[form-cash]");
  const buttonBuy = document.querySelector("[button-buy]");
  if (buttonBuy) {
    buttonBuy.addEventListener("click", () => {
      formCash.submit();
    });
  }
}

const cancelPayment = document.querySelector(".x-icon-img");
if (cancelPayment) {
  const paymentImg = document.querySelector("[payment-img]");
  cancelPayment.addEventListener("click", () => {
    paymentImg.classList.add("d-none");
  });
}

const formPaymentSuccess = document.querySelector(".btn-payment-div");
if (formPaymentSuccess) {
  formPaymentSuccess.addEventListener("submit", (e) => {
    const confirmPayment = confirm("Mày Có Chắc Là Thanh Toán Rồi Không???");
    if (!confirmPayment) {
      e.preventDefault();
    }
  });
}