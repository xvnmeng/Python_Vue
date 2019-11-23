<template>
  <div class="login-container">
    <!-- 绑定loginForm 和loginRule -->
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" autocomplete="on" label-position="left">

      <div class="title-container">
        <h3 class="title">登录表单</h3>
      </div>
      <!-- 表单内容1 -->
      <!-- 绑定loginForm的username -->
      <!-- tab键的索引为1 -->
      <el-form-item prop="username">
        <span class="svg-container">
          <!-- 用户户图标 -->
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="用户名"
          name="username"
          type="text"
          tabindex="1"
          autocomplete="on"
        />
      </el-form-item>
      <!-- 绑定大写提示工具 字母按键时提示-->
      <el-tooltip v-model="capsTooltip" content="大写已经开启" placement="right" manual>
        <!-- 绑定loginForm的内容2,password -->
        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="Password"
            name="password"
            tabindex="2"
            autocomplete="on"
            @keyup.native="checkCapslock"
            @blur="capsTooltip = false"
            @keyup.enter.native="handleLogin"
          />
          <!-- 绑定显示密码 -->
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>
      </el-tooltip>
      <!-- 点击登录触发 -->
      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleLogin">登录</el-button>

      <div style="position:relative">
        <div class="tips">
          <span>用户名 : admin</span>
          <span>密码 : 随意</span>
        </div>
        <div class="tips">
          <span style="margin-right:18px;">用户名 : editor</span>
          <span>密码 : 随意</span>
        </div>

        <!-- <el-button class="thirdparty-button" type="primary" @click="showDialog=true">
          其他登录方式
        </el-button> -->
      </div>
    </el-form>
    <!-- 展示其他登录方式的窗口 -->
    <el-dialog title="其他登录方式" :visible.sync="showDialog">
      不能再本地使用社交账号登录,请选择其他方式! ! !
      <br>
      <br>
      <br>
      <social-sign />
    </el-dialog>
  </div>
</template>

<script>
// 有效用户名
import { validUsername } from '@/utils/validate'
// 社交账号登录
import SocialSign from './components/SocialSignin'

export default {
  name: 'Login',
  components: { SocialSign },
  data() {
    // 验证用户名
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('输入正确用户名！'))
      } else {
        callback()
      }
    }
    // 验证密码
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('密码长度不能少于6位'))
      } else {
        callback()
      }
    }
    // 显示在界面上的用户名和密码  admin  111111
    // loginForm loginRules
    // otherQuery 其他查询是 字典
    return {
      loginForm: {
        username: '',
        password: ''
      },
      // validator：验证器
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      // 初始的类型为password，不可见
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      // 不显示详情页
      showDialog: false,
      redirect: undefined,
      otherQuery: {}
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        const query = route.query
        if (query) {
          this.redirect = query.redirect
          this.otherQuery = this.getOtherQuery(query)
        }
      },
      immediate: true
    }
  },
  created() {
    // window.addEventListener('storage', this.afterQRScan)
  },
  mounted() {
    // 用户名或者密码为空，聚焦
    if (this.loginForm.username === '') {
      this.$refs.username.focus()
    } else if (this.loginForm.password === '') {
      this.$refs.password.focus()
    }
  },
  destroyed() {
    // window.removeEventListener('storage', this.afterQRScan)
  },
  methods: {
    // 大写工具提示
    checkCapslock({ shiftKey, key } = {}) {
      // 没有shift键时，输入大写字母； 有shift键时，按下小写字母
      if (key && key.length === 1) {
        if (shiftKey && (key >= 'a' && key <= 'z') || !shiftKey && (key >= 'A' && key <= 'Z')) {
          this.capsTooltip = true
        } else {
          this.capsTooltip = false
        }
      }
      // 开启大写，按下大写键，切换大写提示信息为false
      if (key === 'CapsLock' && this.capsTooltip === true) {
        this.capsTooltip = false
      }
    },
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      // 聚焦在密码框
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    // 点击登录按钮或者回车按键,开始调用这个方法
    // $refs 是所有注册过的ref的一个集合
    // 登录控制
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          // 标记为加载状态,防止多次提交
          this.loading = true
          // 传送登录表单内容到，登录接口
          // 重新匹配路由，加载其他查询
          // this.otherQuery与getOtherQuery有关
          this.$store.dispatch('user/login', this.loginForm)
          // this.$store.dispatch('http://127.0.0.1:8000/login', this.loginForm)
            .then(() => {
              this.$router.push({ path: this.redirect || '/', query: this.otherQuery })
              // 终止加载状态
              this.loading = false
            })
            .catch(() => {
              this.loading = false
            })
        } else {
          console.log('错误提交!')
          return false
        }
      })
    },
    getOtherQuery(query) {
      return Object.keys(query).reduce((acc, cur) => {
        if (cur !== 'redirect') {
          acc[cur] = query[cur]
        }
        return acc
      }, {})
    }
  }
}
</script>

<!-- 样式修饰 -->
<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<!-- 位置修饰 -->
<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }

  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }

  @media only screen and (max-width: 470px) {
    .thirdparty-button {
      display: none;
    }
  }
}
</style>
