<template>
  <div class="home-div">
    <el-container
      class="home-container"
      style="height: 748.3px; border: 1px solid #eee"
    >
      <el-aside width="200px" style="background-color: rgb(57, 47, 65, 1)">
        <div class="avatar">
          <el-avatar
            :size="100"
            :src="image_src"
          ></el-avatar>
        </div>
        <el-menu
          router
          :default-active="$route.path"
          :default-openeds="['1', '2', '3']"
          background-color="rgba(57, 47, 65, 1)"
          text-color="#fff"
          class="el-menu-container"
        >
          <el-submenu index="1">
            <template slot="title"
              ><i class="el-icon-service"></i>对话问答</template
            >
            <el-menu-item index="/chat/radar"> RAG问答 </el-menu-item>
            <el-menu-item index="/chat/gpt"> Chat-gpt </el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"
              ><i class="el-icon-upload"></i>上传文件</template
            >
            <el-menu-item index="/upload/txt"> txt </el-menu-item>
            <el-menu-item index="/upload/pdf"> pdf </el-menu-item>
            <el-menu-item index="/upload/md"> md </el-menu-item>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title"
              ><i class="el-icon-upload"></i>个人中心</template
            >
            <el-menu-item index="/user/history">历史记录</el-menu-item>
            <el-menu-item index="/user/info">个人信息</el-menu-item>
          </el-submenu>
          <el-menu-item index="/help"
            ><i class="el-icon-question"></i> 帮助
          </el-menu-item>
        </el-menu>
      </el-aside>

      <router-view />
    </el-container>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      image_src: '',
    };
  },
  methods: {
    set_image: function () {
      let admin = JSON.parse(window.localStorage.getItem('access-admin'))
      axios({
        url: "http://127.0.0.1:5000/get-img",
        method: "get",
        headers: {
          token: admin.token,
        },
      }).then((res) => {
        this.image_src = res.data.data;
      });
    },
  },
  mounted: function () {
    this.set_image();
  },
};
</script>

<style>
body {
  margin: 0 2px;
}

.home-container {
  height: 100%;
}

.el-menu-container {
  height: 85%;
}

/* 鼠标悬浮侧边栏时字体颜色 */
.el-menu-item:hover {
  outline: 0 !important;
  color: #000000 !important;
}
/* 鼠标点击之后功能选项背景颜色和字体颜色 */
.el-menu-item.is-active {
  color: #000 !important;
  background: #00c8ff !important;
}
/* 头像居中 */
.avatar {
  /*垂直居中 */
  vertical-align: middle;
  /*水平居中*/
  text-align: center;
  margin: 6px 0 0 0;
}
</style>