<template>
  <div>
    <el-container class="help">
      <el-header>
        <div class="title">欢迎-浏览下文，更好的使用该平台</div>
      </el-header>
      <!-- main主体部分的代码 -->
      <el-main>
        <h1>功能介绍</h1><br>
        1. RAG问答：给chat-gpt外接一个知识库，用户可以在此处提问问题，系统将基于本地知识库提供智能回答，保证回答真实有效。<br><br>
        2. Chat-gpt：大模型接口。用户可以在此处进行对话，与Chat-gpt模型进行交互，将答案与小雷达平台答案进行对比。<br><br>
        3. 文件上传：用户可以在此处上传对应格式文件，系统将读取文件内容并处理加载为本地知识库，作为日后平台提供答案的参考来源。<br><br>
        4. 历史记录：用户可以查看之前的提问记录，方便回顾和查找之前的交互内容。<br><br>
        5. 个人信息：用户可以修改和查询个人信息，包括用户名、密码等。<br><br>
        <h1>使用说明</h1><br>
        1. RAG问答：在输入框中输入问题，点击提交按钮，系统将返回基于本地知识库的智能回答，用户可以进行连续的对话交流<br><br>
        2. Chat-gpt：在输入框中输入对话内容，点击提交按钮，系统将返回Chat-gpt模型的回答，但不能保证回答是否符合客观事实。<br><br>
        3. 文件上传：点击上传按钮或者拖拽，选择本地的文件进行上传。系统将读取文件内容并进行处理，该过程请不要离开网页。<br><br>
        4. 历史记录：点击历史记录按钮，系统将显示之前的提问记录。用户可以点击记录进行查看或者删除某一条历史记录。<br><br>
        5. 个人信息：点击个人信息按钮，系统将显示当前用户的个人信息。用户可以修改用户名、密码等信息，并保存修改。
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
     
    }
  }
};
</script>

<style>
.help {
  width: 1280px;
  height: 100%;
}
.el-header {
  background-color: #96ce54;
}
.el-main {
  background-color: #bbcdc5;
}
.el-footer {
  background-color: #96ce54;
}

/* header标题样式 */
.title {
  text-align: center;
  font-size: 40px;
}
</style>