<template>
  <div>
    <el-container class="radar">
      <el-header>
        <div class="title">RAG问答服务</div>
      </el-header>
      <!-- main主体部分的代码 -->
      <el-main>
        <div>
          <div v-for="(item, index) in alternatingList" :key="index">
            <el-descriptions title="" :column="1" border>
              <el-descriptions-item :labelStyle="labelStyle"
                v-if="item.type === 'question' && item.id != 0"
              >
                <template slot="label" >
                  <i class="el-icon-user"></i>
                  问题
                </template>
                {{ item.content }}
              </el-descriptions-item>
              <el-descriptions-item :labelStyle="labelStyle"
                v-if="item.type === 'answer' && item.id != 0"
              >
                <template slot="label">
                  <i class="el-icon-user"></i>
                  回答
                </template>
                {{ item.content }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </div>
      </el-main>
      <!-- Footer部分的代码，主要用来提问 -->
      <el-footer>
        <div class="qa_footer">
          <el-form :inline="true" class="demo-form-inline">
            <el-form-item label="请提问：" class="footer-item">
              <el-input
                v-model="question"
                style="width: 1000px"
                clearable
                placeholder="请输入内容"
              ></el-input>
            </el-form-item>
            <el-form-item class="footer-item">
              <el-button type="primary" @click="onSubmit">发送</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      question: "",
      answer: "",
      questionList: [{ id: 0, content: "null" }],
      answerList: [{ id: 0, content: "null" }],
      id: 0,
      //label样式
      labelStyle: { 'width': '100px' }
    };
  },

  computed: {
    alternatingList() {
      let list = [];
      let i = 0;
      while (this.questionList[i] || this.answerList[i]) {
        // 如果问题或回答列表还有元素
        if (this.questionList[i]) {
          // 如果问题列表还有元素，则添加到交替展示数组中
          list.push({
            id: this.questionList[i].id,
            content: this.questionList[i].content,
            type: "question",
          });
        }
        if (this.answerList[i]) {
          // 如果回答列表还有元素，则添加到交替展示数组中
          list.push({
            id: this.answerList[i].id,
            content: this.answerList[i].content,
            type: "answer",
          });
        }
        i++;
      }
      return list;
    },
  },

  methods: {
    onSubmit() {
      let admin = JSON.parse(window.localStorage.getItem('access-admin'))
      let param = { question: this.question };
      axios
        .post("http://127.0.0.1:5000/answerradarBM25", param, {headers: { token: admin.token,},})
        .then((res) => {
          this.id = this.id + 1;
          let newques = { id: this.id, content: this.question };
          let newansw = { id: this.id, content: res.data.answer };
          this.questionList.push(newques);
          this.answerList.push(newansw);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style>
.radar {
  width: 1280px;
  height: 100%;
}
.el-header {
  background-color: #70695d;
}
.el-main {
  background-color: #c0d695;
}
.el-footer {
  background-color: #70695d;
}
/* header标题样式 */
.title {
  text-align: center;
  font-size: 40px;
}
.demo-form-inline {
  margin: 0px 0 0 0;
}
.footer-item {
  margin-bottom: 0px;
}
.qa_footer {
  height: 60px;
  /*垂直居中 */
  vertical-align: middle;
  /*水平居中*/
  text-align: center;
}
</style>