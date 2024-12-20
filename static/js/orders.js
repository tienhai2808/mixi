const formAction = document.querySelector('.form-action')

const btnCancels = document.querySelectorAll('.btn-cancel')
if (btnCancels.length > 0) {
  btnCancels.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmCancel = confirm("Bạn muốn hủy đơn hàng này chứ?")
      if (confirmCancel) {
        formAction.querySelector("#id_order").value = btn.getAttribute('value')
        formAction.querySelector("#action").value = 'cancel'
        formAction.submit()
      }
    })
  })
}

const btnShippings = document.querySelectorAll('.btn-shipping')
if (btnShippings.length > 0) {
  btnShippings.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmShipping = confirm("Đã giao đơn hàng cho đơn vị vận chuyển?")
      if (confirmShipping) {
        formAction.querySelector("#id_order").value = btn.getAttribute('value')
        formAction.querySelector("#action").value = 'shipping'
        formAction.submit()
      }
    })
  })
}

const btnShippeds = document.querySelectorAll('.btn-shipped')
if (btnShippeds.length > 0) {
  btnShippeds.forEach((btn) => {
    const roleUser = btn.getAttribute('data-role')
    btn.addEventListener('click', () => {
      let message = ''
      if (roleUser === 'customer') {
        message = 'Bạn đã nhận hàng rồi chứ?'
      } else {
        message = 'Đã giao đơn hàng thành công?'
      }
      const confirmShipped = confirm(message)
      if (confirmShipped) {
        formAction.querySelector("#id_order").value = btn.getAttribute('value')
        formAction.querySelector("#action").value = 'shipped'
        formAction.submit()
      }
    })
  })
}

const formStatus = document.querySelector('.form-status')
formStatus.querySelector('select').addEventListener('change', () => {
  formStatus.submit()
})