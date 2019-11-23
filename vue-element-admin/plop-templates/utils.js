exports.notEmpty = name => {
  return v => {
    // 不等于v，或者除去头尾空格=没有
    if (!v || v.trim === '') {
      return `${name} is required`
    } else {
      return true
    }
  }
}
