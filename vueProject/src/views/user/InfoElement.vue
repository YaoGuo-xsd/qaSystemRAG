<template>
  <div>
    <el-container class="info">
      <el-header>
        <div class="title">个人信息展示</div>
      </el-header>
      <!-- main代码 -->
      <el-main>
        <div class="user-profile">
          <div class="user-avatar">
            <img class="uavatar" :src="this.image_src" alt="User Avatar" />
          </div>

          <div class="user-info">
            用户名：{{this.username}}<br>
            邮箱号码：{{this.email}}<br>
            账户创建时间：{{this.join_time}}<br>
          </div>
        </div>
      </el-main>
      <!-- Footer代码 -->
      <el-footer> </el-footer>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      username: "",
      email: "",
      join_time: "",
      image_src: "",
    };
  },
  methods: {
    set_info: function () {
      let admin = JSON.parse(window.localStorage.getItem("access-admin"));
      axios({
        url: "http://127.0.0.1:5000/get-info",
        method: "get",
        headers: {
          token: admin.token,
        },
      }).then((res) => {
        (this.username = res.data.uname), (this.email = res.data.email);
        this.join_time = res.data.join_time;
        this.image_src = res.data.img;
      });
    },
  },
  mounted: function () {
    this.set_info();
  },
};
</script>


<style>
.info {
  width: 1280px;
  height: 100%;
}
.el-header {
  background-color: #e6a23c;
}
.el-main {
  background-color: #ebef28;
}
.el-footer {
  background-color: #67c23a;
}
/* header鐨勬牱寮� */
.title {
  text-align: center;
  font-size: 40px;
}

.user-avatar {
  float: left;
  width: 50%;
  height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.user-info {
  float: left;
  width: 50%;
  height: 600px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.uavatar {
  width: 200px;
  height: 200px;
}
</style>