const paymentType = document.querySelectorAll('#payment-type input[type="radio"]')
const cardInfoDiv = document.querySelector('#card-info')
if (paymentType.length > 0) {
  paymentType.forEach((choose) => {
    choose.addEventListener('click', () => {
      if (choose.value === 'card') {
        cardInfoDiv.classList.remove('d-none')
        cardInfoDiv.querySelector("input[name='shipping_card_number']").setAttribute('required', true)
        cardInfoDiv.querySelector("input[name='shipping_bank']").setAttribute('required', true)
      } else {
        if (!cardInfoDiv.classList.contains('d-none')) {
          cardInfoDiv.classList.add('d-none')
          cardInfoDiv.querySelector("input[name='shipping_card_number']").removeAttribute('required')
          cardInfoDiv.querySelector("input[name='shipping_bank']").removeAttribute('required')
        }
      }
    })
  })
}