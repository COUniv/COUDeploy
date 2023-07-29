<template>
  <div class="CreateWrapper">
    <div class="upload-contents">
      <el-form
        ref="form"
        :model="formCodeReview"
        :rules="rules"
        label-position="top"
        label-width="70px"
      >
        <div class="category">
          <div class="selectform" style="width: 30%; margin-right: auto">
            <Select
              v-model="formCodeReview.languagetype"
              aria-placeholder="언어"
              clearable
              size="large"
            >
              <Option
                v-for="type in typeList"
                :value="type.value"
                :key="type.value"
              >
                {{ type.label }}
              </Option>
            </Select>
          </div>

          <div
            style="
              padding-top: 15px;
              width: 30%;
              margin-left: auto;
              margin-top: 2px;
            "
          >
            <el-form-item prop="problemid" required>
              <Input
                v-model="formCodeReview.problemid"
                :border="true"
                placeholder="문제 번호"
                size="large"
              ></Input>
            </el-form-item>
          </div>
        </div>

        <div class="title_form">
          <el-form-item prop="title" required>
            <!-- 게시글 제목 입력 - formArticle.title -->
            <el-input
              v-model="formCodeReview.title"
              :border="true"
              placeholder="제목"
              size="large"
            ></el-input>
          </el-form-item>
        </div>

        <div class="contents_form">
          <el-form-item prop="content" required>
            <Simditor v-model="formCodeReview.content"> </Simditor>
          </el-form-item>
        </div>

        <div class="code_form">
          <p class="caTitle">코드 작성</p>
          <el-form-item prop="code" required>
            <CodeInput v-model="formCodeReview.code" />
          </el-form-item>
        </div>

        <div class="submit_btn">
          <Button type="primary" size="large" @click="submit"
            >제출 <Icon id="submit-icon" size="17" type="ios-paper-plane" />
          </Button>
          <Button class="cancelBtn" size="large" onclick="history.back()"
            >취소</Button
          >
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
import Simditor from "@/pages/admin/components/Simditor";
import CodeInput from "@/pages/admin/components/CodeInput";
import api from "@oj/api";

export default {
  name: "CreateReviewCode",
  components: {
    Simditor,
    CodeInput
  },

  data() {
    return {
      typeList: [
        {
          value: "1",
          label: "C++",
        },
        {
          value: "2",
          label: "C",
        },
        {
          value: "3",
          label: "Kotlin",
        },
        {
          value: "4",
          label: "Python",
        },
        {
          value: "5",
          label: "Java",
        },
        {
          value: "6",
          label: "Javascript",
        },
        {
          value: "7",
          label: "Typescript",
        },
        {
          value: "8",
          label: "Swift",
        },
      ],
      rules: {
        title: [
          {
            required: true,
            message: "제목은 6이상 30이하 자리까지만 허용됩니다.",
            trigger: "blur",
            min: 6,
            max: 30,
          },
        ],
        content: [
          { required: true, message: "Content is required", trigger: "blur" },
        ],
      },

      formCodeReview: {
        // 전송 데이터
        title: "", // 게시글 제목
        content: "", // 게시글 내용
        languagetype: "", // 질문 게시글의 경우 질문 관련 언어
        problemid: "", // 질문 게시글의 경우 질문 관련 문제 ID
        code: [],
      },
    };
  },
  computed: {
    processedCode() {
      return this.formCodeReview.code.split("\n");
    },
  },
  methods: {
    submit() {
      const data = {
        ...this.formCodeReview,
        code: this.processedCode,
      };
      api.CreateReviewCode(data).then((res) => {
        this.$success("success!!");
        this.$router.push({ name: "codereviewmain" }).catch(() => {});
      });
    },
  },
};
</script>

<style scoped lang="less">
.CreateWrapper {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  overflow-x: auto;
}

.upload-contents {
  width: 100%;
  min-width: 800px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.category {
  width: 100%;
  display: flex;
  align-items: center;
}

.caTitle {
  font-size: 1.5rem;
  margin: 0 0 20px 5px;
  font-weight: bold;
}

.cancelBtn {
  margin-left: 20px;
}

.codeArea {
  font-size: 15px;
  border: 1px solid rgb(219, 219, 219);
  border-radius: 7px;
}

.codeArea textarea::placeholder {
  color: rgb(237, 237, 237);
}
</style>
