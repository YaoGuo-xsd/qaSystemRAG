<template>
  <div>
    <el-container class="help">
      <el-header>
        <div class="title">回忆站~在这里，看到你之前的提问~</div>
      </el-header>
      <!-- main主体部分的代码 -->
      <el-main>
        <el-collapse>
          <el-collapse-item v-for="item in this.qaList" :key="item">
            <template slot="title">
              <span
                style="
                  margin-left: 30px;
                  float: left;
                  font-weight: bold;
                  font-size: 14px;
                  color: #2c8df4;
                "
              >
                {{ item.question }}

                <el-button
                  slot="reference"
                  size="mini"
                  type="danger"
                  icon="el-icon-delete"
                  circle
                  @click="deleteById(item.id)"
                ></el-button>
              </span>
            </template>
            <div style="margin-left: 30px">回答：{{ item.answer }}</div>
            <div style="margin-left: 30px">答案来源：{{ item.type }}</div>
            <div style="margin-left: 30px">提问时间：{{ item.join_time }}</div>
          </el-collapse-item>
        </el-collapse>
      </el-main>
      <!-- Footer部分的代码，主要用来提问 -->
      <el-footer> </el-footer>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      qaList: [],
    };
  },

  methods: {
    show: function () {
      let admin = JSON.parse(window.localStorage.getItem("access-admin"));
      axios
        .get("http://127.0.0.1:5000/history", {
          headers: { token: admin.token },
        })
        .then((res) => {
          console.log(res.data.data);
          this.qaList = res.data.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },

    deleteById(qa_id) {
      let params = { qaId: qa_id };
      axios
        .get("http://127.0.0.1:5000/delete", { params })
        .then((res) => {
          console.log(res.data);
        })
        .catch((err) => {
          console.error(err);
        });
      this.show();
      this.$message({
        message: "删除成功",
        type: "warning",
      });
    },
  },

  mounted: function () {
    this.show();
  },
};
</script>

<style>
.help {
  width: 1270px;
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
</style>