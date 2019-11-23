import Vue from 'vue'
import SvgIcon from '@/components/SvgIcon'// svg component

// register globally
Vue.component('svg-icon', SvgIcon)

const req = require.context('./svg', false, /\.svg$/)
// 匹配地图值内容
const requireAll = requireContext => requireContext.keys().map(requireContext)
requireAll(req)
