<template>
  <div>
    <el-container class="log">
      <el-header></el-header>
      <el-main class="main-login">
        <!--用户登录-->
        <el-form ref="form" :model="form" :rules="rules" class="login">
          <h3 class="login-title">欢迎登录</h3>
          <el-form-item label="账号" prop="name">
            <el-input
              type="text"
              placeholder="请输入用户名"
              v-model="form.name"
            ></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input
              type="password"
              placeholder="请输入密码"
              v-model="form.password"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm()">登录</el-button>
            <el-button
              style="float: right"
              type="primary"
              @click="dialogVisible = true"
              >注册</el-button
            >
          </el-form-item>
        </el-form>

        <!--用户注册添加数据对话框表单-->
        <el-dialog title="用户注册" :visible.sync="dialogVisible" width="30%">
          <el-form
            :model="ruleForm"
            :rules="rules"
            ref="ruleForm"
            label-width="100px"
            class="demo-ruleForm"
          >
            <el-form-item label="用户名" prop="username">
              <el-input
                type="text"
                placeholder="请输入用户名"
                v-model="ruleForm.username"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pass">
              <el-input
                type="password"
                v-model="ruleForm.pass"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="确认密码" prop="checkPass">
              <el-input
                type="password"
                v-model="ruleForm.checkPass"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="ruleForm.email"></el-input>
            </el-form-item>
            <el-form-item label="头像">
              <el-upload
                class="avatar-uploader"
                action="http://127.0.0.1:5000/uploadavatar"
                :headers="token"
                name="image"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
              >
                <img
                  v-if="ruleForm.image"
                  :src="ruleForm.image"
                  class="avatar"
                />
                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
              </el-upload>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="register()">提交</el-button>
              <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </el-dialog>
      </el-main>
      <el-footer></el-footer>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "LoginElement",
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      //登录表单
      form: {
        name: "",
        password: "",
      },
      //注册表单
      ruleForm: {
        username: "",
        pass: "",
        checkPass: "",
        email: "",
        image: "",
      },
      rules: {
        name: [
          {
            required: true,
            message: "请输入用户名",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            message: "请输入密码",
            trigger: "blur",
          },
        ],
        // 针对注册页面的验证规则，这里的username规则要重写，因为prop的名字和data中定义的属性名字要一致
        username: [
          {
            required: true,
            message: "请输入用户名",
            trigger: "blur",
          },
        ],
        pass: [{ required: true, validator: validatePass, trigger: "blur" }],
        checkPass: [
          { required: true, validator: validatePass2, trigger: "blur" },
        ],
      },
      // 添加数据对话框是否展示的标记
      dialogVisible: false,
    };
  },
  methods: {
    submitForm() {
      const param = { name: this.form.name, password: this.form.password };
      axios
        .post("http://127.0.0.1:5000/login", param)
        .then((res) => {
          if (res.data.code == "200") {
            console.log(res.data);
            localStorage.setItem("access-admin", JSON.stringify(res.data));
            this.$router.push("/help");
          } else {
            this.$message({
              showClose: true,
              message: "请正确输入用户名和密码哦",
              type: "warning",
            });
            return false;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    register() {
      const param = {
        name: this.ruleForm.username,
        password: this.ruleForm.pass,
        email: this.ruleForm.email,
        image: this.ruleForm.image,
      };
      axios
        .post("http://127.0.0.1:5000/register", param)
        .then((res) => {
          console.log("这是register函数获取后端返回数据后的验证");
          console.log(res.data);
          if (res.data.code == "200") {
            console.log(res.data);
            localStorage.setItem("access-admin", JSON.stringify(res.data));
            this.$message({
              message: "恭喜，注册成功！",
              type: "success",
            });
            this.$router.push("/help");
          } else {
            this.$message({
              showClose: true,
              message: "请正确输入用户名和密码哦",
              type: "warning",
            });
            return false;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },

    //文件上传相关
    handleAvatarSuccess(res) {
      this.ruleForm.image = res.data;
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === "image/jpeg";
      const isLt3M = file.size / 1024 / 1024 < 3;
      if (!isJPG) {
        this.$message.error("上传头像图片只能是 JPG 格式!");
      }
      if (!isLt3M) {
        this.$message.error("上传头像图片大小不能超过 2MB!");
      }
      return isJPG && isLt3M;
    },
  },
};
</script>

<style scoped>
.log {
  width: 1480px;
  /* height: 748px; */
   height: 748px
}
.el-header {
  background-color: #96ce54;
}
.el-main {
  background-color: #bbcdc5;
  overflow-y: hidden;
}
.el-footer {
  background-color: #96ce54;
}
.el-main main-login {
  padding: 0;
  margin: 0;
  height: 100%;
}

.login {
  width: 350px;
  margin: 150px auto;
  border: 1px solid #dcdfe6;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 30px #dcdfe6;
}
.login-title {
  text-align: center;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}
.avatar {
  width: 100px;
  height: 100px;
  display: block;
}
</style>