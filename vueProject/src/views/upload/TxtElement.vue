<template>
  <div>
    <el-container class="txt">
      <el-header>
        <div class="title">txt文件上传</div>
      </el-header>
      <!-- main主体部分的代码 -->
      <el-main>
        <el-upload
          :limit='1'
          name="file"
          class="upload-txt"
          accept=".txt"
          drag
          action="http://127.0.0.1:5000/uploadtxt"
          :on-success="handle_success"
          :headers="uploadHeaders" 
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">
            只能上传txt文件哦~如要上传其它类型文件，请移步左侧导航栏
          </div>
        </el-upload>
      </el-main>
      <!-- Footer部分的代码，主要用来提问 -->
      <el-footer> </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      uploadHeaders: {  
        token: JSON.parse(window.localStorage.getItem("access-admin")).token ,  // 设置请求头的 Authorization  
      },
    };
  },
  methods: {
    handle_success(response) {
      if (response.code == 200) {
        console.log("文件上传成功",response)
        this.$message({
          message: '文件上传成功',
          type: 'success'
        });
      }
    },
  },
};
</script>

<style>
.txt {
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

/* header标题样式 */
.title {
  text-align: center;
  font-size: 40px;
}

.upload-txt {
  width: 350px;
  margin: 150px auto;
  border: 1px solid #dcdfe6;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 30px #dcdfe6;
}
</style>