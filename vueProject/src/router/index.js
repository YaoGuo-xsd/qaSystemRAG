import Vue from 'vue'
import Router from 'vue-router'
import LoginElement from '../views/LoginElement'   // 登录页
import MainElement from '../views/MainElement'  //主页（侧边栏）
import ChatgptElement from '../views/chat/ChatgptElement'   //chatgpt
import RadarElement from '../views/chat/RadarElement'  //radar
import TxtElement from '../views/upload/TxtElement'  //txt文件上传
import PdfElement from '../views/upload/PdfElement'  //pdf文件上传
import MdElement from '../views/upload/MdElement'  //md文件上传
import HistoryElement from '../views/user/HistoryElement'  //历史记录
import InfoElement from '../views/user/InfoElement'  //个人信息
import HelpElement from '../views/HelpElement'  //帮助页面
import axios from 'axios'

Vue.use(Router)

const routes = [
  {
    //登录页
    path: '/login', //路由跳转路径
    name: 'LoginElement',  //路由名称
    component: LoginElement  //路由跳转组件
  },
  {
    //侧边栏~小雷达
    path: '/main', //路由跳转路径
    name: 'MainElement',  //路由名称
    component: MainElement,  //路由跳转组件
    children: [
      {
        //帮助页面
        path: '/help', //路由跳转路径
        name: 'HelpElement',  //路由名称
        component: HelpElement  //路由跳转组件
      },
      {
        //radar
        path: '/chat/radar', //路由跳转路径
        name: 'RadarElement',  //路由名称
        component: RadarElement  //路由跳转组件
      },
      {
        //chat-gpt
        path: '/chat/gpt', //路由跳转路径
        name: 'ChatgptElement',  //路由名称
        component: ChatgptElement  //路由跳转组件
      },
      {
        //txt上传
        path: '/upload/txt', //路由跳转路径
        name: 'TxtElement',  //路由名称
        component: TxtElement  //路由跳转组件
      },
      {
        //pdf上传
        path: '/upload/pdf', //路由跳转路径
        name: 'PdfElement',  //路由名称
        component: PdfElement  //路由跳转组件
      },
      {
        //md上传
        path: '/upload/md', //路由跳转路径
        name: 'MdElement',  //路由名称
        component: MdElement  //路由跳转组件
      },
      {
        //历史记录
        path: '/user/history', //路由跳转路径
        name: 'HistoryElement',  //路由名称
        component: HistoryElement  //路由跳转组件
      },
      {
        //个人信息
        path: '/user/info', //路由跳转路径
        name: 'InfoElement',  //路由名称
        component: InfoElement  //路由跳转组件
      },
    ]
  }
]

const router = new Router({
  mode:'history',
  routes
})

router.beforeEach((to, from, next) => {
  if (to.path.startsWith('/login')) {  //  如果去登录页面
    window.localStorage.removeItem('access-admin')
    next()
  } else{
    let admin = JSON.parse(window.localStorage.getItem('access-admin'))
    if (!admin) {
      next({path: '/login'})  //跳转登录
    } else {    //去其他页面
      //校验token合法性
      axios({
        url:'http://127.0.0.1:5000/verify',
        method:'get',
        headers:{
          token: admin.token
        }
      }).then((res) => {
        console.log(res.data)
        if(res.data.code != 200){
          console.log('校验失败')
          next({path: '/login'})
        }
      })
      next()
    }
  }
})

export default router
