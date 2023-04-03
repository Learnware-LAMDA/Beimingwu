function downloadLearnware(id) {
  const url = 'http://210.28.134.173:1248/download/resources/Learnware/market/M5_Shop1_LGB.tar'
  const a = document.createElement('a')
  a.href = url
  a.download = 'Learnware.pdf'
  document.body.appendChild(a)
  a.click()
}

export { downloadLearnware }