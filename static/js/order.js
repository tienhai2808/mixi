const formAction = document.querySelector('.form-action')

const btnCancel = document.querySelector('.btn-cancel')
if (btnCancel) {
  btnCancel.addEventListener('click', () => {
    const confirmCancel = confirm("Bạn muốn hủy đơn hàng này chứ?")
    if (confirmCancel) {
      formAction.querySelector('[hidden]').value = 'cancel'
      formAction.submit()
    }
  })
}

const btnShipping = document.querySelector('.btn-shipping')
if (btnShipping) {
  btnShipping.addEventListener('click', () => {
    const confirmShipping = confirm("Đã giao đơn hàng cho đơn vị vận chuyển?")
    if (confirmShipping) {
      formAction.querySelector('[hidden]').value = 'shipping'
      formAction.submit()
    }
  })
}

const btnShipped = document.querySelector('.btn-shipped')
if (btnShipped) {
  const roleUser = btnShipped.getAttribute('data-role')
  btnShipped.addEventListener('click', () => {
    let message = ''
    if (roleUser === 'customer') {
      message = 'Bạn đã nhận hàng rồi chứ?'
    } else {
      message = 'Đã giao đơn hàng thành công?'
    }
    const confirmShipped = confirm(message)
    if (confirmShipped) {
      formAction.querySelector('[hidden]').value = 'shipped'
      formAction.submit()
    }
  })
}