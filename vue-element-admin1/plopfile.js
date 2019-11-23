// 视图生成器
const viewGenerator = require('./plop-templates/view/prompt')
// 组件生成器
const componentGenerator = require('./plop-templates/component/prompt')

module.exports = function(plop) {
  plop.setGenerator('view', viewGenerator)
  plop.setGenerator('component', componentGenerator)
}
