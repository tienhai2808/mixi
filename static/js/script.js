const sortByProduct = document.querySelector('[sort-by-product]')
if (sortByProduct) {
  sortByProduct.addEventListener('change', () => {
    const sortByForm = document.querySelector('[form-sort-by]')
    sortByForm.submit()
  })
}


const xIcon = document.querySelector('[x-icon]')
if (xIcon) {
  const alertDiv = document.querySelector('[mess-div]')
  xIcon.addEventListener('click', () => {
    alertDiv.remove()
  })
  setTimeout (() => {
    alertDiv.remove()
  }, 5000)
}